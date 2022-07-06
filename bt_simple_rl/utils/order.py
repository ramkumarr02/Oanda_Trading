from utils.packages import *
from utils.i_o import *
from utils.dir_slope import *



#...............................................................................................
def make_order(data):
    if not data['open_order']:
        if data['to_order'] == 'long':
            data = make_long_order(data)

        elif data['to_order'] == 'short':
            data = make_short_order(data)

        elif data['reverse'] == 'long':
            data = make_long_order(data)
            data['reverse'] = 'reversed'

        elif data['reverse'] == 'short':
            data = make_short_order(data)
            data['reverse'] = 'reversed'

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
def loss_reverse_position(data):   
    data['stop_loss_pip']               = min(data['min_stop_loss_pip'], -data['h_l_gap'] * 0.5)

    if data['reverse'] == None:
        if data['open_order']:
            if data['pl'] <= data['stop_loss_pip']:
                if data['open_order_type'] == 'long':
                    data['stop_text'] = 'reversed'
                    data = close_long_order(data)
                    data['reverse'] = 'short'
                        
                if data['open_order_type'] == 'short':                
                    data['stop_text'] = 'reversed'
                    data = close_short_order(data)            
                    data['reverse'] = 'long'            
    return(data)   
# ...............................................................................................   

# ...............................................................................................
def simple_stop_loss(data):   
    data['stop_loss_pip']               = min(data['min_stop_loss_pip'], -data['h_l_gap'] * data['stop_loss_multiplier'])

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

    data['pl_move_trail_trigger']       = max(data['min_take_profit_pip'], data['h_l_gap'] * data['take_profit_multiplier'])

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
def trail_take_profit(data):
    data['pl_move_trail_trigger']       = max(data['min_take_profit_pip'], data['h_l_gap'] * data['take_profit_multiplier'])

    if data['open_order']:
        if data['pl'] >= data['pl_move_trail_trigger']:
            data['pl_positive'] = True
            data['pl_move_min'] = max((data['pl'] * data['pl_move_trail_ratio']), data['pl_move_min'])

        if data['pl_positive']:    
            if 0 < data['pl'] <= data['pl_move_min']: 
                if data['open_order_type'] == 'long':
                    data['stop_text'] = 'pl_move_close'
                    data['to_order'] = None
                    data['pl_positive'] = False
                    data['pl_move_min'] = 0
                    data = close_long_order(data)             
                    
                if data['open_order_type'] == 'short':
                    data['stop_text'] = 'pl_move_close'
                    data['to_order'] = None
                    data['pl_positive'] = False
                    data['pl_move_min'] = 0
                    data = close_short_order(data)

    return(data)    
#...............................................................................................


#...............................................................................................
def lock_profit(data):
    data['safety_pip_level']       = -data['h_l_gap'] * 0.5

    if data['open_order']:
        if data['pl'] <= data['safety_pip_level']:
            data['pl_safety_reached'] = True

        if data['pl_safety_reached']:    
            if data['pl'] > 0: 
                if data['open_order_type'] == 'long':
                    data['stop_text'] = 'profit_lock_close'
                    data['to_order'] = None
                    data['pl_positive'] = False
                    data['pl_safety_reached'] = False
                    data = close_long_order(data)             
                    
                if data['open_order_type'] == 'short':
                    data['stop_text'] = 'profit_lock_close'
                    data['to_order'] = None
                    data['pl_positive'] = False
                    data['pl_safety_reached'] = False
                    data = close_short_order(data)

    return(data)    
#...............................................................................................


#...............................................................................................
def make_long_order(data):
    data['order_ask_price'] = data['ask']
    data['open_order'] = True
    data['open_order_type'] = 'long'
    data['pl_positive'] = False
    data['pl_safety_reached'] = False
    data['pl_move_min'] = 0
    data['reverse'] = None
    data['df']['order_side'].iloc[data['i']]    = 'long'
    data['df']['long_open'].iloc[data['i']]     = data['ask']
    data['ordered_touched_line']                = data['touched_line']
    data['df']['touched_line'].iloc[data['i']]  = data['ordered_touched_line']
    return(data)


def make_short_order(data):
    data['order_bid_price'] = data['bid']
    data['open_order'] = True
    data['open_order_type'] = 'short'
    data['pl_positive'] = False
    data['pl_safety_reached'] = False
    data['pl_move_min'] = 0
    data['reverse'] = None
    data['df']['order_side'].iloc[data['i']] = 'short'
    data['df']['short_open'].iloc[data['i']] = data['bid']
    data['ordered_touched_line']                = data['touched_line']
    data['df']['touched_line'].iloc[data['i']] = data['ordered_touched_line']
    return(data)


def close_long_order(data):
    data['open_order'] = False
    data['pl_positive'] = False
    data['pl_safety_reached'] = False
    data['pl_move_min'] = 0
    data['reverse'] = None
    data['df']['close_type'].iloc[data['i']] = data['stop_text']
    data['df']['long_close'].iloc[data['i']] = data['bid']  
    data['df']['pl'].iloc[data['i']] = data['pl']
    data['df']['order_side'].iloc[data['i']] = 'long'
    data['df']['touched_line'].iloc[data['i']]  = data['ordered_touched_line']
    create_report(data)
    return(data)


def close_short_order(data):
    data['open_order'] = False
    data['pl_positive'] = False
    data['pl_safety_reached'] = False
    data['pl_move_min'] = 0
    data['df']['close_type'].iloc[data['i']] = data['stop_text']
    data['df']['short_close'].iloc[data['i']] = data['ask']  
    data['df']['pl'].iloc[data['i']] = data['pl']
    data['df']['order_side'].iloc[data['i']] = 'short'
    data['df']['touched_line'].iloc[data['i']]  = data['ordered_touched_line']
    data['reverse'] = None
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