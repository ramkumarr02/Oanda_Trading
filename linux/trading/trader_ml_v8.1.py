# # ML Trader

# ## Setup
# ### Packages
from utils.packages import *
warnings.filterwarnings('ignore')

# ### Inputs and Parameters
# #### Read Yaml files
temp_file = 'config/access_keys.yaml'
with open(temp_file) as temp_file:
    config = yaml.load(temp_file)     
    

filename = 'data/model/xgb.model'
model_new = xgboost.XGBClassifier(tree_method='gpu_hist', gpu_id=0)
model_new.load_model(filename)


# ## Functions

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
    #tot_ts = tot_ts + timedelta(hours=8)
    data['tot_ts'] = tot_ts.strftime("%Y-%b-%d, %I:%M:%S (%p)")
      
    t2 = datetime.now()    
    #t2 = datetime.now() + timedelta(hours=5, minutes=0)
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


# ### Loops
# #### Tick AVG
def tick_gap_checker():
    if data['act_tick_gap'] > 0.1:
        data['tick_gap_error'] =  True  
    return()

#--------------------------------------------------------------------------------------------------------------------------
def before_avg_len(data):
    #global data
    data['list_tick_avg'].append(data['price_tick'])
    data['list_spread'].append(data['price_spread'])   
    return(data)
#--------------------------------------------------------------------------------------------------------------------------

def after_avg_len(data):
    #global data
    
    data['tick_avg'] = np.mean(data['list_tick_avg'])
    data['tick_sd'] = np.std(data['list_tick_avg'])
    data['spread_avg'] = np.mean(data['list_spread'])
    
    data['act_max_tick'] = np.max(data['list_tick_avg'])
    data['act_min_tick'] = np.min(data['list_tick_avg'])
    data['act_tick_gap'] = float(data['act_max_tick'] - data['act_min_tick'])
    
    data['max_lema_loss'] = data['act_tick_gap'] * (data['stop_loss_val'] / 2)
    data['max_lema_loss'] = min(-data['max_lema_loss'], -0.0002)
    
    data['stop_loss_pip'] = data['act_tick_gap'] * data['stop_loss_val']
    data['stop_loss_pip'] = max(data['stop_loss_pip'], 0.0002)
    
    
    data['list_tick_avg'] = collections.deque([])
    data['list_spread'] = collections.deque([])
    
    return(data)
#==========================================================================================================================    


# #### RSI
#--------------------------------------------------------------------------------------------------------------------------
def before_rsi_len(data):
    #global data
    data['list_tick'].append(data['tick_avg'])

    if len(data['list_tick']) == 1:
        data['list_up'].append(0)
        data['list_down'].append(0)
        data['list_AvgGain'].append(0)
        data['list_Avgloss'].append(0)
        data['list_RS'].append(0)
        data['list_RSI'].append(0)
    elif len(data['list_tick']) > 1:        
        old_price = data['list_tick'][len(data['list_tick'])-2]
        new_price = data['tick_avg']
        data['diff'] = new_price - old_price
        
        if data['diff'] > 0:
            data['list_up'].append(new_price - old_price)
            data['list_down'].append(0)
            data['list_AvgGain'].append(np.mean(data['list_up']))
            data['list_Avgloss'].append(np.mean(data['list_down']))
            data['list_RS'].append(data['list_AvgGain'][len(data['list_AvgGain'])-1]/data['list_Avgloss'][len(data['list_Avgloss'])-1])
            data['rsi'] = 100 - (100/(1+data['list_RS'][len(data['list_RS'])-1]))
            data['list_RSI'].append(data['rsi'])            
        elif data['diff'] < 0:
            data['list_up'].append(0)
            data['list_down'].append(old_price - new_price)
            data['list_AvgGain'].append(np.mean(data['list_up']))
            data['list_Avgloss'].append(np.mean(data['list_down']))
            data['list_RS'].append(data['list_AvgGain'][len(data['list_AvgGain'])-1]/data['list_Avgloss'][len(data['list_Avgloss'])-1])
            data['rsi'] = 100 - (100/(1+data['list_RS'][len(data['list_RS'])-1]))
            data['list_RSI'].append(data['rsi'])            
        elif data['diff'] == 0:
            data['list_up'].append(0)
            data['list_down'].append(0)
            data['list_AvgGain'].append(np.mean(data['list_up']))
            data['list_Avgloss'].append(np.mean(data['list_down']))
            data['list_RS'].append(data['list_AvgGain'][len(data['list_AvgGain'])-1]/data['list_Avgloss'][len(data['list_Avgloss'])-1])
            data['rsi'] = 100 - (100/(1+data['list_RS'][len(data['list_RS'])-1]))
            data['list_RSI'].append(data['rsi'])    
            
    return(data)
