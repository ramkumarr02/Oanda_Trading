from utils.packages import *
from utils.i_o import *


#...............................................................................................
def make_order(data):
    if not data['open_order']:
        if data['dir_change']:
            if data['to_order'] == 'long':
                data['order_ask_price'] = data['ask']
                data['open_order'] = True
                data['open_order_type'] = 'long'
                
                if data["plot"]:
                    data['buy_markers_x'].append(data['i_list'][-1])
                    data['buy_markers_y'].append(data['ask'])
                
            elif data['to_order'] == 'short':
                data['order_bid_price'] = data['bid']
                data['open_order'] = True
                data['open_order_type'] = 'short'

                if data["plot"]:
                    data['buy_markers_x'].append(data['i_list'][-1])
                    data['buy_markers_y'].append(data['bid'])
                
    return(data)
#...............................................................................................

#...............................................................................................
def reverse_order(data):
    if data['open_order']:
        if data['dir_change']:
            if data['open_order_type'] == 'long':
                if data['to_order'] == 'short':
                    data['close_bid_price'] = data['bid']
                    data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 4)
                    data['pl_list'].append(data['pl'])
                    data['dt_list'].append(data['dt_val'])
                    data['open_order'] = False
                    data['close_type'].append('sema_close')

                    if data["plot"]:
                        data['sell_markers_x'].append(data['i_list'][-1])
                        data['sell_markers_y'].append(data['bid'])      
                    
                    create_report(data)         
                
            if data['open_order_type'] == 'short':
                if data['to_order'] == 'long':
                    data['close_ask_price'] = data['ask']
                    data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 4)
                    data['pl_list'].append(data['pl'])
                    data['dt_list'].append(data['dt_val'])
                    data['open_order'] = False
                    data['close_type'].append('sema_close')

                    if data["plot"]:
                        data['sell_markers_x'].append(data['i_list'][-1])
                        data['sell_markers_y'].append(data['ask'])                  
                    
                    create_report(data)

    return(data)    
#...............................................................................................

#...............................................................................................
def close_order(data):
    if data['open_order']:
        if data['dir_change']:
            if data['position'] < 0 and data['open_order_type'] == 'long' and data['sema_angle'] < -data['sema_close_order_angle']:
                data['close_bid_price'] = data['bid']
                data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 4)
                data['pl_list'].append(data['pl'])
                data['dt_list'].append(data['dt_val'])
                data['open_order'] = False
                data['close_type'].append('sema_close')

                if data["plot"]:
                    data['sell_markers_x'].append(data['i_list'][-1])
                    data['sell_markers_y'].append(data['bid'])      
                
                create_report(data)         
                
            elif data['position'] > 0 and data['open_order_type'] == 'short' and data['sema_angle'] > data['sema_close_order_angle']:
                data['close_ask_price'] = data['ask']
                data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 4)
                data['pl_list'].append(data['pl'])
                data['dt_list'].append(data['dt_val'])
                data['open_order'] = False
                data['close_type'].append('sema_close')

                if data["plot"]:
                    data['sell_markers_x'].append(data['i_list'][-1])
                    data['sell_markers_y'].append(data['ask'])                  
                
                create_report(data)

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



#...............................................................................................
def tick_close(data):
    if data['open_order']:
        if data['open_order_type'] == 'short':
            if data['tick'] - data['lema'] >= 0 and data['sema_angle'] > data['tick_order_angle']:
                data['close_ask_price'] = data['ask']
                data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 4)
                data['pl_list'].append(data['pl'])
                data['dt_list'].append(data['dt_val'])
                data['open_order'] = False
                data['close_type'].append('tick_close')
                
                if data["plot"]:
                    data['sell_markers_x'].append(data['i_list'][-1])
                    data['sell_markers_y'].append(data['ask'])  
                
                create_report(data)

        if data['open_order_type'] == 'long':
            if data['lema'] - data['tick'] >= 0 and data['sema_angle'] < -data['tick_order_angle']:
                data['close_bid_price'] = data['bid']
                data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 4)
                data['pl_list'].append(data['pl'])
                data['dt_list'].append(data['dt_val'])
                data['open_order'] = False
                data['close_type'].append('tick_close')
                
                if data["plot"]:
                    data['sell_markers_x'].append(data['i_list'][-1])
                    data['sell_markers_y'].append(data['bid'])   

                create_report(data)               
                
    return(data)    
#...............................................................................................  



#...............................................................................................
def stop_loss(data):
    if data['open_order']:

        if data['open_order_type'] == 'long':
            data['close_bid_price'] = data['bid']
            data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 4)

            if data['pl'] <= -data['stop_loss_pip']:
                data['pl_list'].append(data['pl'])
                data['dt_list'].append(data['dt_val'])
                data['open_order'] = False
                data['close_type'].append('stop_loss')
                
                if data["plot"]:
                    data['sell_markers_x'].append(data['i_list'][-1])
                    data['sell_markers_y'].append(data['bid'])   

                create_report(data)               
                
        if data['open_order_type'] == 'short':
                data['close_ask_price'] = data['ask']
                data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 4)

                if data['pl'] <= -data['stop_loss_pip']:
                    data['pl_list'].append(data['pl'])
                    data['dt_list'].append(data['dt_val'])
                    data['open_order'] = False
                    data['close_type'].append('stop_loss')
                    
                    if data["plot"]:
                        data['sell_markers_x'].append(data['i_list'][-1])
                        data['sell_markers_y'].append(data['ask'])  
                    
                    create_report(data)

    return(data)    
#...............................................................................................    