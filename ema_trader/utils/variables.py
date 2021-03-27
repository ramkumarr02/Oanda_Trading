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

data['open_order'] = False    
data['open_order_type'] = None
data['df_subset_size'] = None

data['close_type'] = []

data['running_in'] = 'notebook'

data['sema_make_order_angle'] = 40
data['sema_close_order_angle'] = 40
data['tick_order_angle'] = 40
data['close_angle'] = 40
data['stop_loss_pip'] = 0.0010

data["year"] = 2021
data['input_rows'] = None
data["plot"] = True

data['start_date'] = {'year':2021, 'month':3, 'date':2}
data['end_date']   = {'year':2021, 'month':3, 'date':2}

data['sema_len'] = 500
data['lema_len'] = 50000

data['angle_len'] = 50
#...............................................................................................