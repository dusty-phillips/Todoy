from .forms import RegistrationForm
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from mongoengine.django.auth import User

def register(request):
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
