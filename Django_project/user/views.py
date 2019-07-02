from django.shortcuts import render
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from Django_project.settings import PRED_URL, CSV_URL, PREDICT_URL, BASE_PROJ_DIR
import datetime
import numpy as np
import glob
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath("../"))
import predict


def home(request):
    return render(request, 'user/home.html')

def about(request):
    return render(request, 'user/about.html')

def base(request):
    return render(request, 'user/base.html')

@login_required
def user(request):
    now = datetime.datetime.today()
    today = str(now)[:10]
    max_date = today
    plot_exist = None;
    stocks_names = ['AAPL', 'AMZN', 'NDAQ', 'SNP', 'SCCO']
    if request.method == 'POST':
        data = request.POST
        stock_name = data['stockName']
        print(stock_name)

        start_date = now - timedelta(days=5)
        end_date = now - timedelta(days=1)

        start_date = str(start_date)
        end_date = str(end_date)

        print(start_date)
        print(end_date)

        plot = check_for_file(stock_name)
        stock_vals = get_values(plot, 0)
        dates = get_values(plot, 1)
     #   print(stock_vals)

        end_date = now.date()
        end_date = str(end_date)

        updodate = predict.Predict(stock_name).up_to_date
        if updodate == 0:
            plot_exist = False
            return render(request, 'user/user.html', {'max_date': max_date,
                                                      'plot_exist': plot_exist,
                                                      'stocks_names': stocks_names})
        else:
            plot_exist = True
            pred_results = read_pred_file(stock_name)
            # print(pred_results)
            decisions = get_decisions(pred_results)
            # Send it to html
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
                                                  'pred5': decisions[0],
                                                  'pred4': decisions[1],
                                                  'pred3': decisions[2],
                                                  'pred2': decisions[3],
                                                  'pred1': decisions[4],
                                                  'pred0': decisions[5],
                                                  'stocks_names': stocks_names,
                                                  'stock_name': stock_name})
    else:
        return render(request, 'user/user.html', {'max_date': max_date,
                                                  'plot_exist': plot_exist,
                                                  'stocks_names': stocks_names})


def get_values(data, option):
    ret = []
    if option == 0:
        for det in data[1]:
            ret.append(det[0])
        return ret
    if option == 1:
        for det in data[1]:
            t_date = datetime.datetime.strptime(det[1], '%m/%d/%Y')
            s_date = datetime.datetime.strftime(t_date, '%m/%d/%Y')
            #print(s_date)
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
    return [dates, plot_det]

def read_pred_file(stock_name):
    pred_file = glob.glob(PRED_URL + stock_name + '-predicts.csv')[0]
    df = pd.read_csv(pred_file)
    pred_results = df['Predict']
    pred_results = pred_results.get_values()
    pred_results = pred_results[-6:]
    #print(pred_results)
    return pred_results

def get_decisions(predictions):
    decisions_results = []
    for prediction in predictions:
        if prediction >= 0.85:
            decisions_results.append('Strong Buy')
        elif prediction >= 0.6:
            decisions_results.append('Buy')
        elif prediction >= 0.45:
            decisions_results.append('Stay')
        elif prediction >= 0.3:
            decisions_results.append('Sell')
        else:
            decisions_results.append('Strong Sell')

    return decisions_results