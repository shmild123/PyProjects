import pandas
import numpy
import time
from pandas import Series,DataFrame

def  init(context):
    context.stock_list=[]
    context.set_commission(0.00025)
    context.set_benchmark("")
    task.daily(open_deal,time_rule=market_open(hour=1))
    #task.monthly(update_stock_list,tradingday=t)

def before_trade(context):
    #

def handle_data(context,data_dict):
    #...


def open_deal(context):
    sell_list=[]
    update_value=DataFrame(index=['stock','ishold','dt_value','update_value'])
    update_list=[]
    for stock in context.stock_list:
        dt_value=dual_thrust(stock)
        ishold=context.portfolio.positions[stock].quantity
        if  ishold and not dt_value:
            context.sell_list.append(stock)
        elif dt_value:
            update=Series([stock,ishold,dt_value,numpy.nan],index=['stock','ishold','dt_value','update_value'])
            update_value.append(update)
        else:
            pass
        


def dual_thrust(stock):
    pass
