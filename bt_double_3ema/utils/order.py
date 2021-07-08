from utils.packages import *
from utils.i_o import *


#...............................................................................................
def make_orders(data):
    if not data['long_open_order'] and not data['short_open_order']:
        if data['dir_change']:
            data =  make_long_order(data)
            data =  make_short_order(data)
            data['reverse_order_flag'] = 'new'
                
    # if not data['long_open_order'] and data['short_open_order']:
    #     if data['dir_change']:
    #         data =  make_long_order(data)            
    #         data['reverse_order_flag'] = 'new'
            
    # if data['long_open_order'] and not data['short_open_order']:
    #     if data['dir_change']:            
    #         data =  make_short_order(data)
    #         data['reverse_order_flag'] = 'new'
                
    return(data)
#...............................................................................................
def sema_close_order(data):
    if data['long_open_order']:
        if data['position'] != 1 and data['order_long_position'] != data['position']:        
            data['temp_text'] = 'sema_close'    
            data = close_long_order(data)
            
    if data['short_open_order']:
        if data['position'] != -1 and data['order_short_position'] != data['position']:
            data['temp_text'] = 'sema_close'    
            data = close_short_order(data)
            
    return(data)    
#...............................................................................................


#...............................................................................................
def simple_take_profit(data):
   
    if data['long_open_order']:                        
        if data['long_pl'] >= data['simple_tp']:
            data['temp_text'] = 'simple_take_profit'
            data = close_long_order(data)  
            # data = make_orders(data)

    if data['short_open_order']:                        
        if data['short_pl'] >= data['simple_tp']:
            data['temp_text'] = 'simple_take_profit'
            data = close_short_order(data)  
            # data = make_orders(data)
    
    return(data)    
#...............................................................................................

# ...............................................................................................
def simple_stop_loss(data):
    if data['long_open_order']:
        if data['long_pl'] <= -data['stop_loss_pip']:
            data['temp_text'] = 'simple_stop_loss'
            data = close_long_order(data)    
                
    if data['short_open_order']:
        if data['short_pl'] <= -data['stop_loss_pip']:
            data['temp_text'] = 'simple_stop_loss'
            data = close_short_order(data) 

    return(data)   
# ...............................................................................................   

#...............................................................................................
def stop_loss(data):

    if data['reverse_order_flag'] == 'new':
        data = reverse_stop_loss(data)
        
    elif data['reverse_order_flag'] == 'reversed':
        data = simple_stop_loss(data)

    return(data)
# ...............................................................................................
def reverse_stop_loss(data):
    if data['long_open_order']:
        if data['long_pl'] <= -data['stop_loss_pip']:
            data['temp_text'] = 'reverse_stop_loss'
            data = close_long_order(data)  
            data = make_short_order(data)
            data['reverse_order_flag'] = 'reversed'     
                
    if data['short_open_order']:
        if data['short_pl'] <= -data['stop_loss_pip']:
            data['temp_text'] = 'reverse_stop_loss'
            data = close_short_order(data)  
            data = make_long_order(data)
            data['reverse_order_flag'] = 'reversed' 

    return(data)   
# ...............................................................................................   

#...............................................................................................
def pl_positive_check(data):
                
    if data['long_open_order']:
        data['long_close_bid_price'] = data['bid']
        data['long_pl'] = np.round(data['long_close_bid_price'] - data['long_order_ask_price'], 5)
        
        if data['long_pl'] >= data['pl_move_trail_trigger']:
            data['long_pl_positive'] = True
            data['long_pl_move_min'] = data['long_pl'] * data['pl_move_trail_size']

    if data['short_open_order']:
        data['short_close_ask_price'] = data['ask']
        data['short_pl'] = np.round(data['short_order_bid_price'] - data['short_close_ask_price'], 5)
    
        if data['short_pl'] >= data['pl_move_trail_trigger']:
            data['short_pl_positive'] = True
            data['short_pl_move_min'] = data['short_pl'] * data['pl_move_trail_size']

    return(data)
#...............................................................................................

#...............................................................................................
def pl_move_close(data):
    
    if data['long_open_order']:
        if data['long_pl_positive']:
            if data['long_pl'] > 0:
                if data['long_pl'] <= data['long_pl_move_min']: 
                    data['long_pl_positive'] = False
                    data['long_pl_move_min'] = None
                    data['temp_text'] = 'pl_move_close'
                    data = close_long_order(data)                
              
                
    if data['short_open_order']:
        if data['short_pl_positive']:
            if data['short_pl'] > 0:
                if data['short_pl'] <= data['short_pl_move_min']:
                    data['short_pl_positive'] = False
                    data['short_pl_move_min'] = None
                    data['temp_text'] = 'pl_move_close'
                    data = close_short_order(data)    

    return(data)    
#...............................................................................................    

