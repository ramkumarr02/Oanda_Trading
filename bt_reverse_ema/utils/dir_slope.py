from utils.packages import *


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
        if data["plot"]:
            data['df_lema_angle_list'].append(data['lema_angle'])

    return(data)    
#...............................................................................................    