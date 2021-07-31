from utils.packages import *
from utils.loops import *
from utils.dir_slope import *
from utils.order import *


#...............................................................................................
def run_engine(data):

    data["start_ts"]        = dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d-%H-%M')
    data = get_rolling_emas(data)

    for i in tqdm(range(0, data['df_len'])):
        data['ask'] = data["df"]['Ask'][i]
        data['bid'] = data["df"]['Bid'][i]        
        data['tick'] = data['df']['tick'][i]        
        data['dt_val'] = data['dt_val_series'][i]   
        data['sema'] = data['df']['sema'][i]      
        data['slema'] = data['df']['slema'][i]      
        data['lema'] = data['df']['lema'][i]      
        data['llema'] = data['df']['llema'][i]      
        data['llema_angle'] = data['df']['llema_angle'][i]      
        
        if data["plot"]:     
            data['i_list'].append(i)
            data["df_tick_list"].append(data['tick'])
            data["df_sema_list"].append(data['sema'])
            data["df_slema_list"].append(data['slema'])
            data["df_lema_list"].append(data['lema'])
            data["df_llema_list"].append(data['llema'])
            data['df_llema_angle_list'].append(data['llema_angle'])

        data = get_position(data)
        if data['position'] == None:
            continue
        
        # Get Dirs --------------------------------
        if len(data['dir_list']) < 2:
            data['dir_list'].append(data['position'])   
            continue

        elif len(data['dir_list']) == 2:
            data = get_cross_dir(data)
        # ----------------------------------------------------------  
        
        data = calculate_pl(data)

        data = take_profit(data)
        
        data = slema_positive_check(data)
        data = simple_slema_move_close(data)
        
        data = reverse_order_position(data)
        
        data = stop_loss(data)     
        
        data = make_order(data)    
            
    return(data)
#...............................................................................................    