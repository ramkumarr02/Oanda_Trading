from utils.packages import *
from utils.dir_slope import *
from utils.i_o import *


#...............................................................................................  

def format_tick_time(data):
    
    data['df_name']             = f"data/ema_df-({data['start_date'].year}-{data['end_date'].year})-({data['start_date'].month}-{data['end_date'].month})-({data['start_date'].day}-{data['end_date'].day}).csv"
    data['df']['tick']          = (data["df"]['Ask'] + data["df"]['Bid'])/2
    # data['df']['DateTime_frmt'] = [dt.datetime.strptime(x.split(".")[0],"%Y%m%d %H:%M:%S") for x in data["df"]['DateTime']]    
    data['df']['DateTime_frmt'] = pd.to_datetime(data['df']['DateTime'])

    print('format_tick_time : Completed')

    return(data)


#...............................................................................................  

def get_ohlc(data):
    data['df_ohlc'] = data['df'][['DateTime_frmt', 'tick', 'Volume']]
    data['df_ohlc'] = data['df_ohlc'].set_index('DateTime_frmt')

    ohlc            = data['df_ohlc']['tick'].resample(data['candle_size']).ohlc(_method='ohlc')
    
    ohlc = ohlc.dropna()
    data['df_ohlc'] = ohlc.reset_index()

    data['df_ohlc']['candle_size']  = data['df_ohlc']['high'] - data['df_ohlc']['low']    
    data['df_ohlc']['ask']          = data['df_ohlc']['close'] + (data['spread'] / 2)
    data['df_ohlc']['bid']          = data['df_ohlc']['close'] - (data['spread'] / 2)

    del ohlc

    print('get_ohlc         : completed')    
    if data['send_message_to_phone']:
        send_telegram_message(f'get_ohlc : Completed')    

    return(data)

#...............................................................................................  

