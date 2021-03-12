# ### Packages
from utils.packages import *

# ### Report
#--------------------------------------------------------------------------------------------------------------------------
def print_report(data, live_df_full):
       
    if data['os'] == 'windows':
        os.system('cls')
    elif data['os'] == 'linux':
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