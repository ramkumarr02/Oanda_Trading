# Get timestamp of the price and segregate it
def get_date_time(resp):
    
    time_stamp = resp['time']
    date_val, full_time = time_stamp.split(sep = 'T')
    time_val, time_fraction = full_time.split(sep = '.')
    
    return(date_val, time_val, time_fraction)



# Get bid and ask prices
def get_prices(resp):
    
    bid_price = float(resp['bids'][0]['price'])    
    ask_price = float(resp['asks'][0]['price'])
    spread = ask_price - bid_price
    tick_price = (ask_price + bid_price) / 2
    
    return(bid_price, ask_price, spread, tick_price)



# Terminate connection
def terminate_connection():
    try:
        r.terminate(message = "maxrecs records received")
    except:
        pass


def calc_duration(start_time, end_time):        
    seconds_elapsed = end_time - start_time
    hours, rest = divmod(seconds_elapsed, 3600)
    minutes, seconds = divmod(rest, 60)
    duration = f'{round(hours)}:{round(minutes)}:{round(seconds)}'
    return(duration)