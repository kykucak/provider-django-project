from django.contrib import admin

from .models import *

admin.site.register(Service)
admin.site.register(TVPlan)
admin.site.register(WirelessPlan)
admin.site.register(InternetPlan)
admin.site.register(Customer)
admin.site.register(OrderedPlan)
admin.site.register(OrderedPlansList)
