from utils.packages import *
from utils.dir_slope import *


#...............................................................................................
def before_sema(data):   
    data['sema_tick_list'].append(data['tick'])    
    return(data)
#...............................................................................................
 
    

#...............................................................................................
def after_sema(data):     
    data['sema_tick_list'].popleft()
    data['sema_tick_list'].append(data['tick'])
    data['sema'] = list(pd.DataFrame(list(data['sema_tick_list'])).ewm(span=data['sema_len']).mean()[0])[-1]                
    return(data)
#...............................................................................................



#...............................................................................................
def before_lema(data):   
    data['lema_tick_list'].append(data['tick'])    
    return(data)
#...............................................................................................



#...............................................................................................
def after_lema(data):     
    data['lema_tick_list'].popleft()
    data['lema_tick_list'].append(data['tick'])
    data['lema'] = list(pd.DataFrame(list(data['lema_tick_list'])).ewm(span=data['lema_len']).mean()[0])[-1]
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