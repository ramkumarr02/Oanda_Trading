# ### Packages
from utils.packages import *

# ## Fixed Variables
live_df_full = pd.DataFrame()

data = {}

data['instrument'] = "EUR_USD"
data['pip_size'] = 0.0001
data['iter'] = 0
data["tick_gap"] = 0

data['alarm_flag'] = True
data['error_count'] = 0

data['price_ask'] = 0
data['price_bid'] = 0
data['price_stop'] = 0
data['price_tick'] = 0
data['price_spread'] = 0

data['stop_loss_pip'] = 0

data['act_max_tick'] = float()
data['act_min_tick'] = float()
data['act_tick_gap'] = float()

data['rsi_ready'] = False
data['lma_ready'] = False
data['tick_gap_error'] =  False

data['list_tick_avg'] = collections.deque([])
data['list_spread'] = collections.deque([])

data['list_tick'] = collections.deque([])
data['list_up'] = collections.deque([])
data['list_down'] = collections.deque([])
data['list_AvgGain'] = collections.deque([])
data['list_Avgloss'] = collections.deque([])
data['list_RS'] = collections.deque([])
data['list_RSI'] = collections.deque([])

data['ssma_list'] = collections.deque([])
data['lsma_list'] = collections.deque([])

data['ssma_ready'] = collections.deque([])
data['sema_ready'] = collections.deque([])

data['lsma_ready'] = collections.deque([])
data['lema_ready'] = collections.deque([])

data['num_predictions'] = 0
data['num_orders'] = 0
data['num_took_profit'] = 0
data['num_timed_stop_loss'] = 0

#data['curr_date'] = None

data['order_was_open'] = False

data["run_flg"] = True 

#Data Gen ------------------------------------------
data['rs_max'] = 1e6

#data['select_keys'] = ['tick_avg', 'spread_avg', 'tick_sd', 'diff', 'avg_gain','avg_loss', 'rs', 'rsi', 'sema',  'sema_diff', 'ssma', 'ssma_diff', 'lema', 'lema_diff', 'lsma', 'lsma_diff', 'ema_diff', 'sma_diff', 'max_tick', 'min_tick', 'max_gap', 'min_gap', 'small_sema_slope', 'long_sema_slope', 'slope_diff']
#data['col_order'] = ['spread_avg', 'tick_sd', 'sema_diff', 'lema_diff', 'diff', 'avg_gain','avg_loss', 'rsi', 'ssma_diff', 'lsma_diff', 'sma_diff', 'max_gap','min_gap', 'ema_diff', 'small_sema_slope', 'long_sema_slope', 'slope_diff']

data['select_keys'] = ['tick_avg', 'spread_avg', 'tick_sd', 'diff', 'avg_gain','avg_loss', 'rs', 'rsi', 'sema',  'sema_diff', 'ssma', 'ssma_diff', 'lema', 'lema_diff', 'lsma', 'lsma_diff', 'ema_diff', 'sma_diff', 'max_tick', 'min_tick', 'max_gap', 'min_gap', 'small_sema_slope', 'long_sema_slope', 'slope_diff', 'weekday', 'hour', 'candle_height', 'top_diff', 'bottom_diff']
data['remove_cols'] = ['tick_avg', 'sema', 'ssma', 'lema', 'lsma', 'max_tick', 'min_tick', 'rs']
data['col_order'] = ['weekday', 'hour', 'spread_avg', 'tick_sd', 'candle_height', 'sema_diff', 'lema_diff', 'top_diff', 'bottom_diff', 'diff', 'avg_gain', 'avg_loss', 'rsi', 'ssma_diff', 'lsma_diff', 'sma_diff', 'max_gap', 'min_gap', 'ema_diff', 'small_sema_slope', 'long_sema_slope', 'slope_diff']

data['run_type']    = 'single'
#data['os']          = 'windows'
data['os']          = 'notebook'

# data['run_type']  = 'loop'
# data['os']        = 'linux'