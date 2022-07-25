from utils.packages import *
from utils.i_o import *
from utils.dir_slope import *


# ...............................................................................................

def calculate_total_profit(data):
        
    data['pl'] = 0
    data['pl_list'] = []
    
    for i in data['identified_points']:
        data['up_val']      = max(data['df_ohlc']['high'][i+1:i+1+data['pl_candles']]) - data['df_ohlc']['open'][i+1]
        data['down_val']    = data['df_ohlc']['open'][i+1] - min(data['df_ohlc']['low'][i+1:i+1+data['pl_candles']]) 
                
        if data['test_type'] == 'up':
    
            if data['up_val'] > data['down_val']:                
                data['pl'] = data['up_val'] - data['spread_cost']
                data['pl_list'].append(data['pl'])
            elif data['up_val'] < data['down_val']:                
                data['pl'] = -data['down_val'] - data['spread_cost']
                data['pl_list'].append(data['pl'])


        if data['test_type'] == 'down':
            if data['down_val'] > data['up_val']:                
                data['pl'] = data['down_val'] - data['spread_cost']
                data['pl_list'].append(data['pl'])
                
            elif data['down_val'] < data['up_val']:                
                data['pl'] = -data['up_val'] - data['spread_cost']
                data['pl_list'].append(data['pl'])
            
    x = pd.Series(data['pl_list']).dropna()
    pls = len(x[x>0])
    losses = len(x[x<0])

    print(f"Total pl            : {sum(x)}")
    print(f"Num of Transactions : {len(x)}")
    print(f'pl Transactions     : {pls}')
    print(f'Loss Transactions   : {losses}')

    return(data)


# ...............................................................................................
def dynamic_make_order(data):
    for order_num_i in range(data['num_of_switch_orders']):    
        data['order_num_i'] = order_num_i
        if order_num_i == 0:
            if data['open_order'] == order_num_i:
                if data['to_order'] == 'long':                
                    data['open_order'] = order_num_i + 1
                    data['start_prices'] = {}
                    data = make_long_order(data)

                elif data['to_order'] == 'short':
                    data['open_order'] = order_num_i + 1
                    data['start_prices'] = {}
                    data = make_short_order(data)

        elif order_num_i > 0:
            if data['open_order'] == order_num_i:
                try:
                    data['orders_list'][order_num_i]['pl']
                    data['pl_available'] = True
                except:
                    data['pl_available'] = False

                if data['pl_available']:
                    data['stop_loss_pip'] = min(data['min_stop_loss_pip'], -data['h_l_gap'] * data['stop_loss_multiplier'])
                    if data['orders_list'][order_num_i]['open_order_type'] == 'short':
                        if data['orders_list'][order_num_i]['pl'] < 0:
                            if data['to_order'] == 'long':
                                data['open_order'] = order_num_i + 1
                                data = make_long_order(data)
                             
                    if data['orders_list'][order_num_i]['open_order_type'] == 'long':
                        if data['orders_list'][order_num_i]['pl'] < 0:
                            if data['to_order'] == 'short':
                                data['open_order'] = order_num_i + 1
                                data = make_short_order(data)

                    if data['orders_list'][order_num_i]['pl'] < data['stop_loss_pip']:
                        if data['orders_list'][order_num_i]['open_order_type'] == 'long':
                            if data['tick_angle'] < -data['min_order_angle']:
                                data['open_order'] = order_num_i + 1
                                data = make_short_order(data)

                        if data['orders_list'][order_num_i]['open_order_type'] == 'short':
                            if data['tick_angle'] > data['min_order_angle']:
                                data['open_order'] = order_num_i + 1
                                data = make_long_order(data)

    return(data)
