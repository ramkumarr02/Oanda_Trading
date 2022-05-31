from utils.packages import *
from utils.i_o import *

# #...............................................................................................
# def make_order(data):
#     if not data['open_order']:
#         if data['to_order'] == 'long':                
#             data = make_long_order(data)

#         elif data['to_order'] == 'short':
#             data = make_short_order(data)

#     return(data)
# #...............................................................................................

#...............................................................................................
def make_order(data):
    if data['open_order'] == 0:
        if data['to_order'] == 'long':                
            data['open_order'] = 1
            data = make_long_order(data)

        elif data['to_order'] == 'short':
            data['open_order'] = 1
            data = make_short_order(data)

    if data['open_order'] == 1:
        if data['open_order_type'] == 'short':
            if data['to_order'] == 'long':                
                data['open_order'] = 2
                data = make_long_order(data)

        if data['open_order_type'] == 'long':
            if data['to_order'] == 'short':
                data['open_order'] = 2
                data = make_short_order(data)

    return(data)
#...............................................................................................


#...............................................................................................
def calculate_pl(data):
    if data['open_order_type'] == 'long':
        data['close_bid_price'] = data['bid']
        data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 5)

    if data['open_order_type'] == 'short':
        data['close_ask_price'] = data['ask']
        data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 5)
    
    return(data) 
#...............................................................................................

#...............................................................................................
def calculate_pl(data):
    for i in range(1, data['open_order']+1):
        if data['orders_list'][i]['open_order_type'] == 'long':
            data['close_bid_price'] = data['bid']
            data['orders_list'][data['open_order']]['pl'] = np.round(data['close_bid_price'] - data['orders_list'][i]['ask'], 5)

        if data['orders_list'][i]['open_order_type'] == 'short':
            data['close_ask_price'] = data['ask']
            data['orders_list'][data['open_order']]['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 5)
    
    return(data) 
#...............................................................................................

def make_long_order(data):
    data['order_ask_price'] = data['ask']
    data['open_order_type'] = 'long'
    data['orders_list'][data['open_order']] = {}
    data['orders_list'][data['open_order']]['open_order_type'] = data['open_order_type']
    data['orders_list'][data['open_order']]['ask'] = data['ask'] 
    data['long_start']	= False
    data['short_start']	= False
    data['to_order']	= None
    data['delay_counter']	= 0
    
    if data["plot"]:
        data['buy_markers_x'].append(data['i_list'][-1])
        data['buy_markers_y'].append(data['ask'])
    return(data)


def make_short_order(data):
    data['order_bid_price'] = data['bid']
    data['open_order_type'] = 'short'

    data['orders_list'][data['open_order']] = {}
    data['orders_list'][data['open_order']]['open_order_type'] = data['open_order_type']
    data['orders_list'][data['open_order']]['bid'] = data['bid'] 
    data['long_start']	= False
    data['short_start']	= False
    data['to_order']	= None
    data['delay_counter']	= 0

    if data["plot"]:
        data['buy_markers_x'].append(data['i_list'][-1])
        data['buy_markers_y'].append(data['bid'])
    return(data)


def close_long_order(data):
    data['pl_list'].append(data['pl'])
    data['dt_list'].append(data['dt_val'])
    data['open_order'] = False
    data['close_type'].append(data['stop_text'])
    data['ord_types'].append('long')
    # data['ll_angle'].append(data['ordered_llema_angle'])
    data['take_profit_flag'] = False
    data['dir_change']	= False
    data['long_start']	= False
    data['short_start']	= False
    data['delay_counter']	= 0
    data['to_order']	= None
    
    if data["plot"]:
        data['sell_markers_x'].append(data['i_list'][-1])
        data['sell_markers_y'].append(data['bid'])   

    create_report(data)    
    return(data)


def close_short_order(data):
    data['pl_list'].append(data['pl'])
    data['dt_list'].append(data['dt_val'])
    data['open_order'] = False
    data['close_type'].append(data['stop_text'])
    data['ord_types'].append('short')
    # data['ll_angle'].append(data['ordered_llema_angle'])
    data['take_profit_flag'] = False
    data['dir_change']	= False
    data['long_start']	= False
    data['short_start']	= False
    data['delay_counter']	= 0
    data['to_order']	= None
    
    if data["plot"]:
        data['sell_markers_x'].append(data['i_list'][-1])
        data['sell_markers_y'].append(data['ask'])  
    
    create_report(data)
    return(data)



#...............................................................................................
#...............................................................................................
#...............................................................................................
#...............................................................................................
#...............................................................................................
#...............................................................................................
#...............................................................................................
#...............................................................................................
#...............................................................................................