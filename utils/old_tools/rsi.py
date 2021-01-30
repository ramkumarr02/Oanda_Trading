from utils.packages import *

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