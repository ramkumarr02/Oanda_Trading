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

data["run_flg"] = True 

# data['run_type'] = 'single'
# data['os'] = 'windows'

data['run_type'] = 'loop'
data['os'] = 'linux'