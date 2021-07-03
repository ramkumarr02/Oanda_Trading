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
def before_slema(data):   
    data['slema_list'].append(data['tick'])    
    return(data)
#...............................................................................................



#...............................................................................................
def after_slema(data):     
    data['slema_list'].popleft()
    data['slema_list'].append(data['tick'])
    data['slema'] = list(pd.DataFrame(list(data['slema_list'])).ewm(span=data['slema_len']).mean()[0])[-1]
    
    if data["plot"]:
        data["df_slema_list"].append(data['slema'])
    
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
    # data['y_axis'] = list(data["sema_angle_list"])        
    # data = get_slope(data, 'sema')            
    # # ----------------------------------------------------------  

    # # Get Lema Angle --------------------------------
    # data['y_axis'] = list(data["lema_angle_list"])        
    # data = get_slope(data, 'lema')            
    # ----------------------------------------------------------  
        
    return(data)
#............................................................................................... 

def adjust_plot_list_lengths(data):
    # Adjust df len to lema(shortest) len
    data['df_len'] = len(data["df_lema_list"])

    data["df"] = data['df'][-data['df_len']:]   
    data["df"] = data["df"].reset_index(drop = True)    
    
    data["df"]['lema'] = data["df_lema_list"][-data['df_len']:]            
    data["df"]['slema'] = data["df_slema_list"][-data['df_len']:]            
    data["df"]['sema'] = list(data["df_sema_list"])[-data['df_len']:]    
    data['df']["tick"] = list(data["df_tick_list"])[-data['df_len']:]
            
    # Adjust buy sell markers to the shortened df
    # data['len_to_subtract'] = data['lema_len'] + data['angle_len']
    data['len_to_subtract'] = data['lema_len']
    data['buy_markers_x'] = list(np.array(data['buy_markers_x']) - data['len_to_subtract'])
    data['sell_markers_x'] = list(np.array(data['sell_markers_x']) - data['len_to_subtract'])    
    data["df"] = data["df"].reset_index(drop = True)
    return(data)

#............................................................................................... 