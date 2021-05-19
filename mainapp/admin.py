from django.contrib import admin

from .models import *

admin.site.register(Service)
admin.site.register(TVPlan)
admin.site.register(TelephonePlan)
admin.site.register(InternetPlan)
admin.site.register(Customer)
