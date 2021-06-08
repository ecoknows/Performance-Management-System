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
        elif str(request.user.groups.all()[0]) == 'HR Admin':
            from performance_management_system.hr.models import HRIndexPage
            hr_index_page = HRIndexPage.objects.child_of(self).live()
            return HttpResponseRedirect(hr_index_page[0].slug)
        elif str(request.user.groups.all()[0]) == 'Employee':
            from performance_management_system.employee.models import EmployeeIndexPage
            employee_index_page = EmployeeIndexPage.objects.child_of(self).live()
            return HttpResponseRedirect(employee_index_page[0].slug)
        elif str(request.user.groups.all()[0]) == 'Client':
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
class EvaluationCategoriesAssign(ClusterableModel,Orderable):
    
    user_evaluation = ParentalKey(
        'UserEvaluation', 
        null=True,
        on_delete=models.CASCADE, 
        related_name='evaluation_categories_assign'
    )
    
    evaluation_category = models.ForeignKey(
        'EvaluationCategories',
        null=True,
        related_name='+',
        on_delete=models.CASCADE
    )
    
    panels = [
        FieldPanel('evaluation_category'),
        InlinePanel('evaluation_rates_assign'),
    ]

class EvaluationRateAssign(Orderable):
    
    evaluation_categories_assign = ParentalKey(
        'EvaluationCategoriesAssign', 
        null=True,
        on_delete=models.CASCADE, 
        related_name='evaluation_rates_assign'
    )
    
    evaluation_rates = models.ForeignKey(
        'EvaluationRates',
        null=True,
        related_name='+',
        on_delete=models.CASCADE
    )
    
    rate = models.IntegerField(default=0)
    
    panels = [
        FieldPanel('evaluation_rates'),
    ]
    

class UserEvaluation(ClusterableModel, models.Model):
    employee = models.ForeignKey(
        Employee,
        null=True,
        related_name='+',
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
    
    def save(self):
        super().save()
        
        evaluation_categories = EvaluationCategories.objects.all()
        evaluation_rates = EvaluationRates.objects.all()
        for category in evaluation_categories:
            category_assign = EvaluationCategoriesAssign.objects.create(
                user_evaluation=self,
                evaluation_category=category
            )
            for rate in evaluation_rates.filter(evaluation_categories = category):
                EvaluationRateAssign.objects.create(
                    evaluation_categories_assign=category_assign,
                    evaluation_rates=rate
                )
                
            
    

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
            
        return context

    
    def serve(self, request):
        if request.method == 'POST':
            
            for user_evaluation in  request.user.client.user_evaluation.all():
                for category in user_evaluation.evaluation_categories_assign.all():
                    for rate in category.evaluation_rates_assign.all():
                        rate.rate = request.POST['question-'+str(rate.pk)]
                        rate.save()
            return super().serve(request)
        else:
            # Display event page as usual
            return super().serve(request)
            
        
    
    

    