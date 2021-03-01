# ### Packages
from utils.packages import *
from utils.slope_map import *
 
# #### Tick AVG
def tick_gap_checker():
    if data['act_tick_gap'] > 0.1:
        data['tick_gap_error'] =  True  
    return()

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
    
    # data['act_tick_gap'] = float(data['act_max_tick'] - data['act_min_tick'])    
    # data['max_lema_loss'] = data['act_tick_gap'] * (data['stop_loss_val'] / 3)
    # data['max_lema_loss'] = min(-data['max_lema_loss'], -0.0002)    
    # data['stop_loss_pip'] = data['act_tick_gap'] * data['stop_loss_val']
    # data['stop_loss_pip'] = max(data['stop_loss_pip'], 0.0002)
    
    data['list_tick_avg'] = collections.deque([])
    data['list_spread'] = collections.deque([])
    
    return(data)
#==========================================================================================================================    


# #### RSI
#--------------------------------------------------------------------------------------------------------------------------
def before_rsi_len(data):
    #global data
    data['list_tick'].append(data['tick_avg'])

    if len(data['list_tick']) == 1:
        data['list_up'].append(0)
        data['list_down'].append(0)
        data['list_AvgGain'].append(0)
        data['list_Avgloss'].append(0)
        data['list_RS'].append(0)
        data['list_RSI'].append(0)
    elif len(data['list_tick']) > 1:        
        old_price = data['list_tick'][len(data['list_tick'])-2]
        new_price = data['tick_avg']
        data['diff'] = new_price - old_price
        
        if data['diff'] > 0:
            data['list_up'].append(new_price - old_price)
            data['list_down'].append(0)
            data['list_AvgGain'].append(np.mean(data['list_up']))
            data['list_Avgloss'].append(np.mean(data['list_down']))
            data['list_RS'].append(data['list_AvgGain'][len(data['list_AvgGain'])-1]/data['list_Avgloss'][len(data['list_Avgloss'])-1])
            data['rsi'] = 100 - (100/(1+data['list_RS'][len(data['list_RS'])-1]))
            data['list_RSI'].append(data['rsi'])            
        elif data['diff'] < 0:
            data['list_up'].append(0)
            data['list_down'].append(old_price - new_price)
            data['list_AvgGain'].append(np.mean(data['list_up']))
            data['list_Avgloss'].append(np.mean(data['list_down']))
            data['list_RS'].append(data['list_AvgGain'][len(data['list_AvgGain'])-1]/data['list_Avgloss'][len(data['list_Avgloss'])-1])
            data['rsi'] = 100 - (100/(1+data['list_RS'][len(data['list_RS'])-1]))
            data['list_RSI'].append(data['rsi'])            
        elif data['diff'] == 0:
            data['list_up'].append(0)
            data['list_down'].append(0)
            data['list_AvgGain'].append(np.mean(data['list_up']))
            data['list_Avgloss'].append(np.mean(data['list_down']))
            data['list_RS'].append(data['list_AvgGain'][len(data['list_AvgGain'])-1]/data['list_Avgloss'][len(data['list_Avgloss'])-1])
            data['rsi'] = 100 - (100/(1+data['list_RS'][len(data['list_RS'])-1]))
            data['list_RSI'].append(data['rsi'])    
            
    return(data)
#==========================================================================================================================    


#--------------------------------------------------------------------------------------------------------------------------
def after_rsi_len(data):
    #global data
    data['list_up'].popleft()
    data['list_down'].popleft()
    data['list_AvgGain'].popleft()
    data['list_Avgloss'].popleft()
    data['list_RS'].popleft()
    data['list_RSI'].popleft()
    data['list_tick'].popleft()
    data['list_tick'].append(data['tick_avg'])

    old_price = data['list_tick'][len(data['list_tick'])-2]
    new_price = data['tick_avg']
    data['diff'] = new_price - old_price
    
    if data['diff'] > 0:
        data['list_up'].append(new_price - old_price)
        data['list_down'].append(0)
        data['list_AvgGain'].append(np.mean(data['list_up']))
        data['list_Avgloss'].append(np.mean(data['list_down']))
        data['list_RS'].append(data['list_AvgGain'][len(data['list_AvgGain'])-1]/data['list_Avgloss'][len(data['list_Avgloss'])-1])
        data['rsi'] = 100 - (100/(1+data['list_RS'][len(data['list_RS'])-1]))
        data['list_RSI'].append(data['rsi'])
    elif data['diff'] < 0:
        data['list_up'].append(0)
        data['list_down'].append(old_price - new_price)
        data['list_AvgGain'].append(np.mean(data['list_up']))
        data['list_Avgloss'].append(np.mean(data['list_down']))
        data['list_RS'].append(data['list_AvgGain'][len(data['list_AvgGain'])-1]/data['list_Avgloss'][len(data['list_Avgloss'])-1])
        data['rsi'] = 100 - (100/(1+data['list_RS'][len(data['list_RS'])-1]))
        data['list_RSI'].append(data['rsi'])
    elif data['diff'] == 0:
        data['list_up'].append(0)
        data['list_down'].append(0)
        data['list_AvgGain'].append(np.mean(data['list_up']))
        data['list_Avgloss'].append(np.mean(data['list_down']))
        data['list_RS'].append(data['list_AvgGain'][len(data['list_AvgGain'])-1]/data['list_Avgloss'][len(data['list_Avgloss'])-1])
        data['rsi'] = 100 - (100/(1+data['list_RS'][len(data['list_RS'])-1]))
        data['list_RSI'].append(data['rsi'])            
    
    data['avg_gain'] = data['list_AvgGain'][-1]
    data['avg_loss'] = data['list_Avgloss'][-1]
    data['rs'] = data['list_RS'][-1]
    
    if data['rs'] > data['rs_max']:
        data['rs'] = data['rs_max'] 
        
    data['rsi_ready'] = True
        
    return(data)
