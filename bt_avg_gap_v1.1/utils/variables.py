from utils.packages import *


#...............................................................................................
data = {}

data['df'] = pd.DataFrame()
data['total_df'] = pd.DataFrame()
data['dt_list'] =  collections.deque()
data['start_dt_list'] =  collections.deque()
data['dir_list'] = collections.deque()
data['after_order_dir_list'] = collections.deque()
data['sema_list'] = collections.deque()
data['lema_list'] = collections.deque()
data['slema_list'] = collections.deque()
data['llema_list'] = collections.deque()
data['pl_list'] =  collections.deque()
data['start_price'] =  collections.deque()
data['end_price'] =  collections.deque()
data['num_orders'] =  collections.deque()
data['sema_angle_list'] =  collections.deque()
data['lema_angle_list'] =  collections.deque()
data['llema_angle_list'] =  collections.deque()


data['i_list'] = []
data['tick_list'] = []
data['angle_list'] = []
data['df_sema_list'] = []
data['df_lema_list'] = []
data['df_slema_list'] = []
data['df_llema_list'] = []
data['df_tick_list'] = []
data['df_sema_angle_list'] = []
data['df_lema_angle_list'] = []
data['df_llema_angle_list'] = []


data['buy_markers_x'] = []
data['buy_markers_y'] = []
data['sell_markers_x'] = []
data['sell_markers_y'] = []

data['position'] = False
data['after_order_position'] = False
data['open_order'] = 0    
data['open_order_type'] = None
data['pl_positive'] = False
data['pl_positive_flag'] = True
data['slema_positive'] = False
data['tick_positive'] = False
data['slema_check_flag'] = False
data['tick_check_flag'] = False
data['tick_close_flag'] = False
data['tick_close_flag'] = False
data['pl_available'] = False
data['stop_loss_flag'] = True
data['reverse_order_flag'] =  None
data['slema_closed_flag'] = None
# data['slema_move_close_flag'] =  None

data['position_without_cushion'] = None

data['orders_list'] = {}

data['close_type'] = []
data['ord_types'] = []
data['ll_angle'] = []

# data['running_in'] = 'linux'

data['sema_make_order_angle'] = 1
data['sema_close_order_angle'] = 1
data['direction_flag'] = -1

data['pip_size'] = 0.0001


data['tick_order_angle'] = 20
data['stop_loss_pip'] = 0.0010

# data['min_order_angle'] = 20
data['position'] = None
data['pip_decimal_num'] = 10**-6
data['test_val'] = []

data['date_index'] = 0

data['close_angle'] = 40
data['lema_close_angle'] = 10
data['angle_close_pip'] = 0.0002

data['gap_cushion'] = data['pip_size'] * 2
data['sema_gap_pip'] = 0.0015

# data['pl_move_trigger'] = 0.0003
# data['pl_min']            = 0.0010


data['negative_hit_limit']      = False
data['pl_negative']             = False
data['pl_loss_min']             = -100
data['pl_move_min']             = 0

data['close_angle']     = 25
data['tick_close_angle'] = 5
data['pl_close_angle'] = 15

data['dir_change'] = False
data['to_order'] = None

data['min_llema_angle'] = 0

data['take_profit_method']  = 'simple'
data['stop_loss_method']    = 'simple'

data['pl_move_trail_ratio']         = 0.75
data['pl_loss_trail_trigger']       = -0.0020
data['pl_loss_trail_size']          = 1.25



data['input_rows'] = None
data['sema_close_flag'] = False

# --------------------------------------------------------
data['reversed'] = False
data['order_num_i'] = 0

data['sema_len']    = 100
data['slema_len']   = 250
data['lema_len']    = 1000
data['angle_len']   = 1000

data['min_hl_gap'] = 0.0003
data['min_take_profit_pip'] = 0.00005
data['min_stop_loss_pip']   = -0.0003

data['num_of_switch_orders']    = 6
data['loss_switch_pl_pip']      = -0.0020
data['all_close_min_pip']       = 0
data['order_multiplier']        = 2

data["product"] = 'eurusd'
data["input_year"] = 2021
data["input_file_name"] = f'{data["product"]}_{data["input_year"]}.csv'

data['df_subset_size'] = None

data['start_date'] = {'year':2021, 'month':1, 'date':1}
data['end_date']   = {'year':2021, 'month':1, 'date':10}

data['ema_roll_method'] = 'new'

# data['direction'] = 'reverse'
data['direction'] = 'straight'

# data['columns_list'] = ['DateTime_frmt', 'Bid', 'Ask', 'tick', 'lema', 'tick_angle', 'h_l_gap', 'h_lema', 'l_lema']
# data['columns_list'] = ['DateTime_frmt', 'Bid', 'Ask', 'tick', 'lema', 'h', 'l', 'h_l_gap', 'h_lema', 'l_lema']
data['columns_list'] = ['DateTime_frmt', 'Bid', 'Ask', 'tick', 'lema', 'h_l_gap', 'h_lema', 'l_lema']
data['final_columns_list'] = ['DateTime_frmt', 'month_val', 'date_val', 'hour_val','Bid', 'Ask', 'tick', 'lema', 'h_l_gap', 'h_lema', 'l_lema', 'long_open', 'long_close', 'short_open', 'short_close','close_type', 'pl']

data["plot"] = False
data['plot_type'] = 'file'
data['reduce_plot'] = False
data['plot_start']  = '2021-01-04 03:00:00'
data['plot_stop']   = '2021-01-04 06:00:00'
data['things_to_plot'] = ['tick', 'lema', 'h_l_lema', 'positions']
# data['things_to_plot'] = ['tick', 'lema', 'h_l', 'h_l_Lema', 'tick_angle', 'positions']

data['to_csv']      = True

data['take_profit_flag'] = False

data['short_start'] = False
data['long_start'] = False
data['delay_counter'] = 0
data['delay_tics_num'] = 100

data['candle_size'] = 500
data['avg_candle_num'] = 3
data['marker_size'] = 1

data['positions_half_closed'] = False

data['temp_df'] = pd.DataFrame()
data['open_order_temp_list']   = []
data['pl_temp_list']           = []
data['first_type']             = None
data['forward_order_list'] = []

data["csv_file_name"] = 'ema_df-(2021-2021)-(1-1)-(1-10)'

data['csv_list'] = ['ema_2021_jan_aug' , 'ema_df-(2021-2021)-(9-9)-(1-30)', 'ema_df-(2021-2021)-(10-10)-(1-31)', 'ema_df-(2021-2021)-(12-12)-(1-31)']
data['new_file'] = 'ema_2021-jan_dec'

data['chrome_path'] = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"

data['temp_total_pl'] = []
#...............................................................................................