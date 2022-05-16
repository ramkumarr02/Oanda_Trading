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
data['direction'] = None

data['pl_move_trail_ratio']         = 0.75
data['pl_loss_trail_trigger']       = -0.0040
data['pl_loss_trail_size']          = 0.75

# data['slema_len']   = 600


data['angle_len']       = 100

data['pl_move_trail_trigger']       = 0.0002
data['stop_loss_pip']               = -0.0002

data['min_llema_angle'] = 0

data['take_profit_method']  = 'simple'
data['stop_loss_method']    = 'simple'


# data['direction'] = 'reverse'
data['direction'] = 'straight'

data["plot"] = True
data['marker_size'] = 1

data['take_profit_flag'] = False


data['sema_close_flag'] = False


data['df_bars'] = pd.DataFrame()
data['df_bars']['support'] = ''
data['df_bars']['resistance'] = ''

data['start_date'] = {'year':2021, 'month':1, 'date':6}
data['end_date']   = {'year':2021, 'month':1, 'date':6}

# data['input_rows'] = 1_000_000
# data['input_rows'] = 130000
# data['input_rows'] = 130000 - 3000
# data['input_rows'] = 125000 - 4000 - 500
data['input_rows'] = 300000

data['sema_len']    = 60                    * 6
data['lema_len']    = data['sema_len']      * 4

data['candle_size'] = data['sema_len']      * 5
data['line_length'] = data['candle_size']   * 6

data['min_line_points'] = 3
data['pip_decimal_num'] = 3
data['trend_angle']     = 10

data['slope_tick_available'] =  False

data['h_slope_available']       = False
data['l_slope_available']       = False

data['plot_tip_points']         = False
data['plot_trend_lines']        = False
data['plot_angle_line']         = False
data['plot_trend_calc_lines']   = True
data['plot_transactions']       = False

data['plot_type'] = 'file'
data['chrome_path'] = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
data['chart_file_path'] = (f'{os.getcwd()}\\data\\chart.html')
#...............................................................................................