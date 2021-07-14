from utils.packages import *
from utils.variables import *
from utils.i_o import *
from utils.dir_slope import *
from utils.engine import *
from utils.loops import *
from utils.order import *
# import winsound


data["plot"] = False

data['pl_move_trail_trigger']   = 0.0020
data['stop_loss_pip']           = 0.0015

data['start_date'] = {'year':2021, 'month':1, 'date':1}
data['end_date']   = {'year':2021, 'month':1, 'date':31}

data = get_date_list(data)
data = read_data(data)
data = run_engine(data)

if data["plot"]:
    data = adjust_plot_list_lengths(data)
    plot_graph(data)
    
print('-----------------------------------------------------')
print_report(data)
print('-----------------------------------------------------')
print(data['report_df'].groupby(['date_val'])['pls'].sum())
print('-----------------------------------------------------')
print(data['report_df']['pls'].value_counts())
print('-----------------------------------------------------')
data['report_df']

# winsound.PlaySound('C:\\Windows\\Media\\tada.wav', winsound.SND_ASYNC)

