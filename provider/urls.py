from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from mainapp.api import api_views

router = routers.DefaultRouter()
router.register(r'services', api_views.ServiceViewSet)
router.register(r'internet', api_views.InternetViewSet)
router.register(r'wireless', api_views.WirelessViewSet)
router.register(r'tv', api_views.TvViewSet)
# router.register(r'customers', api_views.CustomerViewSet)

urlpatterns = [
    path('', include('mainapp.urls')),
    path('', include('users.urls')),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls)
]
