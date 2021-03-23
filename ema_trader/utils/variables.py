from utils.packages import *



#...............................................................................................
data = {}

data['total_df'] = pd.DataFrame()
data['dt_list'] =  collections.deque()
data['dir_list'] = collections.deque()
data['sema_list'] = collections.deque()
data['lema_list'] = collections.deque()
data['pl_list'] =  collections.deque()


data['i_list'] = []
data['tick_list'] = []
data['angle_list'] = []
data['df_sema_list'] = []
data['df_lema_list'] = []

data['buy_markers_x'] = []
data['buy_markers_y'] = []
data['sell_markers_x'] = []
data['sell_markers_y'] = []

data['open_order'] = False    
data['open_order_type'] = None
data['df_subset_size'] = None

data['running_in'] = 'linux'

data['order_angle'] = 10
data['tick_order_angle'] = 20
data['close_angle'] = 30

data["year"] = 2021
data['input_rows'] = None

data['start_date'] = {'year':2021, 'month':3, 'date':8}
data['end_date']   = {'year':2021, 'month':3, 'date':8}

data['sema_len'] = 2000
data['lema_len'] = 5000

data['angle_len'] = 2000
#...............................................................................................