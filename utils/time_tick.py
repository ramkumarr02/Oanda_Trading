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
    
    #Windows-------------------------
    tot_ts = tot_ts + timedelta(hours=8)
    #Windows-------------------------
    
    data['tot_ts'] = tot_ts.strftime("%Y-%b-%d, %I:%M:%S (%p)")
      
    t2 = datetime.now()    
    #t2 = datetime.now() + timedelta(hours=5, minutes=0)
    data['time_diff'] = (t2 - tot_ts).total_seconds()
    
    return(data)

#--------------------------------------------------------------------------------------------------------------------------
# Get average candle height
def get_avg_candle_height(data, candle_count, granularity):
    #global data
    data["candle_param"] = {"count": candle_count, "granularity": granularity}
    data["candle_r"] = instruments.InstrumentsCandles(instrument=data['instrument'], params=data["candle_param"])
    data["api"].request(data["candle_r"])
    data["candle_data"] = data["candle_r"].response

    candle_height_list = []

    for candle in data["candle_data"]['candles']:
        high = np.float(candle['mid']['h'])
        low = np.float(candle['mid']['l'])
        candle_height_list.append(high - low) 

    data['avg_candle_height'] = np.round(np.mean(candle_height_list),5)
    data['stop_loss_pip'] = data['avg_candle_height'] / 2
    data['stop_loss_pip'] = max(data['stop_loss_pip'], 0.0005)
    return()
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