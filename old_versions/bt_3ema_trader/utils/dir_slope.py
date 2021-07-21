from utils.packages import *


# #...............................................................................................
# def get_position(data):

#     if data['sema'] == data['lema']:
#         data['position'] = 0

#     elif data['sema'] > data['lema']:
#         data['position'] = 1 * data['direction_flag']

#     elif data['sema'] < data['lema']:
#         data['position'] = -1 * data['direction_flag']
    
#     return(data)
# #...............................................................................................


#...............................................................................................
def get_position(data):

    if abs(data['sema'] - data['lema']) < data['sema_gap_pip']:
        data['position'] = 0

    elif data['sema'] - data['lema'] >= data['sema_gap_pip']:
        data['position'] = 1 * data['direction_flag']

    elif data['sema'] - data['lema'] <= -data['sema_gap_pip']:
        data['position'] = -1 * data['direction_flag']
    
    return(data)
#...............................................................................................



#...............................................................................................
def get_cross_dir(data):   
    
    data['dir_list'].popleft()
    data['dir_list'].append(data['position'])   
    
    pos_1 = data['dir_list'][0]
    pos_2 = data['dir_list'][1]
    
    if pos_2 == 1 and pos_2 != pos_1:
        data['dir_change'] = True    
        data['to_order'] = 'long'

    elif pos_2 == -1 and pos_2 != pos_1:
        data['dir_change'] = True
        data['to_order'] = 'short'

    else:
        data['dir_change'] = False
        data['to_order'] = None

    return(data)    
#................................................................................................