from utils.packages import *


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Terminate connection
def terminate_connection():
    try:
        r.terminate(message = "maxrecs records received")
    except:
        pass
#=============================================================================================================================================================================    



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_hit_speed(access_token, accountID, instrument, iter_limit = 100):
    api = API(access_token = access_token)
    params = {'instruments': instrument}
    r = pricing.PricingStream(accountID=accountID, params=params)
    rv = api.request(r)
    iter_counts = 0
    heart_beats = 0
    
    start_time = time.time()
    
    for i, resp in tqdm(enumerate(rv)):        
        resp_type = resp['type']     
        
        if resp_type == 'HEARTBEAT': 
            heart_beats += 1
            
        elif resp_type == 'PRICE': 
            iter_counts += 1
            
        if i == iter_limit-1:
            break

    end_time = time.time()    
    seconds_elapsed = round((end_time - start_time),0)
    sec_per_iter = round((seconds_elapsed / i),0)
        
    iter_per = round((iter_counts / (i+1)),2)
    heart_per = round((heart_beats / (i+1)),2)
    
    print(f'seconds_elapsed:{seconds_elapsed}')
    print(f'sec_per_iter:{sec_per_iter}')
    print(f'iter_counts:{iter_counts} --- iter_per:{iter_per}')
    print(f'heart_beats:{heart_beats} --- heart_per:{heart_per}')
    
    return(seconds_elapsed, sec_per_iter, iter_counts, heart_beats, iter_per, heart_per)
#=============================================================================================================================================================================    



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def convert_to_df(tick_list, short_wma_list, long_wma_list):
    df = pd.DataFrame({'tick_list':tick_list, 'short_wma_list':short_wma_list, 'long_wma_list':long_wma_list}, 
                      columns = ['tick_list', 'short_wma_list', 'long_wma_list'])
    return(df)
#=============================================================================================================================================================================    



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_weights(s):
    n = 1/s
    val = 0
    val_list = []
    for i in range(s):
        val += n
        val_list.append(val)
    val_list = np.array(val_list)
    tot = sum(val_list)
    val_list = val_list/tot
    return(val_list)
#=============================================================================================================================================================================    

     

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Get timestamp of the price and segregate it
def get_date_time(resp):
    time_stamp = resp['time']
    date_val, full_time = time_stamp.split(sep = 'T')
    time_val, time_fraction = full_time.split(sep = '.')
    return(date_val, time_val, time_fraction)
#=============================================================================================================================================================================



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Get bid and ask prices
def get_prices(resp):    
    bid_price = float(resp['bids'][0]['price'])    
    ask_price = float(resp['asks'][0]['price'])
    spread = ask_price - bid_price
    tick_price = (ask_price + bid_price) / 2
    return(bid_price, ask_price, spread, tick_price)
#=============================================================================================================================================================================



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def calc_duration(start_time, end_time):        
    seconds_elapsed = end_time - start_time
    hours, rest = divmod(seconds_elapsed, 3600)
    minutes, seconds = divmod(rest, 60)
    duration = f'{round(hours)}:{round(minutes)}:{round(seconds)}'
    return(duration)
#=============================================================================================================================================================================



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_loss_limits(min_trans_num, loss_limits):
    dividing_val = 1
    per_list = list(loss_limits.keys())    
    for i, val in enumerate(per_list):
        dividing_val = 100/val
        loss_limits[val]['half_min_trans_num'] = (round((min_trans_num/dividing_val),0))*(-1)
    return(loss_limits)
#=============================================================================================================================================================================



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def run_currency_num_check(accountID, currencies, iter_num, api):
    for i, instrument in enumerate(currencies['currs']):        
        pip_size = currencies['currs'][instrument]['pip_size']
        pip_gap = currencies['currs'][instrument]['pip_gap']
        num = get_min_trans_num(instrument, accountID, iter_num, pip_gap, pip_size, api)
        print(f'instrument : {instrument}, num : {num}, pip_size : {pip_size}')
    return()
#=============================================================================================================================================================================



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_targets(start_price, target_num, pip_size):
    positive_targets = {}
    negative_targets = {}
    
    for i in range(target_num):
        move_val = pip_size*(i+1)
        positive_targets[i] = start_price + move_val
        negative_targets[i] = start_price - move_val
        
    return(positive_targets, negative_targets)
#=============================================================================================================================================================================



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def make_order(accountID, stop_price, instrument, units, api):
    stopLossOnFill = StopLossDetails(price=stop_price)

    ordr = MarketOrderRequest(
        instrument = instrument,
        units=units,
        stopLossOnFill=stopLossOnFill.data)

    r = orders.OrderCreate(accountID, data=ordr.data)
    rv = api.request(r)
    return(rv)
#=============================================================================================================================================================================



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def close_order(accountID, order_type, instrument, api):
    data_long = {"longUnits": "ALL"}
    data_short = {"shortUnits": "ALL"}
    
    if order_type == 'long':
        data = data_long
    elif order_type == 'short':
        data = data_short
        
    r = positions.PositionClose(accountID=accountID,
                                instrument=instrument,
                                data=data)
    rv = api.request(r)
    return(rv)
#=============================================================================================================================================================================



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_direction(df_reached_targets, target_num,  min_count, pip_position, min_count_mulitplier):
    tot_pos = sum(df_reached_targets['positive'] * df_reached_targets['target_num'])
    tot_neg = sum(df_reached_targets['negative'] * df_reached_targets['target_num'])

    if ((tot_pos+1) / (tot_neg+1)) > min_count and tot_pos > (round((min_count * min_count_mulitplier),0)) and df_reached_targets['positive'][pip_position] > 0:
        direction = 'positive'

    elif ((tot_neg+1) / (tot_pos+1)) > min_count and tot_neg > (round((min_count * min_count_mulitplier),0)) and df_reached_targets['negative'][pip_position] > 0:
        direction = 'negative'
        
    else:
        direction = 'no_direction'
    
    return(direction)
#=============================================================================================================================================================================



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_min_trans_num(instrument,accountID,iter_num, pip_gap, pip_size, api):
    pip_gap = pip_gap * pip_size
    
    price_df = pd.DataFrame()
    diff = 0
    ticks = []
    iter_req = []
    params = {'instruments': instrument}

    r = pricing.PricingStream(accountID=accountID, params=params)
    rv = api.request(r)
    

    for i, resp in tqdm(enumerate(rv)):    
        resp_type = resp['type']
        if resp_type == 'HEARTBEAT': # Heart beat response to keep the api connection alive (Avoid timeout)
            pass

        else:
            if i < iter_num:
                date_val, time_val, time_fraction = get_date_time(resp) # Get time stamp for reference            
                sell_price, buy_price, spread, tick_price = get_prices(resp) # Get prices from the response                      
                ticks.append(tick_price)

            else:
                break

    price_df['tick_price'] = ticks


    for i, ival in enumerate(price_df['tick_price']):
        for j, jval in enumerate(price_df['tick_price']):
            if i == j:
                pass
            elif j > i:
                diff = abs(jval - ival)
                if diff >= pip_gap:
                    iter_req.append(j-i)
                    break
            else:
                pass
    
    #print(iter_req)
    min_trans = round(np.mean(iter_req),0)
    return(np.mean(min_trans))    
#=============================================================================================================================================================================