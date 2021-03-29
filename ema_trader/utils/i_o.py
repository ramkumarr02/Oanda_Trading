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
    print(f"time : {data['tot_ts']}")
    print(f"tick : {data['tick']}")
    print(f"sema : {data['sema']}")
    print(f"sema len : {len(data['sema_tick_list'])}")
    print(f"sema list : {data['sema_tick_list']}")
    print(f"lema : {data['lema']}")    
    print(f"lema len : {len(data['lema_tick_list'])}")
    print(f"lema list : {data['lema_tick_list']}")
    print('---------------------------')    
#...............................................................................................    