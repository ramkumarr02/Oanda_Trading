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
    vol             = data['df_ohlc']['Volume'].resample(data['candle_size']).sum()
    ticks_in_candle = data['df_ohlc']['tick'].resample(data['candle_size']).count()

    ohlc = ohlc.join(vol)
    ohlc = ohlc.join(ticks_in_candle)

    ohlc = ohlc.dropna()
    data['df_ohlc'] = ohlc.reset_index()
    data['df_ohlc'] = data['df_ohlc'].rename(columns={'tick':'num_ticks'})

    data['df_ohlc']['candle_size'] = data['df_ohlc']['high'] - data['df_ohlc']['low']

    del ohlc
    del vol
    del ticks_in_candle

    data['df_ohlc']['dir'] = np.nan

    for i in tqdm(range(0,len(data['df_ohlc'])-1)):
        # open_tick = data['df_ohlc']['open'][i+1]    
        # high_tick = max(data['df_ohlc']['high'][i+1:i+1+data['num_fwd_candles']])
        # low_tick = min(data['df_ohlc']['low'][i+1:i+1+data['num_fwd_candles']])
        
        # up_range = high_tick - open_tick
        # down_range = open_tick - low_tick

        # data['min_pip_move'] = max(data['df_ohlc']['candle_size'][i], data['min_pip_target'])
        
        # if up_range > down_range:
        #     if up_range > data['min_pip_move']:
        #         data['df_ohlc']['dir'][i] = 'up'
        #     else:
        #         data['df_ohlc']['dir'][i] = 'no_dir'
                
        # elif up_range < down_range:
        #     if down_range > data['min_pip_move']:
        #         data['df_ohlc']['dir'][i] = 'down'
        #     else:
        #         data['df_ohlc']['dir'][i] = 'no_dir'

        # else:
        #     data['df_ohlc']['dir'][i] = 'no_dir'

        open_tick = data['df_ohlc']['open'][i+1] 
        close_tick = data['df_ohlc']['close'][i+1] 

        if open_tick > close_tick:
            data['df_ohlc']['dir'][i] = 'red'
        elif open_tick < close_tick:
            data['df_ohlc']['dir'][i] = 'green'

        
    # Split timestamp --------------------------------------------------------
    # data['df_ohlc']['year'] = data['df_ohlc']['DateTime_frmt'].dt.year
    # data['df_ohlc']['month'] = data['df_ohlc']['DateTime_frmt'].dt.month
    # data['df_ohlc']['day'] = data['df_ohlc']['DateTime_frmt'].dt.day
    data['df_ohlc']['weekday'] = data['df_ohlc']['DateTime_frmt'].dt.weekday
    data['df_ohlc']['hour'] = data['df_ohlc']['DateTime_frmt'].dt.hour
    data['df_ohlc']['min'] = data['df_ohlc']['DateTime_frmt'].dt.minute

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
    data['df_ohlc']['sema'] = talib.EMA(data['df_ohlc']['close'], timeperiod = data['sema_len'])

    # BBands --------------------------------------
    data['df_ohlc']['BBand_upper'], data['df_ohlc']['BBand_middle'], data['df_ohlc']['BBand_lower'] = talib.BBANDS(data['df_ohlc']['close'], timeperiod = data['sema_len'], nbdevup = 2, nbdevdn = 2, matype=0)

    data['df_ohlc']['green_candle'] = 0
    data['df_ohlc']['red_candle'] = 0
    data['df_ohlc'].loc[data['df_ohlc']['close'] > data['df_ohlc']['open'], 'green_candle'] = 1
    data['df_ohlc'].loc[data['df_ohlc']['open'] > data['df_ohlc']['close'], 'red_candle'] = 1

    data['df_ohlc']['lower_touch'] = 0
    data['df_ohlc']['middle_touch'] = 0
    data['df_ohlc']['high_touch'] = 0    
    data['df_ohlc'].loc[(data['df_ohlc']['high'] >= data['df_ohlc']['BBand_lower']) & (data['df_ohlc']['BBand_lower'] >= data['df_ohlc']['low']), 'lower_touch'] = 1
    data['df_ohlc'].loc[(data['df_ohlc']['high'] >= data['df_ohlc']['BBand_middle']) & (data['df_ohlc']['BBand_middle'] >= data['df_ohlc']['low']), 'middle_touch'] = 1
    data['df_ohlc'].loc[(data['df_ohlc']['high'] >= data['df_ohlc']['BBand_upper']) & (data['df_ohlc']['BBand_upper'] >= data['df_ohlc']['low']), 'high_touch'] = 1

    # HT Trendline --------------------------------------
    data['df_ohlc']['HT_trendline'] = talib.HT_TRENDLINE(data['df_ohlc']['close'])

    # Average Directional Movement Index --------------------------------------
    data['df_ohlc']['ADX'] = talib.ADX(data['df_ohlc']['high'], data['df_ohlc']['low'], data['df_ohlc']['close'], timeperiod = data['sema_len'])

    # Absolute Price Oscillator --------------------------------------
    data['df_ohlc']['APO'] = talib.APO(data['df_ohlc']['close'], fastperiod = data['sema_len'], slowperiod = data['lema_len'], matype=0)

    # cdl_hammer & Shooting star--------------------------------------
    data['df_ohlc']['cdl_hammer'] = talib.CDLHAMMER(data['df_ohlc']['open'], data['df_ohlc']['high'], data['df_ohlc']['low'], data['df_ohlc']['close'])
    data['df_ohlc']['cdl_shootingstar'] = talib.CDLSHOOTINGSTAR(data['df_ohlc']['open'], data['df_ohlc']['high'], data['df_ohlc']['low'], data['df_ohlc']['close'])

    # cdl_engulfing --------------------------------------
    data['df_ohlc']['cdl_engulfing'] = talib.CDLENGULFING(data['df_ohlc']['open'], data['df_ohlc']['high'], data['df_ohlc']['low'], data['df_ohlc']['close'])


    data['df_ohlc'] = data['df_ohlc'].reset_index(drop=True).round(6)  
    data['df_ohlc'] = data['df_ohlc'].round(6)  

    data['df_ohlc'] = data['df_ohlc'].dropna()
    data['df_ohlc'] = data['df_ohlc'].reset_index(drop=True) 

    print(f'Record num : {len(data["df_ohlc"])}')
    
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