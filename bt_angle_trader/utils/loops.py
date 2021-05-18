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
    data['sema_angle_list'].append(data['tick'])

    return(data)
#...............................................................................................



#...............................................................................................
def after_angle(data):     
    data['sema_angle_list'].popleft()

    data['sema_angle_list'].append(data['tick'])

    # Get Sema Angle --------------------------------
    data['y_axis'] = list(data["sema_angle_list"])        
    data = get_slope(data, 'sema')            
    # ----------------------------------------------------------  
        
    return(data)
#............................................................................................... 


#...............................................................................................
def before_angle_angle(data):   
    
    data['angle_angle_list'].append(data['sema_angle'])

    return(data)
#...............................................................................................



#...............................................................................................
def after_angle_angle(data):     
    data['angle_angle_list'].popleft()
    data['angle_angle_list'].append(data['sema_angle'])

    # Get Sema Angle --------------------------------
    data['y_axis'] = list(data["angle_angle_list"])        
    data = get_angle_slope(data)            
    # ----------------------------------------------------------  
        
    return(data)
#............................................................................................... 