#==========================================================================================================================    


#--------------------------------------------------------------------------------------------------------------------------
def after_rsi_len(data):
    #global data
    data['list_up'].popleft()
    data['list_down'].popleft()
    data['list_AvgGain'].popleft()
    data['list_Avgloss'].popleft()
    data['list_RS'].popleft()
    data['list_RSI'].popleft()
    data['list_tick'].popleft()
    data['list_tick'].append(data['tick_avg'])

    old_price = data['list_tick'][len(data['list_tick'])-2]
    new_price = data['tick_avg']
    data['diff'] = new_price - old_price
    
    if data['diff'] > 0:
        data['list_up'].append(new_price - old_price)
        data['list_down'].append(0)
        data['list_AvgGain'].append(np.mean(data['list_up']))
        data['list_Avgloss'].append(np.mean(data['list_down']))
        data['list_RS'].append(data['list_AvgGain'][len(data['list_AvgGain'])-1]/data['list_Avgloss'][len(data['list_Avgloss'])-1])
        data['rsi'] = 100 - (100/(1+data['list_RS'][len(data['list_RS'])-1]))
        data['list_RSI'].append(data['rsi'])
    elif data['diff'] < 0:
        data['list_up'].append(0)
        data['list_down'].append(old_price - new_price)
        data['list_AvgGain'].append(np.mean(data['list_up']))
        data['list_Avgloss'].append(np.mean(data['list_down']))
        data['list_RS'].append(data['list_AvgGain'][len(data['list_AvgGain'])-1]/data['list_Avgloss'][len(data['list_Avgloss'])-1])
        data['rsi'] = 100 - (100/(1+data['list_RS'][len(data['list_RS'])-1]))
        data['list_RSI'].append(data['rsi'])
    elif data['diff'] == 0:
        data['list_up'].append(0)
        data['list_down'].append(0)
        data['list_AvgGain'].append(np.mean(data['list_up']))
        data['list_Avgloss'].append(np.mean(data['list_down']))
        data['list_RS'].append(data['list_AvgGain'][len(data['list_AvgGain'])-1]/data['list_Avgloss'][len(data['list_Avgloss'])-1])
        data['rsi'] = 100 - (100/(1+data['list_RS'][len(data['list_RS'])-1]))
        data['list_RSI'].append(data['rsi'])            
    
    data['avg_gain'] = data['list_AvgGain'][-1]
    data['avg_loss'] = data['list_Avgloss'][-1]
    data['rs'] = data['list_RS'][-1]
    
    if data['rs'] > data['rs_max']:
        data['rs'] = data['rs_max'] 
        
    data['rsi_ready'] = True
        
    return(data)
#==========================================================================================================================    


# #### MA
#--------------------------------------------------------------------------------------------------------------------------
def before_sma(data):
    #global data    
    data['ssma_list'].append(data['tick_avg'])    
    return(data)
#--------------------------------------------------------------------------------------------------------------------------
def after_sma(data):
    #global data
    
    data['ssma_list'].popleft()
    data['ssma_list'].append(data['tick_avg'])

    data['ssma'] = np.mean(data['ssma_list'])
    data['sema'] = list(pd.DataFrame(list(data['ssma_list'])).ewm(span=data['sma_len']).mean()[0])[data['sma_len'] - 1]
    
    data['small_sema_slope'] = get_slope(data['ssma_list'], data)
    
    if len(data['ssma_ready']) < 2:
        data['ssma_ready'].append(data['ssma'])
        data['sema_ready'].append(data['sema'])

    elif len(data['ssma_ready']) > 1:
        data['ssma_ready'].popleft()
        data['sema_ready'].popleft()
        data['ssma_ready'].append(data['ssma'])
        data['sema_ready'].append(data['sema'])

        data['ssma_diff'] = data['ssma_ready'][-1] - data['ssma_ready'][len(data['ssma_ready'])-2]
        data['sema_diff'] = data['sema_ready'][-1] - data['sema_ready'][len(data['sema_ready'])-2]
        
        data['max_tick'] = np.max(data['ssma_list'])
        data['min_tick'] = np.min(data['ssma_list'])
        
        data['max_gap'] = data['max_tick'] -  data['tick_avg']
        data['min_gap'] = data['min_tick'] - data['tick_avg']
    
    return(data)
