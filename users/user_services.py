from django.contrib.auth.models import User

from mainapp.models import Customer, OrderedPlansList


def create_customer__ordered_plan_list(username: str) -> None:
    """Creates customer and customer's ordered plan list"""
    new_customer = Customer.objects.create(user=User.objects.get(username=username))
    OrderedPlansList.objects.create(owner=new_customer)


def get_ordered_plan_list(user: User) -> OrderedPlansList:
    """Returns user's ordered plan list"""
    customer = Customer.objects.get(user=user)
    plans_list = OrderedPlansList.objects.get(owner=customer)
    return plans_list
