from django.core.mail import send_mail
from django.conf import settings


def admin_order_mail(order_data, admin_mail):
    """Sends notification order mail to 'admin_mail', with custom info passed to 'order_data' and 'plan_name'"""
    subject = 'New Order Shvarc'
    message = 'New order request was sent!\n' \
              f'Address: {order_data.get("city")} {order_data.get("street")} {order_data.get("house_num")}\n' \
              f'Name: {order_data.get("first_name")} {order_data.get("last_name")}\n' \
              f'Phone: {order_data.get("phone")}\n' \
              f'Plan name: {order_data.get("plan")}\n'
    recipient = admin_mail
    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)


def customer_order_mail(order_data):
    """
    Sends notification order mail to email passed in order submission form, with custom info passed to 'order_data'
    """
    subject = 'Order Plan in Shvarc'
    message = f'Hello, {order_data.get("first_name")}.\n' \
              f'Your order wes sent to our manager and he will connect with you soon.\nGood day!'
    recipient = order_data["email"]
    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