#...............................................................................................
def pl_negative_check(data):
    if not data['negative_hit_limit']:
        if data['long_open_order']:
            if data['long_pl'] < data['pl_loss_trail_trigger']:
                data['negative_hit_limit'] = True
                data['long_pl_loss_min'] = data['long_pl'] * data['pl_loss_trail_size']
        
        if data['short_open_order']:
            if data['short_pl'] < data['pl_loss_trail_trigger']:
                data['negative_hit_limit'] = True
                data['short_pl_loss_min'] = data['short_pl'] * data['pl_loss_trail_size']

    if data['negative_hit_limit']:                
        if data['long_open_order']:
            data['long_close_bid_price'] = data['bid']
            data['long_pl'] = np.round(data['long_close_bid_price'] - data['long_order_ask_price'], 5)
            
            if data['long_pl'] > data['pl_loss_trail_trigger']:
                data['long_pl_negative'] = True
                data['long_pl_loss_min'] = data['long_pl'] * data['pl_loss_trail_size']

        if data['short_open_order']:
            data['short_close_ask_price'] = data['ask']
            data['short_pl'] = np.round(data['short_order_bid_price'] - data['short_close_ask_price'], 5)
        
            if data['short_pl'] > data['pl_loss_trail_trigger']:
                data['short_pl_negative'] = True
                data['short_pl_loss_min'] = data['short_pl'] * data['pl_loss_trail_size']

    return(data)
#...............................................................................................

#...............................................................................................
def pl_loss_close(data):
    
    if data['long_open_order']:
        if data['long_pl_negative']:
            if data['long_pl'] > data['long_pl_loss_min']: 
                data['long_pl_negative'] = False
                data['long_pl_loss_min'] = None
                data['temp_text'] = 'pl_loss_close'
                data = close_long_order(data)                
              
                
    if data['short_open_order']:
        if data['short_pl_negative']:
            if data['short_pl'] > data['short_pl_loss_min']:
                data['short_pl_negative'] = False
                data['short_pl_loss_min'] = None
                data['temp_text'] = 'pl_loss_close'
                data = close_short_order(data)    

    return(data)    
#...............................................................................................    

#...............................................................................................
def make_long_order(data):
    data['long_order_ask_price']    = data['ask']
    data['long_open_order']         = True
    data['long_slema_check_flag']   = True
    data['order_long_position']     = data['position']
    data['long_pl_move_min']        = None
    data['long_pl_positive']        = False
    data['negative_hit_limit']      = False

    data['long_close_bid_price'] = data['bid']
    data['long_pl'] = np.round(data['long_close_bid_price'] - data['long_order_ask_price'], 5)

    if data["plot"]:
        data['long_buy_markers_x'].append(data['i_list'][-1])
        data['long_buy_markers_y'].append(data['ask'])
    return(data)
#...............................................................................................
def make_short_order(data):
    data['short_order_bid_price']   = data['bid']
    data['short_open_order']        = True
    data['short_slema_check_flag']  = True
    data['order_short_position']    = data['position']
    data['short_pl_move_min']       = None
    data['short_pl_positive']       = False
    data['negative_hit_limit']      = False

    data['short_close_ask_price'] = data['ask']
    data['short_pl'] = np.round(data['short_order_bid_price'] - data['short_close_ask_price'], 5)

    if data["plot"]:
        data['short_buy_markers_x'].append(data['i_list'][-1])
        data['short_buy_markers_y'].append(data['bid'])

    return(data)
#...............................................................................................
def close_long_order(data): 
    data['long_open_order'] = False
    data['long_slema_check_flag'] = False
    data['pl_list'].append(data['long_pl'])
    data['dt_list'].append(data['dt_val'])
    data['close_type'].append(data['temp_text'])
    data['ord_types'].append('long')

    if data["plot"]:
        data['long_sell_markers_x'].append(data['i_list'][-1])
        data['long_sell_markers_y'].append(data['bid'])      
    
    create_report(data)

    return(data)
#...............................................................................................
def close_short_order(data):
    data['short_open_order'] = False
    data['short_slema_check_flag'] = False
    data['pl_list'].append(data['short_pl'])
    data['dt_list'].append(data['dt_val'])
    data['close_type'].append(data['temp_text'])
    data['ord_types'].append('short')

    if data["plot"]:
        data['short_sell_markers_x'].append(data['i_list'][-1])
        data['short_sell_markers_y'].append(data['ask'])                  
    
    create_report(data)

    return(data)
#...............................................................................................

def calculate_pl(data):
    if data['long_open_order']:
        data['long_close_bid_price'] = data['bid']
        data['long_pl'] = np.round(data['long_close_bid_price'] - data['long_order_ask_price'], 5)

    if data['short_open_order']:
        data['short_close_ask_price'] = data['ask']
        data['short_pl'] = np.round(data['short_order_bid_price'] - data['short_close_ask_price'], 5)
    
    return(data)    
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
            if data['sema'] <= data['slema']:
                data['temp_text'] = 'simple_slema_move_close'
                data = close_long_order(data)            
    
    if data['short_open_order']:
        if data['short_slema_positive']:
            if data['sema'] >= data['slema']:                
                data['temp_text'] = 'simple_slema_move_close'
                data = close_short_order(data) 

    return(data)    
#...............................................................................................