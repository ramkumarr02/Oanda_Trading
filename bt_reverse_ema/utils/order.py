from utils.packages import *
from utils.i_o import *


def order_dir_check(data):
    if not data['open_order']:
        if abs(data['ema_diff']) >= data['avg_ema_gap'] * data['gap_ratio']:
            if data['ema_diff'] < 0:
                    data['to_open'] = 'long'

            if data['ema_diff'] > 0:
                data['to_open'] = 'short'
    return(data)


#...............................................................................................
def make_order(data):
    if not data['open_order']:
        if data['to_open'] == 'long':
            data['order_ask_price'] = data['ask']
            data['open_order'] = True
            data['open_order_type'] = 'long'
            
            if data["plot"]:
                data['buy_markers_x'].append(data['i_list'][-1])
                data['buy_markers_y'].append(data['ask'])
                
        if data['to_open'] == 'short':
            data['order_bid_price'] = data['bid']
            data['open_order'] = True
            data['open_order_type'] = 'short'

            if data["plot"]:
                data['buy_markers_x'].append(data['i_list'][-1])
                data['buy_markers_y'].append(data['bid'])
                
    return(data)
#...............................................................................................




#...............................................................................................
def angle_close(data):
    if data['open_order']:
        if data['open_order_type'] == 'short':
            if data['sema_angle'] > data['close_angle']:
                data['close_ask_price'] = data['ask']
                data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 4)
                if data['pl'] >= data['angle_close_pip']:
                    data['pl_list'].append(data['pl'])
                    data['dt_list'].append(data['dt_val'])
                    data['open_order'] = False
                    data['close_type'].append('angle_close')
                    
                    if data["plot"]:
                        data['sell_markers_x'].append(data['i_list'][-1])
                        data['sell_markers_y'].append(data['ask'])  

                    create_report(data)
                
        if data['open_order_type'] == 'long':
            if data['sema_angle'] < -data['close_angle']:
                data['close_bid_price'] = data['bid']
                data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 4)
                if data['pl'] >= data['angle_close_pip']:
                    data['pl_list'].append(data['pl'])
                    data['dt_list'].append(data['dt_val'])
                    data['open_order'] = False
                    data['close_type'].append('angle_close')
                    
                    if data["plot"]:
                        data['sell_markers_x'].append(data['i_list'][-1])
                        data['sell_markers_y'].append(data['bid'])     

                    create_report(data)             
                
    return(data)    
#...............................................................................................



