from utils.packages import *


#...............................................................................................
def get_position(data):

    if data['sema'] > data['lema'] and data['slema'] > data['lema']:
        data['position'] = 1

    elif data['sema'] < data['lema'] and data['slema'] < data['lema']:
        data['position'] = -1

    else:
        data['position'] = 0
        # print('get pos 2')
        # sys.exit()
    
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
        # print('dirslope area 1')
        # sys.exit()

    elif pos_2 == -1 and pos_2 != pos_1:
        data['dir_change'] = True
        data['to_order'] = 'short'
        # print('dirslope area 2')
        # sys.exit()

    else:
        data['dir_change'] = False
        data['to_order'] = None

    return(data)    
#................................................................................................