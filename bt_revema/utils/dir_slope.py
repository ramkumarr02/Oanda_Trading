from utils.packages import *


#...............................................................................................
def get_position(data):

    data['short'] = data['sema']
    data['long'] = data['lema']

    if data['short'] == data['long']:
        data['position'] = 0

    elif data['short'] > data['long']:
        data['position'] = 1

    elif data['short'] < data['long']:
        data['position'] = -1
    
    return(data)
#...............................................................................................

#...............................................................................................
def get_cross_dir(data):   
    
    data['dir_list'].popleft()
    data['dir_list'].append(data['position'])   
    
    pos_1 = data['dir_list'][0]
    pos_2 = data['dir_list'][1]

    if not data['open_order']:
        if pos_1 != pos_2 and pos_2 == 1:
            data['dir_change'] = True    
            data['to_order'] = 'short'

        elif pos_1 != pos_2 and pos_2 == -1:
            data['dir_change'] = True    
            data['to_order'] = 'long'   
            
        else:
            data['dir_change'] = False
            data['to_order'] = None
            data['sema_close_flag'] = False

    # --- Profit Dir switch stopper ------------------------------------
    if data['open_order']:
        if data['open_order_type'] == 'long':
            if pos_1 != pos_2 and pos_2 == 1:
                data['dir_change'] = True    
                data['to_order'] = 'long'

            elif pos_1 != pos_2 and pos_2 == -1:
                data['dir_change'] = True    
                data['to_order'] = 'short'   
                
            else:
                data['dir_change'] = False
                data['to_order'] = None
                data['sema_close_flag'] = False
        
        if data['open_order_type'] == 'short':    
            if pos_1 != pos_2 and pos_2 == 1:
                data['dir_change'] = True    
                data['to_order'] = 'long'

            elif pos_1 != pos_2 and pos_2 == -1:
                data['dir_change'] = True    
                data['to_order'] = 'short'   
                
            else:
                data['dir_change'] = False
                data['to_order'] = None
                data['sema_close_flag'] = False
    # --- Profit Dir switch stopper ------------------------------------

    return(data)    
#................................................................................................


#...............................................................................................
def get_slope(data):
    
    data['y_axis'] = list(np.round(data['y_axis'],data['pip_decimal_num']))
    ma_len = len(data['y_axis'])
    
    x_axis = []
    for i in range(ma_len):
        x_axis.append(1 + ((i+1) * 10**(-data['pip_decimal_num'])))
    
    slope_tick, intercept, _, _, _ = linregress(x_axis, data['y_axis'])
    
    data['llema_angle'] = math.degrees(math.atan(slope_tick))        

    return(data)    
#...............................................................................................    