from utils.packages import *
from utils.loops import *
from utils.dir_slope import *
from utils.order import *

if data['plot']:
    import matplotlib.pyplot as plt
    from matplotlib.pyplot import figure

#...............................................................................................
def run_engine(data):

    data["start_ts"]    = dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d-%H-%M')
    data                = get_date_list(data)
    data                = get_rolling_emas(data)   
    data                = get_ohlc(data)
    # data                = get_cdl_hammer_sstar(data)
    # data                = get_cdl_engulfing(data)
    # data                = merge_ohlc_data(data)

    # data['df']['touched_line']  = np.nan
    # data['df']['order_side']    = np.nan
    # data['df']['order_size']    = np.nan
    # data['df']['order_num']    = np.nan
    # data['df']['long_open']     = np.nan
    # data['df']['long_close']    = np.nan
    # data['df']['short_open']    = np.nan
    # data['df']['short_close']   = np.nan
    # data['df']['all_close']     = np.nan
    # data['df']['close_type']    = np.nan
    # data['df']['pl']            = np.nan

    # for data['i'] in tqdm(range(0, data['df_len'])):

    #     data = capture_iterative_data(data)
    #     data = get_candle_indicator_direction(data)

    #     data = slema_positive_check(data)
    #     data = simple_slema_move_close(data)          
    #     data = dynamic_make_order(data)
    #     data = calculate_multi_pl(data)
    #     # data = simple_stop_loss(data)          
    #     # data = close_all_orders(data)          
    #     # data = make_order(data)
    #     # data = calculate_pl(data)

    # data = split_date_col(data)
            
    return(data)
#...............................................................................................    