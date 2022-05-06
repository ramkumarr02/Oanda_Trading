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
    
    # slope = np.round(math.degrees(math.atan(slope_tick)),0)
    slope = math.degrees(math.atan(slope_tick))

    return(slope)    
#...............................................................................................  


#...............................................................................................  
def get_rolling_emas(data):

    print('Building Lema...')
    data['df']['lema'] = data['df']['tick'].rolling(window=data['lema_len']).progress_apply(roll_ema)
    data['df'] = data['df'][data['lema_len']:]

    print('Building SLema...')
    data['df']['slema'] = data['df']['tick'].rolling(window=data['slema_len']).progress_apply(roll_ema)
    data['df'] = data['df'][data['slema_len']:]

    print('Building Sema...')
    data['df']['sema'] = data['df']['tick'].rolling(window=data['sema_len']).progress_apply(roll_ema)
    data['df'] = data['df'][data['sema_len']:]

    return(data)
#...............................................................................................  

#...............................................................................................  
def get_emas_from_file(data):
    # data['df'] = pd.read_csv(f'data/full_df_2020.csv')   

    if data['input_rows'] is None:
        data['df'] = pd.read_csv(f'data/full_df_2020.csv')
        print(len(data['df']))
    else:
        data['df'] = pd.read_csv(f'data/full_df_2020.csv', nrows=data['input_rows'])
        print(len(data['df']))
    
    data["df"] = data["df"][data["df"]['DateTime'].str.contains('|'.join(data['date_list']))]
    print(len(data['df']))
    
    data['dt_val_series']   = [dt.datetime.strptime(x.split(".")[0],"%Y%m%d %H:%M:%S") for x in data["df"]['DateTime']]

    data['df'] = data['df'].reset_index(drop=True)        
    data['df_len'] = len(data["df"])

    data['df'] = data['df'][['DateTime', 'Bid', 'Ask', 'tick', 'sema', 'lema', 'slema']].round(6)
    # data['df'].to_csv('data/full_df.csv', index = False)
    
    return(data)
#...............................................................................................  
def find_switch_points(data):
    data['df']['switch_point'] = 0
    data['switch_counter'] = 0

    data['temp_df'] = data['df'].reset_index()

    for i in np.arange(1, len(data['df'])):

        if data['temp_df']['sema'][i] > data['temp_df']['lema'][i]:
            if data['temp_df']['sema'][i-1] <= data['temp_df']['lema'][i-1]:
                data['switch_counter'] = data['switch_counter'] + 1        

        if data['temp_df']['sema'][i] < data['temp_df']['lema'][i]:
            if data['temp_df']['sema'][i-1] >= data['temp_df']['lema'][i-1]:
                data['switch_counter'] = data['switch_counter'] + 1

        data['df']['switch_point'][i] = data['switch_counter']

    del data['temp_df']
    
    return(data)
#...............................................................................................  
def get_trend_lines(data):
    data['df']['sno'] = np.arange(len(data['df']))
    
    for i in np.arange(1,data['num_lines']+1):
        high_line = f'h_line_{i}'
        low_line = f'l_line_{i}'
        data['df'][high_line] = np.nan
        data['df'][low_line] = np.nan

    data['df']['m'] = np.nan
    data['df']['b'] = np.nan
    line_count = 1

    data['temp_df'] = pd.DataFrame()
    data['temp_df']['m'] = np.nan
    data['temp_df']['b'] = np.nan

    for switch_point in list(set(data['df']['switch_point']))[-data['num_lines']:]:
        m = np.nan
        b = np.nan

        data['temp_df'] = data['df'][data['df']['switch_point'] == switch_point]

        x = data['temp_df']['sno'][data['temp_df']['h'].notnull()].values
        y = data['temp_df']['h'][data['temp_df']['h'].notnull()].values

        if len(x) == 0:
            continue
        else:
            m, b = np.polyfit(x = x, y = y, deg = 1)

        data['df']['m'][data['df']['switch_point'] == switch_point] = m
        data['df']['b'][data['df']['switch_point'] == switch_point] = b

        for ind in data['df'][data['df']['switch_point'] >= switch_point].index:
            data['df'][f'h_line_{line_count}'].loc[ind] = m * (data['df']['sno'].loc[ind]) + b

        line_count = line_count + 1


    #----------------------------------------------------------    

    data['df']['m'] = np.nan
    data['df']['b'] = np.nan

    data['temp_df'] = pd.DataFrame()
    data['temp_df']['m'] = np.nan
    data['temp_df']['b'] = np.nan
    line_count = 1

    for switch_point in list(set(data['df']['switch_point']))[-data['num_lines']:]:
        m = np.nan
        b = np.nan

        data['temp_df'] = data['df'][data['df']['switch_point'] == switch_point]

        x = data['temp_df']['sno'][data['temp_df']['l'].notnull()].values
        y = data['temp_df']['l'][data['temp_df']['l'].notnull()].values

        if len(x) == 0:
            continue
        else:
            m, b = np.polyfit(x = x, y = y, deg = 1)

        data['df']['m'][data['df']['switch_point'] == switch_point] = m
        data['df']['b'][data['df']['switch_point'] == switch_point] = b

        for ind in data['df'][data['df']['switch_point'] >= switch_point].index:
            data['df'][f'l_line_{line_count}'].loc[ind] = m * (data['df']['sno'].loc[ind]) + b

        line_count = line_count + 1
        
    return(data)
#...............................................................................................  