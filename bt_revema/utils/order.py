from utils.packages import *
from utils.i_o import *


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

def stop_loss(data):
    if data['stop_loss_method'] == 'simple':
        data = simple_stop_loss(data)

    elif data['stop_loss_method'] == 'trail':
        data = pl_negative_check(data)
        data = pl_loss_close(data)
        # data = simple_stop_loss(data)
        
    return(data)  

# ...............................................................................................
def simple_stop_loss(data):
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
def pl_negative_check(data):
    if data['open_order']:
        if not data['negative_hit_limit']:    
            if data['pl'] <= data['pl_loss_trail_trigger']:
                data['negative_hit_limit'] = True                
                data['pl_loss_min'] = max((data['pl'] * data['pl_loss_trail_size']), data['pl_loss_min'])
        
        if data['negative_hit_limit']:                
            if data['pl'] > data['pl_loss_trail_trigger']:
                data['pl_negative'] = True
                data['pl_loss_min'] = max((data['pl'] * data['pl_loss_trail_size']), data['pl_loss_min'])

    return(data)
#...............................................................................................

#...............................................................................................
def pl_loss_close(data):
    if data['open_order']:
        if data['pl_negative']:
            if 0 > data['pl'] > data['pl_loss_min']: 
                data['negative_hit_limit']  = False
                data['pl_negative']         = False
                data['pl_loss_min']         = -100
                data['to_order']            = None
                data['stop_text']           = 'pl_loss_close'

                if data['open_order_type'] == 'long':
                    data = close_long_order(data)             
                    
                if data['open_order_type'] == 'short':
                    data = close_short_order(data) 

    return(data)    
#...............................................................................................    

def tick_close(data):
    if data['open_order']:
        if data['open_order_type'] == 'long':
            if data['pl'] > 0:
                if data['tick'] < data['sema'] and data['tick'] < data['slema'] and data['tick'] < data['lema']:
                    data['stop_text'] = 'tick_close'
                    data = close_long_order(data)  

        if data['open_order_type'] == 'short':
            if data['pl'] > 0:
                if data['tick'] > data['sema'] and data['tick'] > data['slema'] and data['tick'] > data['lema']:
                    data['stop_text'] = 'tick_close'
                    data = close_short_order(data)  

    return(data)

#...............................................................................................    


def take_profit(data):
    if data['take_profit_method'] == 'simple':
        data = simple_take_profit(data)

    elif data['take_profit_method'] == 'trail':
        data = pl_positive_check(data)
        data = pl_move_close(data)
        
    return(data)    

#...............................................................................................
def simple_take_profit(data):       
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
def pl_positive_check(data):
    if data['open_order']:
        if data['pl'] >= data['pl_move_trail_trigger']:
            data['pl_positive'] = True
            data['pl_move_min'] = max((data['pl'] * data['pl_move_trail_ratio']), data['pl_move_min'])

    return(data)

#...............................................................................................

def pl_move_close(data):
    if data['open_order']:
        if data['pl_positive']:    
            if 0 < data['pl'] <= data['pl_move_min']: 
                data['stop_text'] = 'pl_move_close'
                data['to_order'] = None
                data['pl_positive'] = False
                data['pl_move_min'] = 0

                if data['open_order_type'] == 'long':
                    data = close_long_order(data)             
                    
                if data['open_order_type'] == 'short':
                    data = close_short_order(data)

    return(data)    
#...............................................................................................


#...............................................................................................
def slema_positive_check(data):
    if data['slema_check_flag']:
        if data['open_order']:
            if data['open_order_type'] == 'long':
                if data['sema'] > data['slema']:
                    data['slema_positive'] = True
                    data['slema_check_flag'] = False
                else:
                    data['slema_positive'] = False

            if data['open_order_type'] == 'short':
                if data['sema'] < data['slema']:
                    data['slema_positive'] = True
                    data['slema_check_flag'] = False
                else:
                    data['slema_positive'] = False

    return(data)
#...............................................................................................


def simple_slema_move_close(data):
    if data['open_order']:
        if data['slema_positive']: 
            # if data['pl'] > 0:            
                if data['open_order_type'] == 'long':
                    if data['sema'] < data['slema']:
                        data['stop_text'] = 'simple_slema_move_close'
                        data = close_long_order(data)               
            
                if data['open_order_type'] == 'short':
                    if data['sema'] > data['slema']:                
                        data['stop_text'] = 'simple_slema_move_close'
                        data = close_short_order(data)  

    return(data)    
