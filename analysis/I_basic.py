from django.shortcuts import render
from django.http import HttpResponse
import json

import baostock as bs
import pandas as pd

def basic(request):
    stock_code = request.GET.get("stock_code")
    data = "date,code,close,tradeStatus"

    if not stock_code:
        jsonres = {
            'code': '500',
            'msg': '股票代码(stock_code)不能为空'
        }
        return HttpResponse(json.dumps(jsonres))

    lg = bs.login()

    if lg.error_msg != 'success':
        jsonres = {
            'code': '500',
            'msg': lg.error_msg
        }
        return HttpResponse(json.dumps(jsonres))

    rs = bs.query_stock_basic(code=stock_code)
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
    res = result.to_json( orient='records')
    #### 登出系统 ####
    bs.logout()
    return HttpResponse(res)

def search(request):
    stock_name = request.GET.get("stock_name")
    data = "date,code,close,tradeStatus"

    if not stock_name:
        jsonres = {
            'code': '500',
            'msg': '股票名称(stock_name)不能为空'
        }
        return HttpResponse(json.dumps(jsonres))

    lg = bs.login()

    if lg.error_msg != 'success':
        jsonres = {
            'code': '500',
            'msg': lg.error_msg
        }
        return HttpResponse(json.dumps(jsonres))

    rs = bs.query_stock_basic(code_name=stock_name)
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
    res = result.to_json( orient='records')
    #### 登出系统 ####
    bs.logout()
    return HttpResponse(res)