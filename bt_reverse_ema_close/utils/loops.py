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
    
    data['ema_diff'] = data['sema'] - data['lema']

    if data["plot"]:
        data["df_lema_list"].append(data['lema'])
    
    return(data)
#...............................................................................................    

 

#...............................................................................................
def before_sema_angle(data):   
    data['sema_angle_list'].append(data['sema'])
    return(data)
#...............................................................................................



#...............................................................................................
def after_sema_angle(data):     
    data['sema_angle_list'].popleft()
    data['sema_angle_list'].append(data['sema'])

    # Get Sema Angle --------------------------------
    data['y_axis'] = list(data["sema_angle_list"])        
    data = get_slope(data, 'sema')            
    # ----------------------------------------------------------  
        
    return(data)
#............................................................................................... 


# ...............................................................................................
def before_lema_angle(data):   
    data['lema_angle_list'].append(data['lema'])
    return(data)
#...............................................................................................


#...............................................................................................
def after_lema_angle(data):     
    data['lema_angle_list'].popleft()
    data['lema_angle_list'].append(data['lema'])

    # Get Lema Angle --------------------------------
    data['y_axis'] = list(data["lema_angle_list"])        
    data = get_slope(data, 'lema')            
    # ----------------------------------------------------------  
        
    return(data)
#...............................................................................................


# ...............................................................................................
def before_tick_angle(data):   
    data['tick_angle_list'].append(data['tick'])
    return(data)
#...............................................................................................


#...............................................................................................
def after_tick_angle(data):     
    data['tick_angle_list'].popleft()
    data['tick_angle_list'].append(data['tick'])

    # Get Lema Angle --------------------------------
    data['y_axis'] = list(data["tick_angle_list"])        
    data = get_slope(data, 'tick')            
    # ----------------------------------------------------------  
        
    return(data)
#............................................................................................... 