#==========================================================================================================================

#--------------------------------------------------------------------------------------------------------------------------
def before_lma(data):
    #global data
    data['lsma_list'].append(data['tick_avg'])
    return(data)
#--------------------------------------------------------------------------------------------------------------------------
def after_lma(data):
    #global data
    
    data['lsma_list'].popleft()
    data['lsma_list'].append(data['tick_avg'])

    data['lsma'] = np.mean(data['lsma_list'])
    data['lema'] = list(pd.DataFrame(list(data['lsma_list'])).ewm(span=data['lma_len']).mean()[0])[data['lma_len'] - 1]
    data['long_sema_slope'] = get_slope(data['lsma_list'], data)
    data['slope_diff'] = data['small_sema_slope'] - data['long_sema_slope']
    
    if len(data['lsma_ready']) < 2:
        data['lsma_ready'].append(data['lsma'])
        data['lema_ready'].append(data['lema'])

    elif len(data['lsma_ready']) > 1:
        data['lsma_ready'].popleft()
        data['lema_ready'].popleft()
        data['lsma_ready'].append(data['lsma'])
        data['lema_ready'].append(data['lema'])

        data['lsma_diff'] = data['lsma_ready'][-1] - data['lsma_ready'][len(data['lsma_ready'])-2]
        data['lema_diff'] = data['lema_ready'][-1] - data['lema_ready'][len(data['lema_ready'])-2]
        
        data['ema_diff'] = data['sema'] - data['lema']
        data['sma_diff'] = data['ssma'] - data['lsma']
                
        data['min_tick_gap'] = min(data["lsma_list"])
        data['max_tick_gap'] = max(data["lsma_list"])
        data['tick_gap'] = float(data['max_tick_gap'] - data['min_tick_gap'])

        data['lma_ready'] = True
    
    return(data)
#==========================================================================================================================


# ### Slope
#--------------------------------------------------------------------------------------------------------------------------
def get_slope(y_axis, data):
    #global data
    ma_len = len(y_axis)
    
    x_axis = []
    for i in range(ma_len):
        x_axis.append(1 + ((i+1) * 0.0001 * 0.1))
    
    slope_tick, intercept, _, _, _ = linregress(x_axis, y_axis)
    slope_tick = math.degrees(math.atan(slope_tick))
    
    return(slope_tick)
#==========================================================================================================================


# ### Class Mapping
#--------------------------------------------------------------------------------------------------------------------------
def map_predictions(data):
    #global data
    
    if data['prediction'] == 'same':
        data['order_create'] = None
    
    elif data['prediction'] == 'increase':
        data['order_create'] = 'long'
        
    elif data['prediction'] == 'decrease':
        data['order_create'] = 'short'
        
    return(data)
#==========================================================================================================================


# ### Orders

# #### check_for_open_orders
#--------------------------------------------------------------------------------------------------------------------------
def check_for_open_orders(data):
    #global data
    
    request_position_data = positions.OpenPositions(accountID=data['accountID'])
    data['positions_info'] = data['api'].request(request_position_data)

    if len(data['positions_info']['positions']) == 0:
        data['order_current_open'] = False
        data['positions_long'] = 0
        data['positions_short'] = 0

    elif len(data['positions_info']['positions']) == 1:
        data['positions_long'] = abs(int(data['positions_info']['positions'][0]['long']['units']))
        data['positions_short'] = abs(int(data['positions_info']['positions'][0]['short']['units']))

        if data['positions_long'] >= 1 and data['positions_short'] == 0:
            data['order_current_open'] = 'long'
        elif data['positions_long'] == 0 and data['positions_short'] >= 1:
            data['order_current_open'] = 'short'                              

    return(data)
#==========================================================================================================================    


