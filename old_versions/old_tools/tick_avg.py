from utils.packages import *

# Tick AVG
#--------------------------------------------------------------------------------------------------------------------------
def before_avg_len(data):
    #global data
    data['list_tick_avg'].append(data['price_tick'])
    data['list_spread'].append(data['price_spread'])   
    return(data)
#--------------------------------------------------------------------------------------------------------------------------

def after_avg_len(data):
    #global data
    
    data['tick_avg'] = np.mean(data['list_tick_avg'])
    data['tick_sd'] = np.std(data['list_tick_avg'])
    data['spread_avg'] = np.mean(data['list_spread'])
    
    data['act_max_tick'] = np.max(data['list_tick_avg'])
    data['act_min_tick'] = np.min(data['list_tick_avg'])
    data['act_tick_gap'] = float(data['act_max_tick'] - data['act_min_tick'])
    data['max_lema_loss'] = data['act_tick_gap'] * (data['stop_loss_val'] / 2)
    data['max_lema_loss'] = min(-data['max_lema_loss'], -0.0002)
    
    data['stop_loss_pip'] = data['act_tick_gap'] * data['stop_loss_val']
    data['stop_loss_pip'] = max(data['stop_loss_pip'], 0.0002)
    
    data['list_tick_avg'] = collections.deque([])
    data['list_spread'] = collections.deque([])
    
    return(data)
#==========================================================================================================================    