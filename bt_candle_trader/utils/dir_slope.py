from utils.packages import *
from utils.order import *

#...............................................................................................
def get_candle_color(data):
    if data['dt_val'].minute % data['min_val'] == 0:

        if not data['open_val']:            
            if not data['close_val']:
                data['high_val']    = max(data['high_val'], data['tick'])
                data['low_val']     = min(data['low_val'], data['tick'])

                data['open_min'] = data['dt_val'].minute
                data['close_min'] = data['dt_val'].minute + data['min_val']
                if data['close_min'] == 60:
                    data['close_min'] = 0
                data['open_val'] = data['tick']

                print('-----------------------------------')
                print(f'Candle time : {data["dt_val"]}')    

        if data['open_val'] is not False:
            data['high_val']    = max(data['high_val'], data['tick'])
            data['low_val']     = min(data['low_val'], data['tick'])

            if not data['close_val']:           
                if data['dt_val'].minute == data['close_min']:
                    data['close_min_started'] = True
                    data['close_val'] = data['tick']
                    data['candle_size'] = data['close_val'] - data['open_val']
                    if data['candle_size'] > 0:
                        data['candle_color'] = 'green'
                    elif data['candle_size'] < 0:
                        data['candle_color'] = 'red'
                    
                    print('------------------------------------')
                    print(f"close_time : {data['dt_val']}")
                    print(f"high_val : {data['high_val']} ")                     
                    print(f"open_val : {data['open_val']} ")                     
                    print(f"close_val : {data['close_val']} ")                     
                    print(f"low_val : {data['low_val']} ")                                         
                    print(f'candle color : {data["candle_color"]}')
                    print(f'candle size : {data["candle_size"]}')
                    print('-----------------------------------')
                    # data['open_min']    = False
                    # data['close_min']   = False
                    data['open_val']    = False
                    data['close_val']   = False
                    data['close_min_started']   = False
                    data['high_val']   = 0
                    data['low_val']   = 100
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
#................................................................................................



#...............................................................................................
def get_slope(data, ma_type):
    
    data['y_axis'] = list(np.round(data['y_axis'],data['pip_decimal_num']))
    ma_len = len(data['y_axis'])
    
    x_axis = []
    for i in range(ma_len):
        x_axis.append(1 + ((i+1) * 10**(-data['pip_decimal_num'])))
    
    slope_tick, intercept, _, _, _ = linregress(x_axis, data['y_axis'])
    
    if ma_type == 'sema':
        data['sema_angle'] = math.degrees(math.atan(slope_tick))
        if data["plot"]:
            data['df_sema_angle_list'].append(data['sema_angle'])

    if ma_type == 'lema':
        data['lema_angle'] = math.degrees(math.atan(slope_tick))
        data['angle_diff'] = abs(data['sema_angle'] - data['lema_angle'])        
        if data["plot"]:
            data['df_lema_angle_list'].append(data['lema_angle'])
    return(data)    
#...............................................................................................    