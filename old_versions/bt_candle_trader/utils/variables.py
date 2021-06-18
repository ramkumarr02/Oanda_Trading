from utils.packages import *


#...............................................................................................
data = {}

data['total_df'] = pd.DataFrame()
data['dt_list'] =  collections.deque()
data['dir_list'] = collections.deque()
data['sema_list'] = collections.deque()
data['lema_list'] = collections.deque()
data['pl_list'] =  collections.deque()
data['sema_angle_list'] =  collections.deque()
data['lema_angle_list'] =  collections.deque()
data['candle_size_list'] =  collections.deque()

data['i_list'] = []
data['tick_list'] = []
data['angle_list'] = []
data['df_sema_list'] = []
data['df_lema_list'] = []
data['df_tick_list'] = []
data['df_sema_angle_list'] = []
data['df_lema_angle_list'] = []


data['buy_markers_x'] = []
data['buy_markers_y'] = []
data['sell_markers_x'] = []
data['sell_markers_y'] = []

data['position'] = False
data['open_order'] = False    
data['open_order_type'] = None
data['df_subset_size'] = None
data['pl_positive'] = False
data['tick_close_flag'] = False
data['tick_close_flag'] = False
data['stop_loss_flag'] = True
data['open_min'] = False
data['close_min'] = False
data['open_val'] = False
data['close_val'] = False
data['close_min_started'] = False
data['high_val']   = 0
data['low_val']   = 100

data['avg_candle_size'] = None
data["candle_size"] = None

data['position_without_cushion'] = None

data['close_type'] = []

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
data["plot"] = False

data['start_date'] = {'year':2021, 'month':6, 'date':10}
data['end_date']   = {'year':2021, 'month':6, 'date':11}

data['close_angle'] = 40
data['lema_close_angle'] = 10
data['angle_close_pip'] = 0.0002

data['gap_cushion'] = data['pip_size'] * 2

data['pl_move_trigger'] = 0.0003
data['pl_move_min']     = 0.00006
data['pl_move_trail_trigger']   = 0.0001
data['pl_move_trail_ratio']     = 0.5
data['pl_min']                  = 0.0010
data['stop_loss_pip']           = 0.0006

data['tick_close_angle'] = 5
data['pl_close_angle'] = 15

data['sema_len']        = 30
data['lema_len']        = 30000
data['angle_len']       = 75
data['close_angle']     = 25


data['pip_decimal_num'] = 6

data['min_val'] = 30

data['candle_color'] = None
data['candle_count'] = 4
data['candle_granularity'] = f'M{data["min_val"]}'
data['min_candle_sl'] = 0.0002
#...............................................................................................