from utils.packages import *



#...............................................................................................
def get_dir(data):
    
    if data['sema'] > data['lema']:
        data['position'] = 1

    elif data['sema'] < data['lema']:
        data['position'] = -1
    
    return(data)
#...............................................................................................



#...............................................................................................
def after_dir(data):   
    
    data['dir_list'].popleft()
    data['dir_list'].append(data['position'])   
    
    if sum(data['dir_list']) != 0:
        data['dir_change'] = False

    elif sum(data['dir_list']) == 0:
        data['dir_change'] = True

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
    data['angle_list'].append(data['angle'])
    
    return(data)    
#...............................................................................................    