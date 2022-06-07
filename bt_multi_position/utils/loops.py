from utils.packages import *
from utils.dir_slope import *
from utils.i_o import *


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
    # data = get_slope(data)            
    # ----------------------------------------------------------  
        
    return(data)
#............................................................................................... 

def roll_ema(ema_list):
    return(pd.DataFrame(ema_list).ewm(span=len(ema_list)).mean()[0].iloc[-1])

#...............................................................................................
def roll_slope(slope_list):
    
    slope_list = list(np.round(slope_list, 6))    
    slope_tick, _, _, _, _ = linregress(data['x_axis'], slope_list)
    slope = math.degrees(math.atan(slope_tick))

    return(slope)    
#...............................................................................................  

def get_x_axis(data):
    start = 1 + 1 * data['pip_decimal_num']
    stop = 1 + (data['angle_len']) * data['pip_decimal_num']
    data['x_axis'] = list(np.arange(start, stop, data['pip_decimal_num']).round(6))

    if len(data['x_axis']) < data['angle_len']:
        data['x_axis'].append(data['x_axis'][-1] + data['pip_decimal_num'])
    return(data)

#...............................................................................................  
def get_rolling_emas(data):

    data['df_name'] = f"data/ema_df-({data['start_date'].year}-{data['end_date'].year})-({data['start_date'].month}-{data['end_date'].month})-({data['start_date'].day}-{data['end_date'].day}).csv"

    if data['ema_roll_method'] == 'new':
        data = read_data(data)
        data['df']['tick']      = (data["df"]['Ask'] + data["df"]['Bid'])/2
        data['dt_val_series']   = [dt.datetime.strptime(x.split(".")[0],"%Y%m%d %H:%M:%S") for x in data["df"]['DateTime']]
        
        print('Building Lema...')
        data['df']['lema'] = data['df']['tick'].rolling(window=data['lema_len']).progress_apply(roll_ema)
        data['df'] = data['df'].dropna()
        send_telegram_message(f'Lema Complete : {data["df_name"]}')

        print('Building tick slope...')        
        data = get_x_axis(data)
        data['df']['tick_angle'] = data['df']['lema'].rolling(window=data['angle_len']).progress_apply(roll_slope)
        data['df'] = data['df'].dropna()   
        send_telegram_message(f'Slope Complete : {data["df_name"]}')

        print('Building SLema...')
        data['df']['slema'] = data['df']['tick'].rolling(window=data['slema_len']).progress_apply(roll_ema)
        data['df'] = data['df'].dropna()
        send_telegram_message(f'Slema Complete : {data["df_name"]}')
        
        print('Building Sema...')
        data['df']['sema'] = data['df']['tick'].rolling(window=data['sema_len']).progress_apply(roll_ema)
        data['df'] = data['df'].dropna()   
        send_telegram_message(f'Sema Complete : {data["df_name"]}')

        # print('Building lema slope...')        
        # data = get_x_axis(data)
        # data['df']['lema_angle'] = data['df']['lema'].rolling(window=data['angle_len']).progress_apply(roll_slope)
        # data['df'] = data['df'].dropna()   

        data['df'] = data['df'][['DateTime', 'Bid', 'Ask', 'tick', 'sema', 'slema', 'lema', 'tick_angle']].round(6)
        # data['df'] = data['df'][['DateTime', 'Bid', 'Ask', 'tick', 'sema', 'slema', 'lema']].round(6)
        data['df'] = data['df'].reset_index(drop=True) 
        data['df_len'] = len(data["df"])
        data['df'].to_csv(data['df_name'], index = False)

    # ---------------------------------------------------------------------------------------------------------------------

    elif data['ema_roll_method'] == 'file':
        data['df'] = pd.read_csv(f'data/ema_2021-jan_dec.csv')    
        # data['df'] = pd.read_csv(f'data/ema_df-(2021-2021)-(1-1)-(1-31).csv')    
        data["df"] = data["df"][data["df"]['DateTime'].str.contains('|'.join(data['date_list']))]
        print(f'Record num : {len(data["df"])}') 
        
        data['dt_val_series']   = [dt.datetime.strptime(x.split(".")[0],"%Y%m%d %H:%M:%S") for x in data["df"]['DateTime']]

        data['df'] = data['df'].reset_index(drop=True)        
        data['df_len'] = len(data["df"])

        data['df'] = data['df'][['DateTime', 'Bid', 'Ask', 'tick', 'sema', 'slema', 'lema', 'tick_angle']].round(6)

    # ---------------------------------------------------------------------------------------------------------------------

    elif data['ema_roll_method'] == 'mix':
        data['df'] = pd.read_csv(f'data/full_df_Jan_lemangle.csv')    
        data["df"] = data["df"][data["df"]['DateTime'].str.contains('|'.join(data['date_list']))]
        print(f'Record num : {len(data["df"])}') 
        
        data['dt_val_series']   = [dt.datetime.strptime(x.split(".")[0],"%Y%m%d %H:%M:%S") for x in data["df"]['DateTime']]

        print('Building tick slope...')        
        data = get_x_axis(data)
        data['df']['tick_angle'] = data['df']['lema'].rolling(window=data['angle_len']).progress_apply(roll_slope)
        data['df'] = data['df'].dropna() 

        data['df'] = data['df'].reset_index(drop=True)        
        data['df_len'] = len(data["df"])

        data['df'] = data['df'][['DateTime', 'Bid', 'Ask', 'tick', 'sema', 'slema', 'lema', 'tick_angle']].round(6) 

    return(data)
#...............................................................................................  

