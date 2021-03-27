from utils.packages import *



#...............................................................................................
def get_dir(data):
    
    if data['sema'] > data['lema']:
        data['position'] = 'above'

    elif data['sema'] < data['lema']:
        data['position'] = 'below'
    
    return(data)
#...............................................................................................



#...............................................................................................
def get_slope(data):
    pip_decimal_num = 6
    
    data['y_axis'] = list(np.round(data['y_axis'],pip_decimal_num))
    ma_len = len(data['y_axis'])
    
    x_axis = []
    for i in range(ma_len):
        x_axis.append(1 + ((i+1) * 10**(-pip_decimal_num)))
    
    slope_tick, intercept, _, _, _ = linregress(x_axis, data['y_axis'])
    data['angle'] = math.degrees(math.atan(slope_tick))

    if data["plot"]:
        data['angle_list'].append(data['angle'])
    
    return(data)    
#...............................................................................................    