# #### make_order
#--------------------------------------------------------------------------------------------------------------------------
def make_order(data):
    #global data
    if not data['order_current_open']:
        if data['order_create'] == 'long':      
            
            data['order_val'] = data['order_num'] * 1
                        
            # !!!!!!!!!!stop loss line max to be introduced and tested    
            data['price_stop'] = data['price_ask'] - data['stop_loss_pip']
            
            stopLossOnFill = StopLossDetails(price=data['price_stop'])
                       
            ordr = MarketOrderRequest(instrument = data['instrument'], 
                                      units=data['order_val'], 
                                      stopLossOnFill=stopLossOnFill.data)

            order_request_data = orders.OrderCreate(accountID=data['accountID'], data=ordr.data)
            
            data['response_order'] = data['api'].request(order_request_data)
            data['num_orders'] = data['num_orders'] + 1
            data = check_for_open_orders(data)


        if data['order_create'] == 'short':
            data['order_val'] = data['order_num'] * -1
            
            # !!!!!!!!!!stop loss line min to be introduced and tested            
            data['price_stop'] = data['price_bid'] + data['stop_loss_pip']
            stopLossOnFill = StopLossDetails(price=data['price_stop'])

            ordr = MarketOrderRequest(instrument = data['instrument'], 
                                      units=data['order_val'], 
                                      stopLossOnFill=stopLossOnFill.data)
            
            order_request_data = orders.OrderCreate(accountID=data['accountID'], data=ordr.data)
            
            data['response_order'] = data['api'].request(order_request_data)
            data['num_orders'] = data['num_orders'] + 1
            data = check_for_open_orders(data)
    
    return(data)
#==========================================================================================================================


# #### close_order
def close_long_orders(data):
    #global data
    data_long = {"longUnits": "ALL"}
    order_close_data = positions.PositionClose(accountID=data['accountID'],
                                instrument=data['instrument'],
                                data=data_long)
    data['response_close'] = data['api'].request(order_close_data)
    return(data)

def close_short_orders(data):
    #global data
    data_short = {"shortUnits": "ALL"}
    order_close_data = positions.PositionClose(accountID=data['accountID'],
                                instrument=data['instrument'],
                                data=data_short)
    data['response_close'] = data['api'].request(order_close_data)
    return(data)


# #### take_profit
#--------------------------------------------------------------------------------------------------------------------------
def take_profit(data):
    #global data
    
    if data['order_current_open'] == 'long':
        data['price_order_ask']      = float(data['positions_info']['positions'][0]['long']['averagePrice'])
        data['long_profit_val']      = data['price_bid'] - data['price_order_ask']
        
        data['long_max_profit']      = max(data['long_max_profit'], data['long_profit_val'])        
        data['long_buffer_val']      = max(data['pip_take_profit'], data['long_max_profit'] * data['pip_take_profit_ratio'])        
        data['long_buffer_profit']   = data['long_max_profit'] - data['long_buffer_val']
        
        if data['long_profit_val'] <= data['long_buffer_profit'] and data['long_profit_val'] >= data['pip_take_profit']:
            data = close_long_orders(data)
            data = reset_data(data)
            data = check_for_open_orders(data)
            data['num_took_profit'] = data['num_took_profit'] + 1
                
                
    if data['order_current_open'] == 'short':
        data['price_order_bid'] = float(data['positions_info']['positions'][0]['short']['averagePrice'])
        data['short_profit_val']      = data['price_order_bid'] - data['price_ask']
        
        data['short_max_profit']      = max(data['short_max_profit'], data['short_profit_val'])        
        data['short_buffer_val']      = max(data['pip_take_profit'], data['short_max_profit'] * data['pip_take_profit_ratio'])        
        data['short_buffer_profit']   = data['short_max_profit'] - data['short_buffer_val']
        
        if data['short_profit_val'] <= data['short_buffer_profit'] and data['short_profit_val'] >= data['pip_take_profit']:
            data = close_short_orders(data)
            data = reset_data(data)
            data = check_for_open_orders(data)
            data['num_took_profit'] = data['num_took_profit'] + 1
    
    return(data)
#==========================================================================================================================


