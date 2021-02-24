# ### Packages
from utils.packages import *
from utils.report import *
from utils.orders import *
from utils.slope_map import *
from utils.time_tick import *
from utils.loops import *
from utils.reset import *
warnings.filterwarnings('ignore')


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

        today_date = datetime.today().date()
        if data['curr_date'] != today_date:
            data['curr_date'] = today_date
            get_avg_candle_height(data, candle_count = 5, granularity = 'D')

        data = get_prices(resp, data)
        data = take_profit(data)
        #data = timed_stop_loss(data)
        
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