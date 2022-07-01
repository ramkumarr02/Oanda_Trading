from utils.packages import *
from utils.loops import *
from utils.dir_slope import *
from utils.order import *
from utils.time_tick import *


#...............................................................................................
def run_engine(data):

    data['api'] = API(access_token = data['access_token'])
    data['request_stream_data'] = pricing.PricingStream(accountID=data['accountID'], params=data['params'])
    data['response_stream'] = data['api'].request(data['request_stream_data'])

    for data['iter'], data['resp'] in enumerate(data['response_stream']):    

        # Check for sleeping window
        if data['sleep_check']:
            sleep_check()

        data["start_ts"] = dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d-%H-%M')
        
        # Heartbeat check ---------------------------------------------
        if data['resp']['type'] == 'HEARTBEAT': # Heart beat response to keep the data['api'] connection alive (Avoid timeout)
            continue

        # Get time ---------------------------------------------
        data = get_date_time(data)
            
        
        # Time diff check ---------------------------------------------
        if data['time_diff'] > data['max_time_diff']:        
            raise ValueError(f'Time difference is above limit : {data["time_diff"]}')
        
        # Get Data ---------------------------------------------
        data = get_prices(data)
        
        print_report(data)
        
        # sema before after loops --------------------------------
        if len(data['sema_tick_list']) < data['sema_len']:
            data =  before_sema(data)

        if len(data['sema_tick_list']) == data['sema_len']:
            data = after_sema(data)                 
        # ----------------------------------------------------------


        # lema before after loops --------------------------------
        if len(data['tick_list']) < data['lema_len']:
            data = before_lema(data)        
            continue        
        
        if len(data['tick_list']) == data['lema_len']:
            data = after_lema(data)                  
        # ----------------------------------------------------------

        

        # Angle of Sema and Lema --------------------------------
        if len(data['sema_angle_list']) < data['angle_len']:
            data = before_angle(data)        
            continue

        if len(data['sema_angle_list']) == data['angle_len']:
            data = after_angle(data)                  
        # ----------------------------------------------------------
        
        data = get_position(data)

        if not data['position']:
            continue

        # Get Dirs --------------------------------
        if len(data['dir_list']) < 2:
            data['dir_list'].append(data['position'])   
            continue

        elif len(data['dir_list']) == 2:
            data = get_cross_dir(data)
        # ----------------------------------------------------------  
                
        
        data = check_for_open_orders(data)
        data = get_candle_size(data)
        data = set_take_profit(data)
        data = angle_close(data)
        
        data = check_for_open_orders(data)
        data = reverse_order(data)
        
        data = check_for_open_orders(data)
        data = make_order(data)    

    return(data)
#...............................................................................................    