from utils.packages import *



#...............................................................................................
data = {}

data['instrument'] = "EUR_USD"
#data['account'] = 'oanda_demo_primary'
data['account'] = 'oanda_demo_1'

data['sema_tick_list'] = collections.deque()
data['lema_tick_list'] = collections.deque()
data['sema'] = np.float()
data['lema'] = np.float()
data['pl'] = np.float()
data['sema_angle'] = np.int()
data['lema_angle'] = np.int()

data['sema_angle_list'] =  collections.deque()
data['lema_angle_list'] =  collections.deque()

data['dir_list'] = collections.deque()

data['position'] = None
data['to_order'] = None
data['order_type'] = None
data['opened_order'] = None
data['follow_order'] = False
data['dir_change'] = False
data['position'] = False
data["run_flg"] =  True

data['num_orders'] = 0
data['error_count'] = 0
data['follow_order_num'] = 0
data["invest_ratio"] = 12.635353654172
data['margin_call_ratio'] = 0.8 

data['max_time_diff'] = 15

data['pip_size'] = 0.0001
data['pip_decimal_num'] = 6

# data['os'] = 'windows'
data['os'] = 'notebook'
# data['os'] = 'linux'

# data['run_type'] = 'single'
data['run_type']  = 'loop'

data['order_num'] = np.float()
data['gap_cushion'] = data['pip_size'] * 2

data['sema_len'] = 3000
data['lema_len'] = 30000
data['angle_len'] = 10

data['close_angle'] = 40
data['angle_close_pip'] = 0.0002
#...............................................................................................