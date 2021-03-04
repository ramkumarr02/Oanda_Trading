# ### Packages
from utils.packages import *
from utils.reset import *
from utils.time_tick import *

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

    if data['order_current_open'] != False:
        data['order_was_open'] = True

    if not data['order_current_open']:
        if data['order_was_open']:            
            data = reset_data(data)
            data['order_was_open'] = False

    return(data)
#==========================================================================================================================    


# #### make_order
#--------------------------------------------------------------------------------------------------------------------------
def make_order(data):
    #global data
    data = check_for_open_orders(data)
    
    if not data['order_current_open']:
        
        get_avg_candle_height(data, candle_count = 6, granularity = 'M5')
        
        # get_ema_diff(data = data, granularity = 'M5', ema_long = 50, ema_short = 5)        
        # data['stop_loss_pip'] = max(data['stop_loss_candle_height'], data['stop_loss_ema_diff'])        

        data['max_take_profit'] = data['stop_loss_candle_height'] * data['len_multiplier']        
        data['stop_loss_pip'] = data['max_take_profit'] * data['stop_profit_ratio']
        
        if data['order_create'] == 'long':      
            
            data['order_val'] = data['order_num'] * 1
                        
            # !!!!!!!!!!stop loss line max to be introduced and tested    
            data['price_stop']          = data['price_ask'] - data['stop_loss_pip']            
            data['price_take_profit']   = data['price_bid'] + data['max_take_profit']
            
            # stopLossOnFill = StopLossDetails(price=data['price_stop'])
            # takeProfitOnFillOrder = TakeProfitDetails(price=data['price_take_profit'])
            
                       
            ordr = MarketOrderRequest(instrument = data['instrument'], 
                                      units=data['order_val'])
                                    #   , 
                                    #   stopLossOnFill=stopLossOnFill.data,
                                    #   takeProfitOnFill=takeProfitOnFillOrder.data)

            order_request_data = orders.OrderCreate(accountID=data['accountID'], data=ordr.data)
            
            data['response_order'] = data['api'].request(order_request_data)
            data['num_orders'] = data['num_orders'] + 1
            data = check_for_open_orders(data)
            data['price_order_ask']      = float(data['positions_info']['positions'][0]['long']['averagePrice'])

        if data['order_create'] == 'short':
            data['order_val'] = data['order_num'] * -1
            
            # !!!!!!!!!!stop loss line min to be introduced and tested            
            data['price_stop'] = data['price_bid'] + data['stop_loss_pip']
            data['price_take_profit']   = data['price_ask'] - data['max_take_profit']
            
            # stopLossOnFill = StopLossDetails(price=data['price_stop'])
            # takeProfitOnFillOrder = TakeProfitDetails(price=data['price_take_profit'])

            ordr = MarketOrderRequest(instrument = data['instrument'], 
                                      units=data['order_val'])
                                    #   , 
                                    #   stopLossOnFill=stopLossOnFill.data,
                                    #   takeProfitOnFill=takeProfitOnFillOrder.data)
            
            order_request_data = orders.OrderCreate(accountID=data['accountID'], data=ordr.data)
            
            data['response_order'] = data['api'].request(order_request_data)
            data['num_orders'] = data['num_orders'] + 1
            data = check_for_open_orders(data)
            data['price_order_bid']       = float(data['positions_info']['positions'][0]['short']['averagePrice'])
    
    return(data)
#==========================================================================================================================


# #### close_order
def close_long_orders(data):
    #global data
    data = check_for_open_orders(data)
    data_long = {"longUnits": "ALL"}
    order_close_data = positions.PositionClose(accountID=data['accountID'],
                                instrument=data['instrument'],
                                data=data_long)
    data['response_close'] = data['api'].request(order_close_data)
    return(data)

def close_short_orders(data):
    #global data
    data = check_for_open_orders(data)
    data_short = {"shortUnits": "ALL"}
    order_close_data = positions.PositionClose(accountID=data['accountID'],
                                instrument=data['instrument'],
                                data=data_short)
    data['response_close'] = data['api'].request(order_close_data)
    return(data)


