from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UsernameField
from django.contrib.auth import authenticate, login
# Create your views here.

def register(request):
    form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login(request):
    return render(request, 'users/login.html')


