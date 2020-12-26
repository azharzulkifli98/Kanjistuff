from django.shortcuts import render
#from django.http import HttpResponsedef index(request):
#    return HttpResponse("<h1>Hello, this is not a disaster!</h1>")
# Create your views here.

def hello(request):
    return render(request, "template/home.html", {})