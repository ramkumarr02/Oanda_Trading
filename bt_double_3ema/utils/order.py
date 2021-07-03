from utils.packages import *
from utils.i_o import *


#...............................................................................................
def make_double_order(data):
    if not data['open_order']:
        if data['dir_change']:
            
            data['long_order_ask_price'] = data['ask']
            data['long_open_order'] = True
            data['slema_check_flag'] = True
            data['ord_types'].append(data['long'])
            
            if data["plot"]:
                data['long_buy_markers_x'].append(data['i_list'][-1])
                data['long_buy_markers_y'].append(data['ask'])
            
            data['short_order_bid_price'] = data['bid']
            data['short_open_order'] = True
            data['slema_check_flag'] = True
            data['ord_types'].append(data['short'])

            if data["plot"]:
                data['short_buy_markers_x'].append(data['i_list'][-1])
                data['short_buy_markers_y'].append(data['bid'])
                
    return(data)
#...............................................................................................


#...............................................................................................
def slema_positive_check(data):
    if data['slema_check_flag']:
        if data['long_open_order']:
            if data['sema'] > data['slema']:
                data['long_slema_positive'] = True
                data['slema_check_flag'] = False
            else:
                data['long_slema_positive'] = False

        if data['short_open_order']:
            if data['sema'] < data['slema']:
                data['short_slema_positive'] = True
                data['slema_check_flag'] = False
            else:
                data['short_slema_positive'] = False

    return(data)
#...............................................................................................

def simple_slema_move_close(data):
    if data['long_open_order']:
        if data['long_slema_positive']: 
            data['long_close_bid_price'] = data['bid']
            data['long_pl'] = np.round(data['long_close_bid_price'] - data['long_order_ask_price'], 5)

            if data['sema'] <= data['slema']:
                data['pl_list'].append(data['long_pl'])
                data['dt_list'].append(data['dt_val'])
                data['long_open_order'] = False
                data['close_type'].append('simple_slema_move_close')
        
                if data["plot"]:
                    data['long_sell_markers_x'].append(data['i_list'][-1])
                    data['long_sell_markers_y'].append(data['bid'])   

                create_report(data)               
    
    if data['short_open_order']:
        if data['short_slema_positive']:
            data['short_close_ask_price'] = data['ask']
            data['short_pl'] = np.round(data['short_order_bid_price'] - data['short_close_ask_price'], 5)

            if data['sema'] >= data['slema']:                
                data['pl_list'].append(data['short_pl'])
                data['dt_list'].append(data['dt_val'])
                data['short_open_order'] = False
                data['close_type'].append('simple_slema_move_close')
        
                if data["plot"]:
                    data['short_sell_markers_x'].append(data['i_list'][-1])
                    data['short_sell_markers_y'].append(data['ask'])  
        
                create_report(data)

    return(data)    
#...............................................................................................