from django.views.generic.detail import SingleObjectMixin

from .models import Service, TVPlan, WirelessPlan, InternetPlan


SERVICE_SLUG2PLAN_MODEL = {
    'tv': TVPlan,
    'wireless': WirelessPlan,
    'internet': InternetPlan
}


class ServicePlansMixin(SingleObjectMixin):
    """
    Mixin for adding plans of a service to ServiceDetailView context data in order,
    that was passed in 'filter' argument
    """

    ALLOWED_PARAMS = ['name', '-name', 'price', '-price']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if isinstance(self.get_object(), Service):
            model = SERVICE_SLUG2PLAN_MODEL[self.get_object().slug]
            if self.filter not in self.ALLOWED_PARAMS:
                self.filter = 'id'
            context['service_plans'] = model.objects.order_by(self.filter)
        return context
