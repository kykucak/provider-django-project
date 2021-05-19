from django.shortcuts import render
from django.views.generic import View, DetailView

from .models import TVPlan, TelephonePlan, InternetPlan, Service
from .mixins import ServicePlansMixin

from random import choice


class BaseView(View):

    def get(self, request, *args, **kwargs):
        best_plans = [choice(TVPlan.objects.all()), choice(TelephonePlan.objects.all()), choice(InternetPlan.objects.all())]
        context = {
            'best_plans': best_plans
        }
        return render(request, 'base.html', context=context)


class ServiceDetailView(ServicePlansMixin, DetailView):

    model = Service
    queryset = Service.objects.all()
    context_object_name = 'service'
    template_name = 'mainapp/service_details.html'


class PlanDetailView(DetailView):

    CT_MODEL__CLASS = {
        'internetplan': InternetPlan,
        'tvplan': TVPlan,
        'telephoneplan': TelephonePlan
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL__CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'plan'
    template_name = 'mainapp/plan_details.html'
    slug_url_kwarg = 'slug'

class ProfileView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'mainapp/profile.html')

