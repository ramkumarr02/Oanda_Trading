from utils.packages import *
from utils.i_o import *


#...............................................................................................
def make_order(data):
    if not data['open_order']:
        if data['dir_change']:
            if data['to_order'] == 'long':
                data['order_ask_price'] = data['ask']
                data['open_order'] = True
                data['slema_check_flag'] = True
                data['open_order_type'] = 'long'
                data['ord_types'].append(data['open_order_type'])
                data['reverse_order_flag'] =  'new'
                data['slema_move_close_flag'] =  'new'
                data['pl_positive'] = False
                data['pl_move_min'] = None
                
                if data["plot"]:
                    data['buy_markers_x'].append(data['i_list'][-1])
                    data['buy_markers_y'].append(data['ask'])
                
            elif data['to_order'] == 'short':
                data['order_bid_price'] = data['bid']
                data['open_order'] = True
                data['slema_check_flag'] = True
                data['open_order_type'] = 'short'
                data['ord_types'].append(data['open_order_type'])
                data['reverse_order_flag'] =  'new'
                data['slema_move_close_flag'] =  'new'
                data['pl_positive'] = False
                data['pl_move_min'] = None

                if data["plot"]:
                    data['buy_markers_x'].append(data['i_list'][-1])
                    data['buy_markers_y'].append(data['bid'])
                
    return(data)
#...............................................................................................



#...............................................................................................
def stop_loss(data):
    if data['reverse_order_flag'] == 'new':
        data = stop_loss_reverse(data)
        
    elif data['reverse_order_flag'] == 'reversed':
        data = simple_stop_loss(data)
    return(data)
# ...............................................................................................


# ...............................................................................................
def simple_stop_loss(data):
    if data['open_order']:

        if data['open_order_type'] == 'long':
            data['close_bid_price'] = data['bid']
            data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 5)

            if data['pl'] <= -data['stop_loss_pip']:
                data['pl_list'].append(data['pl'])
                data['dt_list'].append(data['dt_val'])
                data['open_order'] = False
                data['close_type'].append('simple_stop')
                
                if data["plot"]:
                    data['sell_markers_x'].append(data['i_list'][-1])
                    data['sell_markers_y'].append(data['bid'])   

                create_report(data)               
                
        if data['open_order_type'] == 'short':
                data['close_ask_price'] = data['ask']
                data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 5)

                if data['pl'] <= -data['stop_loss_pip']:
                    data['pl_list'].append(data['pl'])
                    data['dt_list'].append(data['dt_val'])
                    data['open_order'] = False
                    data['close_type'].append('simple_stop')
                    
                    if data["plot"]:
                        data['sell_markers_x'].append(data['i_list'][-1])
                        data['sell_markers_y'].append(data['ask'])  
                    
                    create_report(data)

    return(data)   
# ...............................................................................................   


#...............................................................................................
def stop_loss_reverse(data):
    if data['open_order']:
    
        if data['open_order_type'] == 'long':
            data['close_bid_price'] = data['bid']
            data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 5)

            if data['pl'] <= -data['stop_loss_pip']:
                data = reverse_order(data, 'reverse_stop')
                data['reverse_order_flag'] =  'reversed'
                return(data)
                
        if data['open_order_type'] == 'short':
                data['close_ask_price'] = data['ask']
                data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 5)

                if data['pl'] <= -data['stop_loss_pip']:
                    data = reverse_order(data, 'reverse_stop')
                    data['reverse_order_flag'] =  'reversed'
                    return(data)

    return(data)   

#...............................................................................................   


#...............................................................................................
def reverse_order(data, stop_text):
    if data['open_order']:
            if data['open_order_type'] == 'long':
                data['close_bid_price'] = data['bid']
                data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 5)
                data['pl_list'].append(data['pl'])
                data['dt_list'].append(data['dt_val'])
                data['open_order'] = 'False'
                data['close_type'].append(stop_text)
                data['slema_check_flag'] = False

                data['order_bid_price'] = data['bid']
                data['open_order'] = True
                data['slema_check_flag'] = True
                data['open_order_type'] = 'short'

                if data["plot"]:
                    data['sell_markers_x'].append(data['i_list'][-1])
                    data['sell_markers_y'].append(data['bid'])      
                    
                    data['buy_markers_x'].append(data['i_list'][-1])
                    data['buy_markers_y'].append(data['bid'])
                
                create_report(data)  
                data['ord_types'].append(data['open_order_type'])                       
                return(data)
                
            if data['open_order_type'] == 'short':
                data['close_ask_price'] = data['ask']
                data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 5)
                data['pl_list'].append(data['pl'])
                data['dt_list'].append(data['dt_val'])
                data['open_order'] = False
                data['slema_check_flag'] = False
                data['close_type'].append(stop_text)

                data['order_ask_price'] = data['ask']
                data['open_order'] = True
                data['slema_check_flag'] = True
                data['open_order_type'] = 'long'

                if data["plot"]:
                    data['sell_markers_x'].append(data['i_list'][-1])
                    data['sell_markers_y'].append(data['ask'])         

                    data['buy_markers_x'].append(data['i_list'][-1])
                    data['buy_markers_y'].append(data['ask'])         
                
                create_report(data)
                data['ord_types'].append(data['open_order_type'])
                return(data)

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

