from django.urls import path

from .views import (
    BaseView,
    ServiceDetailView,
    PlanDetailView,
    order_submission,
    ordered_plan_cancel,
    anonymous_order,
    service_in_use_order
)

urlpatterns = [
    path('', BaseView.as_view(), name='home'),
    path('services/<str:slug>/', ServiceDetailView.as_view(), name='service_details'),
    path('plans/<str:s_slug>/<str:p_slug>/', PlanDetailView.as_view(), name='plan_details'),
    path('order-submission/<str:s_slug>/<str:p_slug>/', order_submission, name='order_submission'),
    path('cancel-plan/<str:s_slug>/<str:p_slug>/', ordered_plan_cancel, name='cancel_plan'),
    path('anonym-order/', anonymous_order, name='anonym_order'),
    path('service_in_use/', service_in_use_order, name='service_in_use_order'),
]
