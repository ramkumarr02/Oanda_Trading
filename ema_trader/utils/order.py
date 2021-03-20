from utils.packages import *



#...............................................................................................
def make_order(data):
    if not data['open_order']:
        if data['dir_change']:
            if data['position'] > 0 and data['angle'] >= data['mandatory_order_angle']:
                data['order_ask_price'] = data['ask']
                data['open_order'] = True
                data['open_order_type'] = 'long'
                
                data['buy_markers_x'].append(data['i_list'][-1])
                data['buy_markers_y'].append(data['ask'])
                
            elif data['position'] < 0 and data['angle'] <= -data['mandatory_order_angle']:
                data['order_bid_price'] = data['bid']
                data['open_order'] = True
                data['open_order_type'] = 'short'
                
                data['buy_markers_x'].append(data['i_list'][-1])
                data['buy_markers_y'].append(data['bid'])
                
    return(data)
#...............................................................................................



#...............................................................................................
def close_order(data):
    if data['open_order']:
        if data['dir_change']:
            if data['position'] < 0 and data['angle'] <= -data['mandatory_order_angle']:
                data['close_bid_price'] = data['bid']
                data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 4)
                data['pl_list'].append(data['pl'])
                data['dt_list'].append(data['dt_val'])
                data['open_order'] = False
                
                data['sell_markers_x'].append(data['i_list'][-1])
                data['sell_markers_y'].append(data['bid'])               
                
            elif data['position'] > 0 and data['angle'] >= data['mandatory_order_angle']:
                data['close_ask_price'] = data['ask']
                data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 4)
                data['pl_list'].append(data['pl'])
                data['dt_list'].append(data['dt_val'])
                data['open_order'] = False
                
                data['sell_markers_x'].append(data['i_list'][-1])
                data['sell_markers_y'].append(data['ask'])                  
                
    return(data)    
#...............................................................................................



#...............................................................................................
def angle_close(data):
    if data['open_order']:
        if data['open_order_type'] == 'short':
            if data['lema'] - data['tick'] <= 0.0002 and data['angle'] >= data['close_angle']:
                data['close_ask_price'] = data['ask']
                data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 4)
                data['pl_list'].append(data['pl'])
                data['dt_list'].append(data['dt_val'])
                data['open_order'] = False
                
                data['sell_markers_x'].append(data['i_list'][-1])
                data['sell_markers_y'].append(data['ask'])  
                
        if data['open_order_type'] == 'long':
            if data['tick'] - data['lema'] >= 0.0002 and data['angle'] <= -data['close_angle']:
                data['close_bid_price'] = data['bid']
                data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 4)
                data['pl_list'].append(data['pl'])
                data['dt_list'].append(data['dt_val'])
                data['open_order'] = False
                
                data['sell_markers_x'].append(data['i_list'][-1])
                data['sell_markers_y'].append(data['bid'])                  
                
    return(data)    
#...............................................................................................



#...............................................................................................
def tick_close(data):
    if data['open_order']:
        if data['open_order_type'] == 'short':
            if data['tick'] - data['lema'] >= 0 and data['angle'] >= data['mandatory_order_angle']:
                data['close_ask_price'] = data['ask']
                data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 4)
                data['pl_list'].append(data['pl'])
                data['dt_list'].append(data['dt_val'])
                data['open_order'] = False
                
                data['sell_markers_x'].append(data['i_list'][-1])
                data['sell_markers_y'].append(data['ask'])  
                
        if data['open_order_type'] == 'long':
            if data['lema'] - data['tick'] >= 0 and data['angle'] <= -data['mandatory_order_angle']:
                data['close_bid_price'] = data['bid']
                data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 4)
                data['pl_list'].append(data['pl'])
                data['dt_list'].append(data['dt_val'])
                data['open_order'] = False
                
                data['sell_markers_x'].append(data['i_list'][-1])
                data['sell_markers_y'].append(data['bid'])                  
                
    return(data)    
#...............................................................................................    