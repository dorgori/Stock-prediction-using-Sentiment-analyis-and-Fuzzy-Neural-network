from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from .forms import UserRegistrationForm

def home(request):
    return render(request, 'user/home.html')

def about(request):
    return render(request, 'user/about.html')

def base(request):
    return render(request, 'user/base.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form' : form})