from utils.packages import *
from utils.i_o import *
from utils.dir_slope import *



#...............................................................................................
def make_order(data):
    if not data['open_order']:
        if data['dir_change']:
            if data['to_order'] == 'long':
                data = make_long_order(data)

            elif data['to_order'] == 'short':
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

# ...............................................................................................
def simple_stop_loss(data):   
    data['stop_loss_pip']               = min(data['min_stop_loss_pip'], -data['h_l_gap'])

    if data['open_order']:
        if data['pl'] <= data['stop_loss_pip']:
            if data['open_order_type'] == 'long':
                data['stop_text'] = 'simple_stop'
                data = close_long_order(data)
                    
            if data['open_order_type'] == 'short':                
                data['stop_text'] = 'simple_stop'
                data = close_short_order(data)            
    return(data)   
# ...............................................................................................   


#...............................................................................................
def simple_take_profit(data):       
    data['pl_move_trail_trigger']       = max(data['min_take_profit_pip'], data['h_l_gap'] * 0.5)

    if data['open_order']:                        
        if data['pl'] >= data['pl_move_trail_trigger']:
            if data['open_order_type'] == 'long':
                data['stop_text'] = 'simple_take_profit'
                data = close_long_order(data)  

            if data['open_order_type'] == 'short':                
                data['stop_text'] = 'simple_take_profit'
                data = close_short_order(data)  
    
    return(data)    
#...............................................................................................


#...............................................................................................
def make_long_order(data):
    data['order_ask_price'] = data['ask']
    data['open_order'] = True
    data['slema_check_flag'] = True
    data['tick_check_flag'] = True
    data['open_order_type'] = 'long'
    data['start_dt_list'].append(data['dt_val'])
    data['reverse_order_flag'] =  'new'    
    data['take_profit_flag'] = False
    data['pl_positive'] = False
    data['pl_move_min'] = 0
    # data['ordered_llema_angle'] = round(data['llema_angle'])
    
    if data["plot"]:
        data['buy_markers_x'].append(data['i_list'][-1])
        data['buy_markers_y'].append(data['ask'])
    return(data)


def make_short_order(data):
    data['order_bid_price'] = data['bid']
    data['open_order'] = True
    data['slema_check_flag'] = True
    data['tick_check_flag'] = True
    data['open_order_type'] = 'short'
    data['start_dt_list'].append(data['dt_val'])
    data['reverse_order_flag'] =  'new'
    data['take_profit_flag'] = False
    data['pl_positive'] = False
    data['pl_move_min'] = 0
    # data['ordered_llema_angle'] = round(data['llema_angle'])

    if data["plot"]:
        data['buy_markers_x'].append(data['i_list'][-1])
        data['buy_markers_y'].append(data['bid'])
    return(data)


def close_long_order(data):
    data['pl_list'].append(data['pl'])
    data['start_price'].append(data['order_ask_price'])
    data['dt_list'].append(data['dt_val'])
    data['end_price'].append(data['bid'])
    data['num_orders'].append(1)
    data['open_order'] = False
    data['close_type'].append(data['stop_text'])
    data['ord_types'].append('long')
    # data['ll_angle'].append(data['ordered_llema_angle'])
    data['take_profit_flag'] = False
    
    if data["plot"]:
        data['sell_markers_x'].append(data['i_list'][-1])
        data['sell_markers_y'].append(data['bid'])   

    create_report(data)    
    return(data)


def close_short_order(data):
    data['pl_list'].append(data['pl'])
    data['start_price'].append(data['order_bid_price'])
    data['end_price'].append(data['ask'])
    data['num_orders'].append(1)
    data['dt_list'].append(data['dt_val'])
    data['open_order'] = False
    data['close_type'].append(data['stop_text'])
    data['ord_types'].append('short')
    # data['ll_angle'].append(data['ordered_llema_angle'])
    data['take_profit_flag'] = False
    
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