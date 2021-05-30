from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from mainapp.models import Customer, OrderedPlansList, OrderedPlan
from mainapp.tests.test_views import create_service, create_net_plan


def create_user_customer(user_data: dict) -> list:
    user = User.objects.create_user(
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


class UserTestCase(TestCase):
    """
    Tests User registration and login views for right redirecting, creating instances and status codes
    """

    def setUp(self):
        self.client = Client()
        self.user_credentials = {
            'username': 'testname',
            'email': 'kykucak@gmail.com',
            'first_name': 'Test',
            'last_name': 'Testovich',
            'password1': 'testing321',
            'password2': 'testing321'
        }
        self.user_login_data = {
            'username': self.user_credentials['username'],
            'password': self.user_credentials['password1']
        }

    def test_GET(self):
        response = self.client.get(reverse('register'))

        self.assertEqual(response.templates[0].name, 'users/register.html')
        self.assertEqual(response.status_code, 200)

    def test_user_registration(self):
        """
        Checks whether User, Customer of the user, OrderedPlansList of the customer are created
        and user is redirected to a 'login' page.
        :return:
        """
        response = self.client.post(reverse('register'), data=self.user_credentials)
        # User was created
        user = User.objects.filter(username=self.user_credentials['username']).first()
        self.assertIn(user, User.objects.all())
        # Customer was created
        customer = Customer.objects.filter(user=user).first()
        self.assertIn(customer, Customer.objects.all())
        # OrderedPlansList was created
        self.assertIn(OrderedPlansList.objects.filter(owner=customer).first(), OrderedPlansList.objects.all())
        # User was redirected to a login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/')

    def test_user_login(self):
        """
        Checks whether User is redirected to a home page.
        :return:
        """
        pas = self.user_credentials.pop('password2')
        self.user_credentials['password'] = pas
        create_user_customer(self.user_credentials)

        response = self.client.post('/login/', data=self.user_login_data)

        self.assertTrue(response.wsgi_request.user.is_authenticated)
        # User is redirected to a home page
        self.assertEqual(response.url, reverse('home'))
        self.assertEqual(response.status_code, 302)


class AccountTestCase(TestCase):
    """
    Tests Account view for updating the fields and status codes
    """

    def setUp(self) -> None:
        self.client = Client()
        self.user_credentials = {
            'username': 'testname',
            'email': 'kykucak@gmail.com',
            'first_name': 'Test',
            'last_name': 'Testovich',
            'password': 'testing321',
            'password2': 'testing321'
        }
        self.data_to_change = {
            'username': self.user_credentials.get('username'),
            'email': 'new_test@email.com',
            'first_name': 'new_name',
            'last_name': 'new_surname'
        }
        self.user, self.customer = create_user_customer(self.user_credentials)
        self.url = reverse('account')

    def test_GET_login(self):
        self.client.login(**self.user_credentials)
        create_service()
        plan = create_net_plan()
        plan_list = OrderedPlansList.objects.create(
            owner=self.customer
        )
        ordered_plan = OrderedPlan.objects.create(
            content_object=plan,
            owner=self.customer,
            related_list=plan_list
        )
        plan_list.plans.add(ordered_plan)

        response = self.client.get(self.url)

        self.assertEqual(response.context.get('plans_list'), plan_list)
        self.assertEqual(response.status_code, 200)

    def test_GET_no_login(self):
        """
        Checks whether unauthenticated user is sent to login page
        :return:
        """
        response = self.client.get(self.url)

        # User is redirected to login page
        self.assertEqual(response.url, f'/login/?next={self.url}')
        self.assertEqual(response.status_code, 302)

    def test_update_with_valid_data(self):
        self.client.login(**self.user_credentials)

        response = self.client.post(self.url, data=self.data_to_change)

        self.assertIsNotNone(User.objects.filter(first_name=self.data_to_change.get('first_name')).first())
        self.assertEqual(response.url, self.url)
        self.assertEqual(response.status_code, 302)

    def test_update_with_invalid_data(self):
        self.client.login(**self.user_credentials)
        invalid_data = {
            'password': 'mypassword1321'
        }

        response = self.client.post(self.url, data=invalid_data)

        self.assertIsNone(User.objects.filter(password=invalid_data['password']).first())
        self.assertEqual(response.status_code, 200)
