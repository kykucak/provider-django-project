from django.shortcuts import render
from django.views.generic import View


class BaseView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'base.html')


class ServiceDetailView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'mainapp/service_details.html')


class PlanDetailView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'mainapp/plan_details.html')


class ProfileView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'mainapp/profile.html')

