from django.http import HttpResponse

def list(request):
    return HttpResponse('hello world')

