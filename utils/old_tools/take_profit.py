from utils.packages import *

##--------------------------------------------------------------------------------------------------------------------------
def take_profit(data):
    #global data
    
    if data['order_current_open'] == 'long':
        data['price_order_ask']      = float(data['positions_info']['positions'][0]['long']['averagePrice'])
        data['long_profit_val']      = data['price_bid'] - data['price_order_ask']
        
        data['long_max_profit']      = max(data['long_max_profit'], data['long_profit_val'])        
        data['long_buffer_val']      = max(data['pip_take_profit'], data['long_max_profit'] * data['pip_take_profit_ratio'])        
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
        data['short_buffer_profit']   = data['short_max_profit'] - data['short_buffer_val']
        
        if data['short_profit_val'] <= data['short_buffer_profit'] and data['short_profit_val'] >= data['pip_take_profit']:
            data = close_short_orders(data)
            data = reset_data(data)
            data = check_for_open_orders(data)
            data['num_took_profit'] = data['num_took_profit'] + 1
    
    return(data)
#==========================================================================================================================