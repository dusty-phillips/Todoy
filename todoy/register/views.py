from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout

from mongoengine.django.auth import User

from .forms import RegistrationForm

def register(request):
    if settings.DISABLE_REGISTRATION:
        return HttpResponseForbidden("Registration has been disabled on this server")

    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        User.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'])
        return redirect("/accounts/login/")
    
    return render(request, "accounts/register.html", {'form': form})

def login(request):
    form = AuthenticationForm(data=request.POST or None)
    
    if form.is_valid():
        auth_login(request, form.user_cache)
        return redirect("/home/%s/" % form.cleaned_data['username'])
    
    return render(request, 'accounts/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect("/")
