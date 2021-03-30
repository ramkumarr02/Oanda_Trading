from utils.packages import *



#...............................................................................................
data = {}

data['sema_tick_list'] = collections.deque()
data['lema_tick_list'] = collections.deque()
data['sema'] = np.float()
data['lema'] = np.float()
data['sema_angle'] = np.int()
data['lema_angle'] = np.int()

data['sema_angle_list'] =  collections.deque()
data['lema_angle_list'] =  collections.deque()

data['position'] = None
data['dir_list'] = collections.deque()
data['to_order'] = None
data['opened_order'] = None
data['dir_change'] = False
data['num_orders'] = 0

data['order_num'] = 1

data['sema_len'] = 60
data['lema_len'] = 600
data['angle_len'] = 10

data['close_angle'] = 30
data['angle_close_pip'] = 0.0001
data['pl'] = np.float()

data['os'] = 'notebook'
data['max_time_diff'] = 15
#...............................................................................................