#...............................................................................................  
def get_indicators(data):

    
    # Lema --------------------------------------
    data['df_ohlc']['lema']         = talib.EMA(data['df_ohlc']['close'], timeperiod = data['lema_len'])
    data['df_ohlc']['lema_angle']   = talib.LINEARREG_ANGLE(data['df_ohlc']['lema'], timeperiod = data['lema_len'])
    data['df_ohlc']['lema_angle_2'] = talib.LINEARREG_ANGLE(data['df_ohlc']['lema_angle'], timeperiod = data['lema_len'])
    # data['df_ohlc']['lema_angle']   = talib.LINEARREG_SLOPE(data['df_ohlc']['lema'], timeperiod = data['lema_len'])
    # data['df_ohlc']['lema_angle_2'] = talib.LINEARREG_SLOPE(data['df_ohlc']['lema_angle'], timeperiod = data['lema_len'])

    # Lema_angle_0 --------------------------------------
    data['df_ohlc'].loc[np.sign(data['df_ohlc']['lema_angle']).diff().ne(0), 'lema_angle_0'] = data['df_ohlc']['lema']
    data['df_ohlc']['lema_angle_0'] = data['df_ohlc']['lema_angle_0'].ffill()

    # Sema --------------------------------------
    data['df_ohlc']['slema'] = talib.EMA(data['df_ohlc']['close'], timeperiod = data['slema_len'])
    data['df_ohlc']['slema_angle']   = talib.LINEARREG_ANGLE(data['df_ohlc']['slema'], timeperiod = data['sema_len'])
    data['df_ohlc']['slema_angle_2'] = talib.LINEARREG_ANGLE(data['df_ohlc']['slema_angle'], timeperiod = data['sema_len'])

    # Sema --------------------------------------
    data['df_ohlc']['sema'] = talib.EMA(data['df_ohlc']['close'], timeperiod = data['sema_len'])
    data['df_ohlc']['sema_angle']   = talib.LINEARREG_ANGLE(data['df_ohlc']['sema'], timeperiod = data['sema_len'])
    data['df_ohlc']['sema_angle_2'] = talib.LINEARREG_ANGLE(data['df_ohlc']['sema_angle'], timeperiod = data['sema_len'])

    data['df_ohlc']['close_diff'] = data['df_ohlc']['sema'].diff(288).abs()

    # data['df_ohlc']['sema_lema_diff'] = data['df_ohlc']['sema'] - data['df_ohlc']['lema']
 
    # Mid Price --------------------------------------
    # data['df_ohlc']['sema_mp'] = talib.MIDPRICE(data['df_ohlc']['high'], data['df_ohlc']['low'], timeperiod = data['sema_len'])
    # data['df_ohlc']['slema_mp'] = talib.MIDPRICE(data['df_ohlc']['high'], data['df_ohlc']['low'], timeperiod = data['slema_len'])
    # data['df_ohlc']['lema_mp'] = talib.MIDPRICE(data['df_ohlc']['high'], data['df_ohlc']['low'], timeperiod = data['lema_len'])

    # data['df_ohlc']['lema_angle']   = pd.Series([math.degrees(math.atan(x)) for x in list(talib.LINEARREG_ANGLE(data['df_ohlc']['lema'], timeperiod = data['sema_len']))])
    # data['df_ohlc']['lema_angle_2'] = pd.Series([math.degrees(math.atan(x)) for x in list(talib.LINEARREG_ANGLE(data['df_ohlc']['lema_angle'], timeperiod = data['sema_len']))])
    # data['df_ohlc']['slema_angle']   = pd.Series([math.degrees(math.atan(x)) for x in list(talib.LINEARREG_ANGLE(data['df_ohlc']['slema'], timeperiod = data['sema_len']))])
    # data['df_ohlc']['slema_angle_2'] = pd.Series([math.degrees(math.atan(x)) for x in list(talib.LINEARREG_ANGLE(data['df_ohlc']['slema_angle'], timeperiod = data['sema_len']))])
    # data['df_ohlc']['sema_angle']   = pd.Series([math.degrees(math.atan(x)) for x in list(talib.LINEARREG_ANGLE(data['df_ohlc']['sema'], timeperiod = data['sema_len']))])
    # data['df_ohlc']['sema_angle_2'] = pd.Series([math.degrees(math.atan(x)) for x in list(talib.LINEARREG_ANGLE(data['df_ohlc']['sema_angle'], timeperiod = data['sema_len']))])


    # BBands --------------------------------------
    data['df_ohlc']['BBand_upper'], data['df_ohlc']['BBand_middle'], data['df_ohlc']['BBand_lower'] = talib.BBANDS(data['df_ohlc']['close'], timeperiod = data['sema_len'], nbdevup = 2, nbdevdn = 2, matype=0)
    data['df_ohlc']['BBand_width'] = data['df_ohlc']['BBand_upper'] - data['df_ohlc']['BBand_lower']    
    data['df_ohlc']['avg_BBand_width'] = talib.EMA(data['df_ohlc']['BBand_width'], timeperiod = data['sema_len'])


    # Lema rolling diff --------------------------------------
    # data['df_ohlc']['lema_diff'] = data['df_ohlc']['lema'].diff(periods=data['lema_len'])

    # # sar --------------------------------------
    # data['df_ohlc']['sar'] = talib.SAR(data['df_ohlc']['high'], data['df_ohlc']['low'], acceleration=0.02, maximum=0.2)

    # # RSI --------------------------------------
    # data['df_ohlc']['rsi'] = talib.RSI(data['df_ohlc']['lema'], timeperiod = data['lema_len'])

    # ADX --------------------------------------
    data['df_ohlc']['adx'] = talib.ADX(data['df_ohlc']['high'], data['df_ohlc']['low'], data['df_ohlc']['close'], timeperiod = data['lema_len'])

    # data['df_ohlc']['sar_gap'] = abs(data['df_ohlc']['sema'] - data['df_ohlc']['sar'])
    # data['df_ohlc'].loc[data['df_ohlc']['sar'] < data['df_ohlc']['close'], 'sar_gap'] = data['df_ohlc']['close'] - data['df_ohlc']['sar']
    # data['df_ohlc'].loc[data['df_ohlc']['sar'] > data['df_ohlc']['open'], 'sar_gap'] = data['df_ohlc']['sar'] - data['df_ohlc']['open']

    # data['df_ohlc']['sar_gap']      = abs(data['df_ohlc']['sar'] - data['df_ohlc']['close'])
    # data['df_ohlc']['avg_gap']      = data['df_ohlc'][['candle_size', 'sar_gap']].mean(axis=1)
    # data['df_ohlc']['avg_gap']      = data['df_ohlc']['sar_gap']

    data['df_ohlc'] = data['df_ohlc'].dropna()
    data['df_ohlc'] = data['df_ohlc'].reset_index(drop=True).round(6)                   


    data['df_len'] = len(data["df_ohlc"])
    print(f'Record num : {data["df_len"]}')
    
    if data['to_csv']:
        data['df_ohlc'].to_csv(data['df_name'], index = False) 

    print('get_tick_indicators  : Completed')    
    if data['send_message_to_phone']:
        send_telegram_message(f'get_tick_indicators : Completed')

    return(data)

