from django.shortcuts import render
from django.http import HttpResponse
import json
import os

import baostock as bs
import pandas as pd

import talib as ta

lg = bs.login()

def index(request):
    # 股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
    stock_code = request.GET.get("stock_code")
    # 开始日期（包含），格式“YYYY-MM-DD”
    start_date = request.GET.get("start_date")
    # 结束日期（包含），格式“YYYY-MM-DD”
    end_date = request.GET.get("end_date")
    # 数据类型，默认为d，日k线；d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟k线数据，不区分大小写；指数没有分钟线数据
    frequency = request.GET.get("frequency")
    data = "date,open,close,low,high,volume,amount,turn,pctChg,adjustflag"

    if not stock_code:
        jsonres = {
            'code': '500',
            'msg': '股票代码(stock_code)不能为空'
        }
        return HttpResponse(json.dumps(jsonres))
    if not start_date:
        jsonres = {
            'code': '500',
            'msg': '开始日期(start_date)不能为空'
        }
        return HttpResponse(json.dumps(jsonres))
    if not end_date:
        jsonres = {
            'code': '500',
            'msg': '起始时间(end_date)不能为空'
        }
        return HttpResponse(json.dumps(jsonres))
    if not frequency:
        jsonres = {
            'code': '500',
            'msg': '数据类型(frequency)不能为空'
        }
        return HttpResponse(json.dumps(jsonres))

    if frequency == '5' or frequency == '15' or frequency == '30' or frequency == '60':
        data = 'time,open,close,low,high,volume,amount,adjustflag'

    file = "./cache/A_" + stock_code + "_" + start_date + "_" + end_date + "_f" + frequency + ".json"
    if os.path.exists(file):
        with open(file,'r') as load_f:
            load_dict = json.load(load_f)
            return HttpResponse(json.dumps(load_dict))

    rs = bs.query_history_k_data_plus(
        stock_code,
        data,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        adjustflag="3")

    if rs.error_msg != 'success':
        jsonres = {
            'code': '500',
            'msg': rs.error_msg
        }
        return HttpResponse(json.dumps(jsonres))

    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)

    res = result.to_json( orient='split')
    result.to_json(file, orient='split')

    return HttpResponse(res)

def macd(request):
    stock_code = request.GET.get("stock_code")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    data = "date,code,close,tradeStatus"

    if not stock_code:
        jsonres = {
            'code': '500',
            'msg': '股票代码(stock_code)不能为空'
        }
        return HttpResponse(json.dumps(jsonres))
    if not start_date:
        jsonres = {
            'code': '500',
            'msg': '开始日期(start_date)不能为空'
        }
        return HttpResponse(json.dumps(jsonres))
    if not end_date:
        jsonres = {
            'code': '500',
            'msg': '起始时间(end_date)不能为空'
        }
        return HttpResponse(json.dumps(jsonres))

    file = "./cache/MACD_" + stock_code + "_" + start_date + "_" + end_date + ".json"
    if os.path.exists(file):
        with open(file,'r') as load_f:
            load_dict = json.load(load_f)
            return HttpResponse(json.dumps(load_dict))

    rs = bs.query_history_k_data_plus(
        stock_code,
        data,
        start_date=start_date,
        end_date=end_date,
        frequency="d",
        adjustflag="3")

    if rs.error_msg != 'success':
        jsonres = {
            'code': '500',
            'msg': rs.error_msg
        }
        return HttpResponse(json.dumps(jsonres))

    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    df2 = result

    dif, dea, hist = ta.MACD(df2['close'].astype(float).values, fastperiod=12, slowperiod=26, signalperiod=9)
    df3 = pd.DataFrame({'dif': dif[33:], 'dea': dea[33:], 'hist': hist[33:]})
    res = df3.to_json( orient='split')
    df3.to_json(file, orient='split')

    return HttpResponse(res)

def kdj(request):
    stock_code = request.GET.get("stock_code")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    data = "date,code,high,close,low,tradeStatus"

    if not stock_code:
        jsonres = {
            'code': '500',
            'msg': '股票代码(stock_code)不能为空'
        }
        return HttpResponse(json.dumps(jsonres))
    if not start_date:
        jsonres = {
            'code': '500',
            'msg': '开始日期(start_date)不能为空'
        }
        return HttpResponse(json.dumps(jsonres))
    if not end_date:
        jsonres = {
            'code': '500',
            'msg': '起始时间(end_date)不能为空'
        }
        return HttpResponse(json.dumps(jsonres))

    file = "./cache/KDJ_" + stock_code + "_" + start_date + "_" + end_date + ".json"
    if os.path.exists(file):
        with open(file,'r') as load_f:
            load_dict = json.load(load_f)
            return HttpResponse(json.dumps(load_dict))

    rs = bs.query_history_k_data_plus(
        stock_code,
        data,
        start_date=start_date,
        end_date=end_date,
        frequency="d",
        adjustflag="3")

    if rs.error_msg != 'success':
        jsonres = {
            'code': '500',
            'msg': rs.error_msg
        }
        return HttpResponse(json.dumps(jsonres))

    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    df_status = result

    low = df_status['low'].astype(float)
    del df_status['low']
    df_status.insert(0, 'low', low)
    high = df_status['high'].astype(float)
    del df_status['high']
    df_status.insert(0, 'high', high)
    close = df_status['close'].astype(float)
    del df_status['close']
    df_status.insert(0, 'close', close)

    # 计算KDJ指标,前9个数据为空
    low_list = df_status['low'].rolling(window=9).min()
    high_list = df_status['high'].rolling(window=9).max()
    rsv = (df_status['close'] - low_list) / (high_list - low_list) * 100
    df_data = pd.DataFrame()
    df_data['K'] = rsv.ewm(com=2).mean()
    df_data['D'] = df_data['K'].ewm(com=2).mean()
    df_data['J'] = 3 * df_data['K'] - 2 * df_data['D']
    df_data.index = df_status['date'].values
    df_data.index.name = 'date'
    # 删除空数据
    df_data = df_data.dropna()

    res = df_data.to_json( orient='split')
    df_data.to_json(file, orient='split')

    return HttpResponse(res)