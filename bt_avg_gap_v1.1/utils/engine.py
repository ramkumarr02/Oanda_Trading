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
    data = get_date_list(data)
    data = get_rolling_emas(data)
    data = get_hl(data)
    data = get_avg_lines(data)
    data['df_len'] = len(data["df"])

    for i in tqdm(range(0, data['df_len'])):

        data['bid'] = data["df"]['Bid'][i]        
        data['ask'] = data["df"]['Ask'][i]
        data['tick'] = data['df']['tick'][i]        
        data['dt_val'] = data['df']['DateTime'][i]   
        data['dt_val'] = data['dt_val_series'][i]     
        data['sema'] = data['df']['sema'][i]      
        data['slema'] = data['df']['slema'][i]      
        data['lema'] = data['df']['lema'][i]    
        data['h_l_gap'] = data['df']['h_l_gap'][i]    
        data['h_lema'] = data['df']['h_lema'][i]    
        data['l_lema'] = data['df']['l_lema'][i]    
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

        data = simple_take_profit(data)                 
        data = simple_stop_loss(data)
        data = make_order(data)
        data = calculate_pl(data)
            
    return(data)
#...............................................................................................    