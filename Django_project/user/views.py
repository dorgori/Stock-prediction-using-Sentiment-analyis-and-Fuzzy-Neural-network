from django.shortcuts import render
from .forms import StockForm
from django.contrib import messages
from datetime import datetime, timedelta



def home(request):
    return render(request, 'user/home.html')

def about(request):
    return render(request, 'user/about.html')

def base(request):
    return render(request, 'user/base.html')

def user(request):
    now = datetime.today()
    today = datetime.strftime(now , '%Y-%m-%d')
    max_day = today

    if request.method == 'POST':
        form = StockForm(request.POST)
        data = request.POST
        max_date = today
        stock_name = data['symbol']
        if form.is_valid():
            print(request.POST)
            return render(request,'user/user.html', {'max_date': max_date,
                                                     'stock_name': stock_name})
        else:
            form = StockForm()
            return render(request, 'user/about.html')

    return render(request, 'user/user.html')