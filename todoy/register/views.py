from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseForbidden

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
    
    return render_to_response("accounts/register.html",
            RequestContext(request, {'form': form}))

def login(request):
    from django.http import HttpResponse
    return HttpResponse("Boilerplate") 
