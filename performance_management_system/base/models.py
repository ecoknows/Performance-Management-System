from django.http import HttpResponseRedirect, HttpResponse
from django.db import models


from wagtail.core.models import Page, Orderable
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
)

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from performance_management_system import LIST_MENU
from performance_management_system.employee.models import Employee
from performance_management_system.client.models import Client

class BaseAbstractPage(RoutablePageMixin, Page):
    
    @route(r'^notifications/$')
    def notification(self, request):
        return self.render(
            request,
            template="base/notifications.html",
        )

    
    class Meta:
        abstract = True

class BaseIndexPage(Page):
    max_count = 1
    def serve(self, request):
        if request.user.is_superuser == True:
            return HttpResponseRedirect('/admin/')
        elif request.user.is_authenticated == False:
            return HttpResponseRedirect('/login/')
        elif request.user.is_hr:
            from performance_management_system.hr.models import HRIndexPage
            hr_index_page = HRIndexPage.objects.child_of(self).live()
            return HttpResponseRedirect(hr_index_page[0].slug)
        elif request.user.is_employee:
            from performance_management_system.employee.models import EmployeeIndexPage
            employee_index_page = EmployeeIndexPage.objects.child_of(self).live()
            return HttpResponseRedirect(employee_index_page[0].slug)
        elif request.user.is_client:
            from performance_management_system.client.models import ClientIndexPage
            client_index_page = ClientIndexPage.objects.child_of(self).live()
            return HttpResponseRedirect(client_index_page[0].slug)
        
        return HttpResponseRedirect('/logout/')

# ABSTRACT
class EvaluationRates(ClusterableModel):
    evaluation_categories = ParentalKey('EvaluationCategories', on_delete=models.CASCADE, related_name='evaluation_rates')
    
    name = models.TextField(
        max_length=255,
        null=True,   
        verbose_name='Question'
    )
    
    panels = [
        FieldPanel('name'),
    ]
    
    def __str__(self):
        return self.name
    
# ABSTRACT
class EvaluationCategories(ClusterableModel):
    
    evaluation_page = ParentalKey(
        'EvaluationPage', 
        null=True,
        on_delete=models.CASCADE, 
        related_name='evaluation_categories'
    )
    
    
    category_name = models.TextField(
        max_length=255,
        null=True,
        verbose_name='Category'
    )
    
    @property
    def list_rates(self):
        return self.evaluation_rates.all()
    
    def __str__(self):
        return self.category_name
     
    panels = [
        FieldPanel('category_name'),
        InlinePanel('evaluation_rates', label="Evaluation Rates"),
    ]

class EvaluationRateAssign(Orderable):
    
    user_evaluation = ParentalKey(
        'UserEvaluation', 
        on_delete=models.CASCADE, 
        null=True,
        related_name='evaluation_rates_assign')
    
    evaluation_rate = ParentalKey(
        'EvaluationRates', 
        on_delete=models.CASCADE, 
        null=True,
        related_name='evaluation_rates_assign')

    
    rate = models.IntegerField(default=0)
    
    panels = [
        FieldPanel('evaluation_rates'),
    ]
    

class UserEvaluation(ClusterableModel, models.Model):
    employee = models.ForeignKey(
        Employee,
        null=True,
        related_name='user_evaluation',
        on_delete=models.CASCADE
    )
    client = models.ForeignKey(
        Client,
        null=True,
        related_name='user_evaluation',
        on_delete=models.CASCADE
    )
    
    evaluated = models.BooleanField(default=False)

    
    panels = [
        FieldPanel('employee'),
        FieldPanel('client'),
    ]
            
    

class EvaluationPage(RoutablePageMixin, Page):
    evaluation_max_rate = models.IntegerField(default=0)
    
    content_panels = Page.content_panels + [
        FieldPanel('evaluation_max_rate'),
        InlinePanel('evaluation_categories', label="Evaluation Categories"),
    ]
    
    parent_page_types = ['client.ClientIndexPage']

    def get_context(self, request):
        context = super().get_context(request)
        if request.user.client == None: 
            return context
        for user_evaluation in  request.user.client.user_evaluation.all():
            context['user_evaluation'] = user_evaluation
        context['evaluation_categories'] = EvaluationCategories.objects.all()
            
        return context

    @route(r'^$') 
    def default_route(self, request):
        return HttpResponseRedirect('../')
    
    def get_menu_list(self):
        return LIST_MENU
    
    @route(r'^(\d+)/$', name='id')
    def evaluate_user_with_id(self, request, id):
        user_evaluation = UserEvaluation.objects.get(pk=id)

        if request.method == 'POST' and request.POST.get('submit-btn', None):
            
            for category in EvaluationCategories.objects.all():
                for rate in category.evaluation_rates.all():
                    evaluation_rate_assign, created = EvaluationRateAssign.objects.get_or_create(
                        user_evaluation=user_evaluation,
                        evaluation_rate=rate,
                    )

                    if evaluation_rate_assign:
                        evaluation_rate_assign.rate= int(request.POST['question-'+str(rate.pk)] )
                        evaluation_rate_assign.save()
                        
            update_user_evaluation = UserEvaluation.objects.get(pk=id)
            update_user_evaluation.evaluated = True
            update_user_evaluation.save()

            employee = user_evaluation.employee
            employee_not_evaluated = employee.user_evaluation.filter(evaluated=False)

            if len(employee_not_evaluated) == 0:
                employee.status = 'evaluated'
                employee.save()

            client = user_evaluation.client
            client_not_evaluated = client.user_evaluation.filter(evaluated=False)
            
            if len(client_not_evaluated) == 0:
                client.status = 'evaluated'
                client.save()


        menu_lists = self.get_menu_list()
        return self.render(
            request,
            context_overrides={
            'user_evaluation': user_evaluation,
            'menu_lists': menu_lists,
            'user_model': request.user.client,
            'employee_model': user_evaluation.employee
            }
        )
            