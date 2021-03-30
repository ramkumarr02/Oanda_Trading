from utils.packages import *



#...............................................................................................
data = {}

data['instrument'] = "EUR_USD"
data['account'] = 'oanda_demo_primary'

data['sema_tick_list'] = collections.deque()
data['lema_tick_list'] = collections.deque()
data['sema'] = np.float()
data['lema'] = np.float()
data['sema_angle'] = np.int()
data['lema_angle'] = np.int()

data['sema_angle_list'] =  collections.deque()
data['lema_angle_list'] =  collections.deque()

data['dir_list'] = collections.deque()

data['position'] = None
data['to_order'] = None
data['opened_order'] = None
data['dir_change'] = False
data['num_orders'] = 0
data['error_count'] = 0

data['order_num'] = 1

data['sema_len'] = 60
data['lema_len'] = 30000
data['angle_len'] = 600

data['close_angle'] = 55
data['angle_close_pip'] = 0.0002
data['pl'] = np.float()

# data['os'] = 'windows'
data['os'] = 'linux'
# data['os'] = 'notebook'

data['run_type']  = 'loop'
# data['run_type'] = 'single'

data['max_time_diff'] = 15
data["run_flg"] =  True
#...............................................................................................