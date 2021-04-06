from utils.packages import *


#...............................................................................................
def print_report(data):
       
    if data['os'] == 'windows':
        os.system('cls')
    elif data['os'] == 'linux':
        os.system('clear')
    elif data['os'] == 'notebook':
        display.clear_output(wait = True)    

    print('---------------------------')
    print(f"iter            : {data['iter']}")
    print(f"time            : {data['tot_ts']}")
    print(f"tick            : {data['tick']}")
    print(f"sema len        : {len(data['sema_tick_list'])}")
    print(f"lema len        : {len(data['lema_tick_list'])}")
    print(f"Angle len       : {len(data['sema_angle_list'])}")
    print(f"sema            : {data['sema']}")
    print(f"lema            : {data['lema']}")    
    print(f"position        : {data['position']}")  
    print(f"dir_change      : {data['dir_change']}")    
    print(f"to_order        : {data['to_order']}")    
    print(f"follow_order_num: {data['follow_order_num']}")  
    print(f"sema angle      : {data['sema_angle']}")
    print(f"lema angle      : {data['lema_angle']}")
    print(f"pl              : {data['pl']}")
    print(f"error_count     : {data['error_count']}")
    print(f"num_orders      : {data['num_orders']}")
    print('---------------------------')    
#...............................................................................................    