# #### timed_stop_loss
#--------------------------------------------------------------------------------------------------------------------------
def timed_stop_loss(data):
    #global data
    
    if data['order_current_open'] == 'long':
        data['price_order_ask']      = float(data['positions_info']['positions'][0]['long']['averagePrice'])        
        data['long_loss_val'] = data['price_bid'] - data['price_order_ask']
        
        data['full_loss_list'].append(data['long_loss_val'])
        data['full_loss_list_len'] = len(data['full_loss_list'])
        
        data['long_loss_list'].append(data['long_loss_val'])        
        data['long_loss_list_len'] = len(data['long_loss_list'])        
        if data['long_loss_list_len'] > data["num_of_ticks"]:
            data['long_loss_list'].popleft()
            data['long_loss_list_len'] = len(data['long_loss_list'])
                
        data['long_loss_lema'] = list(pd.DataFrame(list(data['long_loss_list'])).ewm(span=data['long_loss_list_len']).mean()[0])[data['long_loss_list_len'] - 1]        
        
        if data['full_loss_list_len'] >= data['loss_iter_limit']:                    
            if data['long_loss_lema'] <= data['timed_loss_limit']:
                data = close_long_orders(data)
                data = reset_data(data)
                print(1)
                data = check_for_open_orders(data)
                data['num_timed_stop_loss'] = data['num_timed_stop_loss'] + 1         

        if data['long_loss_val'] < data['max_lema_loss']:
            data = close_long_orders(data)
            data = reset_data(data)
            print(2)
            data = check_for_open_orders(data)
            data['num_timed_stop_loss'] = data['num_timed_stop_loss'] + 1
                
    if data['order_current_open'] == 'short':
        data['price_order_bid'] = float(data['positions_info']['positions'][0]['short']['averagePrice'])        
        data['short_loss_val'] = data['price_order_bid'] - data['price_ask']    
        
        data['full_loss_list'].append(data['short_loss_val'])
        data['full_loss_list_len'] = len(data['full_loss_list'])        
        
        data['short_loss_list'].append(data['short_loss_val'])
        data['short_loss_list_len'] = len(data['short_loss_list'])        
        if data['short_loss_list_len'] > data["num_of_ticks"]:
            data['short_loss_list'].popleft()
            data['short_loss_list_len'] = len(data['short_loss_list'])
        
        data['short_loss_lema'] = list(pd.DataFrame(list(data['short_loss_list'])).ewm(span=data['short_loss_list_len']).mean()[0])[data['short_loss_list_len'] - 1]
        
        if data['full_loss_list_len'] >= data['loss_iter_limit']:        
            if data['short_loss_lema'] <= data['timed_loss_limit']:
                data = close_short_orders(data)
                data = reset_data(data)
                print(3)
                data = check_for_open_orders(data)      
                data['num_timed_stop_loss'] = data['num_timed_stop_loss'] + 1
                
        if data['short_loss_val'] < data['max_lema_loss']:
            data = close_short_orders(data)
            data = reset_data(data)
            print(4)
            data = check_for_open_orders(data)
            data['num_timed_stop_loss'] = data['num_timed_stop_loss'] + 1            
                
    return(data)
#==========================================================================================================================


# ### Core Engine
def run_engine(data, live_df_full):
    
    #global data
    #global live_df_full
    
    data['api'] = API(access_token = data['access_token'])
    request_stream_data = pricing.PricingStream(accountID=data['accountID'], params=data['params'])
    response_stream = data['api'].request(request_stream_data)
    
    for data['iter'], resp in enumerate(response_stream):
        #if i % data['num_of_ticks'] == 0:
        data, live_df_full = print_report(data, live_df_full)        

        if resp['type'] == 'HEARTBEAT': # Heart beat response to keep the data['api'] connection alive (Avoid timeout)
            continue

        # Date and Data ---------------------------------------------
        data = get_date_time(resp, data)
        if data['time_diff'] > data['max_time_diff']:
            print(data['time_diff'])
            raise ValueError('Time difference is above limit')

        data = get_prices(resp, data)
        data = take_profit(data)
        data = timed_stop_loss(data)
        
        # Build avg tick ---------------------------------------------    
        if len(data['list_tick_avg']) < data['num_of_ticks']:
            data = before_avg_len(data)
            continue
        elif len(data['list_tick_avg']) == data['num_of_ticks']:
            data = after_avg_len(data)

        # =================================================================
        # Build RSI ---------------------------------------------
        if len(data['list_tick']) < data['rsi_len']:
            data = before_rsi_len(data)          
        elif len(data['list_tick']) == data['rsi_len']:
            data = after_rsi_len(data) 

        # Build SMA ---------------------------------------------
        if len(data['ssma_list']) < data['sma_len']:
            data = before_sma(data)          
        elif len(data['ssma_list']) == data['sma_len']:
            data = after_sma(data)  

        # Build LMA ---------------------------------------------
        if len(data['lsma_list']) < data['lma_len']:
            data = before_lma(data)          
            continue
        elif len(data['lsma_list']) == data['lma_len']:
            data = after_lma(data)  
        # =================================================================       
        
        if data['rsi_ready'] and data['lma_ready']:
            data['live_df_ready'] = True

        if data['live_df_ready']:
               
            new_data = {your_key: data[your_key] for your_key in data['select_keys']}
            live_df = pd.DataFrame([new_data])        
            live_df.drop(data['remove_cols'], axis=1, inplace=True)
            live_df = live_df[data['col_order']]
            live_df = live_df.round(5)
            
            data['prediction'] = model_new.predict(live_df)     
            data['num_predictions'] = data['num_predictions'] + 1
            
            live_df['predicted_direction'] = data['prediction']
            live_df_full = live_df_full.append(live_df)
            live_df_full.to_csv('data/live_preds.csv', index = False)
            
            data = map_predictions(data)            
            data = check_for_open_orders(data)
            data = make_order(data)
               
    return(data, live_df_full)


