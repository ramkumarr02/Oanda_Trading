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
def before_llema(data):   
    data['llema_list'].append(data['tick'])    
    return(data)
#...............................................................................................



#...............................................................................................
def after_llema(data):     
    data['llema_list'].popleft()
    data['llema_list'].append(data['tick'])
    data['llema'] = list(pd.DataFrame(list(data['llema_list'])).ewm(span=data['llema_len']).mean()[0])[-1]
    
    if data["plot"]:
        data["df_llema_list"].append(data['llema'])
    
    return(data)
#...............................................................................................    


#...............................................................................................
def before_angle(data):   
    data['llema_angle_list'].append(data['llema'])
    return(data)
#...............................................................................................


#...............................................................................................
def after_angle(data):     
    data['llema_angle_list'].popleft()
    data['llema_angle_list'].append(data['llema'])

    # Get Lema Angle --------------------------------
    data['y_axis'] = list(data["llema_angle_list"])        
    data = get_slope(data)            
    # ----------------------------------------------------------  
        
    return(data)
#............................................................................................... 

def roll_ema(ema_list):
    return(pd.DataFrame(ema_list).ewm(span=len(ema_list)).mean()[0].iloc[-1])

#...............................................................................................
def roll_slope(slope_list):
    
    slope_list = list(np.round(slope_list, 6))
    ma_len = len(slope_list)

    x_axis = []
    for i in range(ma_len):
        x_axis.append(1 + ((i+1) * 10**(-6)))
    
    slope_tick, intercept, _, _, _ = linregress(x_axis, slope_list)
    
    slope = math.degrees(math.atan(slope_tick))        

    return(slope)    
#...............................................................................................  


#...............................................................................................  
def get_rolling_emas(data):
    data['df']['tick']      = (data["df"]['Ask'] + data["df"]['Bid'])/2
    data['dt_val_series']   = [dt.datetime.strptime(x.split(".")[0],"%Y%m%d %H:%M:%S") for x in data["df"]['DateTime']]

    print('Building Sema...')
    data['df']['sema'] = data['df']['tick'].rolling(window=data['sema_len']).progress_apply(roll_ema)
    
    print('Building SLema...')
    data['df']['slema'] = data['df']['tick'].rolling(window=data['slema_len']).progress_apply(roll_ema)
    
    print('Building Lema...')
    data['df']['lema'] = data['df']['tick'].rolling(window=data['lema_len']).progress_apply(roll_ema)
    
    print('Building LLema...')
    data['df']['llema'] = data['df']['tick'].rolling(window=data['llema_len']).progress_apply(roll_ema)    
    data['df'] = data['df'].dropna()
    
    print('Building Angle...')
    data['df']['llema_angle'] = data['df']['llema'].rolling(window=data['angle_len']).progress_apply(roll_slope)
    data['df'] = data['df'].dropna()
    data['df'] = data['df'].reset_index(drop=True)        
    data['df_len'] = len(data["df"])
    return(data)
#...............................................................................................  

#...............................................................................................  
def get_rolling_emas(data):
    data['df'] = pd.read_csv(f'data/full_df.csv')
    data['dt_val_series']   = [dt.datetime.strptime(x.split(".")[0],"%Y%m%d %H:%M:%S") for x in data["df"]['DateTime']]
    # print('Building Angle...')
    # data['df']['llema_angle'] = data['df']['llema'].rolling(window=data['angle_len']).progress_apply(roll_slope)
    data['df'] = data['df'].dropna()
    data['df'] = data['df'].reset_index(drop=True)        
    data['df_len'] = len(data["df"])
    return(data)
#...............................................................................................  