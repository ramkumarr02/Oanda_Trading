from utils.packages import *
from utils.i_o import *

# ### Orders

# #### check_for_open_orders
#--------------------------------------------------------------------------------------------------------------------------
def check_for_open_orders(data):
    #global data
    
    request_position_data = positions.OpenPositions(accountID=data['accountID'])
    data['positions_info'] = data['api'].request(request_position_data)

    if len(data['positions_info']['positions']) == 0:
        data['order_current_open'] = False
        data['positions_long'] = 0
        data['positions_short'] = 0

    elif len(data['positions_info']['positions']) == 1:
        data['positions_long'] = abs(int(data['positions_info']['positions'][0]['long']['units']))
        data['positions_short'] = abs(int(data['positions_info']['positions'][0]['short']['units']))

        if data['positions_long'] >= 1 and data['positions_short'] == 0:
            data['order_current_open'] = 'long'
        elif data['positions_long'] == 0 and data['positions_short'] >= 1:
            data['order_current_open'] = 'short'                              

    return(data)
#==========================================================================================================================    
#...............................................................................................
def make_order(data):
    if not data['order_current_open']:
        if data['dir_change']:
            if data['to_order'] == 'long':
                data['order_val']           = data['order_num'] * 1                
                ordr                        = MarketOrderRequest(instrument = data['instrument'],units=data['order_val'])
                order_request_data          = orders.OrderCreate(accountID=data['accountID'], data=ordr.data)
                
                data['response_order']      = data['api'].request(order_request_data)
                data['num_orders']          = data['num_orders'] + 1
                data                        = check_for_open_orders(data)
                data['price_order_ask']     = float(data['positions_info']['positions'][0]['long']['averagePrice'])
                data['opened_order']        = 'long'

            if data['to_order'] == 'short':
        
                data['order_val']           = data['order_num'] * -1                
                ordr                        = MarketOrderRequest(instrument = data['instrument'],units=data['order_val'])
                order_request_data          = orders.OrderCreate(accountID=data['accountID'], data=ordr.data)
                
                data['response_order']      = data['api'].request(order_request_data)
                data['num_orders']          = data['num_orders'] + 1
                data                        = check_for_open_orders(data)
                data['price_order_ask']     = float(data['positions_info']['positions'][0]['short']['averagePrice'])
                data['opened_order']        = 'short'
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