from utils.packages import *


#...............................................................................................
data = {}

data['df'] = pd.DataFrame()
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
data['open_order'] = 0    
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

# data["input_file_name"] = 'eurusd_2021'
# data['min_order_angle'] = 20
data['position'] = None
data['pip_decimal_num'] = 10**-6
data['test_val'] = []

data["product"] = 'EURUSD'
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

data['dir_change'] = False
data['to_order'] = None

data['pl_move_trail_ratio']         = 0.75
data['pl_loss_trail_trigger']       = -0.0020
data['pl_loss_trail_size']          = 1.25

data['sema_len']    = 1800
data['slema_len']   = 3600
data['lema_len']    = 7200
data['angle_len']   = 7200


data['pl_move_trail_trigger']       = 0.0020
data['stop_loss_pip']               = -0.0020

data['min_llema_angle'] = 0

data['take_profit_method']  = 'simple'
data['stop_loss_method']    = 'simple'

data['start_date'] = {'year':2021, 'month':1, 'date':1}
data['end_date']   = {'year':2021, 'month':1, 'date':10}
data['ema_roll_method'] = 'new'

# data['direction'] = 'reverse'
data['direction'] = 'straight'

data["plot"] = True

data['take_profit_flag'] = False

data['input_rows'] = None
data['sema_close_flag'] = False


data['short_start'] = False
data['long_start'] = False
data['delay_counter'] = 0
data['delay_tics_num'] = 1000
#...............................................................................................