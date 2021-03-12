from utils.packages import *

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
    tot_ts = tot_ts + timedelta(hours=8)
    data['tot_ts'] = tot_ts.strftime("%Y-%b-%d, %I:%M:%S (%p)")
      
    t2 = datetime.now()    
    data['time_diff'] = (t2 - tot_ts).total_seconds()
    
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