#...............................................................................................  
def get_max_min_lema(data):

    temp = data['df_ohlc'][['DateTime_frmt', 'lema']]
    temp = temp.set_index('DateTime_frmt')

    max_temp = temp['lema'].resample(data['lema_min_max_duration']).max().reset_index()
    # max_temp['lema'] = max_temp['lema'].ewm(span = data['lema_min_max_span'], min_periods = 1).mean()
    max_temp = max_temp.rename(columns={'lema':'lema_max'})

    min_temp = temp['lema'].resample(data['lema_min_max_duration']).min().reset_index()
    # min_temp['lema'] = min_temp['lema'].ewm(span = data['lema_min_max_span'], min_periods = 1).mean()
    min_temp = min_temp.rename(columns={'lema':'lema_min'})

    temp = max_temp.merge(min_temp, on = 'DateTime_frmt')

    gap     = temp['DateTime_frmt'][1] - temp['DateTime_frmt'][0] - dt.timedelta(seconds=1)
    y       = temp['DateTime_frmt'] + gap

    print('Merging OHLC data with full data ...')

    x       = data['df_ohlc']['DateTime_frmt']


    for idx in tqdm(y.index):
        if idx == 0:
            temp_df = x[(x <= y[idx])][-1:]
            if len(temp_df) > 0:
                y[idx]      = temp_df.values[0]
                temp_start  = y[idx]

        else:
            temp_df = x[(temp_start < x) & (x <= y[idx])][-1:]
            if len(temp_df) > 0:
                y[idx]      = temp_df.values[0]
                temp_start  = y[idx]
                
    temp['DateTime_frmt'] = y

    data['df_ohlc']  = data['df_ohlc'].merge(temp, how='left', on = 'DateTime_frmt')
    temp        = data['df_ohlc'][~pd.isna(data['df_ohlc']['lema_max'])]
    temp        = temp[temp[['DateTime_frmt', 'lema_max']].duplicated(keep = 'last')]
    dup_ind     = temp.index

    data['df_ohlc'].loc[dup_ind, ['lema_max', 'lema_min']] = np.nan

    data['df_ohlc']  = data['df_ohlc'].reset_index(drop=True) 

    data['df_ohlc']['lema_max'] = data['df_ohlc']['lema_max'].ffill()
    data['df_ohlc']['lema_min'] = data['df_ohlc']['lema_min'].ffill()
    data['df_ohlc']['lema_gap'] = data['df_ohlc']['lema_max'] - data['df_ohlc']['lema_min'] 

    # Lema rolling diff --------------------------------------
    data['df_ohlc']['lema_diff'] = np.nan
    # # data['df_ohlc']['lema_diff'] = data['df_ohlc']['lema'] - data['df_ohlc']['lema_angle_0']
    # data['df_ohlc'].loc[data['df_ohlc']['lema'] > data['df_ohlc']['lema_max'], 'lema_diff'] = data['df_ohlc']['lema'] - data['df_ohlc']['lema_max']
    # data['df_ohlc'].loc[data['df_ohlc']['lema'] < data['df_ohlc']['lema_min'], 'lema_diff'] = data['df_ohlc']['lema_min'] - data['df_ohlc']['lema']   
    data['df_ohlc'].loc[data['df_ohlc']['lema'] > data['df_ohlc']['lema_max'], 'lema_diff'] = data['df_ohlc']['sema'] - data['df_ohlc']['lema_max']
    data['df_ohlc'].loc[data['df_ohlc']['lema'] < data['df_ohlc']['lema_min'], 'lema_diff'] = data['df_ohlc']['lema_min'] - data['df_ohlc']['sema']   


    # data['df_ohlc'].to_csv('data/temp.csv', index = False) 

    del temp
    
    return(data)

#...............................................................................................  

def capture_iterative_data(data):
    
    col_names = set(data['df_ohlc'].columns) - set(data['remove_list'])

    for col_name in col_names:
        data[col_name] = data['df_ohlc'][col_name][data['i']]

    return(data)

#...............................................................................................  