#==========================================================================================================================    


# #### MA
#--------------------------------------------------------------------------------------------------------------------------
def before_sma(data):
    #global data    
    data['ssma_list'].append(data['tick_avg'])    
    return(data)
#--------------------------------------------------------------------------------------------------------------------------
def after_sma(data):
    #global data
    
    data['ssma_list'].popleft()
    data['ssma_list'].append(data['tick_avg'])

    data['ssma'] = np.mean(data['ssma_list'])
    data['sema'] = list(pd.DataFrame(list(data['ssma_list'])).ewm(span=data['sma_len']).mean()[0])[-1]
    
    data['small_sema_slope'] = get_slope(data['ssma_list'], data)
    
    if len(data['ssma_ready']) < 2:
        data['ssma_ready'].append(data['ssma'])
        data['sema_ready'].append(data['sema'])

    elif len(data['ssma_ready']) > 1:
        data['ssma_ready'].popleft()
        data['sema_ready'].popleft()
        data['ssma_ready'].append(data['ssma'])
        data['sema_ready'].append(data['sema'])

        data['ssma_diff'] = data['ssma_ready'][-1] - data['ssma_ready'][len(data['ssma_ready'])-2]
        data['sema_diff'] = data['sema_ready'][-1] - data['sema_ready'][len(data['sema_ready'])-2]
        
        data['max_tick'] = np.max(data['ssma_list'])
        data['min_tick'] = np.min(data['ssma_list'])
        
        data['max_gap'] = data['max_tick'] -  data['tick_avg']
        data['min_gap'] = data['min_tick'] - data['tick_avg']
    
    return(data)
#==========================================================================================================================

#--------------------------------------------------------------------------------------------------------------------------
def before_lma(data):
    #global data
    data['lsma_list'].append(data['tick_avg'])
    return(data)
#--------------------------------------------------------------------------------------------------------------------------
def after_lma(data):
    #global data
    
    data['lsma_list'].popleft()
    data['lsma_list'].append(data['tick_avg'])

    data['lsma'] = np.mean(data['lsma_list'])
    data['lema'] = list(pd.DataFrame(list(data['lsma_list'])).ewm(span=data['lma_len']).mean()[0])[-1]
    data['long_sema_slope'] = get_slope(data['lsma_list'], data)
    data['slope_diff'] = data['small_sema_slope'] - data['long_sema_slope']

    data['candle_max_val'] = np.max(data['lsma_list'])
    data['candle_min_val'] = np.min(data['lsma_list'])
    data['candle_height'] = data['candle_max_val'] - data['candle_min_val']

    data['top_diff'] = data['candle_max_val'] - data['price_tick']
    data['bottom_diff'] = data['price_tick'] - data['candle_min_val'] 
    
    if len(data['lsma_ready']) < 2:
        data['lsma_ready'].append(data['lsma'])
        data['lema_ready'].append(data['lema'])

    elif len(data['lsma_ready']) > 1:
        data['lsma_ready'].popleft()
        data['lema_ready'].popleft()
        data['lsma_ready'].append(data['lsma'])
        data['lema_ready'].append(data['lema'])

        data['lsma_diff'] = data['lsma_ready'][-1] - data['lsma_ready'][len(data['lsma_ready'])-2]
        data['lema_diff'] = data['lema_ready'][-1] - data['lema_ready'][len(data['lema_ready'])-2]
        
        data['ema_diff'] = data['sema'] - data['lema']
        data['sma_diff'] = data['ssma'] - data['lsma']
                
        data['min_tick_gap'] = min(data["lsma_list"])
        data['max_tick_gap'] = max(data["lsma_list"])
        data['tick_gap'] = float(data['max_tick_gap'] - data['min_tick_gap'])

        data['lma_ready'] = True
    
    return(data)
#==========================================================================================================================