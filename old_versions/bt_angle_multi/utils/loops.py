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
    return(pd.Series(ema_list).ewm(span=len(ema_list)).mean().iloc[-1])

#...............................................................................................
def roll_slope(slope_list):
    
    slope_list = list(np.round(slope_list, 6))    
    slope_tick, _, _, _, _ = linregress(data['x_axis'], slope_list)
    slope = math.degrees(math.atan(slope_tick))

    return(slope)    
#...............................................................................................  

def get_x_axis(data):
    start = 1 + 1 * data['pip_decimal_num']
    stop = 1 + (data['curr_angle_len']) * data['pip_decimal_num']
    data['x_axis'] = list(np.arange(start, stop, data['pip_decimal_num']).round(6))

    if len(data['x_axis']) < data['curr_angle_len']:
        data['x_axis'].append(data['x_axis'][-1] + data['pip_decimal_num'])
    return(data)

#...............................................................................................  
def get_rolling_emas(data):

    data['df_name'] = f"data/ema_df-({data['start_date'].year}-{data['end_date'].year})-({data['start_date'].month}-{data['end_date'].month})-({data['start_date'].day}-{data['end_date'].day}).csv"

    if data['ema_roll_method'] == 'new':
        data = read_data(data)
        data['df']['tick']      = (data["df"]['Ask'] + data["df"]['Bid'])/2
        data['df']['DateTime_frmt']   = [dt.datetime.strptime(x.split(".")[0],"%Y%m%d %H:%M:%S") for x in data["df"]['DateTime']]
        
        print('Building Lema...')
        data['df']['lema'] = data['df']['tick'].rolling(window=data['lema_len']).progress_apply(roll_ema)
        data['df'] = data['df'].dropna()
        if data['send_message_to_phone']:
            send_telegram_message(f'Lema Complete : {data["df_name"]}')

        print('Building Slope...')
        data['curr_angle_len'] = data['angle_len']
        data = get_x_axis(data)
        data['df']['tick_angle'] = data['df']['tick'].rolling(window=data['angle_len']).progress_apply(roll_slope)
        data['df'] = data['df'].dropna()

        # print('Building Slope_2...')
        # data['curr_angle_len'] = data['angle_len_2']
        # data = get_x_axis(data)
        # data['df']['tick_angle_2'] = data['df']['tick'].rolling(window=data['angle_len_2']).progress_apply(roll_slope)
        # data['df'] = data['df'].dropna()

        print('Building slema...')
        data['df']['slema'] = data['df']['tick'].rolling(window=data['slema_len']).progress_apply(roll_ema)
        data['df'] = data['df'].dropna()
        if data['send_message_to_phone']:
            send_telegram_message(f'slema Complete : {data["df_name"]}')

        print('Building Sema...')
        data['df']['sema'] = data['df']['tick'].rolling(window=data['sema_len']).progress_apply(roll_ema)
        data['df'] = data['df'].dropna()
        if data['send_message_to_phone']:
            send_telegram_message(f'Sema Complete : {data["df_name"]}')

        data['df'] = data['df'].reset_index(drop=True) 
        print('Building H_L_Lema...')
        data = get_h_l_lema(data)
        # data = get_h_l_lema_2(data)

        # data['df'] = data['df'][data['columns_list']].round(6) 

        data['df'] = data['df'].reset_index(drop=True) 
        data['df_len'] = len(data["df"])
        if data['to_csv']:
            data['df'].to_csv(data['df_name'], index = False)

    # ---------------------------------------------------------------------------------------------------------------------

    elif data['ema_roll_method'] == 'file':
        data['df'] = pd.read_csv(f'data/{data["csv_file_name"]}.csv')    
        data['df']['DateTime_frmt']   = [dt.datetime.strptime(x.split(".")[0],"%Y-%m-%d %H:%M:%S") for x in data["df"]['DateTime_frmt']]
        data['df'] = data['df'][(data['df']['DateTime_frmt'] >= data['start_date']) & (data['df']['DateTime_frmt'] <= data['end_date'])]
        # data["df"] = data["df"][data["df"]['DateTime_frmt'].str.contains('|'.join(data['date_list']))]

        if data['df_subset_size'] is not None:
            data["df"] = data["df"][0:data['df_subset_size']]
            
        print(f'Record num : {len(data["df"])}') 
        
        
        data['df'] = data['df'].reset_index(drop=True)        
        data['df_len'] = len(data["df"])

        # data['df'] = data['df'][data['columns_list']].round(6) 

    # ---------------------------------------------------------------------------------------------------------------------

    elif data['ema_roll_method'] == 'mix':
        data['df'] = pd.read_csv(f'data/{data["csv_file_name"]}.csv')    
        data['df']['DateTime_frmt']   = [dt.datetime.strptime(x.split(".")[0],"%Y%m%d %H:%M:%S") for x in data["df"]['DateTime_frmt']]
        data['df'] = data['df'][(data['df']['DateTime_frmt'] > data['start_date']) & (data['df']['DateTime_frmt'] < data['end_date'])]
        # data["df"] = data["df"][data["df"]['DateTime_frmt'].str.contains('|'.join(data['date_list']))]

        if data['df_subset_size'] is not None:
            data["df"] = data["df"][0:data['df_subset_size']]

        data['df'] = data['df'].reset_index(drop=True)        
        print(f'Record num : {len(data["df"])}') 
        
        # data = get_hl(data)
        # data = get_avg_lines(data)  
        data = get_h_l_lema(data)

        # data['df'] = data['df'].dropna() 
        data['df'] = data['df'].reset_index(drop=True)        
        data['df_len'] = len(data["df"])

        # data['df'] = data['df'][data['columns_list']].round(6) 
        if data['to_csv']:
            data['df'].to_csv('data/temp.csv', index = False)

    print('EMA Rolling completed')
    return(data)
