from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.views.generic import View, DetailView
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

from .models import TVPlan, WirelessPlan, InternetPlan, Service, Customer, OrderedPlan, OrderedPlansList
from .mixins import ServicePlansMixin
from .forms import OrderSubmissionForm


CT_MODEL__CLASS = {
    'internetplan': InternetPlan,
    'tvplan': TVPlan,
    'wirelessplan': WirelessPlan
}


def fill_customer_after_order(customer, order_data):
    """

    :param customer:
    :param order_data:
    :return:
    """
    customer.phone = order_data['phone']
    customer.city = order_data['city']
    customer.street = order_data['street']
    customer.house_num = order_data['house_num']
    customer.apartment_num = order_data['apartment_num']
    customer.save()


def admin_order_mail(admin_mail, order_data, plan_name):
    subject = 'New Order Shvarc'
    message = 'New order request was sent!\n' \
              f'Address: {order_data["city"]} {order_data["street"]} {order_data["house_num"]}\n' \
              f'Name: {order_data["first_name"]} {order_data["last_name"]}\n' \
              f'Phone: {order_data["phone"]}\n' \
              f'Plan name: {plan_name}\n'
    recipient = admin_mail
    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)


def customer_order_mail(order_data):
    subject = 'Order Plan in Shvarc'
    message = f'Hello, {order_data["first_name"]}.\n' \
              f'Your order wes sent to our manager and he will connect with you soon.\nGood day!'
    recipient = order_data["email"]
    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)


class BaseView(View):

    def get(self, request, *args, **kwargs):
        best_plans = [TVPlan.objects.first(), WirelessPlan.objects.first(), InternetPlan.objects.first()]
        context = {
            'best_plans': best_plans
        }
        return render(request, 'base.html', context=context)


class ServiceDetailView(ServicePlansMixin, DetailView):

    def dispatch(self, request, *args, **kwargs):
        self.filter = request.GET.get('filter')
        return super().dispatch(request, *args, **kwargs)

    model = Service
    queryset = Service.objects.all()
    context_object_name = 'service'
    template_name = 'mainapp/service_details.html'


class PlanDetailView(DetailView):

    def dispatch(self, request, *args, **kwargs):
        self.model = CT_MODEL__CLASS[kwargs['ct_model']]
        self.queryset = self.model.objects.all()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_in_use = False
        plan_is_ordered = False
        if self.request.user.is_authenticated:
            customer = Customer.objects.get(user=self.request.user)
            ordered_plans = OrderedPlan.objects.filter(owner=customer).all()

            for item in ordered_plans:
                if item.content_object.service == self.get_object().service:
                    service_in_use = True
                if item.content_object == self.get_object():
                    plan_is_ordered = True

        context['service_in_use'] = service_in_use
        context['is_ordered'] = plan_is_ordered
        return context

    context_object_name = 'plan'
    template_name = 'mainapp/plan_details.html'
    slug_url_kwarg = 'slug'


@login_required
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
            # sending notification mails
            admin_order_mail("kykucak@gmail.com", order_form.cleaned_data, plan.name)
            customer_order_mail(order_form.cleaned_data)

            # filling customer with new data
            customer = Customer.objects.get(user=request.user)
            fill_customer_after_order(customer, order_form.cleaned_data)

            # create orderedplan instance
            plan_list = OrderedPlansList.objects.get(owner=customer)
            ordered_plan = OrderedPlan.objects.create(
                content_object=plan,
                related_list=plan_list,
                owner=customer
            )
            plan_list.plans.add(ordered_plan)
            messages.add_message(request, messages.SUCCESS, 'A mail with instructions was sent to your email!')
            return redirect('home')

    context = {
        'order_form': order_form,
        'plan': plan
    }

    return render(request, 'mainapp/order_plan.html', context=context)


@login_required
def ordered_plan_cancel(request, **kwargs):
    ct_model, slug = kwargs['ct_model'], kwargs['slug']
    content_type = ContentType.objects.get(model=ct_model)
    plan = content_type.model_class().objects.get(slug=slug)
    customer = Customer.objects.get(user=request.user)
    ordered_plan_list = OrderedPlansList.objects.get(owner=customer)
    ordered_plan = OrderedPlan.objects.get(
        content_type=content_type,
        object_id=plan.id,
        owner=customer,
        related_list=ordered_plan_list
    )

    ordered_plan_list.plans.remove(ordered_plan)
    ordered_plan.delete()

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
