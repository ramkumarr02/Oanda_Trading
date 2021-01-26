from utils.packages import *


#--------------------------------------------------------------------------------------------------------------------------
def reset_data(data):
    #global data    
    
    # Parameters ##############################################################################
    #Order details ------------------------------------------    
    data['instrument'] = "EUR_USD"
    data['pip_size'] = 0.0001

    data['order_num'] = 1
    
    data['stop_loss_val']  = 10
    data['timed_loss_limit'] = 1
    data['timed_loss_windows'] = 1
    
    
    data['take_profit_val'] = 0.5 
    data['pip_take_profit_ratio'] = 0.3        
    
    #Data Gen ------------------------------------------    
    data['num_of_ticks'] = 300
    data['rsi_len'] = 14   
    data['sma_len'] = 5
    data['lma_len'] = 10    
    
    data['loss_iter_limit'] = data['num_of_ticks'] * data['timed_loss_windows']
    data['timed_loss_limit'] = data['timed_loss_limit'] * data['pip_size'] * -1


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
    data['col_order'] = ['spread_avg', 'tick_sd', 'sema_diff', 'lema_diff', 'diff', 'avg_gain','avg_loss', 'rsi', 'ssma_diff', 'lsma_diff', 'sma_diff', 'max_gap','min_gap', 'small_sema_slope', 'long_sema_slope', 'ema_diff']
    data['select_keys'] = ['tick_avg', 'spread_avg', 'tick_sd', 'diff', 'avg_gain','avg_loss', 'rs', 'rsi', 'sema',  'sema_diff', 'ssma', 'ssma_diff', 'lema', 'lema_diff', 'lsma', 'lsma_diff', 'ema_diff', 'sma_diff', 'max_tick', 'min_tick', 'max_gap', 'min_gap', 'small_sema_slope', 'long_sema_slope']

    # Price and ticks ------------------------------------------
    data['price_ask'] = 0
    data['price_bid'] = 0
    data['price_stop'] = 0
    data['price_tick'] = 0
    data['price_spread'] = 0
    data['list_tick_avg'] = collections.deque([])
    data['list_spread'] = collections.deque([])
    data['min_tick'] = 0
    data['max_tick'] = 0
    data['min_tick_gap'] = 0
    data['max_tick_gap'] = 0
    
    # Prediction ------------------------------------------        
    data['live_df_ready'] = False
    data['prediction'] = None 

    # Orders ------------------------------------------
    data['order_val'] = 0
    data['order_current_open'] = False
    data['order_create'] = None
    data['stop_loss_pip'] = data['stop_loss_val'] * data['pip_size']
    #data['stop_loss_pip'] = data['tick_gap'] * 3

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

    data['pip_take_profit'] = data['take_profit_val'] * data['pip_size']

    # Timed Stop loss ------------------------------------------
    data['long_loss_val'] = 0
    data['long_loss_list'] = []
    data['long_loss_list_len'] = 0
    data['long_loss_lema'] = 0
    
    data['short_loss_val'] = 0
    data['short_loss_list'] = []
    data['short_loss_list_len'] = 0
    data['short_loss_lema'] = 0   
    
    return(data)
#==========================================================================================================================