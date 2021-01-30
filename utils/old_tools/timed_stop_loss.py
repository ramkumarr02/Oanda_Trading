from utils.packages import *

#--------------------------------------------------------------------------------------------------------------------------
def timed_stop_loss(data):
    #global data
    
    if data['order_current_open'] == 'long':
        data['price_order_ask']      = float(data['positions_info']['positions'][0]['long']['averagePrice'])        
        data['long_loss_val'] = data['price_bid'] - data['price_order_ask']
        
        data['full_loss_list'].append(data['long_loss_val'])
        data['full_loss_list_len'] = len(data['full_loss_list'])
        
        data['long_loss_list'].append(data['long_loss_val'])        
        data['long_loss_list_len'] = len(data['long_loss_list'])        
        if data['long_loss_list_len'] > data["num_of_ticks"]:
            data['long_loss_list'].popleft()
            data['long_loss_list_len'] = len(data['long_loss_list'])
                
        data['long_loss_lema'] = list(pd.DataFrame(list(data['long_loss_list'])).ewm(span=data['long_loss_list_len']).mean()[0])[data['long_loss_list_len'] - 1]        
        
        if data['full_loss_list_len'] >= data['loss_iter_limit']:                    
            if data['long_loss_lema'] <= data['timed_loss_limit'] and data['order_create'] != 'long':
                data = close_long_orders(data)
                data = reset_data(data)
                print(1)
                data = check_for_open_orders(data)
                data['num_timed_stop_loss'] = data['num_timed_stop_loss'] + 1         

        if data['long_loss_lema'] <= data['max_lema_loss']:
            data = close_long_orders(data)
            data = reset_data(data)
            print(2)
            data = check_for_open_orders(data)
            data['num_timed_stop_loss'] = data['num_timed_stop_loss'] + 1
                
    if data['order_current_open'] == 'short':
        data['price_order_bid'] = float(data['positions_info']['positions'][0]['short']['averagePrice'])        
        data['short_loss_val'] = data['price_order_bid'] - data['price_ask']    
        
        data['full_loss_list'].append(data['short_loss_val'])
        data['full_loss_list_len'] = len(data['full_loss_list'])        
        
        data['short_loss_list'].append(data['short_loss_val'])
        data['short_loss_list_len'] = len(data['short_loss_list'])        
        if data['short_loss_list_len'] > data["num_of_ticks"]:
            data['short_loss_list'].popleft()
            data['short_loss_list_len'] = len(data['short_loss_list'])
        
        data['short_loss_lema'] = list(pd.DataFrame(list(data['short_loss_list'])).ewm(span=data['short_loss_list_len']).mean()[0])[data['short_loss_list_len'] - 1]
        
        if data['full_loss_list_len'] >= data['loss_iter_limit']:        
            if data['short_loss_lema'] <= data['timed_loss_limit'] and data['order_create'] != 'short':
                data = close_short_orders(data)
                data = reset_data(data)
                print(3)
                data = check_for_open_orders(data)      
                data['num_timed_stop_loss'] = data['num_timed_stop_loss'] + 1
                
        if data['short_loss_lema'] <= data['max_lema_loss']:
            data = close_short_orders(data)
            data = reset_data(data)
            print(4)
            data = check_for_open_orders(data)
            data['num_timed_stop_loss'] = data['num_timed_stop_loss'] + 1            
                
    return(data)
#==========================================================================================================================