def slema_move_close(data):
    if data['slema_move_close_flag'] == 'new':
        data = slema_move_close_reverse(data)
        
    elif data['slema_move_close_flag'] == 'reversed':
        data = simple_slema_move_close(data)
    return(data)

#...............................................................................................
def slema_move_close_reverse(data):
    if data['open_order']:
        if data['slema_positive']: 

            if data['open_order_type'] == 'long':
                data['close_bid_price'] = data['bid']
                data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 5)
            
                if data['pl'] > 0:
                    if data['sema'] <= data['slema']:
                        data = reverse_order(data, 'reverse_slema_move_close')
                        data['slema_move_close_flag'] =  'reversed'
                        return(data)
                
            if data['open_order_type'] == 'short':
                data['close_ask_price'] = data['ask']
                data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 5)

                if data['pl'] > 0:
                    if data['sema'] <= data['slema']:
                        data = reverse_order(data, 'reverse_slema_move_close')
                        data['slema_move_close_flag'] =  'reversed'
                        return(data)

    return(data)   

#...............................................................................................  

def simple_slema_move_close(data):
    if data['open_order']:
        if data['slema_positive']: 

            if data['open_order_type'] == 'long':
                data['close_bid_price'] = data['bid']
                data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 5)

                # check close with out profit
                if data['pl'] > 0:
                    if data['sema'] <= data['slema']:
                        data['pl_list'].append(data['pl'])
                        data['dt_list'].append(data['dt_val'])
                        data['open_order'] = False
                        data['close_type'].append('simple_slema_move_close')
                
                        if data["plot"]:
                            data['sell_markers_x'].append(data['i_list'][-1])
                            data['sell_markers_y'].append(data['bid'])   

                        create_report(data)               
    
            if data['open_order_type'] == 'short':
                data['close_ask_price'] = data['ask']
                data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 5)
        
                if data['pl'] > 0:
                    if data['sema'] >= data['slema']:                
                        data['pl_list'].append(data['pl'])
                        data['dt_list'].append(data['dt_val'])
                        data['open_order'] = False
                        data['close_type'].append('simple_slema_move_close')
                
                        if data["plot"]:
                            data['sell_markers_x'].append(data['i_list'][-1])
                            data['sell_markers_y'].append(data['ask'])  
                
                        create_report(data)

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
def pl_positive_check(data):
    if data['open_order']:
        if data['open_order_type'] == 'short':
            data['close_ask_price'] = data['ask']
            data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 5)
                
        if data['open_order_type'] == 'long':
            data['close_bid_price'] = data['bid']
            data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 5)

        if data['pl'] >= data['pl_move_trail_trigger']:
            data['pl_positive'] = True
            data['pl_move_min'] = data['pl'] * data['pl_move_trail_ratio']

    return(data)


def pl_move_close(data):
    if data['open_order']:
    
        if data['open_order_type'] == 'long':
            data['close_bid_price'] = data['bid']
            data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 5)

            if data['pl_positive']:
                if data['pl'] > 0:
                    if data['pl'] <= data['pl_move_min']: 
                        data['pl_list'].append(data['pl'])
                        data['dt_list'].append(data['dt_val'])
                        data['open_order'] = False
                        data['to_order'] = None
                        data['close_type'].append('pl_move_close')
                        data['pl_positive'] = False
                        data['pl_move_min'] = None
                        # data['order_types'].append(data['open_order_type'])
                        
                        if data["plot"]:
                            data['sell_markers_x'].append(data['i_list'][-1])
                            data['sell_markers_y'].append(data['bid'])   

                        create_report(data)               
                
        if data['open_order_type'] == 'short':
            data['close_ask_price'] = data['ask']
            data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 5)

            if data['pl_positive']:
                if data['pl'] > 0:
                    if data['pl'] <= data['pl_move_min']:
                        data['pl_list'].append(data['pl'])
                        data['dt_list'].append(data['dt_val'])
                        data['open_order'] = False
                        data['to_order'] = None
                        data['close_type'].append('pl_move_close')
                        data['pl_positive'] = False
                        data['pl_move_min'] = None
                        # data['order_types'].append(data['open_order_type'])
                        
                        if data["plot"]:
                            data['sell_markers_x'].append(data['i_list'][-1])
                            data['sell_markers_y'].append(data['ask'])  
                        
                        create_report(data)


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
