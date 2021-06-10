from utils.packages import *


#...............................................................................................
def get_candle_size(data):
    params = {"count": data['candle_count']+1, "granularity": data['candle_granularity']}
    candle_size_data = instruments.InstrumentsCandles(instrument="EUR_USD", params=params)
    data['candle_size_info'] = data["api"].request(candle_size_data)
    
    height_list = []
    for candle in data['candle_size_info']['candles']:
        if candle['complete']:
            height_list.append(np.float(candle['mid']['h']) - np.float(candle['mid']['l']))
    
    data['avg_ema_gap']         =   np.mean(height_list)
    
    data['candle_swing']        =   data['avg_ema_gap'] * data['gap_ratio']
    
    data['stop_loss_pip']       =   data['avg_ema_gap']
    data['trailing_stop_pip']   =   data['avg_ema_gap']
    
    # data['stop_loss_pip']       =   data['candle_swing'] * data['gap_ratio'] 
    # data['trailing_stop_pip']   =   data['candle_swing'] * data['gap_ratio']

    return(data)
#...............................................................................................


#...............................................................................................
def get_position(data):

    if data['sema'] == data['lema']:
        data['position'] = 0

    elif data['sema'] > data['lema']:
        data['position'] = 1

    elif data['sema'] < data['lema']:
        data['position'] = -1
    
    return(data)
#...............................................................................................





#...............................................................................................
def get_cross_dir(data):   
    
    data['dir_list'].popleft()
    data['dir_list'].append(data['position'])   
    
    pos_1 = data['dir_list'][0]
    pos_2 = data['dir_list'][1]
    
    if pos_2 == 1 and pos_2 != pos_1:
        data['dir_change'] = True    
        data['to_order'] = 'long'

    elif pos_2 == -1 and pos_2 != pos_1:
        data['dir_change'] = True
        data['to_order'] = 'short'

    else:
        data['dir_change'] = False
        data['to_order'] = None


    return(data)    
#...............................................................................................



#...............................................................................................
def get_slope(data, ma_type):
    data['pip_decimal_num'] = 6

    if ma_type =='sema':
        data['y_axis'] = list(data["sema_angle_list"])
    elif ma_type == 'lema':
        data['y_axis'] = list(data["lema_angle_list"])
    

    data['y_axis'] = list(np.round(data['y_axis'],data['pip_decimal_num']))
    ma_len = len(data['y_axis'])
    
    x_axis = []
    for i in range(ma_len):
        x_axis.append(1 + ((i+1) * 10**(-data['pip_decimal_num'])))
    
    slope_tick, intercept, _, _, _ = linregress(x_axis, data['y_axis'])
    

    if ma_type == 'sema':
        data['sema_angle'] = math.degrees(math.atan(slope_tick))
        data['sema_angle'] = np.round(data['sema_angle'],1)

    elif ma_type == 'lema':
        data['lema_angle'] = math.degrees(math.atan(slope_tick))
        data['lema_angle'] = np.round(data['lema_angle'],1)
    
    return(data)    
#...............................................................................................    



#...............................................................................................
def get_cushion_position(data):

    data['ema_gap'] = data['sema'] - data['lema']

    if abs(data['ema_gap']) <= data['gap_cushion'] * 0.1:
        data['position'] = 0

    elif data['ema_gap'] > data['gap_cushion']:
        data['position'] = 1

    elif data['ema_gap'] < -data['gap_cushion']:
        data['position'] = -1
    

    if data['sema'] == data['lema']:
        data['position_without_cushion'] = 0

    elif data['sema'] > data['lema']:
        data['position_without_cushion'] = 1

    elif data['sema'] < data['lema']:
        data['position_without_cushion'] = -1


    return(data)
#...............................................................................................