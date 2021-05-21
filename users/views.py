from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .forms import UserRegistrationForm, UserUpdateForm
from mainapp.models import Customer


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            new_customer = Customer(user=User.objects.get(email=form.cleaned_data['email']), phone='123', address='fjskafjd')
            new_customer.save()
            return redirect('login')
    form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'users/register.html', context=context)


def account(request):
    u_form = UserUpdateForm(instance=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return redirect('account')

    context = {
        'u_form': u_form
    }

    return render(request, 'users/account.html', context=context)
