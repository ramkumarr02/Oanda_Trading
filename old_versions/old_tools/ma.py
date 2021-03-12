from utils.packages import *

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
    data['sema'] = list(pd.DataFrame(list(data['ssma_list'])).ewm(span=data['sma_len']).mean()[0])[data['sma_len'] - 1]
    
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
    data['lema'] = list(pd.DataFrame(list(data['lsma_list'])).ewm(span=data['lma_len']).mean()[0])[data['lma_len'] - 1]
    data['long_sema_slope'] = get_slope(data['lsma_list'], data)
    
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