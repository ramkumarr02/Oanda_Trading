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
    # data['dt_series_frmt']  = [dt.datetime.strptime(x.split(".")[0],"%Y%m%d %H:%M:%S") for x in data['dt_series']]

    data['df_len'] = len(data["df"])
    

    for i in tqdm(range(0, data['df_len'])):
        
        data['ask'] = data['ask_series'][i]
        data['bid'] = data['bid_series'][i]
        data['tick'] = (data['ask'] + data['bid'])/2                 
        data['dt_val'] = dt.datetime.strptime(data['dt_series'][i].split(".")[0],"%Y%m%d %H:%M:%S")


        if data["plot"]:     
            data['i_list'].append(i)
            data["df_tick_list"].append(data['tick'])
        
        data = get_candle_color(data)

        # if len(data['candle_size_list']) < 4:
        #     data['candle_size_list'].append(abs(data['candle_size']))
        #     continue
        # else:
        #     data['candle_size_list'].popleft()
        #     data['candle_size_list'].append(abs(data['candle_size']))
        #     data['avg_candle_size'] = np.mean(data['candle_size_list'])
        #     data['avg_candle_size'] = max(data['avg_candle_size'], data['min_candle_sl'])   
        

        # if data["avg_candle_size"] != None:
        #     data = close_order(data)    
        #     data = stop_loss(data)
        #     data = make_order(data)    
        

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