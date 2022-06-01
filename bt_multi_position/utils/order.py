from utils.packages import *
from utils.i_o import *

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
                if data['orders_list'][1]['pl'] < 0:
                    data['open_order'] = 2
                    data = make_long_order(data)

        if data['open_order_type'] == 'long':
            if data['to_order'] == 'short':
                if data['orders_list'][1]['pl'] < 0:
                    data['open_order'] = 2
                    data = make_short_order(data)

    if data['open_order'] == 2:
        if data['open_order_type'] == 'short':
            if data['to_order'] == 'long':                
                if data['orders_list'][2]['pl'] < 0:
                    data['open_order'] = 3
                    data = make_long_order(data)

        if data['open_order_type'] == 'long':
            if data['to_order'] == 'short':
                if data['orders_list'][2]['pl'] < 0:
                    data['open_order'] = 3
                    data = make_short_order(data)

    if data['open_order'] == 3:
        if data['open_order_type'] == 'short':
            if data['to_order'] == 'long':                
                if data['orders_list'][3]['pl'] < 0:
                    data['open_order'] = 4
                    data = make_long_order(data)

        if data['open_order_type'] == 'long':
            if data['to_order'] == 'short':
                if data['orders_list'][3]['pl'] < 0:
                    data['open_order'] = 4
                    data = make_short_order(data)

    # if data['open_order'] == 2:
    #     if data['open_order_type'] == 'short':
    #         if data['to_order'] == 'long':                
    #             if data['orders_list'][2]['pl'] < 0:
    #                 data['open_order'] = 3
    #                 data = make_long_order(data)

    #     if data['open_order_type'] == 'long':
    #         if data['to_order'] == 'short':
    #             if data['orders_list'][2]['pl'] < 0:
    #                 data['open_order'] = 3
    #                 data = make_short_order(data)

    return(data)
#...............................................................................................

#...............................................................................................
def close_all_orders(data):

    if data['open_order'] > 1:
        if data['orders_list']['total_pl'] >= 0.0001:            
            for i in range(1, data['open_order']+1):
                if data['orders_list'][i]['open_order_type'] == 'long':   
                    data['pl'] = data['orders_list'][i]['pl']
                    data['close_type_val'] = ('all_close')
                    data = close_long_order(data)

                elif data['orders_list'][i]['open_order_type'] == 'short':
                    data['pl'] = data['orders_list'][i]['pl']
                    data['close_type_val'] = ('all_close')
                    data = close_short_order(data)

            data['open_order'] = 0

    return(data)
#...............................................................................................
def slema_positive_check(data):
    if data['open_order'] == 1:
        if data['slema_check_flag']:
            if data['orders_list'][1]['open_order_type'] == 'long':
                if data['sema'] > data['slema']:
                    data['slema_positive'] = True
                    data['slema_check_flag'] = False
                else:
                    data['slema_positive'] = False

            if data['orders_list'][1]['open_order_type'] == 'short':
                if data['sema'] < data['slema']:
                    data['slema_positive'] = True
                    data['slema_check_flag'] = False
                else:
                    data['slema_positive'] = False

    return(data)
#...............................................................................................


def simple_slema_move_close(data):
    if data['open_order'] == 1:
        if data['slema_positive']: 
            data['pl'] = data['orders_list'][1]['pl']
            if data['pl'] > 0:            
                if data['orders_list'][1]['open_order_type'] == 'long':
                    if data['sema'] < data['slema']:
                        data['close_type_val'] = ('simple_slema_move_close')
                        data = close_long_order(data)               
            
                if data['orders_list'][1]['open_order_type'] == 'short':
                    if data['sema'] > data['slema']:                
                        # data['stop_text'] = 'simple_slema_move_close'
                        data['close_type_val'] = ('simple_slema_move_close')
                        data = close_short_order(data)  

    return(data) 
#...............................................................................................
def calculate_pl(data):
    data['orders_list']['total_pl'] = []

    for i in range(1, data['open_order']+1):
        if i == 1:
            data['order_size'] = 1
        elif i == 2:
            data['order_size'] = 2
        elif i == 3:
            data['order_size'] = 3
        elif i == 4:
            data['order_size'] = 4

        if data['orders_list'][i]['open_order_type'] == 'long':
            data['orders_list'][i]['pl'] = np.round((data['bid'] - data['orders_list'][i]['ask']) * data['order_size'], 5)

        if data['orders_list'][i]['open_order_type'] == 'short':
            data['orders_list'][i]['pl'] = np.round((data['orders_list'][i]['bid'] - data['ask']) * data['order_size'], 5)

        data['orders_list']['total_pl'].append(data['orders_list'][i]['pl'])
    
    data['orders_list']['total_pl'] = np.round(sum(data['orders_list']['total_pl']), 5)

    return(data) 
#...............................................................................................

#...............................................................................................
def make_long_order(data):
    data['order_ask_price'] = data['ask']
    data['open_order_type'] = 'long'
    data['slema_check_flag'] = True
    data['orders_list'][data['open_order']] = {}
    data['orders_list'][data['open_order']]['open_order_type'] = data['open_order_type']
    data['orders_list'][data['open_order']]['ask'] = data['ask'] 
    # data['orders_list'][data['open_order']]['status'] = 'open'
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
    data['slema_check_flag'] = True
    data['orders_list'][data['open_order']] = {}
    data['orders_list'][data['open_order']]['open_order_type'] = data['open_order_type']
    data['orders_list'][data['open_order']]['bid'] = data['bid'] 
    # data['orders_list'][data['open_order']]['status'] = 'open'
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
    data['close_type'].append(data['close_type_val'])
    data['ord_types'].append('long')
    # data['ll_angle'].append(data['ordered_llema_angle'])
    # data['take_profit_flag'] = False
    # data['dir_change']	= False
    # data['orders_list'][data['open_order']]['status'] = 'closed' 
    data['open_order'] = 0
    data['slema_check_flag'] = False
    data['long_start']	= False
    data['short_start']	= False
    data['to_order']	= None
    data['delay_counter']	= 0
    
    if data["plot"]:
        data['sell_markers_x'].append(data['i_list'][-1])
        data['sell_markers_y'].append(data['bid'])   

    create_report(data)    
    return(data)


def close_short_order(data):
    data['pl_list'].append(data['pl'])
    data['dt_list'].append(data['dt_val'])
    data['close_type'].append(data['close_type_val'])
    data['ord_types'].append('short')
    # data['ll_angle'].append(data['ordered_llema_angle'])
    # data['take_profit_flag'] = False
    # data['dir_change']	= False
    # data['orders_list'][data['open_order']]['status'] = 'closed'
    data['open_order'] = 0
    data['slema_check_flag'] = False
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
def get_order_details(data):
    data['no_of_orders'] = len(list(data['orders_list'])[1:])
    last_key = list(data['orders_list'])[-1]
    data['last_order'] = data['orders_list'][last_key]
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