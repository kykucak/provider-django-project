from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User


def get_url_with_service_slug_plan_slug(viewname, s_slug, p_slug):
    return reverse(viewname, kwargs={'s_slug': s_slug, 'p_slug': p_slug})


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
        """Returns url for a details view of the plan"""
        return get_url_with_service_slug_plan_slug('plan_details', self.service.slug, self.slug)

    def get_order_page(self):
        """Returns url for a view to order the plan"""
        return get_url_with_service_slug_plan_slug('order_submission', self.service.slug, self.slug)

    def __str__(self):
        return self.name


class InternetPlan(Plan):

    connection_type = models.CharField(max_length=255)
    speed = models.IntegerField()


class WirelessPlan(Plan):
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
    minutes_abroad = models.IntegerField()
    sms_amount = models.IntegerField()
    connect_with_passport = models.BooleanField()


class TVPlan(Plan):

    quality = models.CharField(max_length=20)
    channels_amount = models.IntegerField()
    parent_control_available = models.BooleanField()


class OrderedPlansList(models.Model):
    """A "cart" for customer's ordered plans"""

    plans = models.ManyToManyField('OrderedPlan', blank=True, related_name='related_plans')
    owner = models.ForeignKey('Customer', on_delete=models.CASCADE)
    final_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"List of {self.owner.user.first_name}"


class OrderedPlan(models.Model):
    """A plan, that a customer has ordered."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    owner = models.ForeignKey('Customer', on_delete=models.CASCADE)
    related_list = models.ForeignKey('OrderedPlansList', related_name='related_plans_list', on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)
    connected_at = models.DateField(null=True, blank=True)

    def get_cancel_url(self):
        """Returns url for a view that deletes the ordered plan"""
        return get_url_with_service_slug_plan_slug(
            'cancel_plan', self.content_object.service.slug, self.content_object.slug
        )

    def __str__(self):
        return f'{self.content_object.name} from {self.related_list.id} cart'


class Customer(models.Model):
    """A unit, that can operate with main part of site logic"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    house_num = models.IntegerField(null=True, blank=True)
    apartment_num = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"