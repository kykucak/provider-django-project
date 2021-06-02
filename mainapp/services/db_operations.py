from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.contrib.contenttypes.models import ContentType

from mainapp.models import TVPlan, WirelessPlan, InternetPlan, Service, Customer, OrderedPlan, OrderedPlansList

SERVICE_SLUG2PLAN_MODEL = {
    'tv': TVPlan,
    'wireless': WirelessPlan,
    'internet': InternetPlan
}

CT_MODEL__CLASS = {
    'internetplan': InternetPlan,
    'tvplan': TVPlan,
    'wirelessplan': WirelessPlan
}


def get_ordered_plan_list_by_user(user: User) -> OrderedPlansList:
    """Returns ordered plan user for a particular user"""
    customer = Customer.objects.get(user=user)
    plan_list = OrderedPlansList.objects.get(owner=customer)
    return plan_list


def get_best_plans() -> list:
    """Returns a list of 3 Plan objects"""
    best_plans = [TVPlan.objects.first(), WirelessPlan.objects.first(), InternetPlan.objects.first()]
    return best_plans


def get_plan_model(slug: str):
    """Returns Plan object with passed service slug"""
    model = SERVICE_SLUG2PLAN_MODEL.get(slug)
    return model


def get_plan_instance(s_slug, p_slug):
    """Returns Plan object with passed service and plan slugs"""
    plan = get_plan_model(s_slug).objects.get(slug=p_slug)
    return plan


def is_service_in_use(service: Service, user: User) -> bool:
    """Returns True if service has an ordered plan by user, otherwise False"""
    plan_list = get_ordered_plan_list_by_user(user)

    service_in_use = False
    for item in plan_list.plans.all():
        if item.content_object.service == service:
            service_in_use = True
            break

    return service_in_use


def is_ordered(plan, user: User) -> bool:
    """Returns True if passed plan is already in user's ordered plan list, otherwise False"""
    plan_list = get_ordered_plan_list_by_user(user)

    plan_is_ordered = False
    for item in plan_list.plans.all():
        if item.content_object == plan:
            plan_is_ordered = True

    return plan_is_ordered


def get_plans_ordered_by_filter(model, q_filter):
    """Returns filtered plans in a specific order (name, -name, price, -price)"""
    try:
        plans = model.objects.order_by(q_filter)
    except FieldError:
        plans = model.objects.all()
    return plans


def create_ordered_plan(plan, user: User):
    """Creates user's ordered plan"""
    customer = Customer.objects.get(user=user)
    plan_list = OrderedPlansList.objects.get(owner=customer)
    ordered_plan = OrderedPlan.objects.create(
        content_object=plan,
        related_list=plan_list,
        owner=customer
    )
    plan_list.plans.add(ordered_plan)

    return ordered_plan


def delete_ordered_plan(plan, user: User):
    """Deletes user's ordered plan"""
    customer = Customer.objects.get(user=user)
    ordered_plan_list = OrderedPlansList.objects.get(owner=customer)
    content_type = ContentType.objects.get(model=plan.__class__._meta.model_name)
    ordered_plan = OrderedPlan.objects.get(
        content_type=content_type,
        object_id=plan.id,
        owner=customer,
        related_list=ordered_plan_list
    )
    ordered_plan_list.plans.remove(ordered_plan)
    ordered_plan.delete()


def update_customer_data_after_order(order_data, user: User):
    """Fills customer's data to paste it into account info"""
    customer = Customer.objects.get(user=user)

    customer.phone = order_data['phone']
    customer.city = order_data['city']
    customer.street = order_data['street']
    customer.house_num = order_data['house_num']
    customer.apartment_num = order_data['apartment_num']
    customer.save()


def get_customer(user: User):
    customer = Customer.objects.get(user=user)
    return customer
