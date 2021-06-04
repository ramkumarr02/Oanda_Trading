from utils.packages import *



#...............................................................................................
def get_position(data):

    if data['sema'] == data['lema']:
        data['position'] = 0
        data['dir_change'] = False
        data['to_order'] = None

    elif data['sema'] > data['tick'] > data['lema']:
        if abs(data['ema_diff']) <= data['ema_order_gap']:
            if data['lema_angle'] < -data['lema_make_order_angle']:
                if data['sema_angle'] < -data['sema_make_order_angle']:
                    if data['tick_angle'] < -data['tick_make_order_angle']:
                        data['position'] = -1
                        data['dir_change'] = True
                        data['to_order'] = 'short'

    elif data['sema'] < data['tick'] < data['lema']:
        if abs(data['ema_diff']) <= data['ema_order_gap']:
            if data['lema_angle'] > data['lema_make_order_angle']:
                if data['sema_angle'] > data['sema_make_order_angle']:
                    if data['tick_angle'] > data['tick_make_order_angle']:
                        data['position'] = 1
                        data['dir_change'] = True    
                        data['to_order'] = 'long'
    
    return(data)
#...............................................................................................



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

    if ma_type == 'tick':
        data['tick_angle'] = math.degrees(math.atan(slope_tick))
        if data["plot"]:
            data['df_tick_angle_list'].append(data['tick_angle'])

    return(data)    
#...............................................................................................    