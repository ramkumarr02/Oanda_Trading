from utils.packages import *


#...............................................................................................
data = {}

data['total_df'] = pd.DataFrame()
data['dt_list'] =  collections.deque()
data['dir_list'] = collections.deque()
data['sema_list'] = collections.deque()
data['lema_list'] = collections.deque()
data['pl_list'] =  collections.deque()
data['sema_angle_list'] = collections.deque()
data['lema_angle_list'] = collections.deque()
data['tick_angle_list'] = collections.deque()
data['lema_tick_diff']  = collections.deque()

data['i_list'] = []
data['tick_list'] = []
data['angle_list'] = []
data['df_sema_list'] = []
data['df_lema_list'] = []
data['df_tick_list'] = []
data['df_sema_angle_list'] = []
data['df_lema_angle_list'] = []
data['df_tick_angle_list'] = []


data['buy_markers_x'] = []
data['buy_markers_y'] = []
data['sell_markers_x'] = []
data['sell_markers_y'] = []

data['position'] = False
data['open_order'] = False    
data['open_order_type'] = None
data['df_subset_size'] = None
data['lema_tick_diff_avg_half'] = None
data['pl_positive'] = False

data['tick_close_flag'] = False
data['pl_move_flag']    = False
data['stop_loss_flag']  = False

data['ema_diff'] = 0

data['position_without_cushion'] = None

data['close_type']      = []
data['order_types']     = []
data['order_methods']   = []
data['lema_vals']       = []

# data['running_in'] = 'linux'


data['sema_close_order_angle'] = 5

data['pip_size'] = 0.0001

data['tick_order_angle'] = 20

# data["input_file_name"] = 'eurusd_2021'
# data['min_order_angle'] = 20

data["product"] = 'eurusd'
data["input_year"] = 2021
data["input_file_name"] = f'{data["product"]}_{data["input_year"]}.csv'

data['input_rows'] = None
data["plot"] = True

data['start_date'] = {'year':2021, 'month':4, 'date':1}
data['end_date']   = {'year':2021, 'month':4, 'date':1}

data['close_angle'] = 40
data['lema_close_angle'] = 10
data['angle_close_pip'] = 0.0002

data['gap_cushion'] = data['pip_size'] * 2

# data['pl_move_trigger_store']   = 0.0003
# data['pl_move_min_store']       = 0.00006

# data['pl_move_trigger'] = data['pl_move_trigger_store']
# data['pl_move_min']     = data['pl_move_min_store']

data['pl_move_trail_trigger']   = 0.0001
data['pl_move_trail_ratio']     = 0.5
data['pl_min']                  = 0.0010
data['stop_loss_pip']           = 0.0005

data['tick_close_angle'] = 5
data['pl_close_angle'] = 15

data['sema_len']        = 200
data['lema_len']        = 4000
data['sema_len']        = 1000
data['lema_len']        = 10000

data['lema_angle_len']      = 50
data['sema_angle_len']      = 200
data['tick_angle_len']      = 300

data['close_angle']     = 25
data['ema_order_gap']   = 0.0002

data['sema_make_order_angle'] = 10
data['tick_make_order_angle'] = 10
data['lema_make_order_angle'] = 1

data['pip_decimal_num'] = 6
#...............................................................................................