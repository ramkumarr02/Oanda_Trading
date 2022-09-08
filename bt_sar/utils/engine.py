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
    data                = get_tips(data)
    data                = get_returning_points(data)
    data                = get_max_min_vals(data)
    
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
    
    # for data['i'] in tqdm(range(0, data['df_len'])):

    #     data = capture_iterative_data(data)
    #     data = calculate_pl(data)

    #     data = get_match_dir(data)

    #     data = sema_cross_close(data)
    #     data = make_order(data)


    # data = split_date_col(data)
    # data = get_report_df(data)
            
    return(data)
#...............................................................................................    