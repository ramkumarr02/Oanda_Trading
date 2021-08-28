from utils.packages import *


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


# #...............................................................................................
# def get_position(data):
    
#     if data['sema'] > data['lema']:
#         if data['llema_angle'] > data['min_llema_angle'] and data['lema_angle'] > data['min_llema_angle'] and data['slema_angle'] > data['min_llema_angle'] and data['sema_angle'] > data['min_llema_angle'] and data['tick_angle'] > data['min_llema_angle']:
#         # if data['llema_angle'] > data['min_llema_angle']:
#             data['position'] = 1
#             data['dir_change'] = True    
#             data['to_order'] = 'long'        

#     elif data['sema'] < data['lema']:
#         if data['llema_angle'] < data['min_llema_angle'] and data['lema_angle'] < data['min_llema_angle'] and data['slema_angle'] < data['min_llema_angle'] and data['sema_angle'] < data['min_llema_angle'] and data['tick_angle'] < data['min_llema_angle']:
#         # if data['llema_angle'] < data['min_llema_angle']:
#             data['position'] = -1
#             data['dir_change'] = True    
#             data['to_order'] = 'short'

#     else:
#         data['position'] = 0
#         data['dir_change'] = False
#         data['to_order'] = None

#     return(data)
# #...............................................................................................


# #...............................................................................................
# def get_cross_dir(data):   
    
#     data['dir_list'].popleft()
#     data['dir_list'].append(data['position'])   
    
#     pos_1 = data['dir_list'][0]
#     pos_2 = data['dir_list'][1]
    
#     # if pos_2 == 1 and pos_2 != pos_1:
#     if pos_2 == 1:
#     # if pos_2 == 1 and data['llema_angle'] > data['min_llema_angle'] and data['lema_angle'] > data['min_llema_angle'] and data['slema_angle'] > data['min_llema_angle'] and data['sema_angle'] > data['min_llema_angle'] and data['tick_angle'] > data['min_llema_angle']:
#             data['dir_change'] = True    
#             data['to_order'] = 'long'        

#     if pos_2 == -1:
#     # elif pos_2 == -1 and data['llema_angle'] < data['min_llema_angle'] and data['lema_angle'] < data['min_llema_angle'] and data['slema_angle'] < data['min_llema_angle'] and data['sema_angle'] < data['min_llema_angle'] and data['tick_angle'] < data['min_llema_angle']:
#             data['dir_change'] = True    
#             data['to_order'] = 'short'
        
#     else:
#         data['dir_change'] = False
#         data['to_order'] = None

#     return(data)    
# #................................................................................................

#...............................................................................................
def get_cross_dir(data):   
    
    data['dir_list'].popleft()
    data['dir_list'].append(data['position'])   
    
    pos_1 = data['dir_list'][0]
    pos_2 = data['dir_list'][1]
    
    if pos_2 == 1 and pos_2 != pos_1:
        if data['llema_angle'] >= data['min_llema_angle']:
            data['dir_change'] = True    
            data['to_order'] = 'long'        

    if pos_2 == -1 and pos_2 != pos_1:
        if data['llema_angle'] <= -data['min_llema_angle']:
            data['dir_change'] = True    
            data['to_order'] = 'short'
        
    else:
        data['dir_change'] = False
        data['to_order'] = None

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