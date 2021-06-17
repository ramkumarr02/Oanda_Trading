from utils.packages import *
from utils.i_o import *


#...............................................................................................
def make_order(data):
    if not data['open_order']:
        if data['candle_color'] == 'green':
            data['order_ask_price'] = data['ask']
            data['open_order'] = True
            data['open_order_type'] = 'long'
            data['pl_positive'] = False
            
            if data["plot"]:
                data['buy_markers_x'].append(data['i_list'][-1])
                data['buy_markers_y'].append(data['ask'])
            
        elif data['candle_color'] == 'red':
            data['order_bid_price'] = data['bid']
            data['open_order'] = True
            data['open_order_type'] = 'short'
            data['pl_positive'] = False

            if data["plot"]:
                data['buy_markers_x'].append(data['i_list'][-1])
                data['buy_markers_y'].append(data['bid'])
                
    return(data)
#...............................................................................................

#...............................................................................................
def close_order(data):
    if data['open_order']:
        if data['open_order_type'] == 'long':
            if data['candle_color'] == 'red':
                data['close_bid_price'] = data['bid']
                data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 5)
                data['pl_list'].append(data['pl'])
                data['dt_list'].append(data['dt_val'])
                data['open_order'] = False
                data['close_type'].append(f'long-{data["avg_candle_size"]}')

                if data["plot"]:
                    data['sell_markers_x'].append(data['i_list'][-1])
                    data['sell_markers_y'].append(data['bid'])      
                
                create_report(data)         
            
        if data['open_order_type'] == 'short':
            if data['candle_color'] == 'green':
                data['close_ask_price'] = data['ask']
                data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 5)
                data['pl_list'].append(data['pl'])
                data['dt_list'].append(data['dt_val'])
                data['open_order'] = False
                data['close_type'].append(f'short-{data["avg_candle_size"]}')

                if data["plot"]:
                    data['sell_markers_x'].append(data['i_list'][-1])
                    data['sell_markers_y'].append(data['ask'])                  
                
                create_report(data)

    return(data)    
#...............................................................................................




#...............................................................................................
def stop_loss(data):
    if data['open_order']:

        if data['open_order_type'] == 'long':
            data['close_bid_price'] = data['bid']
            data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 5)

            if data['pl'] <= -data['avg_candle_size']:
                data['pl_list'].append(data['pl'])
                data['dt_list'].append(data['dt_val'])
                data['open_order'] = False
                data['close_type'].append(f'stop_loss-{data["avg_candle_size"]}')
                
                if data["plot"]:
                    data['sell_markers_x'].append(data['i_list'][-1])
                    data['sell_markers_y'].append(data['bid'])   

                create_report(data)               
                
        if data['open_order_type'] == 'short':
            data['close_ask_price'] = data['ask']
            data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 5)

            if data['pl'] <= -data['avg_candle_size']:
                data['pl_list'].append(data['pl'])
                data['dt_list'].append(data['dt_val'])
                data['open_order'] = False
                data['close_type'].append(f'stop_loss-{data["avg_candle_size"]}')
                
                if data["plot"]:
                    data['sell_markers_x'].append(data['i_list'][-1])
                    data['sell_markers_y'].append(data['ask'])  
                
                create_report(data)

    return(data)    
#...............................................................................................    


#...............................................................................................
def reverse_order(data):
    if data['open_order']:
        if data['dir_change']:
            # if data['angle_diff'] >= data['min_order_angle']:
            if data['open_order_type'] == 'long':
                if data['to_order'] == 'short':
                    data['close_bid_price'] = data['bid']
                    data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 5)
                    data['pl_list'].append(data['pl'])
                    data['dt_list'].append(data['dt_val'])
                    data['open_order'] = False
                    data['close_type'].append('sema_close')

                    if data["plot"]:
                        data['sell_markers_x'].append(data['i_list'][-1])
                        data['sell_markers_y'].append(data['bid'])      
                    
                    create_report(data)         
                
            if data['open_order_type'] == 'short':
                if data['to_order'] == 'long':
                    data['close_ask_price'] = data['ask']
                    data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 5)
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
def close_order_old_2(data):
    if data['open_order']:
        if data['dir_change']:
            if data['position'] < 0 and data['open_order_type'] == 'long' and data['sema_angle'] < -data['sema_close_order_angle']:
                data['close_bid_price'] = data['bid']
                data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 5)
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
                data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 5)
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
                data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 5)
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
                data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 5)
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
        if data['pl_positive'] == False:
            if data['open_order_type'] == 'short':
                if data['tick'] - data['lema'] >= 0 and data['sema_angle'] >= data['tick_close_angle']:
                    data['close_ask_price'] = data['ask']
                    data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 5)
                    data['pl_list'].append(data['pl'])
                    data['dt_list'].append(data['dt_val'])
                    data['open_order'] = False
                    data['close_type'].append('tick_close')
                    
                    if data["plot"]:
                        data['sell_markers_x'].append(data['i_list'][-1])
                        data['sell_markers_y'].append(data['ask'])  
                    
                    create_report(data)

            if data['open_order_type'] == 'long':
                if data['lema'] - data['tick'] >= 0 and data['sema_angle'] <= -data['tick_close_angle']:
                    data['close_bid_price'] = data['bid']
                    data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 5)
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


