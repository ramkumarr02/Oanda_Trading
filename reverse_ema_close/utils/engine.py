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

            
        # lema before after loops --------------------------------
        if len(data['lema_list']) < data['lema_len']:
            data = before_lema(data)        
            continue

        if len(data['lema_list']) == data['lema_len']:
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

        data = angle_close(data)
        data = reverse_order(data)

        if data['pl_move_flag']:
            data = pl_positive_check(data)
            data = pl_move_close(data)

        if data['tick_close_flag']:
            data = tick_close(data)
        
        data = make_order(data)    
        

    if data["plot"]:
        # Adjust df len to lema(shortest) len
        data["df"] = data['df'][-len(data["df_sema_angle_list"]):]   
        data["df"] = data["df"].reset_index(drop = True)    
        
        # Assign sema, lema and tick to df
        data['df']["sema_angle"] = list(data["df_sema_angle_list"])
        data['df']["lema_angle"] = list(data["df_lema_angle_list"])

        data["df"]['lema'] = data["df_lema_list"][-len(data["df_lema_angle_list"]):]            
        data["df"]['sema'] = list(data["df_sema_list"])[-len(data["df_lema_angle_list"]):]    
        data['df']["tick"] = list(data["df_tick_list"])[-len(data["df_lema_angle_list"]):]
                
        # Adjust buy sell markers to the shortened df
        data['len_to_subtract'] = data['lema_len'] + data['angle_len']
        data['buy_markers_x'] = list(np.array(data['buy_markers_x']) - data['len_to_subtract'])
        data['sell_markers_x'] = list(np.array(data['sell_markers_x']) - data['len_to_subtract'])    
        data["df"] = data["df"].reset_index(drop = True)
    
    return(data)
#...............................................................................................    