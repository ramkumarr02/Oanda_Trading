from utils.packages import *

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


#--------------------------------------------------------------------------------------------------------------------------
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
    #==========================================================================================================================