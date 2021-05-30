from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm, UserUpdateForm
from mainapp.models import Customer, OrderedPlansList


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            new_customer = Customer.objects.create(user=User.objects.get(username=form.cleaned_data['username']))
            OrderedPlansList.objects.create(owner=new_customer)
            messages.add_message(request, messages.SUCCESS, 'Your account was successfully created!')
            return redirect('login')
    form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'users/register.html', context=context)


@login_required
def account(request):
    u_form = UserUpdateForm(instance=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.add_message(request, messages.SUCCESS, 'Your account info was successfully updated!')
            return redirect('account')

    customer = Customer.objects.get(user=request.user)
    plans_list = OrderedPlansList.objects.filter(owner=customer).first()
    context = {
        'u_form': u_form,
        'plans_list': plans_list
    }

    return render(request, 'users/account.html', context=context)
