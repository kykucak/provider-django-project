from django.db import models
from django.urls import reverse
from django.conf import settings

from django.contrib.auth.models import User


def get_plan_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class Service(models.Model):

    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Plan(models.Model):

    class Meta:
        abstract = True

    name = models.CharField(max_length=255)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    slug = models.SlugField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    days_to_connect = models.IntegerField()
    description = models.TextField()

    def get_absolute_url(self):
        return get_plan_url(self, 'plan_details')

    def get_order_page(self):
        return get_plan_url(self, 'order_submission')

    def __str__(self):
        return self.name


class InternetPlan(Plan):

    speed = models.IntegerField()


class TelephonePlan(Plan):

    I3G = "3G"
    I4G = "4G"
    I5G = "5G"
    PHONE_INTERNET_TYPES_CHOICES = [
        (I3G, "3G"),
        (I4G, "4G"),
        (I5G, "5G")
    ]

    data_amount = models.IntegerField()
    internet_type = models.CharField(choices=PHONE_INTERNET_TYPES_CHOICES, max_length=2, default=I4G)
    minutes_out = models.IntegerField()
    # minutes_abroad = models.IntegerField()
    sms_amount = models.IntegerField()
    connect_with_passport = models.BooleanField()


class TVPlan(Plan):

    channels_amount = models.IntegerField()
    parent_control_available = models.BooleanField()


class Customer(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    # def __str__(self):
    #     return f"{self.user.first_name} {self.user.last_name}"

