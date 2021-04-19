from utils.packages import *
from utils.dir_slope import *


#...............................................................................................
def before_sema(data):   
    data['sema_list'].append(data['tick'])    
    return(data)
#...............................................................................................
 
    

#...............................................................................................
def after_sema(data):     
    data['sema_list'].popleft()
    data['sema_list'].append(data['tick'])
    data['sema'] = list(pd.DataFrame(list(data['sema_list'])).ewm(span=data['sema_len']).mean()[0])[-1]    
    
    if data["plot"]:
        data["df_sema_list"].append(data['sema'])
        
    return(data)
#...............................................................................................



#...............................................................................................
def before_lema(data):   
    data['lema_list'].append(data['tick'])    
    return(data)
#...............................................................................................



#...............................................................................................
def after_lema(data):     
    data['lema_list'].popleft()
    data['lema_list'].append(data['tick'])
    data['lema'] = list(pd.DataFrame(list(data['lema_list'])).ewm(span=data['lema_len']).mean()[0])[-1]
    
    if data["plot"]:
        data["df_lema_list"].append(data['lema'])
    
    return(data)
#...............................................................................................    

 

#...............................................................................................
def before_angle(data):   
    data['sema_angle_list'].append(data['sema'])
    data['lema_angle_list'].append(data['lema'])
    return(data)
#...............................................................................................



#...............................................................................................
def after_angle(data):     
    data['sema_angle_list'].popleft()
    data['lema_angle_list'].popleft()

    data['sema_angle_list'].append(data['sema'])
    data['lema_angle_list'].append(data['lema'])

    # Get Sema Angle --------------------------------
    data['y_axis'] = list(data["sema_angle_list"])        
    data = get_slope(data, 'sema')            
    # ----------------------------------------------------------  

    # Get Lema Angle --------------------------------
    data['y_axis'] = list(data["lema_angle_list"])        
    data = get_slope(data, 'lema')            
    # ----------------------------------------------------------  
        
    return(data)
#............................................................................................... 



#...............................................................................................
def before_ema_diff(data):   
    data['ema_diff'] = data['sema'] - data['lema']
    data['ema_diff_list'].append(abs(data['ema_diff']))    
    return(data)
#...............................................................................................
 
    

#...............................................................................................
def after_ema_diff(data):     
    data['ema_diff'] = data['sema'] - data['lema']

    data['ema_diff_list'].popleft()
    data['ema_diff_list'].append(abs(data['ema_diff']))

    sorted_list = sorted(data['ema_diff_list'])
    data['avg_ema_gap'] = np.mean(sorted_list[-data['diff_height_count']:])
        
    if data["plot"]:
        data["df_avg_ema_gap_list"].append(data['ema_diff'])
        # data['counter'] = data['counter'] + 1
        # display.clear_output(wait = True)        
        # print(f"counter : {data['counter']}")
    return(data)
#...............................................................................................