# ### Report
#--------------------------------------------------------------------------------------------------------------------------
def print_report(data, live_df_full):
    
    #global data
    #global live_df_full
    
    #display.clear_output(wait = True) 
    #os.system('cls')
    os.system('clear')
    end_ts = time.time()
    elasped_time1 = end_ts - data["start_ts_internal"]
    data['elasped_time'] = str(dt.timedelta(seconds=elasped_time1)).split(".")[0]
    print('===============================================================================')
    print('                      RUN & DATA BUILD')
    print(f'start_ts              : {data["start_ts"]}')
    print(f'elapsed time          : {data["elasped_time"]}')
    print(f'time_diff             : {data["time_diff"]}')    
    print(f'error/iter            : {data["error_count"]}/{data["iter"]}')    
    print('-----------------------------------')
    print(f'num_of_ticks          : {len(data["list_tick_avg"])}/{data["num_of_ticks"]}')
    print(f'rsi_len               : {len(data["list_RSI"])}/{data["rsi_len"]}')
    print(f'sma_len               : {len(data["ssma_list"])}/{data["sma_len"]}')
    print(f'lma_len               : {len(data["lsma_list"])}/{data["lma_len"]}')
    print(f'live_df_ready         : {data["live_df_ready"]}')
    print(f'tick_gap_error        : {data["tick_gap_error"]}')
    print('===============================================================================')   
    print('                      PARAMETERS')
    print(f'instrument            : {data["instrument"]}          take_profit_val       : {data["take_profit_val"]}')
    print(f'pip_size              : {data["pip_size"]}           pip_take_profit_ratio : {data["pip_take_profit_ratio"]}') 
    print(f'order_num             : {data["order_num"]}                stop_loss_pip         : {round(data["stop_loss_pip"],5)}')
    print(f'timed_loss_windows    : {data["timed_loss_windows"]}                timed_loss_limit      : {round(data["timed_loss_limit"],5)}')
    print(f'act_tick_gap          : {round(data["act_tick_gap"],5)}          max_lema_loss         : {round(data["max_lema_loss"],5)}')    

    print('===============================================================================')
    print('                       PREDICTIONS')
    print(f'num_predictions       : {data["num_predictions"]}                num_orders            : {data["num_orders"]}')
    print(f'order_create          : {data["order_create"]}')
    print('===============================================================================')
    print('                         Results')
    print(f'num_took_profit       : {data["num_took_profit"]}                num_timed_stop_loss   : {data["num_timed_stop_loss"]}')
    print('===============================================================================')
    print('                          ORDER')
    print(f'order_current_open    : {data["order_current_open"]}')
          
    if data['order_current_open'] == 'long':
        print(f'long_max_profit       : {data["long_max_profit"]}')
        print(f'long_buffer_val       : {data["long_buffer_val"]}')        
        print(f'long_buffer_profit    : {data["long_buffer_profit"]}')
        print(f'long_p&l              : {data["long_profit_val"]}')
        print('------------------------------------')        
        print(f'full_loss_list_len    : {data["full_loss_list_len"]}')
        print(f'long_loss_list_len    : {data["long_loss_list_len"]}')
        print(f'long_loss_lema        : {data["long_loss_lema"]}')
        

    elif data['order_current_open'] == 'short':
        print(f'short_max_profit       : {data["short_max_profit"]}')
        print(f'short_buffer_val       : {data["short_buffer_val"]}')        
        print(f'short_buffer_profit    : {data["short_buffer_profit"]}')
        print(f'short_p&l              : {data["short_profit_val"]}')
        print('------------------------------------')
        print(f'full_loss_list_len     : {data["full_loss_list_len"]}')        
        print(f'short_loss_list_len    : {data["short_loss_list_len"]}')
        print(f'short_loss_lema        : {data["short_loss_lema"]}')
    print('===============================================================================')
    
    return(data, live_df_full)
