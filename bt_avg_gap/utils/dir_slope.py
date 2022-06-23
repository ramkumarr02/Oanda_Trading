from utils.packages import *


#...............................................................................................
def get_position(data):
    
    if data['tick'] >= data['h_lema']:
        data['position'] = -1

    elif data['tick'] <= data['l_lema']:
        data['position'] = 1
    
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
        if data['h_l_gap'] > 0.0003:
            data['dir_change'] = True
            data['to_order'] = 'short'      

    elif data['pos_1'] != data['pos_2'] and data['pos_2'] == 1:
        if data['h_l_gap'] > 0.0003:
            data['dir_change'] = True    
            data['to_order'] = 'long'
        
    else:
        data['dir_change'] = False
        data['to_order'] = None

    return(data)    
#................................................................................................