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
            
    

class EvaluationPage(Page):
    evaluation_max_rate = models.IntegerField(default=0)
    
    content_panels = Page.content_panels + [
        FieldPanel('evaluation_max_rate'),
        InlinePanel('evaluation_categories', label="Evaluation Categories"),
    ]
    

    def get_context(self, request):
        context = super().get_context(request)
        if request.user.client == None: 
            return context
        for user_evaluation in  request.user.client.user_evaluation.all():
            context['user_evaluation'] = user_evaluation
        context['evaluation_categories'] = EvaluationCategories.objects.all()
            
        return context

    
    def serve(self, request):
        if request.method == 'POST':
            
            for category in EvaluationCategories.objects.all():
                for rate in category.evaluation_rates.all():
                    evaluation_rate_assign = EvaluationRateAssign.objects.get_or_create(
                        user_evaluation=request.user.client.user_evaluation.all()[0],
                        evaluation_rate=rate,
                    )
                    evaluation_rate_assign.rate= request.POST['question-'+str(rate.pk)]
                    evaluation_rate_assign.save()



            return super().serve(request)
        else:
            # Display event page as usual
            return super().serve(request)
            
