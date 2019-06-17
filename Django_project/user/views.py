from django.shortcuts import render
from .forms import StockForm
from django.contrib import messages


def home(request):
    return render(request, 'user/home.html')

def about(request):
    return render(request, 'user/about.html')

def base(request):
    return render(request, 'user/base.html')

def user(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            print(request.POST)
            return render(request,'user/user.html')
        else:
            form = StockForm()

        return render(request,'user/about.html')
    return render(request, 'user/user.html')