from django.shortcuts import render
from django.contrib import messages
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from Django_project.settings import PLOT_URL, CSV_URL
import csv
import glob
import pandas as pd
import matplotlib.pyplot as plt



def home(request):
    return render(request, 'user/home.html')

def about(request):
    return render(request, 'user/about.html')

def base(request):
    return render(request, 'user/base.html')

@login_required
def user(request):
    now = datetime.today()
    today = str(now)[:10]
    max_date = today
    image_exist = False
    stocks_names = ['AAPL', 'SPOT', 'MCRSFT']
    if request.method == 'POST':
        data = request.POST
        stock_name = data['stockName']
        print(stock_name)
        start_date = now - timedelta(days=5)
        end_date = now - timedelta(days=1)
        start_date = start_date.date()
        end_date = end_date.date()
        start_date = str(start_date)
        end_date = str(end_date)
        print(start_date)
        print(end_date)
        check_for_file(stock_name)
        #gets csv details
        #creating plot
        #save as image
        #get prediction

        plot_exist = True
        return render(request, 'user/user.html', {'max_date': max_date,
                                                  'plot_exist': plot_exist,
                                                  'stock_name': stock_name})
    else:
        return render(request, 'user/user.html', {'max_date': max_date,
                                                              'stocks_names': stocks_names})


def check_for_file(filename):
    close_gate_file = glob.glob(CSV_URL + '\\' + filename + '-prices.csv')[0]
    df = pd.read_csv(close_gate_file)
    stock_close_gate = df['Close']
    dates = df['Date']
    stock_close_gate = stock_close_gate[-5:]
    dates = dates[-5:]
    print(stock_close_gate)
    print(dates)
    plt.plot(stock_close_gate)
    plt.ylabel('1,2,3,4')
    #plt.ylabel(dates)
    plt.show()