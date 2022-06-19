from utils.packages import *


#...............................................................................................
def get_position(data):
    
    if data['tick'] > data['sema'] > data['slema'] > data['lema']:
        if data['tick_angle'] > 0:
            data['position'] = 1

    elif data['tick'] < data['sema'] < data['slema'] < data['lema']:
        if data['tick_angle'] < 0:
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
        data['short_start'] = True
        data['long_start'] = False
        data['delay_counter'] = 0        

    elif data['pos_1'] != data['pos_2'] and data['pos_2'] == 1:
        data['long_start'] = True
        data['short_start'] = False
        data['delay_counter'] = 0

    return(data)    
#................................................................................................

#...............................................................................................
def delayed_start_check(data):
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

# def get_open_direction(data):
#     for i in data['orders_list']:
#         if type(i) == int:
#             if data['orders_list'][i]['status'] == 'open':
#                 data['open_direction'] = data['orders_list'][i]['open_order_type']
#                 data['open_direction_pl'] = data['orders_list'][i]['pl']
#                 data['open_direction_order'] = i
#                 print(data['open_direction'])
#                 print(data['open_direction_order'])
#                 break

#     return(data)
# #...............................................................................................