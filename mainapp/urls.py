from django.urls import path

from .views import BaseView, ServiceDetailView, PlanDetailView, ProfileView

urlpatterns = [
    path('', BaseView.as_view(), name='home'),
    path('service-detail/', ServiceDetailView.as_view(), name='service_details'),
    path('plan-details/', PlanDetailView.as_view(), name='plan_details'),
    path('profile/', ProfileView.as_view(), name='profile')
]
