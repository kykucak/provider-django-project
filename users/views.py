from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .forms import UserRegistrationForm
from mainapp.models import Customer


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            new_customer = Customer(user=User.objects.get(email=form.cleaned_data['email']), phone='123', address='fjskafjd')
            new_customer.save()
            return redirect('home')
    form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'users/register.html', context=context)
