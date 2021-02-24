# ### Packages
from utils.packages import *

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


# #### make_order
#--------------------------------------------------------------------------------------------------------------------------
def make_order(data):
    #global data
    if not data['order_current_open']:
        if data['order_create'] == 'long':      
            
            data['order_val'] = data['order_num'] * 1
                        
            # !!!!!!!!!!stop loss line max to be introduced and tested    
            data['price_stop'] = data['price_ask'] - data['stop_loss_pip']
            
            stopLossOnFill = StopLossDetails(price=data['price_stop'])
                       
            ordr = MarketOrderRequest(instrument = data['instrument'], 
                                      units=data['order_val'], 
                                      stopLossOnFill=stopLossOnFill.data)

            order_request_data = orders.OrderCreate(accountID=data['accountID'], data=ordr.data)
            
            data['response_order'] = data['api'].request(order_request_data)
            data['num_orders'] = data['num_orders'] + 1
            data = check_for_open_orders(data)


        if data['order_create'] == 'short':
            data['order_val'] = data['order_num'] * -1
            
            # !!!!!!!!!!stop loss line min to be introduced and tested            
            data['price_stop'] = data['price_bid'] + data['stop_loss_pip']
            stopLossOnFill = StopLossDetails(price=data['price_stop'])

            ordr = MarketOrderRequest(instrument = data['instrument'], 
                                      units=data['order_val'], 
                                      stopLossOnFill=stopLossOnFill.data)
            
            order_request_data = orders.OrderCreate(accountID=data['accountID'], data=ordr.data)
            
            data['response_order'] = data['api'].request(order_request_data)
            data['num_orders'] = data['num_orders'] + 1
            data = check_for_open_orders(data)
    
    return(data)
#==========================================================================================================================


# #### close_order
def close_long_orders(data):
    #global data
    data_long = {"longUnits": "ALL"}
    order_close_data = positions.PositionClose(accountID=data['accountID'],
                                instrument=data['instrument'],
                                data=data_long)
    data['response_close'] = data['api'].request(order_close_data)
    return(data)

def close_short_orders(data):
    #global data
    data_short = {"shortUnits": "ALL"}
    order_close_data = positions.PositionClose(accountID=data['accountID'],
                                instrument=data['instrument'],
                                data=data_short)
    data['response_close'] = data['api'].request(order_close_data)
    return(data)


# #### take_profit
#--------------------------------------------------------------------------------------------------------------------------
def take_profit(data):
    #global data
    
    if data['order_current_open'] == 'long':
        data['price_order_ask']      = float(data['positions_info']['positions'][0]['long']['averagePrice'])
        data['long_profit_val']      = data['price_bid'] - data['price_order_ask']
        
        data['long_max_profit']      = max(data['long_max_profit'], data['long_profit_val'])        
        data['long_buffer_val']      = max(data['pip_take_profit'], data['long_max_profit'] * data['pip_take_profit_ratio'])  
        data['long_buffer_val']      = min(data['long_buffer_val'], data['max_take_profit'])      
        data['long_buffer_profit']   = data['long_max_profit'] - data['long_buffer_val']
        
        if data['long_profit_val'] <= data['long_buffer_profit'] and data['long_profit_val'] >= data['pip_take_profit']:
            data = close_long_orders(data)
            data = reset_data(data)
            data = check_for_open_orders(data)
            data['num_took_profit'] = data['num_took_profit'] + 1
                
                
    if data['order_current_open'] == 'short':
        data['price_order_bid'] = float(data['positions_info']['positions'][0]['short']['averagePrice'])
        data['short_profit_val']      = data['price_order_bid'] - data['price_ask']
        
        data['short_max_profit']      = max(data['short_max_profit'], data['short_profit_val'])        
        data['short_buffer_val']      = max(data['pip_take_profit'], data['short_max_profit'] * data['pip_take_profit_ratio'])        
        data['short_buffer_val']      = min(data['short_buffer_val'], data['max_take_profit'])
        data['short_buffer_profit']   = data['short_max_profit'] - data['short_buffer_val']
        
        if data['short_profit_val'] <= data['short_buffer_profit'] and data['short_profit_val'] >= data['pip_take_profit']:
            data = close_short_orders(data)
            data = reset_data(data)
            data = check_for_open_orders(data)
            data['num_took_profit'] = data['num_took_profit'] + 1
    
    return(data)
#==========================================================================================================================


# #### Hedge to be added below
#--------------------------------------------------------------------------------------------------------------------------

#==========================================================================================================================