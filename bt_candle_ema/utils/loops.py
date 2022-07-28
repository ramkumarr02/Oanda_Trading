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
        
        # print('Building Lema...')
        # data['df']['lema'] = talib.EMA(data['df']['tick'], timeperiod = data['lema_len'])
        # data['df'] = data['df'].dropna()
        # if data['send_message_to_phone']:
        #     send_telegram_message(f'Lema Complete : {data["df_name"]}')

        print('Building slema...')
        data['df']['slema'] = talib.EMA(data['df']['tick'], timeperiod = data['slema_len'])
        data['df'] = data['df'].dropna()
        if data['send_message_to_phone']:
            send_telegram_message(f'slema Complete : {data["df_name"]}')

        print('Building Sema...')
        data['df']['sema'] = talib.EMA(data['df']['tick'], timeperiod = data['sema_len'])
        data['df'] = data['df'].dropna()
        if data['send_message_to_phone']:
            send_telegram_message(f'Sema Complete : {data["df_name"]}')

        data['df'] = data['df'].reset_index(drop=True).round(6)  
        data['df'] = data['df'].round(6)  

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

    print('EMA Rolling completed')
    return(data)
#...............................................................................................  

def get_ohlc(data):
    data['df_ohlc'] = data['df'][['DateTime_frmt', 'tick']]
    data['df_ohlc'] = data['df_ohlc'].set_index('DateTime_frmt')
    data['df_ohlc'] = data['df_ohlc'].resample(data['candle_size']).ohlc(_method='ohlc')

    col_names = [col[1] for col in data['df_ohlc'].columns.values]
    col_names.insert(0,'DateTime_frmt')
    data['df_ohlc'] = pd.DataFrame(data['df_ohlc'].to_records())
    data['df_ohlc'].columns = col_names

    data['df_ohlc']['ind_candle_size'] = data['df_ohlc']['high'] - data['df_ohlc']['low']

    return(data)
#...............................................................................................  

def get_cdl_hammer_sstar(data):
    data['df_ohlc']['cdl_hammer'] = talib.CDLHAMMER(data['df_ohlc']['open'], data['df_ohlc']['high'], data['df_ohlc']['low'], data['df_ohlc']['close'])
    data['df_ohlc']['cdl_hammer'] = data['df_ohlc']['cdl_hammer'].replace({0:np.nan})
    data['df_ohlc']['cdl_hammer'] = np.where(data['df_ohlc']['cdl_hammer'] == 100, data['df_ohlc']['close'], data['df_ohlc']['cdl_hammer'])

    data['df_ohlc']['cdl_shootingstar'] = talib.CDLSHOOTINGSTAR(data['df_ohlc']['open'], data['df_ohlc']['high'], data['df_ohlc']['low'], data['df_ohlc']['close'])
    data['df_ohlc']['cdl_shootingstar'] = data['df_ohlc']['cdl_shootingstar'].replace({0:np.nan})
    data['df_ohlc']['cdl_shootingstar'] = np.where(data['df_ohlc']['cdl_shootingstar'] == -100, data['df_ohlc']['close'], data['df_ohlc']['cdl_shootingstar'])

    return(data)

#...............................................................................................  

#...............................................................................................  

def get_cdl_engulfing(data):
    data['df_ohlc']['cdl_engulfing'] = talib.CDLENGULFING(data['df_ohlc']['open'], data['df_ohlc']['high'], data['df_ohlc']['low'], data['df_ohlc']['close'])

    data['df_ohlc']['cdl_engulfing_up'] = data['df_ohlc']['cdl_engulfing'][data['df_ohlc']['cdl_engulfing'] == 100]
    data['df_ohlc']['cdl_engulfing_down'] = data['df_ohlc']['cdl_engulfing'][data['df_ohlc']['cdl_engulfing'] == -100]

    data['df_ohlc']['cdl_engulfing_up'] = data['df_ohlc']['cdl_engulfing_up'].replace({0:np.nan})
    data['df_ohlc']['cdl_engulfing_up'] = np.where(data['df_ohlc']['cdl_engulfing_up'] == 100, data['df_ohlc']['close'], data['df_ohlc']['cdl_engulfing_up'])

    data['df_ohlc']['cdl_engulfing_down'] = data['df_ohlc']['cdl_engulfing_down'].replace({0:np.nan})
    data['df_ohlc']['cdl_engulfing_down'] = np.where(data['df_ohlc']['cdl_engulfing_down'] == -100, data['df_ohlc']['close'], data['df_ohlc']['cdl_engulfing_down'])

    del data['df_ohlc']['cdl_engulfing'] 

    return(data)

