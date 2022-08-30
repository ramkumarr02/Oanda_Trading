from utils.packages import *
from utils.loops import *
from utils.dir_slope import *
from utils.order import *
from utils.ml import *

if data['plot']:
    import matplotlib.pyplot as plt
    from matplotlib.pyplot import figure

#...............................................................................................
def run_engine(data):

    data["start_ts"]    = dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d-%H-%M')

    # Read and parse data --------------------
    data                = get_date_list(data)
    data                = read_data(data)
    data                = format_tick_time(data)

    # Get OHLC and indicators --------------------
    data                = get_ohlc(data)
    data                = get_indicators(data)
    data                = get_max_min_lema(data)
    data                = get_tips(data)
    
    data["df_ohlc"]['order_side']    = np.nan
    data["df_ohlc"]['order_size']    = np.nan
    data["df_ohlc"]['long_open']     = np.nan
    data["df_ohlc"]['long_close']    = np.nan
    data["df_ohlc"]['short_open']    = np.nan
    data["df_ohlc"]['short_close']   = np.nan
    data["df_ohlc"]['close_type']    = np.nan
    data["df_ohlc"]['pl']            = np.nan

    data["df_ohlc"]['up']            = np.nan
    data["df_ohlc"]['down']          = np.nan
    
    for data['i'] in tqdm(range(0, data['df_len'])):

        data = capture_iterative_data(data)
        # data = get_lema_BBands_dir(data)
        data = get_lema_gap_dir(data)

        # # Get Dirs : Before Order --------------------------------
        # data = get_position(data)
        # if data['position'] == None:
        #     continue

        # if len(data['dir_list']) < 2:
        #     data['dir_list'].append(data['position'])   
        #     continue

        # elif len(data['dir_list']) == 2:
        #     data = get_cross_dir(data)
        # # ----------------------------------------------------------  

        # data = get_multi_angle_close_pos(data)
        # data = get_multi_angle_open_pos(data)
        # data = sema_cross_close(data)
        data = sema_min_max_close(data)
        data = make_order(data)
        data = calculate_pl(data)

        # data = simple_take_profit(data)
        # # data = slema_positive_check(data)
        # # data = simple_slema_move_close(data)
        # data = simple_stop_loss(data)
        # # data = dir_change_close(data)
        
        # # data = simple_close(data)
        
        # # data = reverse_position(data)

    data = split_date_col(data)
    data = get_report_df(data)
            
    return(data)
#...............................................................................................    