from django.shortcuts import render
from django.views.generic import *


# Create your views here.
class HomeView(TemplateView):
    template_name = 'bookSwiping/home.html'
    extra_context = {}

class LoginView(TemplateView):
    template_name = 'bookSwiping/login.html'
    extra_context = {}

class SignupView(TemplateView):
    template_name = 'bookSwiping/signup.html'
    extra_context = {}