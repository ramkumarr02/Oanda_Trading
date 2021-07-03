from utils.packages import *
from utils.i_o import *


#...............................................................................................
def make_double_order(data):
    if not data['long_open_order'] and not data['short_open_order']:
        if data['dir_change']:
            data['long_order_ask_price'] = data['ask']
            data['long_open_order'] = True
            data['long_slema_check_flag'] = True
            data['order_long_position'] = data['position']
            
            if data["plot"]:
                data['long_buy_markers_x'].append(data['i_list'][-1])
                data['long_buy_markers_y'].append(data['ask'])
            
            data['short_order_bid_price'] = data['bid']
            data['short_open_order'] = True
            data['short_slema_check_flag'] = True
            data['order_short_position'] = data['position']

            if data["plot"]:
                data['short_buy_markers_x'].append(data['i_list'][-1])
                data['short_buy_markers_y'].append(data['bid'])

            data['reverse_order_flag'] = 'new'
                
    return(data)
#...............................................................................................

#...............................................................................................
def close_order(data):
    if data['long_open_order']:
        if data['position'] != -1 and data['order_long_position'] != data['position']:
            data['long_close_bid_price'] = data['bid']
            data['long_pl'] = np.round(data['long_close_bid_price'] - data['long_order_ask_price'], 5)
            data['long_open_order'] = False
            data['long_slema_check_flag'] = False
            data['pl_list'].append(data['long_pl'])
            data['dt_list'].append(data['dt_val'])
            data['close_type'].append('long_sema_close')
            data['ord_types'].append('long')

            if data["plot"]:
                data['long_sell_markers_x'].append(data['i_list'][-1])
                data['long_sell_markers_y'].append(data['bid'])      
            
            create_report(data)         
            
    if data['short_open_order']:
        if data['position'] != 1 and data['order_short_position'] != data['position']:
            data['short_close_ask_price'] = data['ask']
            data['short_pl'] = np.round(data['short_order_bid_price'] - data['short_close_ask_price'], 5)
            data['short_open_order'] = False
            data['short_slema_check_flag'] = False
            data['pl_list'].append(data['short_pl'])
            data['dt_list'].append(data['dt_val'])
            data['close_type'].append('short_sema_close')
            data['ord_types'].append('short')

            if data["plot"]:
                data['short_sell_markers_x'].append(data['i_list'][-1])
                data['short_sell_markers_y'].append(data['ask'])                  
            
            create_report(data)

    return(data)    
#...............................................................................................


#...............................................................................................
def slema_positive_check(data):
    if data['long_slema_check_flag']:
        if data['long_open_order']:
            if data['sema'] > data['slema']:
                data['long_slema_positive'] = True
                data['long_slema_check_flag'] = False
            else:
                data['long_slema_positive'] = False

    if data['short_slema_check_flag']:
        if data['short_open_order']:
            if data['sema'] < data['slema']:
                data['short_slema_positive'] = True
                data['short_slema_check_flag'] = False
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
                data['long_open_order'] = False
                data['pl_list'].append(data['long_pl'])
                data['dt_list'].append(data['dt_val'])
                data['close_type'].append('simple_slema_move_close')
                data['ord_types'].append('long')
        
                if data["plot"]:
                    data['long_sell_markers_x'].append(data['i_list'][-1])
                    data['long_sell_markers_y'].append(data['bid'])   

                create_report(data)               
    
    if data['short_open_order']:
        if data['short_slema_positive']:
            data['short_close_ask_price'] = data['ask']
            data['short_pl'] = np.round(data['short_order_bid_price'] - data['short_close_ask_price'], 5)

            if data['sema'] >= data['slema']:                
                data['short_open_order'] = False
                data['pl_list'].append(data['short_pl'])
                data['dt_list'].append(data['dt_val'])
                data['close_type'].append('simple_slema_move_close')
                data['ord_types'].append('short')
        
                if data["plot"]:
                    data['short_sell_markers_x'].append(data['i_list'][-1])
                    data['short_sell_markers_y'].append(data['ask'])  
        
                create_report(data)

    return(data)    
