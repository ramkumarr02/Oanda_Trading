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
        data["take_profit_flg"]     = False
        data['positions_long']      = 0
        data['positions_short']     = 0
        data['pl']                  = 0

    elif len(data['positions_info']['positions']) == 1:
        data['positions_long'] = abs(int(data['positions_info']['positions'][0]['long']['units']))
        data['positions_short'] = abs(int(data['positions_info']['positions'][0]['short']['units']))

        if data['positions_long'] >= 1 and data['positions_short'] == 0:
            data['order_current_open'] = 'long'
            data['trade_id'] = data['positions_info']['positions'][0]['long']['tradeIDs'][0]

        elif data['positions_long'] == 0 and data['positions_short'] >= 1:
            data['order_current_open'] = 'short'                              
            data['trade_id'] = data['positions_info']['positions'][0]['short']['tradeIDs'][0]

    return(data)
#==========================================================================================================================    



#...............................................................................................
def set_take_profit(data):

    if not data["take_profit_flg"]:
        if data['order_current_open']:
            if data['pl'] > data['trailing_stop_pip']:
                ordr = TrailingStopLossOrderRequest(tradeID=data['trade_id'], distance=data['trailing_stop_pip'])
                take_profit_data = orders.OrderCreate(data['accountID'], data=ordr.data)
                data['take_profit_info'] = data['api'].request(take_profit_data)
                data["take_profit_flg"] = True

    return(data)
#...............................................................................................



#...............................................................................................
def get_invest_details(data):    
    account_data = accounts.AccountDetails(data["accountID"])
    data["account_data"] = data["api"].request(account_data)

    data["account_balance"] = float(data["account_data"]["account"]["balance"])
    data["order_amount"] = data["account_balance"] * data["invest_ratio"] * data['margin_call_ratio']
    data["order_amount"] = int(np.floor(data["order_amount"]))
    data['order_num']    = data["order_amount"]

    return(data)
#...............................................................................................



#...............................................................................................
def make_long_order(data):
    data['order_val']           = data['order_num'] * 1       

    data['price_stop']          = data['ask'] - data['stop_loss_pip']            
    data['price_take_profit']   = data['ask'] + data['take_profit_pip']
    
    stopLossOnFill              = StopLossDetails(price=data['price_stop'])
    takeProfitOnFillOrder       = TakeProfitDetails(price=data['price_take_profit'])
    trailingStopLossOnFill      = TrailingStopLossDetails(distance=data['trailing_stop_pip'])

    ordr                        = MarketOrderRequest(instrument = data['instrument'],
                                                    units=data['order_val'],
                                                    stopLossOnFill=stopLossOnFill.data,
                                                    # trailingStopLossOnFill=trailingStopLossOnFill.data,
                                                    takeProfitOnFill=takeProfitOnFillOrder.data)

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
    data['order_val']           = data['order_num'] * -1                
    
    data['price_stop']          = data['bid'] + data['stop_loss_pip']            
    data['price_take_profit']   = data['bid'] - data['take_profit_pip']
    
    stopLossOnFill              = StopLossDetails(price=data['price_stop'])
    takeProfitOnFillOrder       = TakeProfitDetails(price=data['price_take_profit'])
    trailingStopLossOnFill      = TrailingStopLossDetails(distance=data['trailing_stop_pip'])

    ordr                        = MarketOrderRequest(instrument = data['instrument'],
                                                    units=data['order_val'],
                                                    stopLossOnFill=stopLossOnFill.data,
                                                    # trailingStopLossOnFill=trailingStopLossOnFill.data,
                                                    takeProfitOnFill=takeProfitOnFillOrder.data)

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
    data['to_order']            = None
    data['pl']                  = 0    
    data["take_profit_flg"]     = False

    return(data)
#...............................................................................................


#...............................................................................................
def close_short_order(data):
    data                        = check_for_open_orders(data)
    data_short                  = {"shortUnits": "ALL"}
    order_close_data            = positions.PositionClose(accountID=data['accountID'], instrument=data['instrument'], data=data_short)
    data['response_close']      = data['api'].request(order_close_data)
    data['to_order']            = None
    data['pl']                  = 0
    data["take_profit_flg"]     = False

    return(data)
#...............................................................................................



#...............................................................................................
def make_order(data):
    if not data['order_current_open']:
        if data['dir_change']:
            data = get_invest_details(data)
            
            if data['to_order'] == 'long':
                make_long_order(data)

            if data['to_order'] == 'short':
                make_short_order(data)

            data['dir_change'] = False
            
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