#...............................................................................................  

def get_h_l_lema(data):

    data['df']['h']         = np.nan
    data['df']['l']         = np.nan
    data['df']['h_l_gap']   = np.nan

    data['df']['h_gap']     = np.nan
    data['df']['l_gap']     = np.nan

    data['df']['h_lema']    = np.nan
    data['df']['l_lema']    = np.nan

    for i in tqdm(range(len(data['df']))):
        if i % data['candle_size'] == 0 and i > 0:        
            data['tick_list'] = data['df']['tick'].loc[i - data['candle_size'] : i-1]
            max_val     = max(data['tick_list'])
            min_val     = min(data['tick_list'])

            data['df']['h'].loc[i]  = max_val
            data['df']['l'].loc[i]  = min_val

            ind = data['df']['h'][data['df']['h'].notnull()].loc[i - data['candle_size'] * data['avg_candle_num'] + 1 : i].index
            data['df']['h_gap'].loc[i:i+data['candle_size']] = np.mean(data['df']['h'].loc[ind] - data['df']['lema'].loc[ind])
            data['df']['l_gap'].loc[i:i+data['candle_size']] = np.mean(data['df']['lema'].loc[ind] - data['df']['l'].loc[ind])

    data['df']['h_l_gap'] = data['df']['h_gap'] + data['df']['l_gap']
    data['df']['h_lema'] = data['df']['h_gap'] + data['df']['lema']
    data['df']['l_lema'] = data['df']['lema'] - data['df']['l_gap']

    #---------------------
    print('HL Created')
    
    del data['df']['h']
    del data['df']['l']
    del data['df']['h_gap']
    del data['df']['l_gap']
    # data['df'] = data['df'].round(6)
    # data['df'] = data['df'].dropna()
    # data['df'] = data['df'].reset_index(drop=True) 

    print('Avg HL Created')

    return(data)
#...............................................................................................  

def get_h_l_lema_2(data):
    
    data['df']['h']         = np.nan
    data['df']['l']         = np.nan
    data['df']['h_l_gap']   = np.nan

    data['df']['h_gap']     = np.nan
    data['df']['l_gap']     = np.nan

    data['df']['h_lema_2']    = np.nan
    data['df']['l_lema_2']    = np.nan

    for i in tqdm(range(len(data['df']))):
        if i % data['candle_size_2'] == 0 and i > 0:        
            data['tick_list'] = data['df']['tick'].loc[i - data['candle_size_2'] : i-1]
            max_val     = max(data['tick_list'])
            min_val     = min(data['tick_list'])

            data['df']['h'].loc[i]  = max_val
            data['df']['l'].loc[i]  = min_val

            ind = data['df']['h'][data['df']['h'].notnull()].loc[i - data['candle_size_2'] * data['avg_candle_num'] + 1 : i].index
            data['df']['h_gap'].loc[i:i+data['candle_size_2']] = np.mean(data['df']['h'].loc[ind] - data['df']['lema'].loc[ind])
            data['df']['l_gap'].loc[i:i+data['candle_size_2']] = np.mean(data['df']['lema'].loc[ind] - data['df']['l'].loc[ind])

    data['df']['h_l_gap'] = data['df']['h_gap'] + data['df']['l_gap']
    data['df']['h_lema_2'] = data['df']['h_gap'] + data['df']['lema']
    data['df']['l_lema_2'] = data['df']['lema'] - data['df']['l_gap']

    #---------------------
    print('HL Created')
    
    del data['df']['h']
    del data['df']['l']
    del data['df']['h_gap']
    del data['df']['l_gap']
    # data['df'] = data['df'].round(6)
    # data['df'] = data['df'].dropna()
    # data['df'] = data['df'].reset_index(drop=True) 

    print('Avg HL Created')

    return(data)
#...............................................................................................  