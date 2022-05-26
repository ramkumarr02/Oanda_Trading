from utils.packages import *


#...............................................................................................
def get_position(data):

    if data['sema'] == data['lema']:
        data['position'] = 0

    elif data['sema'] - data['lema'] >= 0.00001:
        data['position'] = 1

    elif data['lema'] - data['sema'] >= 0.00001:
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

#...............................................................................................
def delayed_start_check(data):
    if data['short_start']:
        if data['delay_counter'] < data['delay_tics_num']:
            data['delay_counter'] += 1
        else:
            data['to_order'] = 'short'
            data['dir_change'] = True 
    
    if data['long_start']:
        if data['delay_counter'] < data['delay_tics_num']:
            data['delay_counter'] += 1
        else:
            data['to_order'] = 'long'
            data['dir_change'] = True

    return(data)
#...............................................................................................


#...............................................................................................
def dir_switch_check(data):

    if data['direction'] == 'straight':
        if data['pos_1'] != data['pos_2'] and data['pos_2'] == -1:
            data['dir_change'] = True    
            data['short_start'] = True
            data['long_start'] = False
            data['delay_counter'] = 0

        elif data['pos_1'] != data['pos_2'] and data['pos_2'] == 1:
            data['dir_change'] = True    
            data['long_start'] = True
            data['short_start'] = False
            data['delay_counter'] = 0
        
        # else:
            # data['dir_change'] = False
            # data['short_start'] = False
            # data['long_start'] = False
            # data['sema_close_flag'] = False        

    #-------------------------

    if data['direction'] == 'reverse':
        if not data['open_order']:
            if data['pos_1'] != data['pos_2'] and data['pos_2'] == 1:
                data['dir_change'] = True    
                data['to_order'] = 'short'

            elif data['pos_1'] != data['pos_2'] and data['pos_2'] == -1:
                data['dir_change'] = True    
                data['to_order'] = 'long'   
            
            else:
                data['dir_change'] = False
                data['to_order'] = None
                data['sema_close_flag'] = False        


        if data['open_order']:
            if data['open_order_type'] == 'long':
                if data['pos_1'] != data['pos_2'] and data['pos_2'] == 1:
                    data['dir_change'] = True    
                    data['to_order'] = 'long'

                elif data['pos_1'] != data['pos_2'] and data['pos_2'] == -1:
                    data['dir_change'] = True    
                    data['to_order'] = 'short'   
                    
                else:
                    data['dir_change'] = False
                    data['to_order'] = None
                    data['sema_close_flag'] = False
            
            if data['open_order_type'] == 'short':    
                if data['pos_1'] != data['pos_2'] and data['pos_2'] == 1:
                    data['dir_change'] = True    
                    data['to_order'] = 'long'

                elif data['pos_1'] != data['pos_2'] and data['pos_2'] == -1:
                    data['dir_change'] = True    
                    data['to_order'] = 'short'   
                    
                else:
                    data['dir_change'] = False
                    data['to_order'] = None
                    data['sema_close_flag'] = False

    return(data)    

#...............................................................................................


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