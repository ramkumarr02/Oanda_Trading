from utils.packages import *

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