def pl_positive_check(data):
    if data['open_order']:
        if data['open_order_type'] == 'short':
            data['close_ask_price'] = data['ask']
            data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 5)
                
        if data['open_order_type'] == 'long':
            data['close_bid_price'] = data['bid']
            data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 5)

        if data['pl'] >= data['pl_move_trigger']:
            data['pl_positive'] = True
            if data['pl'] > 0.001:
                data['pl_move_min'] = data['pl_move_min'] - 0.001

    return(data)


def pl_move_close(data):
    if data['open_order']:

        if data['open_order_type'] == 'long':
            data['close_bid_price'] = data['bid']
            data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 5)

            if data['pl_positive']:
                if data['pl'] <= data['pl_move_min'] and data['sema_angle'] < data['pl_close_angle']:
                    data['pl_list'].append(data['pl'])
                    data['dt_list'].append(data['dt_val'])
                    data['open_order'] = False
                    data['close_type'].append('pl_move_close')
                    
                    if data["plot"]:
                        data['sell_markers_x'].append(data['i_list'][-1])
                        data['sell_markers_y'].append(data['bid'])   

                    create_report(data)               
                
        if data['open_order_type'] == 'short':
            data['close_ask_price'] = data['ask']
            data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 5)

            if data['pl_positive']:
                if data['pl'] <= data['pl_move_min'] and data['sema_angle'] > -data['pl_close_angle']:
                    data['pl_list'].append(data['pl'])
                    data['dt_list'].append(data['dt_val'])
                    data['open_order'] = False
                    data['close_type'].append('pl_move_close')
                    
                    if data["plot"]:
                        data['sell_markers_x'].append(data['i_list'][-1])
                        data['sell_markers_y'].append(data['ask'])  
                    
                    create_report(data)

    return(data)    



#...............................................................................................
def pl_positive_check(data):
    if data['open_order']:
        if data['open_order_type'] == 'short':
            data['close_ask_price'] = data['ask']
            data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 5)
                
        if data['open_order_type'] == 'long':
            data['close_bid_price'] = data['bid']
            data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 5)

        # if data['pl'] >= data['pl_move_trigger']:
        #     data['pl_positive'] = True
        #     if data['pl'] > data['pl_move_trail_trigger']:
        #         data['pl_move_min'] = data['pl'] * data['pl_move_trail_ratio']

        if data['pl'] >= data['pl_move_trail_trigger']:
            data['pl_positive'] = True
            data['pl_move_min'] = data['pl'] * data['pl_move_trail_ratio']
            data['pl_move_min'] = max(data['pl_move_min'], data['pl'] - data['pl_min'])

    return(data)


def pl_move_close(data):
    if data['open_order']:

        if data['open_order_type'] == 'long':
            data['close_bid_price'] = data['bid']
            data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 5)

            if data['pl_positive']:
                if data['pl'] <= data['pl_move_min']: 
                    data['pl_list'].append(data['pl'])
                    data['dt_list'].append(data['dt_val'])
                    data['open_order'] = False
                    data['to_order'] = None
                    data['close_type'].append('pl_move_close')
                    # data['order_types'].append(data['open_order_type'])
                    
                    if data["plot"]:
                        data['sell_markers_x'].append(data['i_list'][-1])
                        data['sell_markers_y'].append(data['bid'])   

                    create_report(data)               
                
        if data['open_order_type'] == 'short':
            data['close_ask_price'] = data['ask']
            data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 5)

            if data['pl_positive']:
                if data['pl'] <= data['pl_move_min']:
                    data['pl_list'].append(data['pl'])
                    data['dt_list'].append(data['dt_val'])
                    data['open_order'] = False
                    data['to_order'] = None
                    data['close_type'].append('pl_move_close')
                    # data['order_types'].append(data['open_order_type'])
                    
                    if data["plot"]:
                        data['sell_markers_x'].append(data['i_list'][-1])
                        data['sell_markers_y'].append(data['ask'])  
                    
                    create_report(data)


    return(data)    
#...............................................................................................    