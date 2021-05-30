from django.contrib.auth.models import User
from rest_framework import serializers

from ..models import Service, InternetPlan, WirelessPlan, TVPlan, Customer


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = ['name', 'slug']


class BasePlanSerializer:

    name = serializers.CharField()
    service = ServiceSerializer()
    slug = serializers.SlugField()
    price = serializers.DecimalField(max_digits=9, decimal_places=2)
    days_to_connect = serializers.IntegerField()
    description = serializers.CharField()


class InternetPlanSerializer(BasePlanSerializer, serializers.ModelSerializer):

    class Meta:
        model = InternetPlan
        fields = '__all__'


class WirelessPlanSerializer(BasePlanSerializer, serializers.ModelSerializer):

    class Meta:
        model = WirelessPlan
        fields = '__all__'


class TVPlanSerializer(BasePlanSerializer, serializers.ModelSerializer):

    class Meta:
        model = TVPlan
        fields = '__all__'