#...............................................................................................

def sema_close(data):
    if data['open_order']:
        if data['dir_change']:
            if data['open_order_type'] == 'long':
                if data['to_order'] == 'short':
                    data['stop_text'] = 'sema_close'
                    data = close_long_order(data)
                
            if data['open_order_type'] == 'short':
                if data['to_order'] == 'long':
                    data['stop_text'] = 'sema_close'
                    data = close_short_order(data)

    return(data) 

#...............................................................................................  

def reverse_order_position(data):
    if data['open_order']:
        if data['dir_change']:
            if data['open_order_type'] == 'long':
                if data['to_order'] == 'short':
                    data['stop_text'] = 'sema_close'
                    data = reverse_order(data)
                
            if data['open_order_type'] == 'short':
                if data['to_order'] == 'long':
                    data['stop_text'] = 'sema_close'
                    data = reverse_order(data)

    return(data)  

#...............................................................................................

def make_long_order(data):
    data['order_ask_price'] = data['ask']
    data['open_order'] = True
    data['slema_check_flag'] = True
    data['open_order_type'] = 'long'
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
    data['open_order_type'] = 'short'
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
    data['dt_list'].append(data['dt_val'])
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
def slema_move_close(data):
    if data['reverse_order_flag'] == 'new':
        data = slema_move_close_reverse(data)
        
    elif data['reverse_order_flag'] == 'reversed':
        data = simple_slema_move_close(data)
    return(data)
#...............................................................................................

def slema_move_close_reverse(data):
    if data['open_order']:
        if data['slema_positive']: 
            if data['pl'] > 0:

                if data['open_order_type'] == 'long':            
                    if data['sema'] <= data['slema']:
                        data['stop_text'] = 'reverse_slema_move_close'
                        data = reverse_order(data)
                        data['reverse_order_flag'] =  'reversed'
                        return(data)
                    
                if data['open_order_type'] == 'short':
                    if data['sema'] >= data['slema']:
                        data['stop_text'] = 'reverse_slema_move_close'
                        data = reverse_order(data)
                        data['reverse_order_flag'] =  'reversed'
                        return(data)

    return(data)   

#...............................................................................................  
#...............................................................................................
def stop_loss_dynamic(data):
    if data['reverse_order_flag'] == 'new':
        data = stop_loss_reverse(data)
        
    elif data['reverse_order_flag'] == 'reversed':
        data = simple_stop_loss(data)
    return(data)
# ...............................................................................................

#...............................................................................................
def stop_loss_reverse(data):
    if data['open_order']:
    
        if data['open_order_type'] == 'long':
            data['close_bid_price'] = data['bid']
            data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 5)

            if data['pl'] <= data['stop_loss_pip']:
                data['stop_text'] = 'reverse_stop'
                data = reverse_order(data)
                data['reverse_order_flag'] =  'reversed'
                data['take_profit_flag'] = True
                return(data)
                
        if data['open_order_type'] == 'short':
                data['close_ask_price'] = data['ask']
                data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 5)

                if data['pl'] <= data['stop_loss_pip']:
                    data['stop_text'] = 'reverse_stop'
                    data = reverse_order(data)
                    data['reverse_order_flag'] =  'reversed'
                    data['take_profit_flag'] = True
                    return(data)

    return(data)   

#...............................................................................................   

#...............................................................................................
def reverse_order(data):
    if data['open_order']:
        if data['open_order_type'] == 'long':            
            data = close_long_order(data)
            data = make_short_order(data)            
            create_report(data)  
            return(data)
            
        if data['open_order_type'] == 'short':
            data = close_short_order(data)
            data = make_long_order(data) 
            return(data)

    return(data)    
#...............................................................................................