# #### take_profit
#--------------------------------------------------------------------------------------------------------------------------
def dynamic_take_profit(data):
    #global data
    
    if data['order_current_open'] == 'long':
        data = check_for_open_orders(data)
        data['long_profit_val']      = data['price_bid'] - data['price_order_ask']
        
        if data['long_profit_val'] >= data['max_take_profit'] + data['pip_take_profit']:
            data['take_profit_flag'] = True

        if data['take_profit_flag']:
            data['long_max_profit']     = max(data['long_max_profit'], data['long_profit_val'])        
            data['long_buffer_profit']  = data['long_max_profit'] - data['pip_take_profit']
                       
            if data['long_profit_val'] <= data['long_buffer_profit']:
                data = close_long_orders(data)
                data = reset_data(data)
                data = check_for_open_orders(data)
                data['num_took_profit'] = data['num_took_profit'] + 1
                
                
    if data['order_current_open'] == 'short':
        data = check_for_open_orders(data)
        data['short_profit_val']      = data['price_order_bid'] - data['price_ask']

        if data['short_profit_val'] >= data['max_take_profit'] + data['pip_take_profit']:
            data['take_profit_flag'] = True

        if data['take_profit_flag']:
            data['short_max_profit']      = max(data['short_max_profit'], data['short_profit_val'])        
            data['short_buffer_profit']   = data['short_max_profit'] - data['pip_take_profit']
        
        if data['short_profit_val'] <= data['short_buffer_profit']:
            data = close_short_orders(data)
            data = reset_data(data)
            data = check_for_open_orders(data)
            data['num_took_profit'] = data['num_took_profit'] + 1
    
    return(data)
#==========================================================================================================================


# #### stop_loss
#--------------------------------------------------------------------------------------------------------------------------
def dynamic_stop_loss(data):
    #global data
    
    if data['order_current_open'] == 'long':
        data = check_for_open_orders(data)
        data['long_loss_val']      = data['price_bid'] - data['price_order_ask']
        
        if data['long_loss_val'] >= data['stop_loss_pip'] - data['pip_take_profit']:
            data['stop_loss_flag'] = True

        if data['stop_loss_flag']:
            data['long_min_loss']     = min(data['long_min_loss'], data['long_loss_val'])        
            data['long_buffer_loss']  = data['long_min_loss'] + data['pip_take_profit']
                       
            if data['long_loss_val'] >= data['long_buffer_loss']:
                data = close_long_orders(data)
                data = reset_data(data)
                data = check_for_open_orders(data)
                data['num_took_loss'] = data['num_took_loss'] + 1
                
                
    if data['order_current_open'] == 'short':
        data = check_for_open_orders(data)
        data['short_loss_val']      = data['price_order_bid'] - data['price_ask']

        if data['short_loss_val'] >= data['stop_loss_pip'] - data['pip_take_profit']:
            data['stop_loss_flag'] = True

        if data['stop_loss_flag']:
            data['short_min_loss']      = min(data['short_min_loss'], data['short_loss_val'])        
            data['short_buffer_loss']  = data['short_min_loss'] + data['pip_take_profit']
        
        if data['short_loss_val'] >= data['short_buffer_loss']:
            data = close_short_orders(data)
            data = reset_data(data)
            data = check_for_open_orders(data)
            data['num_took_loss'] = data['num_took_loss'] + 1
    
    return(data)
#==========================================================================================================================


#--------------------------------------------------------------------------------------------------------------------------
def take_profit_old(data):
    #global data
    
    if data['order_current_open'] == 'long':
        data = check_for_open_orders(data)
        data['long_profit_val']      = data['price_bid'] - data['price_order_ask']
        
        data['long_max_profit']      = max(data['long_max_profit'], data['long_profit_val'])        
        data['long_buffer_val']      = max(data['pip_take_profit'], data['long_max_profit'] * data['pip_take_profit_ratio'])  
        data['long_buffer_val']      = min(data['long_buffer_val'], data['max_take_profit'])      
        data['long_buffer_profit']   = data['long_max_profit'] - data['long_buffer_val']
        
        if data['pip_take_profit'] > data['long_buffer_profit'] > 0:
            data['long_buffer_profit'] = data['pip_take_profit']

        data['long_buffer_profit']   = max(data['long_buffer_profit'], data['pip_take_profit'])
        
        if data['long_profit_val'] <= data['long_buffer_profit'] and data['long_profit_val'] >= data['pip_take_profit']:
            data = close_long_orders(data)
            data = reset_data(data)
            data = check_for_open_orders(data)
            data['num_took_profit'] = data['num_took_profit'] + 1
                
                
    if data['order_current_open'] == 'short':
        data = check_for_open_orders(data)
        data['short_profit_val']      = data['price_order_bid'] - data['price_ask']
        
        data['short_max_profit']      = max(data['short_max_profit'], data['short_profit_val'])        
        data['short_buffer_val']      = max(data['pip_take_profit'], data['short_max_profit'] * data['pip_take_profit_ratio'])        
        data['short_buffer_val']      = min(data['short_buffer_val'], data['max_take_profit'])
        data['short_buffer_profit']   = data['short_max_profit'] - data['short_buffer_val']

        if data['pip_take_profit'] > data['short_buffer_profit'] > 0:
            data['short_buffer_profit'] = data['pip_take_profit']
        
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