#...............................................................................................
def close_all_orders(data):
    
    if data['open_order'] > 1:
        if data['orders_list']['total_pl'] >= data['all_close_min_pip']:       

            data['pl_positive']         = False
            data['pl_move_min']         = 0
            data['slema_check_flag'] = False
            #------------------------
            data['df']['close_type'].iloc[data['i']]    = 'all_close'
            data['df']['all_close'].iloc[data['i']]    = data['tick']  
            data['df']['pl'].iloc[data['i']]            = data['orders_list']['total_pl']
            data['df']['order_side'].iloc[data['i']]    = 'all'
            data['df']['order_size'].iloc[data['i']]    = data['order_size']
            data['df']['touched_line'].iloc[data['i']]  = data['ordered_touched_line']
            #------------------------
            data['orders_list'] = {}
            data['open_order'] = 0
            data['to_order']	= None
            #------------------------
            create_report(data)

        if data['open_order'] == data['num_of_switch_orders']:
            if data['orders_list']['total_pl'] < data['stop_loss_pip']/2:
                if data['orders_list'][data['num_of_switch_orders']]['pl'] < data['stop_loss_pip']/2:
                    data['pl_positive']         = False
                    data['pl_move_min']         = 0
                    data['slema_check_flag'] = False
                    #------------------------
                    data['df']['close_type'].iloc[data['i']]    = 'all_close'
                    data['df']['all_close'].iloc[data['i']]    = data['tick']  
                    data['df']['pl'].iloc[data['i']]            = data['orders_list']['total_pl']
                    data['df']['order_side'].iloc[data['i']]    = 'all'
                    data['df']['order_size'].iloc[data['i']]    = data['order_size']
                    data['df']['touched_line'].iloc[data['i']]  = data['ordered_touched_line']
                    #------------------------
                    data['orders_list'] = {}
                    data['open_order'] = 0
                    data['to_order']	= None
                    #------------------------
                    create_report(data)

    return(data)
#...............................................................................................
#...............................................................................................
def calculate_multi_pl(data):
    data['orders_list']['total_pl'] = []
    data['orders_list']['pl_list'] = []

    for i in range(1, data['open_order']+1):
        if i == 1:
            data['order_size'] = 1
        else:
            data['order_size'] = 2
            # data['order_size'] = i * 5
            # data['order_size'] = (i-1) * data['order_multiplier']
            # data['order_size'] = i

        if data['orders_list'][i]['open_order_type'] == 'long':
            data['orders_list'][i]['pl'] = np.round((data['bid'] - data['orders_list'][i]['ask']) * data['order_size'], 5)            
            data['orders_list']['pl_list'].append(data['orders_list'][i]['pl'])

        if data['orders_list'][i]['open_order_type'] == 'short':
            data['orders_list'][i]['pl'] = np.round((data['orders_list'][i]['bid'] - data['ask']) * data['order_size'], 5)
            data['orders_list']['pl_list'].append(data['orders_list'][i]['pl'])
    
    data['orders_list']['total_pl'] = np.round(sum(data['orders_list']['pl_list']), 5)

    data['open_order_temp_list'].append(data['open_order'])
    data['pl_temp_list'].append(data['orders_list']['total_pl'])
    # if data['orders_list']['total_pl'] <= -0.31915:
    #     print(data['orders_list'])
    #     sys.exit()

    return(data) 
#...............................................................................................
# #...............................................................................................
# def make_order(data):
#     if not data['open_order']:
#         if data['to_order'] == 'long':
#             data = make_long_order(data)

#         elif data['to_order'] == 'short':
#             data = make_short_order(data)

#     return(data)
# #...............................................................................................

# #...............................................................................................
# def calculate_pl(data):
#     if data['open_order_type'] == 'long':
#         data['close_bid_price'] = data['bid']
#         data['pl'] = np.round(data['close_bid_price'] - data['order_ask_price'], 5)

#     if data['open_order_type'] == 'short':
#         data['close_ask_price'] = data['ask']
#         data['pl'] = np.round(data['order_bid_price'] - data['close_ask_price'], 5)

#     return(data) 
# #...............................................................................................

# ...............................................................................................
def simple_stop_loss(data):   
    data['stop_loss_pip']               = min(data['min_stop_loss_pip'], -data['h_l_gap'] * data['stop_loss_multiplier'])

    if data['open_order']:
        if data['pl'] <= data['stop_loss_pip']:
            if data['open_order_type'] == 'long':
                data['stop_text'] = 'simple_stop'
                data = close_long_order(data)
                    
            if data['open_order_type'] == 'short':                
                data['stop_text'] = 'simple_stop'
                data = close_short_order(data)
    return(data)   
# ...............................................................................................   

#...............................................................................................
#...............................................................................................
def slema_positive_check(data):
    if data['open_order'] == 1:
        if data['slema_check_flag']:
            if data['orders_list'][1]['open_order_type'] == 'long':
                if data['sema'] > data[data['ema_type']]:
                    data['slema_positive'] = True
                    data['slema_check_flag'] = False
                else:
                    data['slema_positive'] = False

            if data['orders_list'][1]['open_order_type'] == 'short':
                if data['sema'] < data[data['ema_type']]:
                    data['slema_positive'] = True
                    data['slema_check_flag'] = False
                else:
                    data['slema_positive'] = False

    return(data)
