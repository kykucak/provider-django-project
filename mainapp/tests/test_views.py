from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from bs4 import BeautifulSoup

from .. import views
from ..models import TVPlan, WirelessPlan, InternetPlan, Service, Customer, OrderedPlan, OrderedPlansList


def create_service(name: str = 'Internet', slug: str = 'internet'):
    """Creates and returns a service instance. By default, name='Internet' slug='internet'"""
    return Service.objects.create(name=name, slug=slug)


def create_net_plan(name: str = 'Internet 5', slug: str = 'net5', price: int = 100):
    """
    Creates and returns an internet plan instance. By default, name='Internet 5', slug='net5', price=100,
    days_to_connect=1, description='JFJFKJSLJFLSJFLSJ', connectino_type='ultra hard', speed='5'
    """
    plan = InternetPlan.objects.create(
        name=name,
        service=Service.objects.get(name='Internet'),
        slug=slug,
        price=price,
        days_to_connect=1,
        description='JFJFKJSLJFLSJFLSJ',
        connection_type='ultra hard',
        speed='5'
    )
    return plan


def create_wireless_plan(name: str = 'Ultra 4G', slug: str = 'ultra4g'):
    """
    Creates and returns a wireless plan instance.
    By default, name='Ultra 4G' slug='ultra4g', price=100, days_to_connect=1, description='JFJFKJSLJFLSJFLSJ'
    data_amount=20000, internet_type='4G', minutes_out=100, minutes_abroad=200, sms_amount=20,
    connect_with_passport=False
    """
    plan = WirelessPlan.objects.create(
        name=name,
        service=Service.objects.get(name='Wireless'),
        slug=slug,
        price=100,
        days_to_connect=1,
        description='JFJFKJSLJFLSJFLSJ',
        data_amount=20000,
        internet_type='4G',
        minutes_out=100,
        minutes_abroad=200,
        sms_amount=20,
        connect_with_passport=False
    )
    return plan


def create_tv_plan(name: str = 'TV 100', slug: str = 'tv100'):
    """
    Creates and returns a tv plan instance.
    By default, name='TV 100', slug='tv100', price=100, days_to_connect=1, description='JFJFKJSLJFLSJFLSJ',
    quality='4K', channels_amount=500, parent_control_available=True
    """
    plan = TVPlan.objects.create(
        name=name,
        service=Service.objects.get(name='Television'),
        slug=slug,
        price=100,
        days_to_connect=1,
        description='JFJFKJSLJFLSJFLSJ',
        quality='4K',
        channels_amount=500,
        parent_control_available=True
    )
    return plan


def create_user_customer(user_data: dict) -> list:
    """
    Creates and returns a list of a user instance with passed in 'user_data' info and a customer with values, by default,
    phone='test phone', city='test city', street='test street', house_num=13, apartment_num=18
    """
    user = get_user_model().objects.create_user(
        username=user_data['username'],
        first_name=user_data.get('first_name', ''),
        last_name=user_data.get('last_name', ''),
        email=user_data.get('email', ''),
        password=user_data['password']
    )
    customer = Customer.objects.create(
        user=user,
        phone='test phone',
        city='test city',
        street='test street',
        house_num=13,
        apartment_num=18
    )
    return [user, customer]


class BaseViewTestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse('home')

    def test_GET_with_one_plan_instance(self):
        """
        Tests BaseView for right context data('best_plans'), status code and resolver match function
        while there's only one plan instance
        :return:
        """
        create_service()
        create_net_plan()

        response = self.client.get(self.url)

        # BaseView class operates the request
        self.assertEqual(response.resolver_match.func.__name__, views.BaseView.as_view().__name__)
        # Right plans were uploaded
        self.assertEqual(response.context['best_plans'],
                         [TVPlan.objects.first(), WirelessPlan.objects.first(), InternetPlan.objects.first()])
        self.assertEqual(response.status_code, 200)

    def test_BaseView_GET_with_three_plan_instances(self):
        """
        Tests BaseView for right context data('best_plans'), status code and resolver match function
        while there are three plan instances
        :return:
        """
        create_service()
        create_net_plan()
        create_service('Wireless', 'wireless')
        create_wireless_plan()
        create_service('Television', 'tv')
        create_tv_plan()

        response = self.client.get(self.url)

        # BaseView class operates the request
        self.assertEqual(response.resolver_match.func.__name__, views.BaseView.as_view().__name__)
        # Right plans were uploaded
        self.assertEqual(response.context['best_plans'],
                         [TVPlan.objects.first(), WirelessPlan.objects.first(), InternetPlan.objects.first()]
                         )
        self.assertEqual(response.status_code, 200)


class ServiceDetailViewTestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.service = create_service()
        self.plan1 = create_net_plan()
        self.plan2 = create_net_plan('Smart Net', 'smartnet', 50)
        self.plan3 = create_net_plan('Unlim Ultra Net', 'unlimultranet', 200)
        self.plan_list = [self.plan1, self.plan2, self.plan3]
        self.url = reverse('service_details', kwargs={'slug': 'internet'})

    def test_ascending_name_order(self):
        """
        Tests ServiceDetailView for right plans order when an argument 'filter' is set to 'name'
        :return:
        """
        response = self.client.get(self.url, {'filter': 'name'})

        self.assertEqual(list(response.context['service_plans']),
                         sorted(self.plan_list, key=lambda plan: plan.name))
        self.assertEqual(response.status_code, 200)

    def test_descending_name_order(self):
        """
        Tests ServiceDetailView for right plans order when an argument 'filter' is set to '-name'
        :return:
        """
        response = self.client.get(self.url, {'filter': '-name'})
        self.assertEqual(list(response.context['service_plans']),
                         sorted(self.plan_list, key=lambda plan: plan.name, reverse=True))
        self.assertEqual(response.status_code, 200)

    def test_ascending_price_order(self):
        """
        Tests ServiceDetailView for right plans order when an argument 'filter' is set to 'price'
        :return:
        """
        response = self.client.get(self.url, {'filter': 'price'})

        self.assertEqual(list(response.context['service_plans']),
                         sorted(self.plan_list, key=lambda plan: plan.price))
        self.assertEqual(response.status_code, 200)

    def test_descending_price_order(self):
        """
        Tests ServiceDetailView for right plans order when an argument 'filter' is set to'-price'
        :return:
        """
        response = self.client.get(self.url, {'filter': '-price'})

        self.assertEqual(list(response.context['service_plans']),
                         sorted(self.plan_list, key=lambda plan: plan.price, reverse=True))
        self.assertEqual(response.status_code, 200)

    def test_no_filter_param(self):
        """
        Tests ServiceDetailView for right plans order when an argument 'filter' is not passed
        :return:
        """
        response = self.client.get(self.url)

        self.assertEqual(list(response.context['service_plans']), self.plan_list)
        self.assertEqual(response.status_code, 200)

    def test_invalid_filter_param(self):
        """
        Tests ServiceDetailView for right plans order when a passed argument 'filter' is invalid
        :return:
        """
        response = self.client.get(self.url, {'filter': 'weird123'})

        self.assertEqual(list(response.context['service_plans']), self.plan_list)
        self.assertEqual(response.status_code, 200)

    def test_right_context_service(self):
        """Tests ServiceDetailView for right context data('service')"""
        response = self.client.get(self.url)

        self.assertEqual(response.context['service'], self.service)
        self.assertEqual(response.status_code, 200)

    def test_wrong_slug(self):
        """Tests ServiceDetailView for a right status code when passed 'slug' is invalid"""
        response = self.client.get(reverse('service_details', kwargs={'slug': 'weird_slug'}))

        self.assertEqual(response.status_code, 404)


class PlanDetailViewTestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        create_service()
        self.plan = create_net_plan()
        self.user_credentials = {
            'username': 'testuser',
            'password': 'testing321'
        }
        self.user, self.customer = create_user_customer(self.user_credentials)
        self.url = self.plan.get_absolute_url()

    def test_context_data_with_no_login(self):
        """
        Tests context data and order button info when user is not authenticated
        :return:
        """
        response = self.client.get(self.url)
        soup = BeautifulSoup(response.rendered_content, 'html.parser')
        order_btn = soup.find(class_='btn btn-success')

        self.assertEqual(order_btn.get('href').strip(), reverse('anonym_order'))
        self.assertEqual(order_btn.text, 'Order')
        self.assertEqual(response.context.get('service_in_use'), False)
        self.assertEqual(response.context.get('is_ordered'), False)
        self.assertEqual(response.context.get('plan'), self.plan)
        self.assertEqual(response.status_code, 200)

    def test_context_data_with_login_and_no_ordered_plan(self):
        """
        Tests context data and order button info when user is authenticated
        and don't have an ordered plan in the service.
        :return:
        """
        self.client.login(**self.user_credentials)
        response = self.client.get(self.url)

        soup = BeautifulSoup(response.rendered_content, 'html.parser')
        order_btn = soup.find(class_='btn btn-success')

        self.assertEqual(order_btn.get('href').strip(), self.plan.get_order_page())
        self.assertEqual(order_btn.text, 'Order')
        self.assertEqual(response.context.get('service_in_use'), False)
        self.assertEqual(response.context.get('is_ordered'), False)
        self.assertEqual(response.context.get('plan'), self.plan)
        self.assertEqual(response.status_code, 200)

    def test_context_data_with_login_and_check_ordered_plan(self):
        """
        Tests context data and order button info when user is authenticated
        and have an ordered plan that he's checking now
        :return:
        """
        ordered_plan_list = OrderedPlansList.objects.create(
            owner=self.customer
        )
        ordered_plan = OrderedPlan.objects.create(
            content_object=self.plan,
            owner=self.customer,
            related_list=ordered_plan_list
        )
        ordered_plan_list.plans.add(ordered_plan)

        self.client.login(**self.user_credentials)
        response = self.client.get(self.url)

        soup = BeautifulSoup(response.rendered_content, 'html.parser')
        order_btn = soup.find(class_='btn btn-success')

        self.assertEqual(order_btn.text, 'Already ordered')
        self.assertEqual(order_btn.get('href'), None)
        self.assertEqual(response.context.get('service_in_use'), True)
        self.assertEqual(response.context.get('is_ordered'), True)
        self.assertEqual(response.context.get('plan'), self.plan)
        self.assertEqual(response.status_code, 200)

    def test_context_data_with_login_and_ordered_plan(self):
        """
        Tests context data and order button info when user is authenticated
        and check a plan of the service, the plan of which he's already ordered
        :return:
        """
        ordered_plan_list = OrderedPlansList.objects.create(
            owner=self.customer
        )
        ordered_plan = OrderedPlan.objects.create(
            content_object=self.plan,
            owner=self.customer,
            related_list=ordered_plan_list
        )
        ordered_plan_list.plans.add(ordered_plan)
        plan2 = create_net_plan(name='Giga Speed', slug='gigaspeed')

        self.client.login(**self.user_credentials)
        response = self.client.get(plan2.get_absolute_url())

        soup = BeautifulSoup(response.rendered_content, 'html.parser')
        order_btn = soup.find(class_='btn btn-success')

        self.assertEqual(order_btn.text, 'Order')
        self.assertEqual(order_btn.get('href').strip(), reverse('service_in_use_order'))
        self.assertEqual(response.context.get('service_in_use'), True)
        self.assertEqual(response.context.get('is_ordered'), False)
        self.assertEqual(response.context.get('plan'), plan2)
        self.assertEqual(response.status_code, 200)


class OrderSubmissionTesCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user_credentials = {
            'username': 'testuser',
            'first_name': 'testname',
            'last_name': 'testsurname',
            'email': 'test@email.com',
            'password': 'testing321'
        }
        self.user, self.customer = create_user_customer(self.user_credentials)
        OrderedPlansList.objects.create(
            owner=self.customer
        )
        create_service(name='Internet', slug='internet')
        self.plan = create_net_plan()
        self.url = self.plan.get_order_page()

    def test_GET_with_no_login(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_GET_with_login(self):
        self.client.login(**self.user_credentials)

        response = self.client.get(self.url)

        self.assertEqual(response.templates[0].name, 'mainapp/order_plan.html')
        self.assertEqual(response.context['plan'], self.plan)
        self.assertEqual(response.status_code, 200)

    def test_POST_with_valid_form_data(self):
        """
        Tests order_submission view for correct changing customer's info with passed valid data
        :return:
        """
        self.client.login(**self.user_credentials)

        response = self.client.post(self.url, data={
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'phone': '0674324959',
            'city': 'Kharkiv',
            'street': 'Teststreet',
            'house_num': 13,
            'apartment_num': 58
        })

        self.assertEqual(Customer.objects.get(user=self.user).city, 'Kharkiv')
        self.assertIn(OrderedPlan.objects.filter(object_id=self.plan.id, owner=self.customer).first(),
                      OrderedPlansList.objects.get(owner=self.customer).plans.all())
        self.assertEqual(response.status_code, 302)

    def test_POST_with_invalid_form_data(self):
        """
        Tests order_submission view for not changing customer's info with passed invalid data
        :return:
        """
        self.client.login(**self.user_credentials)

        response = self.client.post(self.url, data={
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': 'voha228',
            'phone': '0674324959',
            'city': 'Kharkiv',
            'street': 'Teststreet',
            'house_num': 13,
            'apartment_num': 58
        })

        self.assertEqual(response.templates[0].name, 'mainapp/order_plan.html')
        self.assertNotEqual(self.customer.city, 'Kharkiv')
        self.assertEqual(response.status_code, 200)


class OrderedPlanCancelTestCase(TestCase):

    def setUp(self) -> None:
        """
        Set up user credentials, user, customer, plan, ordered_plan_list for the customer, ordered_plan, and url
        :return:
        """
        self.client = Client()
        self.user_credentials = {
            'username': 'testuser',
            'first_name': 'testname',
            'last_name': 'testsurname',
            'email': 'test@email.com',
            'password': 'testing321'
        }
        self.user, self.customer = create_user_customer(self.user_credentials)
        create_service(name='Internet', slug='internet')
        self.plan = create_net_plan()
        self.ordered_plan_list = OrderedPlansList.objects.create(
            owner=self.customer
        )
        self.ordered_plan = OrderedPlan.objects.create(
            content_object=self.plan,
            related_list=self.ordered_plan_list,
            owner=self.customer
        )
        self.ordered_plan_list.plans.add(self.ordered_plan)
        self.url = self.ordered_plan.get_cancel_url()

    def test_no_login(self):
        """Tests ordered_plan_cancel with unauthenticated user"""
        response = self.client.get(self.url)

        self.assertEqual(response.url, f'/login/?next={self.url}')
        self.assertEqual(response.status_code, 302)

    def test_GET(self):
        """Tests ordered_plan_cancel for correct deleting ordered plan from customer's ordered plan list"""
        self.client.login(**self.user_credentials)

        response = self.client.get(self.url)

        self.assertIsNone(OrderedPlan.objects.filter(content_type=self.ordered_plan.content_type,
                                                     owner=self.customer).first())
        self.assertNotIn(
            OrderedPlan.objects.filter(content_type=self.ordered_plan.content_type, owner=self.customer).first(),
            OrderedPlansList.objects.get(owner=self.customer).plans.all()
        )
        self.assertEqual(response.url, reverse('account'))
        self.assertEqual(response.status_code, 302)


class AnonymousOrderTestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse('anonym_order')

    def test_GET(self):
        response = self.client.get(self.url)

        self.assertEqual(response.url, reverse('login'))
        self.assertEqual(response.status_code, 302)


class ServiceInUseOrderTestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user_credentials = {
            'username': 'testuser',
            'first_name': 'testname',
            'last_name': 'testsurname',
            'email': 'test@email.com',
            'password': 'testing321'
        }
        self.user, self.customer = create_user_customer(self.user_credentials)
        self.url = reverse('service_in_use_order')

    def test_no_login(self):
        response = self.client.get(self.url)

        self.assertEqual(response.url, f'/login/?next={self.url}')
        self.assertEqual(response.status_code, 302)

    def test_GET(self):
        self.client.login(**self.user_credentials)

        response = self.client.get(self.url)

        self.assertEqual(response.url, reverse('account'))
        self.assertEqual(response.status_code, 302)