#...............................................................................................
def close_order(data):
    if data['open_order']:
        if data['open_order_type'] == 'long':
            if data['position'] != 1:
                data['close_bid_price'] = data['bid']
                data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 5)
                data['pl_list'].append(data['pl'])
                data['dt_list'].append(data['dt_val'])
                data['open_order'] = False
                data['slema_check_flag'] = False
                data['close_type'].append('sema_close')

                if data["plot"]:
                    data['sell_markers_x'].append(data['i_list'][-1])
                    data['sell_markers_y'].append(data['bid'])      
                
                create_report(data)         
            
        if data['open_order_type'] == 'short':
            if data['position'] != -1:
                data['close_ask_price'] = data['ask']
                data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 5)
                data['pl_list'].append(data['pl'])
                data['dt_list'].append(data['dt_val'])
                data['open_order'] = False
                data['slema_check_flag'] = False
                data['close_type'].append('sema_close')

                if data["plot"]:
                    data['sell_markers_x'].append(data['i_list'][-1])
                    data['sell_markers_y'].append(data['ask'])                  
                
                create_report(data)

    return(data)    
#...............................................................................................

#...............................................................................................
def slema_just_close_reverse_check(data):
    
    if data['slema_closed_flag'] == 'short':
        if data['sema'] < data['slema']:
            data['dir_change'] = True
            data['to_order'] = 'short'
    
    if data['slema_closed_flag'] == 'long':
        if data['sema'] > data['slema']:
            data['dir_change'] = True
            data['to_order'] = 'long'
    
    return(data)
#...............................................................................................

# def slema_move_close(data):
#     if data['open_order']:
#         if data['slema_positive']: 

#             if data['open_order_type'] == 'long':
#                 data['close_bid_price'] = data['bid']
#                 data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 5)

#                 if data['pl'] > 0:
#                     if data['sema'] < data['slema']:
#                         data = reverse_order(data)
#                         return(data)

#             if data['open_order_type'] == 'short':
#                 data['close_ask_price'] = data['ask']
#                 data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 5)
                
#                 if data['pl'] > 0:
#                     if data['sema'] > data['slema']:  
#                         data = reverse_order(data)
#                         return(data)    
#     return(data)

#...............................................................................................

# def reverse_order_position(data):
#     if data['open_order']:
#         if data['dir_change']:
#             if data['open_order_type'] == 'long':
#                 if data['to_order'] == 'short':
#                     data['close_bid_price'] = data['bid']
#                     data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 5)
#                     data['pl_list'].append(data['pl'])
#                     data['dt_list'].append(data['dt_val'])
#                     data['open_order'] = 'False'
#                     data['close_type'].append('sema_close')
#                     # data['order_types'].append(data['open_order_type'])

#                     data['order_bid_price'] = data['bid']
#                     data['open_order'] = True
#                     data['slema_check_flag'] = True
#                     data['open_order_type'] = 'short'
#                     data['pl_positive'] = False

#                     if data["plot"]:
#                         data['sell_markers_x'].append(data['i_list'][-1])
#                         data['sell_markers_y'].append(data['bid'])      
                        
#                         data['buy_markers_x'].append(data['i_list'][-1])
#                         data['buy_markers_y'].append(data['bid'])
                    
#                     create_report(data)  
#                     data['ord_types'].append(data['open_order_type'])       
#                     # data['order_methods'].append('reverse')
#                     # data['lema_vals'].append(data['lema_angle'])
                
#             if data['open_order_type'] == 'short':
#                 if data['to_order'] == 'long':
#                     data['close_ask_price'] = data['ask']
#                     data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 5)
#                     data['pl_list'].append(data['pl'])
#                     data['dt_list'].append(data['dt_val'])
#                     data['open_order'] = False
#                     data['close_type'].append('sema_close')
#                     # data['order_types'].append(data['open_order_type'])

#                     data['order_ask_price'] = data['ask']
#                     data['open_order'] = True
#                     data['slema_check_flag'] = True
#                     data['open_order_type'] = 'long'
#                     data['pl_positive'] = False

#                     if data["plot"]:
#                         data['sell_markers_x'].append(data['i_list'][-1])
#                         data['sell_markers_y'].append(data['ask'])         

#                         data['buy_markers_x'].append(data['i_list'][-1])
#                         data['buy_markers_y'].append(data['ask'])         
                    
#                     create_report(data)
#                     data['ord_types'].append(data['open_order_type'])
#                     # data['order_methods'].append('reverse')
#                     # data['lema_vals'].append(data['lema_angle'])

#     return(data)    
#...............................................................................................