from utils.packages import *
from utils.loops import *
from utils.dir_slope import *
from utils.order import *


#...............................................................................................
def run_engine(data):

    data["start_ts"] = dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d-%H-%M')

    data['ask_series'] = list(data["df"]['Ask'])
    data['bid_series'] = list(data["df"]['Bid'])
    data['dt_series']  = list(data["df"]['DateTime'])
  
    data['df_len'] = len(data["df"])
    

    for i in tqdm(range(0, data['df_len'])):
        
        data['ask'] = data['ask_series'][i]
        data['bid'] = data['bid_series'][i]        
        data['tick'] = (data['ask'] + data['bid'])/2                 
        data['dt_val'] = dt.datetime.strptime(data['dt_series'][i].split(".")[0],"%Y%m%d %H:%M:%S")
        
        if data["plot"]:     
            data['i_list'].append(i)
            data["df_tick_list"].append(data['tick'])

        # sema before after loops --------------------------------
        if len(data['sema_list']) < data['sema_len']:
            data =  before_sema(data)

        if len(data['sema_list']) == data['sema_len']:
            data = after_sema(data)                 
        # ----------------------------------------------------------

        # slema before after loops --------------------------------
        if len(data['slema_list']) < data['slema_len']:
            data = before_slema(data)        

        if len(data['slema_list']) == data['slema_len']:
            data = after_slema(data)                  
        # ----------------------------------------------------------

            
        # lema before after loops --------------------------------
        if len(data['lema_list']) < data['lema_len']:
            data = before_lema(data)                    

        if len(data['lema_list']) == data['lema_len']:
            data = after_lema(data)                  
        # ----------------------------------------------------------


        # long lema before after loops --------------------------------
        if len(data['llema_list']) < data['llema_len']:
            data = before_llema(data)        
            continue

        if len(data['llema_list']) == data['llema_len']:
            data = after_llema(data)                  
        # ----------------------------------------------------------


        # Angle of Sema and Lema --------------------------------
        if len(data['llema_angle_list']) < data['angle_len']:
            data = before_angle(data)        
            continue

        if len(data['llema_angle_list']) == data['angle_len']:
            data = after_angle(data)                  
        # ----------------------------------------------------------

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
        
        if data['pl_positive_flag']:
            data = pl_positive_check(data)
            data = pl_move_close(data)

        data = slema_positive_check(data)
        data = simple_slema_move_close(data)
        data = reverse_order_position(data)
        data = stop_loss(data)     
        data = make_order(data)    
            
    return(data)
#...............................................................................................    