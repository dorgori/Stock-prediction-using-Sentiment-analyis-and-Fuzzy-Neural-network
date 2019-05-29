from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django import forms
from .forms import UserRegistrationForm

# Create your views here.
def home(request):
    return render(request, 'site/home.html')

def about(request):
    return render(request, 'site/about.html')

def register(request):
    return render(request, 'site/register.html')