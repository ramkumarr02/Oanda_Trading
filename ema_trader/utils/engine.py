from utils.packages import *
from utils.loops import *
from utils.dir_slope import *
from utils.order import *


#...............................................................................................
def run_engine(data):

    data['ask_series'] = list(data["df"]['Ask'])
    data['bid_series'] = list(data["df"]['Bid'])
    data['dt_series']  = list(data["df"]['DateTime'])
  
    data['df_len'] = len(data["df"])

    for i in tqdm(range(0, data['df_len'])):
        
        data['ask'] = data['ask_series'][i]
        data['bid'] = data['bid_series'][i]
        data['tick'] = (data['ask'] + data['bid'])/2    
        data["tick_list"].append(data['tick'])
        
        data['dt_val'] = dt.datetime.strptime(data['dt_series'][i].split(".")[0],"%Y%m%d %H:%M:%S")

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
                                   
        # Get Angle --------------------------------
        data['y_axis'] = list(data["tick_list"][-data['angle_len']:])        
        if 0 not in data['y_axis']:            
            if len(data['y_axis']) >= data['angle_len']:
                data = get_slope(data)            
        # ----------------------------------------------------------         
             
        data['i_list'].append(i)
        data = get_dir(data)

        # Get Dirs --------------------------------
        if len(data['dir_list']) < 2:
            data['dir_list'].append(data['position'])   
            continue
            
        elif len(data['dir_list']) == 2:
            data = after_dir(data)
        # ----------------------------------------------------------

        data = angle_close(data)
        data = tick_close(data)
        data = close_order(data)
        data = make_order(data)    

    
    # Adjust df len to lema(shortest) len
    data["df"] = data['df'][-len(data["df_lema_list"]):]   
    data["df"] = data["df"].reset_index(drop = True)    
    
    # Assign sema, lema and tick to df
    data["df"]['lema'] = data["df_lema_list"]            
    data["df"]['sema'] = list(data["df_sema_list"])[-len(data["df_lema_list"]):]    
    data['df']["tick"] = list(data["tick_list"])[-len(data["df_lema_list"]):]
    data['df']["angle"] = list(data["angle_list"])[-len(data["df_lema_list"]):]
    
    # Adjust buy sell markers to the shortened df
    data['len_to_subtract'] = data['lema_len']
    data['buy_markers_x'] = list(np.array(data['buy_markers_x']) - data['len_to_subtract'])
    data['sell_markers_x'] = list(np.array(data['sell_markers_x']) - data['len_to_subtract'])    
    data["df"] = data["df"].reset_index(drop = True)
    
    return(data)
#...............................................................................................    