from utils.packages import *


#...............................................................................................
def print_report(data):
       
    if data['os'] == 'windows':
        os.system('cls')
    elif data['os'] == 'linux':
        os.system('clear')
    elif data['os'] == 'notebook':
        from IPython import display
        display.clear_output(wait = True)    

    print('---------------------------')
    print(f"Bot             : Rev - {data['instrument']}")
    print('---------------------------')
    print(f"iter            : {data['iter']}")
    print(f"time            : {data['disp_ts']}")
    print(f"time_diff       : {data['time_diff']}")
    print(f"tick            : {data['tick']}")
    print(f"sema len        : {len(data['sema_tick_list'])}/{data['sema_len']}")
    print(f"lema len        : {len(data['lema_tick_list'])}/{data['lema_len']}")
    print(f"Angle len       : {len(data['sema_angle_list'])}/{data['angle_len']}")
    print(f"sema            : {data['sema']}")
    print(f"lema            : {data['lema']}")    
    print(f"ema_diff        : {data['ema_diff']}")    
    print(f"position        : {data['position']}")    
    print(f"old_position    : {data['old_position']}")    
    print(f"position        : {data['position']}")    
    print(f"dir_change      : {data['dir_change']}")    
    print(f"candle_swing    : {data['candle_swing']}")    
    print(f"to_order        : {data['to_order']}")    
    print(f"sema angle      : {data['sema_angle']}")
    print(f"pl              : {data['pl']}")
    print(f"error_count     : {data['error_count']}")
    print(f"num_orders      : {data['num_orders']}")
    print('---------------------------')    
#...............................................................................................    