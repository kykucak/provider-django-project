from django.urls import path

from .views import BaseView, ServiceDetailView, PlanDetailView, order_submission

urlpatterns = [
    path('', BaseView.as_view(), name='home'),
    path('services/<str:slug>/', ServiceDetailView.as_view(), name='service_details'),
    path('plans/<str:ct_model>/<str:slug>/', PlanDetailView.as_view(), name='plan_details'),
    path('order-submission/<str:ct_model>/<str:slug>/', order_submission, name='order_submission'),
]
