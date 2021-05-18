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
    

    for data['i'] in tqdm(range(0, data['df_len'])):
        
        data['ask'] = data['ask_series'][data['i']]
        data['bid'] = data['bid_series'][data['i']]
        data['tick'] = (data['ask'] + data['bid'])/2                 
        data['dt_val'] = dt.datetime.strptime(data['dt_series'][data['i']].split(".")[0],"%Y%m%d %H:%M:%S")
        
        if data["plot"]:     
            # data['i_list'].append(i)
            data["df_tick_list"].append(data['tick'])

        # Angle of Sema and Lema --------------------------------
        if len(data['sema_angle_list']) < data['angle_len']:
            data = before_angle(data)        
            continue

        if len(data['sema_angle_list']) == data['angle_len']:
            data = after_angle(data)                  
        # ----------------------------------------------------------



        # Angle of Angle --------------------------------
        if len(data['angle_angle_list']) < data['angle_angle_len']:
            data = before_angle_angle(data)        
            continue

        if len(data['angle_angle_list']) == data['angle_angle_len']:
            data = after_angle_angle(data)                  
        # ----------------------------------------------------------

        if data['angle_angle'] == 0 and data['sema_angle'] >= 40:
            data['dir_change'] = True
            data['to_order'] = 'short'

        elif data['angle_angle'] == 0 and data['sema_angle'] <= -40:
            data['dir_change'] = True
            data['to_order'] = 'long'            
        else:
            data['dir_change'] = False
            data['to_order'] = None 
    
        data = angle_close(data)
        # data = reverse_order(data)

        if data['stop_loss_flag']:
            data = stop_loss(data)

        if data['pl_move_flag']:
            data = pl_positive_check(data)
            data = pl_move_close(data)
        
        data = make_order(data)    
        


    if data["plot"]:
        # Adjust df len to lema(shortest) len
        data["df"] = data['df'][-len(data["df_sema_angle_list"]):]   
        data["df"] = data["df"].reset_index(drop = True)    
        
        # Assign sema, lema and tick to df
        data['df']["sema_angle"] = list(data["df_sema_angle_list"])
        data['df']["tick"] = list(data["df_tick_list"])[-len(data["df_sema_angle_list"]):]
                
        # Adjust buy sell markers to the shortened df
        data['len_to_subtract'] = data['angle_angle_len'] + data['angle_len']
        data['buy_markers_x'] = list(np.array(data['buy_markers_x']) - data['len_to_subtract'])
        data['sell_markers_x'] = list(np.array(data['sell_markers_x']) - data['len_to_subtract'])
        data["df"] = data["df"].reset_index(drop = True)
    
    return(data)
#...............................................................................................    