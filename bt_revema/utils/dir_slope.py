from utils.packages import *


#...............................................................................................
def get_position(data):

    data['short'] = data['sema']
    data['long'] = data['lema']

    if data['short'] == data['long']:
        data['position'] = 0

    elif data['short'] - data['long'] >= 0.00001:
        data['position'] = 1

    elif data['long'] - data['short'] >= 0.00001:
        data['position'] = -1
    
    return(data)
#...............................................................................................

#...............................................................................................
def get_cross_dir(data):   
    
    data['dir_list'].popleft()
    data['dir_list'].append(data['position'])   
    
    data['pos_1'] = data['dir_list'][0]
    data['pos_2'] = data['dir_list'][1]

    data = dir_switch_check(data)

    return(data)    
#................................................................................................

def dir_switch_check(data):

    if not data['open_order']:
        if data['pos_1'] != data['pos_2'] and data['pos_2'] == -1 * data['dir_decider']:
            data['dir_change'] = True    
            data['to_order'] = 'short'

        elif data['pos_1'] != data['pos_2'] and data['pos_2'] == 1 * data['dir_decider']:
            data['dir_change'] = True    
            data['to_order'] = 'long'   
        
        else:
            data['dir_change'] = False
            data['to_order'] = None
            data['sema_close_flag'] = False        


    if data['open_order']:
        if data['open_order_type'] == 'long':
            if data['pos_1'] != data['pos_2'] and data['pos_2'] == -1 * data['dir_decider']:
                data['dir_change'] = True    
                data['to_order'] = 'long'

            elif data['pos_1'] != data['pos_2'] and data['pos_2'] == 1 * data['dir_decider']:
                data['dir_change'] = True    
                data['to_order'] = 'short'   
                
            else:
                data['dir_change'] = False
                data['to_order'] = None
                data['sema_close_flag'] = False
        
        if data['open_order_type'] == 'short':    
            if data['pos_1'] != data['pos_2'] and data['pos_2'] == -1 * data['dir_decider']:
                data['dir_change'] = True    
                data['to_order'] = 'long'

            elif data['pos_1'] != data['pos_2'] and data['pos_2'] == 1 * data['dir_decider']:
                data['dir_change'] = True    
                data['to_order'] = 'short'   
                
            else:
                data['dir_change'] = False
                data['to_order'] = None
                data['sema_close_flag'] = False
    return(data)    

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