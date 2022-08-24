from utils.packages import *


def get_position(data):
    
    # if (data['BBand_width'] >= data['min_BBand_width']) & (data['close'] > data['lema']) & (data['close'] > data['sar']):
    # if (data['close'] > data['lema']) & (data['close'] > data['sar']):
    # if data['close'] > data['sar']:
    # if (data['close'] > data['sar']) & (data['close'] >= data['BBand_middle']):
    # if data['close'] > data['sar']:
    if data['sema'] > data['lema']:
        data['position'] = 1

    # elif (data['BBand_width'] >= data['min_BBand_width']) & (data['close'] < data['lema']) & (data['close'] < data['sar']):
    # elif (data['close'] < data['lema']) & (data['close'] < data['sar']):
    # elif data['close'] < data['sar']:
    # elif (data['close'] < data['sar']) & (data['close'] <= data['BBand_middle']):
    # elif data['close'] < data['sar']:
    elif data['sema'] < data['lema']:
        data['position'] = -1

    else:
        data['position'] = 0

    return(data)

#...............................................................................................

# def get_cross_dir(data):
#     data['dir_list'].popleft()
#     data['dir_list'].append(data['position'])   
    
#     data['pos_1'] = data['dir_list'][0]
#     data['pos_2'] = data['dir_list'][1]

#     if data['pos_1'] != data['pos_2'] and data['pos_2'] == -1:
#         # if data['high'] >= data['BBand_upper']:
#         # if data['BBand_width'] >= data['min_BBand_width']:
#         if data['close'] < data['lema']:
#             # if data['sema'] < data['slema']:
#             data['to_order'] = 'short'      
#             data["df_ohlc"]['cross'][data['i']] = data['close']

#     elif data['pos_1'] != data['pos_2'] and data['pos_2'] == 1:
#         # if data['low'] <= data['BBand_lower']:
#         # if data['BBand_width'] >= data['min_BBand_width']:
#         if data['close'] > data['lema']:
#             # if data['sema'] > data['slema']:
#             data['to_order'] = 'long'            
#             data["df_ohlc"]['cross'][data['i']] = data['close']

#     else:
#         data['to_order'] = None

#     return(data)
#...............................................................................................
def get_cross_dir(data):
    data['dir_list'].popleft()
    data['dir_list'].append(data['position'])   
    
    data['pos_1'] = data['dir_list'][0]
    data['pos_2'] = data['dir_list'][1]

    if data['pos_1'] != data['pos_2'] and data['pos_2'] == -1:
        data['to_order'] = 'short'      
        # data["df_ohlc"]['cross'][data['i']] = data['close']

    elif data['pos_1'] != data['pos_2'] and data['pos_2'] == 1:
        data['to_order'] = 'long'            
        # data["df_ohlc"]['cross'][data['i']] = data['close']

    else:
        data['to_order'] = None

    return(data)
#...............................................................................................

def get_lema_BBands_dir(data):
    
    data['to_order'] = None

    if data['BBand_upper'] > data['lema']:
        if data['BBand_middle'] > data['lema']:
            if data['BBand_lower'] > data['lema']:
                if data['sema'] > data['lema']:
                    if data['slema'] > data['lema']:
                        if data['lema_angle'] > data['min_lema_angle']:
                            if data['BBand_lower'] - data['lema'] >= data['min_pip_gap']:
                                data["df_ohlc"]['up'][data['i']] = data['close']
                                data['to_order'] = 'long'            

    if data['BBand_upper'] < data['lema']:
        if data['BBand_middle'] < data['lema']:
            if data['BBand_lower'] < data['lema']:
                if data['sema'] < data['lema']:
                    if data['slema'] < data['lema']:
                        if data['lema_angle'] < -data['min_lema_angle']:
                            if data['lema'] - data['BBand_upper'] >= data['min_pip_gap']:
                                data["df_ohlc"]['down'][data['i']] = data['close']
                                data['to_order'] = 'short'      

    return(data)
#...............................................................................................
def get_lema_gap_dir(data):
    
    data['to_order'] = None

    if data['sema'] > data['lema']:
        if data['slema'] > data['lema']:
            if (data['lema_angle'] > 0) & (data['lema_angle_2'] > 0):
                if (data['slema_angle'] > 0) & (data['slema_angle_2'] > 0):
                    if (data['sema_angle'] > 0) & (data['sema_angle_2'] > 0):
                        # if data['lema_diff'] > data['lema_gap'] / 2:
                        # if data['lema_diff'] > min(data['min_lema_diff'], data['lema_gap']):
                        # if data['lema_diff'] > data['min_lema_diff']:
                        if data['sema'] > data['lema_max']:
                            data["df_ohlc"]['up'][data['i']] = data['close']
                            data['to_order'] = 'long'            

    if data['sema'] < data['lema']:
        if data['slema'] < data['lema']:
            if (data['lema_angle'] < 0) & (data['lema_angle_2'] < 0):
                if (data['slema_angle'] < 0) & (data['slema_angle_2'] < 0):
                    if (data['sema_angle'] < 0) & (data['sema_angle_2'] < 0):
                        # if data['lema_diff'] > data['lema_gap'] / 2:
                        # if data['lema_diff'] > min(data['min_lema_diff'], data['lema_gap']):
                        # if data['lema_diff'] < -data['min_lema_diff']:
                        if data['sema'] < data['lema_min']:
                            data["df_ohlc"]['down'][data['i']] = data['close']
                            data['to_order'] = 'short'      

    return(data)
#...............................................................................................