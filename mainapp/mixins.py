from django.views.generic.detail import SingleObjectMixin

from .models import Service, TVPlan, WirelessPlan, InternetPlan

from .services import db_operations


class ServicePlansMixin(SingleObjectMixin):
    """
    Mixin for adding plans of a service to ServiceDetailView context data in order,
    that was passed in 'filter' argument
    """




