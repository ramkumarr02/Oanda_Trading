from utils.packages import *


#...............................................................................................
def get_position(data):

    if data['tick'] > data['sema'] > data['slema'] > data['lema']:
        data['position'] = 1

    elif data['tick'] < data['sema'] < data['slema'] < data['lema']:
        data['position'] = -1
    
    else:
        data['position'] = 0

    return(data)
#...............................................................................................


#...............................................................................................
def get_cross_dir(data):   
    
    data['dir_list'].popleft()
    data['dir_list'].append(data['position'])   
    
    data['pos_1'] = data['dir_list'][0]
    data['pos_2'] = data['dir_list'][1]

    if data['pos_1'] != data['pos_2'] and data['pos_2'] == -1:
        # if data['open_order'] == 0:
        if data['tick_angle'] < 0:
            data['short_start'] = True
            data['long_start'] = False
            data['delay_counter'] = 0
        # else:
        #     data['to_order'] = 'short'
        

    elif data['pos_1'] != data['pos_2'] and data['pos_2'] == 1:
        # if data['open_order'] == 0:
        if data['tick_angle'] > 0:
            data['long_start'] = True
            data['short_start'] = False
            data['delay_counter'] = 0
        # else:
        #     data['to_order'] = 'long'

    return(data)    
#................................................................................................

#...............................................................................................
def after_order_get_position(data):

    if data['open_order'] != 0:
        if data['sema'] > data['slema']:            
            data['after_order_position'] = 1

        elif data['sema'] < data['slema']:
            data['after_order_position'] = -1
        
        else:
            data['after_order_position'] = 0

    return(data)
#...............................................................................................

#...............................................................................................
def after_order_get_cross_dir(data):   
    
    if data['open_order'] != 0:
        data['after_order_dir_list'].popleft()
        data['after_order_dir_list'].append(data['after_order_position'])   
        
        data['pos_1'] = data['after_order_dir_list'][0]
        data['pos_2'] = data['after_order_dir_list'][1]

        if data['pos_1'] != data['pos_2'] and data['pos_2'] == -1:            
            if data['last_order']['pl'] < 0:
                data['to_order'] = 'short'
                data['long_start'] = False
                data['delay_counter'] = 0

        elif data['pos_1'] != data['pos_2'] and data['pos_2'] == 1:
            if data['last_order']['pl'] < 0:
                data['to_order'] = 'long'
                data['short_start'] = False
                data['delay_counter'] = 0

    return(data)    
#................................................................................................

#...............................................................................................
def delayed_start_check(data):
    # if data['open_order'] == 0:
    if data['short_start']:
        if data['delay_counter'] < data['delay_tics_num']:
            if data['tick'] < data['sema'] < data['slema'] < data['lema']:
                data['delay_counter'] += 1
            else:
                data['delay_counter'] = 0
        else:
            data['to_order'] = 'short'
    
    if data['long_start']:
        if data['delay_counter'] < data['delay_tics_num']:
            if data['tick'] > data['sema'] > data['slema'] > data['lema']:
                data['delay_counter'] += 1
            else:
                data['delay_counter'] = 0
        else:
            data['to_order'] = 'long'              

    return(data)
#...............................................................................................