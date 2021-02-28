# ### Packages
from utils.packages import *

# ### Time and Price
#--------------------------------------------------------------------------------------------------------------------------
# Get timestamp of the price and segregate it
def get_date_time(resp, data):
    #global data
    time_stamp = resp['time']
    data['ts_date_val'], full_time = time_stamp.split(sep = 'T')
    data['ts_time_val'], _ = full_time.split(sep = '.')

    data['ts_date_val'] = datetime.strptime(data['ts_date_val'], '%Y-%m-%d')
    data['ts_time_val'] = datetime.strptime(data['ts_time_val'], '%H:%M:%S')

    tot_ts = datetime.combine(datetime.date(data['ts_date_val']), datetime.time(data['ts_time_val']))
    
    if data['os'] == 'windows':
        tot_ts = tot_ts + timedelta(hours=8)
    
    data['tot_ts']    = tot_ts.strftime("%Y-%b-%d, %I:%M:%S (%p)")      
    t2 = datetime.now()    
    data['time_diff'] = (t2 - tot_ts).total_seconds()
    data['weekday']   = t2.weekday()
    data['hour']      = t2.hour

    return(data)
#==========================================================================================================================

#--------------------------------------------------------------------------------------------------------------------------
# Get bid and ask prices
def get_prices(resp, data):    
    #global data
    data['price_bid'] = float(resp['bids'][0]['price'])    
    data['price_ask'] = float(resp['asks'][0]['price'])
    data['price_spread'] = data['price_ask'] - data['price_bid']
    data['price_tick'] = (data['price_ask'] + data['price_bid']) / 2
    return(data)
#==========================================================================================================================

#--------------------------------------------------------------------------------------------------------------------------
# Get average candle height
def get_avg_candle_height(data, candle_count, granularity):
    #global data
    data["candle_param"] = {"count": candle_count, "granularity": granularity}
    data["candle_r"] = instruments.InstrumentsCandles(instrument=data['instrument'], params=data["candle_param"])
    data["api"].request(data["candle_r"])
    data["candle_data"] = data["candle_r"].response

    data['avg_candle_height'] = np.round(np.mean([(np.float(x['mid']['h']) - np.float(x['mid']['l'])) for x in data["candle_data"]['candles']]),5)
    data['stop_loss_candle_height'] = data['avg_candle_height']
    data['stop_loss_candle_height'] = max(data['stop_loss_candle_height'], 0.0005)
    return()
#==========================================================================================================================

#--------------------------------------------------------------------------------------------------------------------------
# Get Ema Diff
def get_ema_diff(data, granularity, ema_long, ema_short):    
    
    data["candle_param"] = {"count": ema_long, "granularity": granularity}
    data["candle_r"] = instruments.InstrumentsCandles(instrument=data['instrument'], params=data["candle_param"])
    data["api"].request(data["candle_r"])
    data["candle_data"] = data["candle_r"].response
    
    ema_l = pd.DataFrame([x['mid']['c'] for x in data["candle_data"]['candles']]).ewm(span=ema_long).mean()[0][ema_long - 1]
    ema_s = pd.DataFrame([x['mid']['c'] for x in data["candle_data"]['candles']]).ewm(span=ema_short).mean()[0][ema_short - 1]   

    data['stop_loss_ema_diff'] = max(abs(ema_s - ema_l)/2, data['stop_loss_val'])
    
    return()
#==========================================================================================================================    