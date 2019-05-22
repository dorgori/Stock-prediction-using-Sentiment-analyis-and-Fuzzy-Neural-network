from django.http import HttpResponseRedirect
from django.shortcuts import render

def home(request):
    return render(request, 'user/home.html')

def about(request):
    return render(request, 'user/about.html')