#...............................................................................................


def simple_slema_move_close(data):
    if data['open_order'] == 1:
        if data['slema_positive']: 
            data['pl'] = data['orders_list'][1]['pl']
            if data['pl'] > 0:            
                if data['orders_list'][1]['open_order_type'] == 'long':
                    if data['sema'] < data[data['ema_type']]:
                        data['stop_text'] = ('simple_slema_move_close')
                        # data['i'] = 1
                        data = close_long_order(data)       
            
                if data['orders_list'][1]['open_order_type'] == 'short':
                    if data['sema'] > data[data['ema_type']]:                
                        data['stop_text'] = ('simple_slema_move_close')
                        # data['i'] = 1
                        data = close_short_order(data)  

    return(data) 
#...............................................................................................


#...............................................................................................
def make_long_order(data):
    data['order_ask_price']     = data['ask']
    #------------------------
    # data['open_order']          = True
    data['to_order']	        = None
    data['open_order_type']     = 'long'
    data['slema_check_flag']    = True
    #------------------------
    data['pl_positive']         = False
    data['pl_move_min']         = 0
    #------------------------
    data['orders_list'][data['open_order']] = {}
    data['orders_list'][data['open_order']]['open_order_type'] = data['open_order_type']
    data['orders_list'][data['open_order']]['ask'] = data['ask'] 
    #------------------------
    data['ordered_touched_line']                = data['touched_line']
    data['df']['touched_line'].iloc[data['i']]  = data['ordered_touched_line']
    data['df']['order_side'].iloc[data['i']]    = 'long'
    data['df']['long_open'].iloc[data['i']]     = data['ask']
    data['df']['order_num'].iloc[data['i']]    = data['open_order']

    return(data)


def make_short_order(data):
    data['order_bid_price']     = data['bid']
    #------------------------
    # data['open_order']          = True
    data['to_order']	        = None
    data['slema_check_flag']    = True
    data['open_order_type']     = 'short'
    #------------------------
    data['pl_positive']         = False
    data['pl_move_min']         = 0
    #------------------------
    data['orders_list'][data['open_order']] = {}
    data['orders_list'][data['open_order']]['open_order_type'] = data['open_order_type']
    data['orders_list'][data['open_order']]['bid'] = data['bid'] 
    #------------------------
    data['ordered_touched_line']                = data['touched_line']
    data['df']['touched_line'].iloc[data['i']]  = data['ordered_touched_line']
    data['df']['order_side'].iloc[data['i']]    = 'short'
    data['df']['short_open'].iloc[data['i']]    = data['bid']
    data['df']['order_num'].iloc[data['i']]    = data['open_order']
    return(data)


def close_long_order(data):
    data['open_order'] = 0
    data['to_order']	= None
    #------------------------
    data['pl_positive']         = False
    data['pl_move_min']         = 0
    data['slema_check_flag'] = False
    #------------------------
    data['df']['close_type'].iloc[data['i']]    = data['stop_text']
    data['df']['long_close'].iloc[data['i']]    = data['bid']  
    data['df']['pl'].iloc[data['i']]            = data['pl']
    data['df']['order_side'].iloc[data['i']]    = 'long'
    data['df']['order_size'].iloc[data['i']]    = data['order_size']
    data['df']['touched_line'].iloc[data['i']]  = data['ordered_touched_line']
    #------------------------
    create_report(data)


    return(data)


def close_short_order(data):
    data['open_order'] = 0
    data['to_order']	= None
    #------------------------
    data['pl_positive'] = False
    data['pl_move_min'] = 0
    data['slema_check_flag'] = False
    #------------------------
    data['df']['close_type'].iloc[data['i']]    = data['stop_text']
    data['df']['short_close'].iloc[data['i']]   = data['ask']  
    data['df']['pl'].iloc[data['i']]            = data['pl']
    data['df']['order_side'].iloc[data['i']]    = 'short'
    data['df']['order_size'].iloc[data['i']]    = data['order_size']
    data['df']['touched_line'].iloc[data['i']]  = data['ordered_touched_line']
    #------------------------
    create_report(data)
    return(data)


#...............................................................................................
#...............................................................................................
#...............................................................................................
#...............................................................................................
#...............................................................................................
#...............................................................................................
#...............................................................................................
#...............................................................................................