from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm, UserUpdateForm
from .user_services import create_customer__ordered_plan_list, get_ordered_plan_list


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            create_customer__ordered_plan_list(form.cleaned_data.get('username'))
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

    plan_list = get_ordered_plan_list(request.user)
    context = {
        'u_form': u_form,
        'plans_list': plan_list
    }

    return render(request, 'users/account.html', context=context)
