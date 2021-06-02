from django.shortcuts import render, redirect
from django.views.generic import View, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Service
from .forms import OrderSubmissionForm
from .services.db_operations import *
from .services.mailing import *


class BaseView(View):
    """Renders main page of the project with best_plans in context data"""

    def get(self, request, *args, **kwargs):
        best_plans = get_best_plans()
        context = {
            'best_plans': best_plans
        }
        return render(request, 'base.html', context=context)


class ServiceDetailView(DetailView):
    """Renders page with plans of the service, and filtering function, which works by passing filter argument in url"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plan = get_plan_model(self.get_object().slug)
        q_filter = self.request.GET.get('filter')

        context['service_plans'] = get_plans_ordered_by_filter(plan, q_filter)
        return context

    model = Service
    queryset = Service.objects.all()
    context_object_name = 'service'
    template_name = 'mainapp/service_details.html'


class PlanDetailView(DetailView):
    """
    Renders page with plan details and "Order" button, which display 'Already ordered', if 'pla_is_ordered' is True,
    if 'plan_in_use' is True, then redirects you to account page and ask to delete already ordered plan in that service,
    if they both are False, user is redirected to order_submission view
    """

    def dispatch(self, request, *args, **kwargs):
        self.model = get_plan_model(kwargs.get('s_slug'))
        self.queryset = self.model.objects.all()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            service_in_use = is_service_in_use(self.get_object().service, self.request.user)
            plan_is_ordered = is_ordered(self.get_object(), self.request.user)
        else:
            service_in_use, plan_is_ordered = False

        context['service_in_use'] = service_in_use
        context['is_ordered'] = plan_is_ordered
        return context

    context_object_name = 'plan'
    template_name = 'mainapp/plan_details.html'
    slug_url_kwarg = 'p_slug'


@login_required
def order_submission(request, **kwargs):
    """
    Renders page with order form with pre-pasted first name, last name, and email from user info,
    if form is valid, ordered_plan with is_confirmed=False is created and added to customer ordered plan list, then
    user is redirected to home page with message about succeed mail sending
    """
    s_slug, p_slug = kwargs.get('s_slug'), kwargs.get('p_slug')

    plan = get_plan_instance(s_slug, p_slug)
    customer = get_customer(request.user)
    order_form = OrderSubmissionForm(
        initial={
            'plan': plan.name,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phone': customer.phone,
            'city': customer.city,
            'street': customer.street,
            'house_num': customer.house_num,
            'apartment_num': customer.apartment_num
        }
    )

    if request.method == 'POST':
        order_form = OrderSubmissionForm(request.POST)
        if order_form.is_valid():
            # sending notification mails
            admin_order_mail(order_form.cleaned_data, "kykucak@gmail.com")
            customer_order_mail(order_form.cleaned_data)

            # filling customer with new data
            update_customer_data_after_order(order_form.cleaned_data, request.user)

            create_ordered_plan(plan, request.user)

            messages.add_message(request, messages.SUCCESS, 'A mail with instructions was sent to your email!')
            return redirect('home')

    context = {
        'order_form': order_form,
        'plan': plan
    }

    return render(request, 'mainapp/order_plan.html', context=context)


@login_required
def ordered_plan_cancel(request, **kwargs):
    """
    Deletes an ordered plan by passed arguments in url
    and redirects to account page with message, plan was successfully deleted
    """
    s_slug, p_slug = kwargs['s_slug'], kwargs['p_slug']

    delete_ordered_plan(get_plan_instance(s_slug, p_slug), request.user)

    messages.add_message(request, messages.SUCCESS, 'The plan was successfully deleted!')
    return redirect('account')


def anonymous_order(request):
    """User tries to order plan without being authenticated"""
    messages.add_message(request, messages.INFO, 'Before you can order plans, you must login first.')
    return redirect('login')


@login_required
def service_in_use_order(request):
    """User tries to order plan when he already has another ordered plan for the service"""
    messages.add_message(request, messages.INFO,
                         f'You already have an ordered plan for this service.'
                         'In order to switch your plan - delete your active one and choose other.')
    return redirect('account')
