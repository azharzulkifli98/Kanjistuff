from django.shortcuts import render
from django.http import HttpResponsedef index(request):
    return HttpResponse("Hello, this is not a disaster!")
# Create your views here.
