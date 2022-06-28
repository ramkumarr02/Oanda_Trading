from utils.packages import *
from utils.dir_slope import *


#...............................................................................................
def before_lema(data):   
    data['lema_tick_list'].append(data['tick'])    
    return(data)
#...............................................................................................



#...............................................................................................
def after_lema(data):     
    data['lema_tick_list'].popleft()
    data['lema_tick_list'].append(data['tick'])
    data['lema'] = list(pd.DataFrame(list(data['lema_tick_list'])).ewm(span=data['lema_len']).mean()[0])[-1]
    # data['lema'] = np.round(data['lema'],5)
    return(data)
#...............................................................................................    


#...............................................................................................
def get_invest_details(data):    
    account_data = accounts.AccountDetails(data["accountID"])
    data["account_data"] = data["api"].request(account_data)

    data["account_balance"] = float(data["account_data"]["account"]["balance"])
    data["order_amount"] = data["account_balance"] * data["invest_ratio"] * data['margin_call_ratio']
    data["order_amount"] = int(np.floor(data["order_amount"]))
    data['order_num']    = data["order_amount"]

    return(data)
#...............................................................................................

#............................................................................................... 
def get_back_data(data):
    
    params = {"count": data['candle_count'], "granularity": data['candle_granularity']}
    candle_size_data = instruments.InstrumentsCandles(instrument=data['instrument'], params=params)
    data['candle_size_info'] = data["api"].request(candle_size_data)
    data['back_ticks'] = [candle['mid']['c'] for candle in data['candle_size_info']['candles']]
    
    return(data)
#............................................................................................... 

def get_conversion_rate(data):
    params = {"count": 1, "granularity": 'S5'}
    candle_size_data = instruments.InstrumentsCandles(instrument=data['curr_conv_pair'], params=params)
    data['candle_size_info'] = data["api"].request(candle_size_data)
    data['convertion_rate'] = float([candle['mid']['c'] for candle in data['candle_size_info']['candles']][0])
    return(data)
#............................................................................................... 

def calculate_purchasable_EURUSD_units(data):
    # Calculate Account balance in USD ------------------------------------
    data['curr_conv_pair'] = 'USD_SGD'
    data = get_conversion_rate(data)
    data['sgd_to_usd_conversion_rate'] = 1 / data['convertion_rate']
    data = get_invest_details(data)
    data["usd_account_balance"] = data["account_balance"] * data['sgd_to_usd_conversion_rate']

    # Calculate purchasable EURUSD units ------------------------------------
    data['curr_conv_pair'] = 'EUR_USD'
    data = get_conversion_rate(data)    
    data['usd_eur_price'] = data['convertion_rate']
    data['purchasable_eur_units'] = data["usd_account_balance"] / data['usd_eur_price']
    data['eurusd_units'] = np.floor(data['purchasable_eur_units'] * data['leverage'])
    
    return(data)
#............................................................................................... 