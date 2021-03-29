from utils.packages import *



#...............................................................................................
data = {}

data['sema_tick_list'] = collections.deque()
data['lema_tick_list'] = collections.deque()
data['sema'] = np.float()
data['lema'] = np.float()

data['sema_len'] = 5
data['lema_len'] = 10

data['os'] = 'notebook'
data['max_time_diff'] = 15
#...............................................................................................