#...............................................................................................

#...............................................................................................
def stop_loss(data):

    if data['reverse_order_flag'] == 'new':
        data = reverse_stop_loss(data)
        
    elif data['reverse_order_flag'] == 'reversed':
        data = simple_stop_loss(data)

    return(data)
# ...............................................................................................

# ...............................................................................................
def simple_stop_loss(data):
    if data['long_open_order']:
        data['long_close_bid_price'] = data['bid']
        data['long_pl'] = np.round(data['long_close_bid_price'] - data['long_order_ask_price'], 5)

        if data['long_pl'] <= -data['stop_loss_pip']:
            data['long_open_order'] = False
            data['pl_list'].append(data['long_pl'])
            data['dt_list'].append(data['dt_val'])
            data['close_type'].append('simple_stop_loss')
            data['ord_types'].append('long')

            if data["plot"]:
                data['long_sell_markers_x'].append(data['i_list'][-1])
                data['long_sell_markers_y'].append(data['bid'])   

            create_report(data)               
                
    if data['short_open_order']:
        data['short_close_ask_price'] = data['ask']
        data['short_pl'] = np.round(data['short_order_bid_price'] - data['short_close_ask_price'], 5)

        if data['short_pl'] <= -data['stop_loss_pip']:
            data['short_open_order'] = False
            data['pl_list'].append(data['short_pl'])
            data['dt_list'].append(data['dt_val'])
            data['close_type'].append('simple_stop_loss')
            data['ord_types'].append('short')
            
            if data["plot"]:
                data['short_sell_markers_x'].append(data['i_list'][-1])
                data['short_sell_markers_y'].append(data['ask'])  
            
            create_report(data)

    return(data)   
# ...............................................................................................   


# ...............................................................................................
def reverse_stop_loss(data):
    if data['long_open_order']:
        data['long_close_bid_price'] = data['bid']
        data['long_pl'] = np.round(data['long_close_bid_price'] - data['long_order_ask_price'], 5)

        if data['long_pl'] <= -data['stop_loss_pip']:
            data['long_open_order'] = False
            data['pl_list'].append(data['long_pl'])
            data['dt_list'].append(data['dt_val'])
            data['close_type'].append('reverse_stop_loss')
            data['ord_types'].append('long')

            data['short_order_bid_price'] = data['bid']
            data['short_open_order'] = True
            data['short_slema_check_flag'] = True
            data['order_short_position'] = data['position']

            data['reverse_order_flag'] = 'reversed'

            if data["plot"]:
                data['long_sell_markers_x'].append(data['i_list'][-1])
                data['long_sell_markers_y'].append(data['bid'])   
                data['short_buy_markers_x'].append(data['i_list'][-1])
                data['short_buy_markers_y'].append(data['bid'])

            create_report(data)               
                
    if data['short_open_order']:
        data['short_close_ask_price'] = data['ask']
        data['short_pl'] = np.round(data['short_order_bid_price'] - data['short_close_ask_price'], 5)

        if data['short_pl'] <= -data['stop_loss_pip']:
            data['short_open_order'] = False
            data['pl_list'].append(data['short_pl'])
            data['dt_list'].append(data['dt_val'])
            data['close_type'].append('reverse_stop_loss')
            data['ord_types'].append('short')
            
            data['long_order_ask_price'] = data['ask']
            data['long_open_order'] = True
            data['long_slema_check_flag'] = True
            data['order_long_position'] = data['position']

            data['reverse_order_flag'] = 'reversed'

            if data["plot"]:
                data['short_sell_markers_x'].append(data['i_list'][-1])
                data['short_sell_markers_y'].append(data['ask'])  
                data['long_buy_markers_x'].append(data['i_list'][-1])
                data['long_buy_markers_y'].append(data['ask'])
            
            create_report(data)

    return(data)   
# ...............................................................................................   