from utils.packages import *
from utils.dir_slope import *
from utils.i_o import *


#...............................................................................................  

def format_tick_time(data):
    
    data['df_name']             = f"data/ema_df-({data['start_date'].year}-{data['end_date'].year})-({data['start_date'].month}-{data['end_date'].month})-({data['start_date'].day}-{data['end_date'].day}).csv"
    data['df']['tick']          = (data["df"]['Ask'] + data["df"]['Bid'])/2
    data['df']['DateTime_frmt'] = [dt.datetime.strptime(x.split(".")[0],"%Y%m%d %H:%M:%S") for x in data["df"]['DateTime']]    

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
    data['df_ohlc']['lema'] = talib.EMA(data['df_ohlc']['close'], timeperiod = data['lema_len'])

    # Sema --------------------------------------
    data['df_ohlc']['slema'] = talib.EMA(data['df_ohlc']['close'], timeperiod = data['slema_len'])

    # Sema --------------------------------------
    data['df_ohlc']['sema'] = talib.EMA(data['df_ohlc']['close'], timeperiod = data['sema_len'])

    # BBands --------------------------------------
    data['df_ohlc']['BBand_upper'], data['df_ohlc']['BBand_middle'], data['df_ohlc']['BBand_lower'] = talib.BBANDS(data['df_ohlc']['close'], timeperiod = data['sema_len'], nbdevup = 2, nbdevdn = 2, matype=0)
    data['df_ohlc']['BBand_width'] = data['df_ohlc']['BBand_upper'] - data['df_ohlc']['BBand_lower']

    # BBands --------------------------------------
    data['df_ohlc']['sar'] = talib.SAR(data['df_ohlc']['high'], data['df_ohlc']['low'], acceleration=0.02, maximum=0.2)

    data['df_ohlc'].loc[data['df_ohlc']['sar'] < data['df_ohlc']['close'], 'sar_gap'] = data['df_ohlc']['close'] - data['df_ohlc']['sar']
    data['df_ohlc'].loc[data['df_ohlc']['sar'] > data['df_ohlc']['open'], 'sar_gap'] = data['df_ohlc']['sar'] - data['df_ohlc']['open']

    # data['df_ohlc']['sar_gap']      = abs(data['df_ohlc']['sar'] - data['df_ohlc']['close'])
    # data['df_ohlc']['avg_gap']      = data['df_ohlc'][['candle_size', 'sar_gap']].mean(axis=1)
    data['df_ohlc']['avg_gap']      = data['df_ohlc']['sar_gap']

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
def merge_ohlc_data(data):

    data['df'] = data['df'].drop(columns = ['Volume', 'DateTime' , 'i'])

    gap     = data['df_ohlc']['DateTime_frmt'][1] - data['df_ohlc']['DateTime_frmt'][0] - dt.timedelta(seconds=1)
    y       = data['df_ohlc']['DateTime_frmt'] + gap

    print('Merging OHLC data with full data ...')

    x       = data['df']['DateTime_frmt']

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

    data['df_ohlc']['DateTime_frmt'] = y

    data['df']  = data['df'].merge(data['df_ohlc'], how='left', on = 'DateTime_frmt')
    temp        = data['df'][~pd.isna(data['df']['open'])]
    temp        = temp[temp[['DateTime_frmt', 'open', 'high', 'low', 'close']].duplicated(keep = 'last')]
    dup_ind     = temp.index

    data['df'].loc[dup_ind, data['merge_col_names']] = np.nan
    
    data['df'].loc[data['df']['dir'] == 'up', 'up'] = data['df']['tick']    
    data['df'].loc[data['df']['dir'] == 'down', 'down'] = data['df']['tick']    

    # data['df'].loc[data['df']['up'].notnull(), 'up'] = data['df']['tick']    
    # data['df'].loc[data['df']['down'].notnull(), 'down'] = data['df']['tick']    
    # data['df'].loc[data['df']['up'].notnull(), 'dir'] = 'up'
    # data['df'].loc[data['df']['down'].notnull(), 'dir'] = 'down'

    data['df']  = data['df'].reset_index(drop=True) 

    # data['df'] = data['df'][data['cols']]

    data['df_len'] = len(data["df"])
    if data['to_csv']:
        data['df'].to_csv(data['df_name'], index = False) 

    # del data['df_ohlc']
    
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