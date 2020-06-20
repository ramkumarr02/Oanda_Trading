from utils.packages import *
from utils.tools import *

def run_order_engine(api, accountID, instrument, direction, profit_target_num, loss_limit_num, price_allowed_buff, min_trans_num, pip_size, loss_limits):    
    
    params = {'instruments': instrument}
    r = pricing.PricingStream(accountID=accountID, params=params)
    rv = api.request(r)
    order_flag = 'not_ordered'
    max_price = 0
    profit_moves = 0
    
    profit_target = profit_target_num * pip_size
    loss_limit = loss_limit_num * pip_size
    price_allowed_buffer = price_allowed_buff * pip_size

    loss_limits_dict = get_loss_limits(min_trans_num, loss_limits)
    print('Running OE : ', min_trans_num, loss_limits)
    
    for i, resp in tqdm(enumerate(rv)):        
        open_positions_r = positions.OpenPositions(accountID=accountID)
        open_positions_rv = api.request(open_positions_r)
        open_positions = len(open_positions_rv['positions'])        
        resp_type = resp['type']       
        
        if resp_type == 'HEARTBEAT': # Heart beat response to keep the api connection alive (Avoid timeout)
            pass
        
        elif resp_type == 'PRICE' and order_flag == 'not_ordered': # Check if we are yet to make the order               
            date_val, time_val, time_fraction = get_date_time(resp) # Get time stamp for reference            
            sell_price, buy_price, spread, tick_price = get_prices(resp) # Get prices from the response                      

            if direction == 'positive':
                order_type = 'long'
                units = +1
                #stop_price = sell_price - loss_limit
                stop_price = buy_price - loss_limit                
                make_order_log = make_order(accountID, stop_price, instrument, units, api)
                order_flag = 'ordered'

            elif direction == 'negative':
                order_type = 'short'
                units = -1                    
                #stop_price = buy_price + loss_limit
                stop_price = sell_price + loss_limit                
                make_order_log = make_order(accountID, stop_price, instrument, units, api)                    
                order_flag = 'ordered'

        elif resp_type == 'PRICE' and order_flag == 'ordered' and open_positions == 1: # Check if we have made the order
            sell_price, buy_price, spread, tick_price = get_prices(resp) # Get prices from the response                                      

            if order_type == 'long':     
                ordered_buy_price = float(make_order_log['orderFillTransaction']['fullPrice']['asks'][0]['price'])
                profit = sell_price - ordered_buy_price 
                
                max_price = max(sell_price, max_price)
                buffered_max_price = max_price - price_allowed_buffer
                
                if profit > 0:
                    profit_moves += 1
                elif profit < 0:
                    profit_moves -= 1                    
                    
                if profit >= profit_target and sell_price <= buffered_max_price:
                    print(f'buffered_max_price : {buffered_max_price} sell_price : {sell_price}')
                    close_order_log = close_order(accountID, order_type ,instrument, api)
                    order_flag = 'closed'
                    close_reason = "Take_profit"
                    
                if i > min_trans_num and profit_moves < 0 and order_flag != 'closed':
                    close_order_log = close_order(accountID, order_type ,instrument, api)
                    order_flag = 'closed'           
                    close_reason = "Min trans moves"

                for _, val in enumerate(list(loss_limits.keys())):
                    if profit_moves <= loss_limits_dict[val]['half_min_trans_num'] and order_flag != 'closed' and profit >= loss_limits_dict[val]['max_loss']:
                        close_order_log = close_order(accountID, order_type ,instrument, api)
                        order_flag = 'closed'           
                        close_reason = f'{val} Neg half min trans'
                    
                    
            if order_type == 'short':     
                ordered_sell_price = float(make_order_log['orderFillTransaction']['fullPrice']['bids'][0]['price'])
                profit = ordered_sell_price - buy_price                

                min_price = min(sell_price, max_price)
                buffered_min_price = min_price + price_allowed_buffer
                
                if profit > 0:
                    profit_moves += 1
                elif profit < 0:
                    profit_moves -= 1                    
                
                if profit >= profit_target and sell_price >= buffered_min_price:
                    print(f'buffered_min_price : {buffered_min_price} sell_price : {sell_price}')
                    close_order_log = close_order(accountID, order_type ,instrument, api)
                    order_flag = 'closed'
                    close_reason = "Take_profit"
                    
                    
                if i > min_trans_num and profit_moves < 0 and order_flag != 'closed':
                    close_order_log = close_order(accountID, order_type ,instrument, api)
                    order_flag = 'closed' 
                    close_reason = "Min trans moves"

                    
                for _, val in enumerate(list(loss_limits.keys())):
                    if profit_moves <= loss_limits_dict[val]['half_min_trans_num'] and order_flag != 'closed' and profit >= loss_limits_dict[val]['max_loss']:
                        close_order_log = close_order(accountID, order_type ,instrument, api)
                        order_flag = 'closed'           
                        close_reason = f'{val} Neg half min trans'

                    
        elif resp_type == 'PRICE' and (order_flag == 'closed' or open_positions == 0): # Check if we have made the order
            try:
                if order_flag != 'closed':
                    close_order_log = 'stop_loss_trigger'
                    close_reason = 'stop_loss'                    
                r.terminate(message = "")
                
            except:
                pass

    return(make_order_log, close_order_log, i, close_reason)