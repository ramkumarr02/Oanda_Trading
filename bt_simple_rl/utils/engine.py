from utils.packages import *
from utils.loops import *
from utils.dir_slope import *
from utils.order import *

if data['plot']:
    import matplotlib.pyplot as plt
    from matplotlib.pyplot import figure

#...............................................................................................
def run_engine(data):

    data["start_ts"]            = dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d-%H-%M')

    data                        = get_date_list(data)
    data                        = get_rolling_emas(data)    
    # data['df']                  = data['df'][data['columns_list']]

    data['df']['touched_line']  = np.nan
    data['df']['order_side']    = np.nan
    data['df']['long_open']     = np.nan
    data['df']['long_close']    = np.nan
    data['df']['short_open']    = np.nan
    data['df']['short_close']   = np.nan
    data['df']['close_type']    = np.nan
    data['df']['pl']            = np.nan

    for data['i'] in tqdm(range(0, data['df_len'])):

        data['bid'] = data["df"]['Bid'][data['i']]        
        data['ask'] = data["df"]['Ask'][data['i']]
        data['tick'] = data['df']['tick'][data['i']]        
        data['sema'] = data['df']['sema'][data['i']]    
        data['slema'] = data['df']['slema'][data['i']]    
        data['lema'] = data['df']['lema'][data['i']]    
        data['tick_angle'] = data['df']['tick_angle'][data['i']]    
        data['tick_angle_2'] = data['df']['tick_angle_2'][data['i']]    
        data['h_l_gap'] = data['df']['h_l_gap'][data['i']]    
        data['h_lema'] = data['df']['h_lema'][data['i']]    
        data['l_lema'] = data['df']['l_lema'][data['i']]    
        
        # Get Dirs : Before Order --------------------------------
        data = get_position(data)
        if data['position'] == None:
            continue

        if len(data['dir_list']) < 2:
            data['dir_list'].append(data['position'])   
            continue

        elif len(data['dir_list']) == 2:
            data = get_cross_dir_chooser(data)
            
        # ----------------------------------------------------------  

        # data = lock_profit(data)                 
        # data = loss_reverse_position(data)
        # data = trail_take_profit(data)                 
        # data = simple_take_profit(data)       
        data = slema_positive_check(data)
        data = simple_slema_move_close(data)          
        data = simple_stop_loss(data)
        data = make_order(data)
        data = calculate_pl(data)

    data = split_date_col(data)
            
    return(data)
#...............................................................................................    