def get_tips(data):
    data["df_ohlc"]['tip'] = np.nan

    for i in tqdm(range(4,len(data['df_ohlc']))):
        if data['df_ohlc']['high'][i] < data['df_ohlc']['high'][i-1]:
            if data['df_ohlc']['high'][i-1] < data['df_ohlc']['high'][i-2]:
                if data['df_ohlc']['high'][i-2] > data['df_ohlc']['high'][i-3]:
                    if data['df_ohlc']['high'][i-3] > data['df_ohlc']['high'][i-4]:                
                        data["df_ohlc"]['tip'][i] = data['df_ohlc']['high'][i]

        if data['df_ohlc']['low'][i] > data['df_ohlc']['low'][i-1]:
            if data['df_ohlc']['low'][i-1] > data['df_ohlc']['low'][i-2]:
                if data['df_ohlc']['low'][i-2] < data['df_ohlc']['low'][i-3]:
                    if data['df_ohlc']['low'][i-3] < data['df_ohlc']['low'][i-4]:                
                        data["df_ohlc"]['tip'][i] = data['df_ohlc']['low'][i]

    return(data)

#...............................................................................................  

def get_tips(data):
    data["df_ohlc"]['tip'] = np.nan

    for i in tqdm(range(4,len(data['df_ohlc']))):
        if data['df_ohlc']['lema'][i] < data['df_ohlc']['lema'][i-1]:
            if data['df_ohlc']['lema'][i-1] < data['df_ohlc']['lema'][i-2]:
                if data['df_ohlc']['lema'][i-2] > data['df_ohlc']['lema'][i-3]:
                    if data['df_ohlc']['lema'][i-3] > data['df_ohlc']['lema'][i-4]:                
                        data["df_ohlc"]['tip'][i] = data['df_ohlc']['lema'][i]

        if data['df_ohlc']['lema'][i] > data['df_ohlc']['lema'][i-1]:
            if data['df_ohlc']['lema'][i-1] > data['df_ohlc']['lema'][i-2]:
                if data['df_ohlc']['lema'][i-2] < data['df_ohlc']['lema'][i-3]:
                    if data['df_ohlc']['lema'][i-3] < data['df_ohlc']['lema'][i-4]:                
                        data["df_ohlc"]['tip'][i] = data['df_ohlc']['lema'][i]

    return(data)
#...............................................................................................

def get_tips(data):
    data["df_ohlc"]['tip'] = np.nan

    for i in tqdm(range(4,len(data['df_ohlc']))):
        if data['df_ohlc']['lema'][i] < data['df_ohlc']['lema'][i-1]:
            if data['df_ohlc']['lema'][i-1] > data['df_ohlc']['lema'][i-2]:
                data["df_ohlc"]['tip'][i] = data['df_ohlc']['lema'][i]

        if data['df_ohlc']['lema'][i] < data['df_ohlc']['lema'][i-1]:
            if data['df_ohlc']['lema'][i-1] == data['df_ohlc']['lema'][i-2]:
                if data['df_ohlc']['lema'][i-2] > data['df_ohlc']['lema'][i-3]:
                    data["df_ohlc"]['tip'][i] = data['df_ohlc']['lema'][i]

        if data['df_ohlc']['lema'][i] > data['df_ohlc']['lema'][i-1]:
            if data['df_ohlc']['lema'][i-1] < data['df_ohlc']['lema'][i-2]:
                data["df_ohlc"]['tip'][i] = data['df_ohlc']['lema'][i]

        if data['df_ohlc']['lema'][i] > data['df_ohlc']['lema'][i-1]:
            if data['df_ohlc']['lema'][i-1] == data['df_ohlc']['lema'][i-2]:
                if data['df_ohlc']['lema'][i-2] < data['df_ohlc']['lema'][i-3]:
                    data["df_ohlc"]['tip'][i] = data['df_ohlc']['lema'][i]

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

def get_lema_pick_points(data):
    a = np.array(data['df_ohlc']['lema'].diff())

    a1 = np.sign(a)

    for i in tqdm(np.arange(1, len(a1))):
        if a1[i] == 0:        
            a1[i] = a1[i+1]

        if a1[i] != a1[i-1]:
            if a1[i+1] == a1[i-1]:
                a1[i] = a1[i-1]

    idx2 = []

    for i in np.arange(len(a1)-1):
        if i > 2:
            if a1[i-1] == a1[i-2]:
                if a1[i] == a1[i+1]:
                    if a1[i] != a1[i-1]:
                        idx2.append(i)

    idx2 = (np.array(idx2))
    
    data['df_ohlc']['lema_change'] = np.nan
    data['df_ohlc'].loc[idx2, 'lema_change'] = data['df_ohlc']['lema']
    
    return(data)

#...............................................................................................  

