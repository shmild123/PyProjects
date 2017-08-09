from pandas import DataFrame
import numpy as np

#交易初始化
def  init(context):
    # 设置股票池
    context.stock_list=['603880.SH','600111.SH','600456.SH']
    stock_num=len(context.stock_list)
    # 交易手续费
    context.set_commission(0.00025)
    # 参考指标
    #context.set_benchmark("")
    columns_list=['is_hold','buyline','sellline','sell_empty','sell_fool','dealable']
    context.stockinfo=DataFrame(np.zeros(stock_num*6).reshape(stock_num,6),index=context.stock_list,columns=columns_list)
    stock_init()
    context.stockinfo['dealable']=1


def stock_init(context,data_dict):
    for stock in context.stock_list:
        close = get_history(6, '1d', 'close')[stock].values[:-2]
        high = get_history(6, '1d', 'high')[stock].values[:-2]
        low = get_history(6, '1d', 'low')[stock].values[:-2]
        high_close = float(max(close))
        low_close = float(min(close))
        high = float(max(high))
        low = float(min(low))
        open_price = float(get_history(2, '1d', 'close')[stock].values[0])
        (buyline,sellline)=dual_thrust(high,high_close,low,low_close,open_price)
        context.stockinfo['buyline'][stock]=buyline
        context.stockinfo['sellline'][stock] = sellline
        if context.portfolio.positions[stock].quantity:
            context.stockinfo['ishold'][stock]=1
            bought_value= context.portfolio.positions[stock].bought_value/context.portfolio.positions[stock].bought_quantity
            context.stockinfo['sell_empty'][stock]=bought_value*0.92
            context.stockinfo['sell_fool'][stock]=bought_value*1.2
        else:
            context.stockinfo['sell_fool']=1000



#日间交易，止盈止损
def handle_data(context,data_dict):
    for stock in context.stock_list:
        if data_dict[stock].sf==1:
            context.stockinfo['dealable'][stock]=0
        if context.stockinfo['dealable'][stock]==1:
            price_now=data_dict[stock].last
            if context.stockinfo['is_hold'][stock]:
                if context.stockinfo['sellline']>price_now or context.stockinfo['sell_empty']>price_now or context.stockinfo['sell_full']<=price_now):
                    id=order_target_value(stock,0)
                    print('sell %d'%id)
            elif context.portfolio.cash/context.portfolio.portfolio_value<0.25:
                continue
            elif context.stockinfo['buyline']<price_now:
                id=order_target_percent(stock,0.3)
                print('buy %d'%id)
                context.stockinfo['dealable'][stock]=0


#m每日交易，根据DT指数进行买卖交易
#def open_deal(context):
#    n=0
#    for stock in context.stock_list:
#        dt_value=dual_thrust(stock)
#        if  dt_value==0:
#            order_target_percent(stock,0)
#        elif dt_value==1:
#            cash_able=context.portfolio.cash
#            order_value(stock,cash_able/3)#
#            n=n+1
#        else:
#            n=n+1
#        if n==4:#最大持仓4支股票
#            break
#        else:
#            pass
#    if context.portfolio.portfolio_value/2>=context.portfolio.market_value:#如果持仓低于50%启动stock list update
#        pass

#DualThrust策略
#def dual_thrust(context,data_dict):
#    #设置买入卖出敏感度参数，绝对值越小越敏感
#    k1 = 0.4
#    k2 = -0.4
#    #取前2~6个交易日的最高收盘价、最低收盘价、最高价、最低价作为基准数据
#    close = get_history(6, '1d', 'close')[stock].values[:-2]
#    high = get_history(6, '1d', 'high')[stock].values[:-2]
#    low = get_history(6, '1d', 'low')[stock].values[:-2]
#    high_close = float(max(close))
#    low_close = float(min(close))
#    high = float(max(high))
#    low = float(min(low))
#    #由基准数据计算波动
#    wave_range = max(high - low_close, high_close - low)
#    #取前一日收盘价作为交易指标
#    open_price = float(get_history(2, '1d', 'close')[stock].values[0])
#    #计算买入卖出线
#    buyline = open_price + k1 * wave_range
#    sellline = open_price + k2 * wave_range
#    ishold=context.portfolio.positions[stock].quantity
#    td=tradeData.last
#    if ishold and td<sellline:
#        #order_target_value(stock,0)
#        return 0
#    elif not ishold and td>buyline:
#        return 1
#    else:
#        return 2


#Dual_Thrust策略
#hh:n日最高，hc：n日收盘最高，ll：n日最低，lc：n日收盘最低，yc：昨日收盘，k1k2：买卖敏感系数
def dual_thrust(hh,hc,ll,lc,yc,k1=0.7,k2=-0.7):
    wave_range=max(hh-lc,hc-ll)
    buyline=yc+k1*wave_range
    sellline=yc+k2*wave_range
    return (buyline,sellline)