from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "index.html")

@login_required
def user_home(request, username):
    return render(request, "home.html")

@login_required
def user_manifest(request, username):
    return render(request, "cache.manifest", content_type="text/cache-manifest")
