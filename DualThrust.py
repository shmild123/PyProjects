import pandas
import numpy
import time
from pandas import Series,DataFrame

def  init(context):
    context.stock_list=[]
    context.set_commission(0.00025)
    context.set_benchmark("")
    task.daily(open_deal,time_rule=market_open(hour=1))

def handle_data(context,data_dict):
    #...


def open_deal(context):
    n=0
    for stock in context.stock_list:
        dt_value=dual_thrust(stock)
        if  dt_value==0:
            order_target_percent(stock,0)
        elif dt_value==1:
            cash_able=context.portfolio.cash
            order_value(stock,cash_able/3)
            n=n+1
        else:
            n=n+1
        if n==5:
            break
        else:
            pass

    if#如果持仓低于50%启动stock list update

        


def dual_thrust(context,data_dict):
    k1 = 0.4
    k2 = -0.4
    close = get_history(6, '1d', 'close')[stock].values[:-2]
    high = get_history(6, '1d', 'high')[stock].values[:-2]
    low = get_history(6, '1d', 'low')[stock].values[:-2]
    high_close = float(max(close))
    low_close = float(min(close))
    high = float(max(high))
    low = float(min(low))
    wave_range = max(high - low_close, high_close - low)
    open_price = float(get_history(2, '1d', 'close')[stock].values[0])
    buyline = open_price + k1 * wave_range
    sellline = open_price + k2 * wave_range
    ishold=context.portfolio.positions[stock].quantity
    td=tradeData.last
    if ishold and td<sellling:
        #order_target_value(stock,0)
        return 0
    elif not ishold and td>buyline:
        return 1
    else:
        return 2