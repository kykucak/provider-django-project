from django.views.generic.detail import SingleObjectMixin

from .models import Service, TVPlan, TelephonePlan, InternetPlan


SERVICE_SLUG2PLAN_MODEL = {
    'tv': TVPlan,
    'wireless': TelephonePlan,
    'internet': InternetPlan
}


class ServicePlansMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if isinstance(self.get_object(), Service):
            model = SERVICE_SLUG2PLAN_MODEL[self.get_object().slug]
            context['service_plans'] = model.objects.all()
        return context
