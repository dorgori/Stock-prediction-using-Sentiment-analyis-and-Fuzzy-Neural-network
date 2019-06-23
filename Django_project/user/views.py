from django.shortcuts import render
from django.contrib import messages
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from Django_project.settings import PLOT_URL, CSV_URL
import csv
import numpy as np
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
        plot = check_for_file(stock_name)

        stock_vals = get_values(plot, 0)
        dates = get_values(plot,1)

        print(dates)
        #gets csv details
        #creating plot
        #save as image
        #get prediction
        if plot != None:
            plot_exist = True
        return render(request, 'user/user.html', {'max_date': max_date,
                                                  'plot_exist': plot_exist,
                                                  'stockVal5': stock_vals[0],
                                                  'stockVal4': stock_vals[1],
                                                  'stockVal3': stock_vals[2],
                                                  'stockVal2': stock_vals[3],
                                                  'stockVal1': stock_vals[4],
                                                  'day5': dates[0],
                                                  'day4': dates[1],
                                                  'day3': dates[2],
                                                  'day2': dates[3],
                                                  'day1': dates[4],
                                                  'stock_name': stock_name})
    else:
        return render(request, 'user/user.html', {'max_date': max_date,
                                                              'stocks_names': stocks_names})


def get_values(data, option):
    ret = []
    if option == 0:
        for det in data[1]:
            ret.append(det[0])
        return ret
    if option == 1:
        for det in data[1]:
            t_date = datetime.strptime(det[1], '%m/%d/%Y')
            s_date = datetime.strftime(t_date, '%d-%m-%Y')
            print(s_date)
            ret.append(str(det[1]))
        return ret

def check_for_file(filename):
    close_gate_file = glob.glob(CSV_URL + '\\' + filename + '-prices.csv')[0]
    df = pd.read_csv(close_gate_file)
    stock_close_gate = df['Open']
    dates = df['Date']
    stock_close_gate = stock_close_gate[-5:]
    dates = dates[-5:]
    plot_det = []
    stock_close_gate = stock_close_gate.get_values()
    dates = dates.get_values()

    for i in range(5):
        plot_det.append((stock_close_gate[i], dates[i]))


    array = np.array(plot_det)

    #plt.plot(dates, stock_close_gate)
    #plt.ylabel('Share Values')
    #plt.xlabel('Dates')
    #plt.show()

    return [dates, plot_det]