#==========================================================================================================================    


# ### Reset Data
#--------------------------------------------------------------------------------------------------------------------------
def reset_data(data):
    #global data    
    
    param_df = pd.read_csv('utils/parameters.csv')
    
    # Parameters ##############################################################################
    #Order details ------------------------------------------    
    data['instrument'] = "EUR_USD"
    data['pip_size'] = 0.0001

    data['order_num']                 = param_df['order_num'][0]
    
    data['stop_loss_val']             = param_df['stop_loss_val'][0]
    data['timed_loss_limit']          = param_df['timed_loss_limit'][0]
    data['timed_loss_windows']        = param_df['timed_loss_windows'][0]
    
    data['take_profit_val']           = param_df['take_profit_val'][0] 
    data['pip_take_profit_ratio']     = param_df['pip_take_profit_ratio'][0]        
    
    #Data Gen ------------------------------------------    
    data['num_of_ticks']              = param_df['num_of_ticks'][0]
    data['rsi_len']                   = param_df['rsi_len'][0]   
    data['sma_len']                   = param_df['sma_len'][0]
    data['lma_len']                   = param_df['lma_len'][0]    
    
    data['loss_iter_limit']           = data['num_of_ticks']          * data['timed_loss_windows']        
    data['pip_take_profit']           = data['take_profit_val']       * data['pip_size']
    data['timed_loss_limit']          = data['timed_loss_limit']      * data['pip_size'] * -1

    data['max_lema_loss']             = 0
    data['stop_loss_pip']             = 0

    # ############################################################################################################################################################
    # ############################################################################################################################################################
    # Declarations ##############################################################################
    #Date and Time ------------------------------------------
    data['ts_date_val'] = 0
    data['ts_time_val'] = 0
    data['tot_ts'] = 0
    data['time_diff'] = 0
    data['max_time_diff'] = 15

    
    #Data Gen ------------------------------------------
    data['rs_max'] = 1e6
    data['remove_cols'] = ['tick_avg', 'sema', 'ssma', 'lema', 'lsma', 'max_tick', 'min_tick', 'rs']
    data['col_order'] = ['spread_avg', 'tick_sd', 'sema_diff', 'lema_diff', 'diff', 'avg_gain','avg_loss', 'rsi', 'ssma_diff', 'lsma_diff', 'sma_diff', 'max_gap','min_gap', 'ema_diff', 'small_sema_slope', 'long_sema_slope', 'slope_diff']
    data['select_keys'] = ['tick_avg', 'spread_avg', 'tick_sd', 'diff', 'avg_gain','avg_loss', 'rs', 'rsi', 'sema',  'sema_diff', 'ssma', 'ssma_diff', 'lema', 'lema_diff', 'lsma', 'lsma_diff', 'ema_diff', 'sma_diff', 'max_tick', 'min_tick', 'max_gap', 'min_gap', 'small_sema_slope', 'long_sema_slope', 'slope_diff']

    # Price and ticks ------------------------------------------
    
    data['list_tick_avg'] = collections.deque([])
    data['list_spread'] = collections.deque([])
    data['min_tick'] = 0
    data['max_tick'] = 0
    data['min_tick_gap'] = 0
    data['max_tick_gap'] = 0
    
    data['act_tick_gap'] = float()
    
    # Prediction ------------------------------------------        
    data['live_df_ready'] = False
    data['prediction'] = None 

    # Orders ------------------------------------------
    #data['order_val'] = 0
    data['order_current_open'] = False
    data['order_create'] = None

    data['positions_info'] = None
    data['positions_long'] = 0
    data['positions_short'] = 0
    data['response_order'] = None
    data['response_close'] = None


    # Take profit ------------------------------------------
    data['long_max_profit'] = 0
    data['price_order_ask'] = 0
    data['long_profit_val'] = 0
    data['long_buffer_val'] = 0
    data['long_buffer_profit'] = 0

    data['short_max_profit'] = 0
    data['price_order_bid'] = 0
    data['short_profit_val'] = 0
    data['short_buffer_val'] = 0
    data['short_buffer_profit'] = 0


    # Timed Stop loss ------------------------------------------
    data['long_loss_val'] = 0
    data['long_loss_list'] = collections.deque([])
    data['long_loss_list_len'] = 0
    data['long_loss_lema'] = 0
    
    data['short_loss_val'] = 0
    data['short_loss_list'] = collections.deque([])
    data['short_loss_list_len'] = 0
    data['short_loss_lema'] = 0   
    
    data['full_loss_list'] = collections.deque([])
    data['full_loss_list_len'] = 0
    
    return(data)
