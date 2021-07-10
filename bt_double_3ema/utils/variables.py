from utils.packages import *


#...............................................................................................
data = {}

data['total_df'] = pd.DataFrame()
data['dt_list'] =  collections.deque()
data['dir_list'] = collections.deque()
data['sema_list'] = collections.deque()
data['lema_list'] = collections.deque()
data['slema_list'] = collections.deque()
data['pl_list'] =  collections.deque()
data['sema_angle_list'] =  collections.deque()
data['lema_angle_list'] =  collections.deque()

data['i_list'] = []
data['tick_list'] = []
data['angle_list'] = []
data['df_sema_list'] = []
data['df_lema_list'] = []
data['df_slema_list'] = []
data['df_tick_list'] = []
data['df_sema_angle_list'] = []
data['df_lema_angle_list'] = []

data['long_buy_markers_x'] = []
data['long_buy_markers_y'] = []
data['short_buy_markers_x'] = []
data['short_buy_markers_y'] = []

data['long_sell_markers_x'] = []
data['long_sell_markers_y'] = []
data['short_sell_markers_x'] = []
data['short_sell_markers_y'] = []

data['position'] = False
data['long_open_order'] = False    
data['short_open_order'] = False    
data['open_order_type'] = None
data['df_subset_size'] = None
data['temp_text'] = None
data['tp_flag'] = None


data['pl_positive_flag'] = True
data['negative_hit_limit'] = False

data['long_pl_positive'] = False
data['short_pl_positive'] = False

data['long_pl_negative'] = False
data['short_pl_negative'] = False

data['slema_positive'] = False

data['long_slema_check_flag'] = False
data['short_slema_check_flag'] = False

data['tick_close_flag'] = False
data['tick_close_flag'] = False
data['stop_loss_flag'] = True
data['one_stop_flag'] = False
data['reverse_order_flag'] =  None
data['slema_closed_flag'] = None
# data['slema_move_close_flag'] =  None

data['position_without_cushion'] = None

data['close_type'] = []
data['ord_types'] = []

# data['running_in'] = 'linux'

data['sema_make_order_angle'] = 1
data['sema_close_order_angle'] = 1

data['pip_size'] = 0.0001

data['tick_order_angle'] = 20
data['stop_loss_pip'] = 0.0010

# data["input_file_name"] = 'eurusd_2021'
# data['min_order_angle'] = 20

data["product"] = 'eurusd'
data["input_year"] = 2021
data["input_file_name"] = f'{data["product"]}_{data["input_year"]}.csv'

data['input_rows'] = None
data["plot"] = True

data['start_date'] = {'year':2021, 'month':5, 'date':20}
data['end_date']   = {'year':2021, 'month':5, 'date':21}

data['close_angle'] = 40
data['lema_close_angle'] = 10
data['angle_close_pip'] = 0.0002

data['gap_cushion'] = data['pip_size'] * 2

# data['pl_move_trigger'] = 0.0003
# data['pl_min']            = 0.0010
data['short_pl_move_min']            = None
data['long_pl_move_min']             = None
data['long_pl_loss_min']             = None
data['short_pl_loss_min']            = None

data['stop_loss_pip']           = 0.0015
data['simple_tp']               = 0.0030

data['pl_move_trail_trigger']   = 0.0030
data['pl_move_trail_size']      = 0.9
data['pl_loss_trail_trigger']   = 0.0028
data['pl_loss_trail_size']      = 0.9

data['max_one_stop_fraction'] = 0.5

data['tick_close_angle'] = 5
data['pl_close_angle'] = 15

# data['sema_len']        = 3000
# data['slema_len']       = 7500
# data['lema_len']        = 30000
# data['sema_len']        = 6000
# data['slema_len']       = 15000
# data['lema_len']        = 60000
data['sema_len']        = 5000
data['slema_len']       = 20000
data['lema_len']        = 50000

data['tp_flag'] = 'trail'

data['angle_len']       = 75
data['close_angle']     = 25

data['position'] = None
data['pip_decimal_num'] = 6
data['test_val'] = []
#...............................................................................................