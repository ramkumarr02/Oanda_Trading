from utils.packages import *


def get_position(data):
    
    # if (data['BBand_width'] >= data['min_BBand_width']) & (data['close'] > data['lema']) & (data['close'] > data['sar']):
    # if (data['close'] > data['lema']) & (data['close'] > data['sar']):
    # if data['close'] > data['sar']:
    # if (data['close'] > data['sar']) & (data['close'] >= data['BBand_middle']):
    if data['close'] > data['sar']:
        data['position'] = 1

    # elif (data['BBand_width'] >= data['min_BBand_width']) & (data['close'] < data['lema']) & (data['close'] < data['sar']):
    # elif (data['close'] < data['lema']) & (data['close'] < data['sar']):
    # elif data['close'] < data['sar']:
    # elif (data['close'] < data['sar']) & (data['close'] <= data['BBand_middle']):
    elif data['close'] < data['sar']:
        data['position'] = -1

    else:
        data['position'] = 0

    return(data)

#...............................................................................................

def get_cross_dir(data):
    data['dir_list'].popleft()
    data['dir_list'].append(data['position'])   
    
    data['pos_1'] = data['dir_list'][0]
    data['pos_2'] = data['dir_list'][1]

    if data['pos_1'] != data['pos_2'] and data['pos_2'] == -1:
        # if data['high'] >= data['BBand_upper']:
        # if data['BBand_width'] >= data['min_BBand_width']:
        # if data['close'] < data['lema']:
        if data['sema'] < data['slema']:
            data['to_order'] = 'short'      
            data["df_ohlc"]['cross'][data['i']] = data['close']

    elif data['pos_1'] != data['pos_2'] and data['pos_2'] == 1:
        # if data['low'] <= data['BBand_lower']:
        # if data['BBand_width'] >= data['min_BBand_width']:
        # if data['close'] > data['lema']:
        if data['sema'] > data['slema']:
            data['to_order'] = 'long'            
            data["df_ohlc"]['cross'][data['i']] = data['close']

    else:
        data['to_order'] = None

    return(data)
#...............................................................................................