#==========================================================================================================================


# ## Fixed Variables
live_df_full = pd.DataFrame()

data = {}
data['instrument'] = "EUR_USD"
data['pip_size'] = 0.0001
data['iter'] = 0
data["tick_gap"] = 0

data['alarm_flag'] = True
data['error_count'] = 0

data['price_ask'] = 0
data['price_bid'] = 0
data['price_stop'] = 0
data['price_tick'] = 0
data['price_spread'] = 0

data['act_max_tick'] = float()
data['act_min_tick'] = float()
data['act_tick_gap'] = float()

data['rsi_ready'] = False
data['lma_ready'] = False
data['tick_gap_error'] =  False

data['list_tick_avg'] = collections.deque([])
data['list_spread'] = collections.deque([])

data['list_tick'] = collections.deque([])
data['list_up'] = collections.deque([])
data['list_down'] = collections.deque([])
data['list_AvgGain'] = collections.deque([])
data['list_Avgloss'] = collections.deque([])
data['list_RS'] = collections.deque([])
data['list_RSI'] = collections.deque([])

data['ssma_list'] = collections.deque([])
data['lsma_list'] = collections.deque([])

data['ssma_ready'] = collections.deque([])
data['sema_ready'] = collections.deque([])

data['lsma_ready'] = collections.deque([])
data['lema_ready'] = collections.deque([])

data['num_predictions'] = 0
data['num_orders'] = 0
data['num_took_profit'] = 0
data['num_timed_stop_loss'] = 0

data['access_token'] = config['oanda_demo_hedge']['token']
data['accountID'] = config['oanda_demo_hedge']['account_id']
data['params'] = {'instruments': data['instrument']}

data['api'] = API(access_token = data['access_token'])
request_stream_data = pricing.PricingStream(accountID=data['accountID'], params=data['params'])
response_stream = data['api'].request(request_stream_data)


# ## never ending loop
data = check_for_open_orders(data)
data = check_for_open_orders(data)
data = check_for_open_orders(data)
logging.basicConfig(filename='traderrun.log', level=logging.DEBUG)

run_flg = true 
data = reset_data(data)
data['start_ts'] = datetime.now().strftime("%y-%b-%d, %i:%m:%s (%p)")
data["start_ts_internal"] = time.time()

while run_flg ==  true:
    try:        
        data, live_df_full = run_engine(data, live_df_full)        
    
    except keyboardinterrupt:
        print("Run manually stopped")
        ts = dt.datetime.now()
        err_msg = 'KeyboardInterrupt'
        logging.error(f'--- Timestamp-{ts}, Error-{err_msg}')
        break           
    
    except Exception as err_msg:
        data['error_count'] = data['error_count'] + 1
        ts = dt.datetime.now()
        logging.error(f'--- Timestamp-{ts}, Error-{err_msg}')


# ## Single loop for testing
# data = check_for_open_orders(data)
# data = check_for_open_orders(data)
# data = check_for_open_orders(data)

# data = reset_data(data)

# #data['start_ts'] = datetime.now().strftime("%Y-%b-%d, %I:%M:%S (%p)")
# data['start_ts'] = (datetime.now() + timedelta(hours=8, minutes=0)).strftime("%Y-%b-%d, %I:%M:%S (%p)")

# data["start_ts_internal"] = time.time()

# data, live_df_full = run_engine(data, live_df_full)        