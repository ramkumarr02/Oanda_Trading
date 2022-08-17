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

    data["df_ohlc"]['order_side']    = np.nan
    data["df_ohlc"]['order_size']    = np.nan
    data["df_ohlc"]['long_open']     = np.nan
    data["df_ohlc"]['long_close']    = np.nan
    data["df_ohlc"]['short_open']    = np.nan
    data["df_ohlc"]['short_close']   = np.nan
    data["df_ohlc"]['close_type']    = np.nan
    data["df_ohlc"]['pl']            = np.nan

    for data['i'] in tqdm(range(0, data['df_len'])):

        data = capture_iterative_data(data)

        data = calculate_pl(data)
        data = get_direction(data)
        data = simple_close(data)
        data = make_order(data)
        # data = reverse_position(data)

    data = split_date_col(data)
            
    return(data)
#...............................................................................................    