def get_returning_lema_points(data):
    data['df_ohlc']['lema_match'] = np.nan

    set2 = set(data['df_ohlc']['lema_change'][data['df_ohlc']['lema_change'].notnull()].index)

    for i in tqdm(np.arange(data['look_back_window_size'], len(data['df_ohlc']))):
        set1 = set(np.arange(i-data['look_back_window_size'],i))
        lema_tips = list(set1 & set2)

        if len(lema_tips) > 0:
            last_lema_tip = lema_tips[-1]
            idx = np.arange(i-data['look_back_window_size'], last_lema_tip+1)
            lema_list = data['df_ohlc']['lema'].loc[idx].round(4)

            if data['df_ohlc']['lema'][i].round(4) in set(lema_list):        
                data['df_ohlc']['lema_match'][i] = data['df_ohlc']['lema'][i]

    return(data)
#...............................................................................................  

# #...............................................................................................  
# def get_max_min_lema(data):

#     temp = data['df_ohlc'][['DateTime_frmt', 'close']]
#     temp = temp.set_index('DateTime_frmt')

#     max_temp = temp['close'].resample(data['lema_min_max_duration']).max().reset_index()
#     # max_temp['lema'] = max_temp['lema'].ewm(span = data['lema_min_max_span'], min_periods = 1).mean()
#     max_temp = max_temp.rename(columns={'close':'lema_max'})

#     min_temp = temp['close'].resample(data['lema_min_max_duration']).min().reset_index()
#     # min_temp['lema'] = min_temp['lema'].ewm(span = data['lema_min_max_span'], min_periods = 1).mean()
#     min_temp = min_temp.rename(columns={'close':'lema_min'})

#     temp = max_temp.merge(min_temp, on = 'DateTime_frmt')

#     gap     = temp['DateTime_frmt'][1] - temp['DateTime_frmt'][0] - dt.timedelta(seconds=1)
#     y       = temp['DateTime_frmt'] + gap

#     print('Merging OHLC data with full data ...')

#     x       = data['df_ohlc']['DateTime_frmt']


#     for idx in tqdm(y.index):
#         if idx == 0:
#             temp_df = x[(x <= y[idx])][-1:]
#             if len(temp_df) > 0:
#                 y[idx]      = temp_df.values[0]
#                 temp_start  = y[idx]

#         else:
#             temp_df = x[(temp_start < x) & (x <= y[idx])][-1:]
#             if len(temp_df) > 0:
#                 y[idx]      = temp_df.values[0]
#                 temp_start  = y[idx]
                
#     temp['DateTime_frmt'] = y

#     data['df_ohlc']  = data['df_ohlc'].merge(temp, how='left', on = 'DateTime_frmt')
#     temp        = data['df_ohlc'][~pd.isna(data['df_ohlc']['lema_max'])]
#     temp        = temp[temp[['DateTime_frmt', 'lema_max']].duplicated(keep = 'last')]
#     dup_ind     = temp.index

#     data['df_ohlc'].loc[dup_ind, ['lema_max', 'lema_min']] = np.nan

#     data['df_ohlc']  = data['df_ohlc'].reset_index(drop=True) 

#     data['df_ohlc']['lema_max'] = data['df_ohlc']['lema_max'].ffill()
#     data['df_ohlc']['lema_min'] = data['df_ohlc']['lema_min'].ffill()
#     data['df_ohlc']['lema_gap'] = data['df_ohlc']['lema_max'] - data['df_ohlc']['lema_min'] 

#     # Lema rolling diff --------------------------------------
#     data['df_ohlc']['lema_diff'] = np.nan
#     # data['df_ohlc']['lema_diff'] = data['df_ohlc']['lema'] - data['df_ohlc']['lema_angle_0']
#     # data['df_ohlc'].loc[data['df_ohlc']['lema'] > data['df_ohlc']['lema_max'], 'lema_diff'] = data['df_ohlc']['lema'] - data['df_ohlc']['lema_max']
#     # data['df_ohlc'].loc[data['df_ohlc']['lema'] < data['df_ohlc']['lema_min'], 'lema_diff'] = data['df_ohlc']['lema_min'] - data['df_ohlc']['lema']   
#     data['df_ohlc'].loc[data['df_ohlc']['lema'] > data['df_ohlc']['lema_max'], 'lema_diff'] = data['df_ohlc']['sema'] - data['df_ohlc']['lema_max']
#     data['df_ohlc'].loc[data['df_ohlc']['lema'] < data['df_ohlc']['lema_min'], 'lema_diff'] = data['df_ohlc']['lema_min'] - data['df_ohlc']['sema']   


#     # data['df_ohlc'].to_csv('data/temp.csv', index = False) 

#     del temp
    
#     return(data)

# #...............................................................................................  