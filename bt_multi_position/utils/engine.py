from utils.packages import *
from utils.loops import *
from utils.dir_slope import *
from utils.order import *

if data['plot']:
    import matplotlib.pyplot as plt
    from matplotlib.pyplot import figure

#...............................................................................................
def run_engine(data):

    data["start_ts"] = dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d-%H-%M')
    data = get_rolling_emas(data)

    for i in tqdm(range(0, data['df_len'])):

        data['bid'] = data["df"]['Bid'][i]        
        data['ask'] = data["df"]['Ask'][i]
        data['tick'] = data['df']['tick'][i]        
        data['dt_val'] = data['df']['DateTime'][i]   
        data['dt_val'] = data['dt_val_series'][i]     
        data['sema'] = data['df']['sema'][i]      
        data['slema'] = data['df']['slema'][i]      
        data['lema'] = data['df']['lema'][i]    
        data['tick_angle'] = data['df']['tick_angle'][i]    
        
        if data["plot"]:     
            data['i_list'].append(i)
            data["df_tick_list"].append(data['tick'])
            data["df_sema_list"].append(data['sema'])
            data["df_slema_list"].append(data['slema'])
            data["df_lema_list"].append(data['lema'])

        # Get Dirs : Before Order --------------------------------
        data = get_position(data)
        if data['position'] == None:
            continue

        if len(data['dir_list']) < 2:
            data['dir_list'].append(data['position'])   
            continue

        elif len(data['dir_list']) == 2:
            data = get_cross_dir(data)
        # ----------------------------------------------------------  
        

        # # after_order_ Get Dirs --------------------------------
        # data = after_order_get_position(data)
        # if data['after_order_position'] == None:
        #     continue
        

        # if len(data['after_order_dir_list']) < 2:
        #     data['after_order_dir_list'].append(data['after_order_position'])   
        #     continue

        # elif len(data['after_order_dir_list']) == 2:
        #     data = after_order_get_cross_dir(data)
        # # ----------------------------------------------------------  

        data = slema_positive_check(data)
        data = simple_slema_move_close(data)
        data = close_all_orders(data)             
        data = delayed_start_check(data)        
        data = dynamic_make_order(data)

        data = calculate_pl(data)
            
    return(data)
#...............................................................................................    