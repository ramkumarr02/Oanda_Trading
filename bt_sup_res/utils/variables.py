from utils.packages import *


#...............................................................................................
data = {}

data['total_df'] = pd.DataFrame()
data['dt_list'] =  collections.deque()
data['dir_list'] = collections.deque()
data['sema_list'] = collections.deque()
data['lema_list'] = collections.deque()
data['slema_list'] = collections.deque()
data['llema_list'] = collections.deque()
data['pl_list'] =  collections.deque()
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
data['open_order'] = False    
data['open_order_type'] = None
data['df_subset_size'] = None
data['pl_positive'] = False
data['pl_positive_flag'] = True
data['slema_positive'] = False
data['tick_positive'] = False
data['slema_check_flag'] = False
data['tick_check_flag'] = False
data['tick_close_flag'] = False
data['tick_close_flag'] = False
data['stop_loss_flag'] = True
data['reverse_order_flag'] =  None
data['slema_closed_flag'] = None
# data['slema_move_close_flag'] =  None

data['position_without_cushion'] = None

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

# data["input_file_name"] = 'eurusd_2021'
# data['min_order_angle'] = 20
data['position'] = None
data['pip_decimal_num'] = 6
data['test_val'] = []

data["product"] = 'eurusd'
data["input_year"] = 2021
data["input_file_name"] = f'{data["product"]}_{data["input_year"]}.csv'

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

# data['sema_len']        = 3000
# data['slema_len']       = 7500
# data['lema_len']        = 30000
# data['sema_len']        = 6000
# data['slema_len']       = 15000
# data['lema_len']        = 60000

data['dir_change'] = False
data['to_order'] = None

data['pl_move_trail_ratio']         = 0.75
data['pl_loss_trail_trigger']       = -0.0040
data['pl_loss_trail_size']          = 0.75

data['sema_len']    = 60
data['slema_len']   = 400
data['lema_len']    = 1200

data['angle_len']       = 100

data['pl_move_trail_trigger']       = 0.0002
data['stop_loss_pip']               = -0.0002

data['min_llema_angle'] = 0

data['take_profit_method']  = 'simple'
data['stop_loss_method']    = 'simple'

data['start_date'] = {'year':2021, 'month':1, 'date':5}
data['end_date']   = {'year':2021, 'month':1, 'date':5}

# data['direction'] = 'reverse'
data['direction'] = 'straight'

data["plot"] = True
data['marker_size'] = 5

data['take_profit_flag'] = False

data['input_rows'] = 130_000
data['sema_close_flag'] = False


data['df_bars'] = pd.DataFrame()
data['df_bars']['support'] = ''
data['df_bars']['resistance'] = ''

data['candle_size'] = 120
data['line_length'] = 1000
data['min_line_points'] = 5
data['fractal_one_side_bar_count'] = 2
data['sup_res_touches'] = 2
data['sup_res_last_ticks_window'] = 130_000

data['num_lines'] = 3

data['plot_transactions']   = False
data['plot_tip_points']     = True
data['plot_trend_lines']    = True

data['min_points_for_line'] = 8
#...............................................................................................