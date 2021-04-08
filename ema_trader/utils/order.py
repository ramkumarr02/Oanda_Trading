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
        data['order_current_open']  = False
        data['positions_long']      = 0
        data['positions_short']     = 0
        data['pl']                  = 0

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
def make_long_order(data):
    if data['order_type'] == 'first':
        data['order_val']           = data['order_num'] * 1       

    elif data['order_type'] == 'follow':
        data['order_val']           = data['follow_order_num'] * 1

    ordr                        = MarketOrderRequest(instrument = data['instrument'],units=data['order_val'])
    order_request_data          = orders.OrderCreate(accountID=data['accountID'], data=ordr.data)
    
    data['response_order']      = data['api'].request(order_request_data)
    data['num_orders']          = data['num_orders'] + 1
    data                        = check_for_open_orders(data)
    data['price_order_ask']     = float(data['positions_info']['positions'][0]['long']['averagePrice'])
    data['opened_order']        = 'long'
    return(data)
#...............................................................................................


#...............................................................................................
def make_short_order(data):
    if data['order_type'] == 'first':
        data['order_val']           = data['order_num'] * -1

    elif data['order_type'] == 'follow':
        data['order_val']           = data['follow_order_num'] * -1
                
    ordr                        = MarketOrderRequest(instrument = data['instrument'],units=data['order_val'])
    order_request_data          = orders.OrderCreate(accountID=data['accountID'], data=ordr.data)
    
    data['response_order']      = data['api'].request(order_request_data)
    data['num_orders']          = data['num_orders'] + 1
    data                        = check_for_open_orders(data)    
    data['price_order_bid']     = float(data['positions_info']['positions'][0]['short']['averagePrice'])
    data['opened_order']        = 'short'
    return(data)
#...............................................................................................


#...............................................................................................
# #### close_order
def close_long_order(data):
    data                        = check_for_open_orders(data)
    data_long                   = {"longUnits": "ALL"}
    order_close_data            = positions.PositionClose(accountID=data['accountID'], instrument=data['instrument'], data=data_long)
    data['response_close']      = data['api'].request(order_close_data)
    data['follow_order']        = False
    data                        = get_invest_details(data)
    data['pl']                  = 0    
    return(data)
#...............................................................................................


#...............................................................................................
def close_short_order(data):
    data                        = check_for_open_orders(data)
    data_short                  = {"shortUnits": "ALL"}
    order_close_data            = positions.PositionClose(accountID=data['accountID'], instrument=data['instrument'], data=data_short)
    data['response_close']      = data['api'].request(order_close_data)
    data['follow_order']        = False
    data                        = get_invest_details(data)
    data['pl']                  = 0
    return(data)
#...............................................................................................



#...............................................................................................
def make_order(data):
    if not data['order_current_open']:
        if data['dir_change']:
            if data['to_order'] == 'long':
                data['order_type'] = 'first'
                make_long_order(data)

            if data['to_order'] == 'short':
                data['order_type'] = 'first'
                make_short_order(data)
    return(data)
#...............................................................................................



#...............................................................................................
def follow_order(data):
    if not data['follow_order']:

        if data['order_current_open'] == 'long':
            if data['pl'] >= data['gap_cushion']:
                data['order_type'] = 'follow'
                make_long_order(data)
                data['follow_order'] = True

        if data['order_current_open'] == 'short':
            if data['pl'] >= data['gap_cushion']:
                data['order_type'] = 'follow'
                make_short_order(data)
                data['follow_order'] = True

    return(data)
#...............................................................................................



#...............................................................................................
def close_order(data):
    if data['dir_change']:
        if data['order_current_open'] == 'long':
            if data['position_without_cushion'] == -1:
                data = close_long_order(data)

        if data['order_current_open'] == 'short':
            if data['position_without_cushion'] == 1:
                data = close_short_order(data)       

    return(data)
#...............................................................................................



#...............................................................................................
def angle_close(data):
    if data['order_current_open'] == 'long':
        data['pl'] = data['bid'] - data['price_order_ask']

        if data['sema_angle'] < -data['close_angle']:    
            if data['pl'] >= data['angle_close_pip']:
                data = close_long_order(data)

    if data['order_current_open'] == 'short':
        data['pl'] = data['price_order_bid'] - data['ask']            
        
        if data['sema_angle'] > data['close_angle']:            
            if data['pl'] >= data['angle_close_pip']:
                data = close_short_order(data)

    return(data)
#...............................................................................................



#...............................................................................................
def reverse_order(data):
    if data['dir_change']:
        if data['order_current_open'] == 'long':
            if data['to_order'] == 'short':
                data = close_long_order(data)
                data = make_short_order(data)

        if data['order_current_open'] == 'short':
            if data['to_order'] == 'long':
                data = close_short_order(data)
                data = make_long_order(data)        

    return(data)
#...............................................................................................



#...............................................................................................
def get_invest_details(data):    
    account_data = accounts.AccountDetails(data["accountID"])
    data["account_data"] = data["api"].request(account_data)

    data["account_balance"] = float(data["account_data"]["account"]["balance"])
    data["order_amount"] = data["account_balance"] * data["invest_ratio"] * data['margin_call_ratio']
    data["order_amount"] = int(np.floor(data["order_amount"]))
    data['follow_order_num'] = data["order_amount"]

    return(data)
#...............................................................................................