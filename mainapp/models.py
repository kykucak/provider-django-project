from django.db import models


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
    sms_amount = models.IntegerField()
    connect_with_passport = models.BooleanField()


class TVPlan(Plan):

    channels_amount = models.IntegerField()
    parent_control_available = models.BooleanField()
