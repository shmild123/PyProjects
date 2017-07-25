import pandas
import numpy
import time
from pandas import Series,DataFrame

#交易初始化
def  init(context):
    # 设置股票池
    context.stock_list=[]
    # 交易手续费
    context.set_commission(0.00025)
    # 参考指标
    context.set_benchmark("")
    # 每日开盘一小时后执行交易
    task.daily(open_deal,time_rule=market_open(hour=1))

#日间交易，止盈止损
def handle_data(context,data_dict):
    for stock in context.stock_list:
        #止损
        if context.position.bought_value[stock]*0.92>context.portfolio.market_value[stock]:
            order_target_percent(stock,0)
        #止盈
        elif context.position.bought_value[stock]*1.2<context.portfolio.market_value[stock]:
            order_target_percent(stock,0)
        else:
            pass

#m每日交易，根据DT指数进行买卖交易
def open_deal(context):
    n=0
    for stock in context.stock_list:
        dt_value=dual_thrust(stock)
        if  dt_value==0:
            order_target_percent(stock,0)
        elif dt_value==1:
            cash_able=context.portfolio.cash
            order_value(stock,cash_able/3)#
            n=n+1
        else:
            n=n+1
        if n==4:#最大持仓4支股票
            break
        else:
            pass
    if context.portfolio.portfolio_value/2>=context.portfolio.market_value:#如果持仓低于50%启动stock list update
        pass

#DualThrust策略
def dual_thrust(context,data_dict):
    #设置买入卖出敏感度参数，绝对值越小越敏感
    k1 = 0.4
    k2 = -0.4
    #取前2~6个交易日的最高收盘价、最低收盘价、最高价、最低价作为基准数据
    close = get_history(6, '1d', 'close')[stock].values[:-2]
    high = get_history(6, '1d', 'high')[stock].values[:-2]
    low = get_history(6, '1d', 'low')[stock].values[:-2]
    high_close = float(max(close))
    low_close = float(min(close))
    high = float(max(high))
    low = float(min(low))
    #由基准数据计算波动
    wave_range = max(high - low_close, high_close - low)
    #取前一日收盘价作为交易指标
    open_price = float(get_history(2, '1d', 'close')[stock].values[0])
    #计算买入卖出线
    buyline = open_price + k1 * wave_range
    sellline = open_price + k2 * wave_range
    ishold=context.portfolio.positions[stock].quantity
    td=tradeData.last
    if ishold and td<sellline:
        #order_target_value(stock,0)
        return 0
    elif not ishold and td>buyline:
        return 1
    else:
        return 2