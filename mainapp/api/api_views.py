from rest_framework import viewsets

from ..models import Service, InternetPlan, WirelessPlan, TVPlan, Customer
from .serializers import ServiceSerializer, InternetPlanSerializer, WirelessPlanSerializer, TVPlanSerializer


class ServiceViewSet(viewsets.ModelViewSet):

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class InternetViewSet(viewsets.ModelViewSet):

    queryset = InternetPlan.objects.all()
    serializer_class = InternetPlanSerializer


class WirelessViewSet(viewsets.ModelViewSet):

    queryset = WirelessPlan.objects.all()
    serializer_class = WirelessPlanSerializer


class TvViewSet(viewsets.ModelViewSet):

    queryset = TVPlan.objects.all()
    serializer_class = TVPlanSerializer


# class CustomerViewSet(viewsets.ModelViewSet):
#
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer
