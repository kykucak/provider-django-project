from django.views.generic.detail import SingleObjectMixin

from .models import Service, TVPlan, TelephonePlan, InternetPlan


SERVICE_SLUG2PLAN_MODEL = {
    'tv': TVPlan,
    'wireless': TelephonePlan,
    'internet': InternetPlan
}


class ServicePlansMixin(SingleObjectMixin):

    ALLOWED_PARAMS = ['name', '-name', 'price', '-price']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if isinstance(self.get_object(), Service):
            model = SERVICE_SLUG2PLAN_MODEL[self.get_object().slug]
            order = self.filter_param
            if order not in self.ALLOWED_PARAMS:
                order = 'id'
            context['service_plans'] = model.objects.order_by(order)
        return context