#...............................................................................................  

#...............................................................................................  
# def merge_ohlc_data(data):

#     for col_name in data['merge_col_names']:
#         data['df'][col_name]          = np.nan

#     for i in tqdm(range(len(data['df_ohlc']['DateTime_frmt']))):
#         if i == 0:
#             time_gap = data['df_ohlc']['DateTime_frmt'][i+1] - data['df_ohlc']['DateTime_frmt'][i]

#         filter_time = data['df_ohlc']['DateTime_frmt'][i] + time_gap
#         df_rows = data['df'][data['df']['DateTime_frmt'] < filter_time]
#         if len(df_rows) > 0:
#             max_row = max(df_rows.index)
            
#             for col_name in data['merge_col_names']:
#                 data['df'][col_name][max_row] = data['df_ohlc'][col_name][i]

#     data['df'] = data['df'].reset_index(drop=True) 
#     data['df_len'] = len(data["df"])
#     if data['to_csv']:
#         data['df'].to_csv(data['df_name'], index = False) 

#     # del data['df_ohlc']
    
#     return(data)
#...............................................................................................  

#...............................................................................................  
def merge_ohlc_data(data):

    gap = data['df_ohlc']['DateTime_frmt'][1] - data['df_ohlc']['DateTime_frmt'][0] - dt.timedelta(seconds=1)
    y = data['df_ohlc']['DateTime_frmt'] + gap

    print('Merging OHLC data with full data ...')

    x = data['df']['DateTime_frmt']

    for idx in tqdm(y.index):
        # df_rows = x[x <= y[idx]]
        # if len(df_rows) > 0:
        # max_row = max(x[x <= y[idx]].index)
        y[idx] = x[max(x[x <= y[idx]].index)]


    data['df_ohlc']['DateTime_frmt'] = y

    data['df'] = data['df'].merge(data['df_ohlc'], how='left', on = 'DateTime_frmt')
    temp = data['df'][~pd.isna(data['df']['open'])]
    temp = temp[temp[['DateTime_frmt', 'open', 'high', 'low', 'close']].duplicated(keep = 'last')]
    dup_ind = temp.index
    # data['df'].loc[dup_ind, ['open', 'high', 'low', 'close']] = np.nan
    data['df'].loc[dup_ind, data['merge_col_names']] = np.nan

    data['df'] = data['df'].reset_index(drop=True) 
    data['df_len'] = len(data["df"])
    if data['to_csv']:
        data['df'].to_csv(data['df_name'], index = False) 

    # del data['df_ohlc']
    
    return(data)
#...............................................................................................  

def capture_iterative_data(data):
    data['bid']                 = data["df"]['Bid'][data['i']]        
    data['ask']                 = data["df"]['Ask'][data['i']]
    data['tick']                = data['df']['tick'][data['i']]        
    data['sema']                = data['df']['sema'][data['i']]    
    data['slema']               = data['df']['slema'][data['i']]    
    data['lema']                = data['df']['lema'][data['i']]    
    # data['open']                = data['df']['open'][data['i']]    
    # data['high']                = data['df']['high'][data['i']]    
    # data['low']                 = data['df']['low'][data['i']]    
    data['close']               = data['df']['close'][data['i']]    
    data['cdl_engulfing_up']    = data['df']['cdl_engulfing_up'][data['i']]    
    data['cdl_engulfing_down']  = data['df']['cdl_engulfing_down'][data['i']]   
    if not pd.isna(data['df']['ind_candle_size'][data['i']]):
        data['min_stop_loss_pip']  = -data['df']['ind_candle_size'][data['i']]    
    return(data)

#...............................................................................................  