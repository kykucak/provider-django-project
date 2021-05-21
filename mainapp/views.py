from django.shortcuts import render, redirect
from django.views.generic import View, DetailView
from django.core.mail import send_mail
from django.conf import settings

from .models import TVPlan, TelephonePlan, InternetPlan, Service
from .mixins import ServicePlansMixin
from .forms import OrderSubmissionForm

from random import choice

CT_MODEL__CLASS = {
        'internetplan': InternetPlan,
        'tvplan': TVPlan,
        'telephoneplan': TelephonePlan
    }


class BaseView(View):

    def get(self, request, *args, **kwargs):
        best_plans = [choice(TVPlan.objects.all()), choice(TelephonePlan.objects.all()), choice(InternetPlan.objects.all())]
        context = {
            'best_plans': best_plans
        }
        return render(request, 'base.html', context=context)


class ServiceDetailView(ServicePlansMixin, DetailView):

    def dispatch(self, request, *args, **kwargs):
        self.filter_param = request.GET.get('filter', '')
        return super().dispatch(request, *args, **kwargs)

    model = Service
    queryset = Service.objects.all()
    context_object_name = 'service'
    template_name = 'mainapp/service_details.html'


class PlanDetailView(DetailView):

    def dispatch(self, request, *args, **kwargs):
        self.model = CT_MODEL__CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'plan'
    template_name = 'mainapp/plan_details.html'
    slug_url_kwarg = 'slug'


def order_submission(request, **kwargs):
    order_form = OrderSubmissionForm(
        initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
    )
    ct_model, slug = kwargs.get('ct_model'), kwargs.get('slug')
    model = CT_MODEL__CLASS.get(ct_model)
    plan = model.objects.get(slug=slug)
    if request.method == 'POST':
        order_form = OrderSubmissionForm(request.POST)
        if order_form.is_valid():
            first_name = order_form.cleaned_data.get("first_name")
            last_name = order_form.cleaned_data.get("last_name")
            city = order_form.cleaned_data.get('city')
            street = order_form.cleaned_data.get('street')
            house = order_form.cleaned_data.get('house')
            subject = 'Order Plan in Shvarc'
            message = 'Hello, your order were sent to our manager and he will connect with you soon. Good day!\n' \
                      f'Address: {city} {street} {house}\n' \
                      f'Name: {first_name} {last_name}\n' \
                      f'Plan name: {plan.name}\n'
            recipient = order_form.cleaned_data.get('email')
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
            return redirect('home')

    context = {
        'order_form': order_form,
        'plan': plan
    }

    return render(request, 'mainapp/order_plan.html', context=context)





