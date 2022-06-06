from utils.packages import *
from utils.i_o import *
from utils.dir_slope import *


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
                    if data['orders_list'][1]['open_order_type'] == 'short':
                        if data['orders_list'][order_num_i]['pl'] < data['loss_switch_pl_pip']:
                            # data['first_type'] = 'short'
                            # data = get_order_list(data)
                            data['open_order'] = order_num_i + 1
                            # if data['forward_order_list'][data['open_order']] == 'long':
                            data = make_long_order(data)
                            # if data['forward_order_list'][data['open_order']] == 'short':
                            #     data = make_short_order(data)
                            # if data['ask'] >= 1.2211 and data['open_order'] == 19:
                            #     sys.exit()

            
                    if data['orders_list'][1]['open_order_type'] == 'long':
                        if data['orders_list'][order_num_i]['pl'] < data['loss_switch_pl_pip']:
                            # data['first_type'] = 'long'
                            # data = get_order_list(data)
                            data['open_order'] = order_num_i + 1
                            # if data['forward_order_list'][data['open_order']] == 'long':
                                # data = make_long_order(data)
                            # if data['forward_order_list'][data['open_order']] == 'short':
                            data = make_short_order(data)
                            # print(4, data['start_prices'])

    return(data)

#...............................................................................................
def make_order(data):
    if data['open_order'] == 0:
        if data['to_order'] == 'long':                
            data['open_order'] = 1
            data = make_long_order(data)

        elif data['to_order'] == 'short':
            data['open_order'] = 1
            data = make_short_order(data)

    elif data['open_order'] == 1:
        if data['open_order_type'] == 'short':
            if data['to_order'] == 'long':                
                if data['orders_list'][1]['pl'] < 0:
                    data['open_order'] = 2
                    data = make_long_order(data)

        if data['open_order_type'] == 'long':
            if data['to_order'] == 'short':
                if data['orders_list'][1]['pl'] < 0:
                    data['open_order'] = 2
                    data = make_short_order(data)

    elif data['open_order'] == 2:
        if data['open_order_type'] == 'short':
            if data['to_order'] == 'long':                
                if data['orders_list'][2]['pl'] < 0:
                    data['open_order'] = 3
                    data = make_long_order(data)

        if data['open_order_type'] == 'long':
            if data['to_order'] == 'short':
                if data['orders_list'][2]['pl'] < 0:
                    data['open_order'] = 3
                    data = make_short_order(data)

    elif data['open_order'] == 3:
        if data['open_order_type'] == 'short':
            if data['to_order'] == 'long':                
                if data['orders_list'][3]['pl'] < 0:
                    data['open_order'] = 4
                    data = make_long_order(data)

        if data['open_order_type'] == 'long':
            if data['to_order'] == 'short':
                if data['orders_list'][3]['pl'] < 0:
                    data['open_order'] = 4
                    data = make_short_order(data)                    

    # # -----------------------------------------------------------------
    # if data['open_order'] == 4:
    #     if data['open_order_type'] == 'short':
    #         if data['to_order'] == 'long':                
    #             if data['orders_list'][4]['pl'] < 0:
    #                 data['open_order'] = 5
    #                 data = make_long_order(data)

    #     if data['open_order_type'] == 'long':
    #         if data['to_order'] == 'short':
    #             if data['orders_list'][4]['pl'] < 0:
    #                 data['open_order'] = 5
    #                 data = make_short_order(data)

    # if data['open_order'] == 5:
    #     if data['open_order_type'] == 'short':
    #         if data['to_order'] == 'long':                
    #             if data['orders_list'][5]['pl'] < 0:
    #                 data['open_order'] = 6
    #                 data = make_long_order(data)

    #     if data['open_order_type'] == 'long':
    #         if data['to_order'] == 'short':
    #             if data['orders_list'][5]['pl'] < 0:
    #                 data['open_order'] = 6
    #                 data = make_short_order(data)

    # if data['open_order'] == 6:
    #     if data['open_order_type'] == 'short':
    #         if data['to_order'] == 'long':                
    #             if data['orders_list'][6]['pl'] < 0:
    #                 data['open_order'] = 7
    #                 data = make_long_order(data)

    #     if data['open_order_type'] == 'long':
    #         if data['to_order'] == 'short':
    #             if data['orders_list'][6]['pl'] < 0:
    #                 data['open_order'] = 7
    #                 data = make_short_order(data)

    # if data['open_order'] == 7:
    #     if data['open_order_type'] == 'short':
    #         if data['to_order'] == 'long':                
    #             if data['orders_list'][7]['pl'] < 0:
    #                 data['open_order'] = 8
    #                 data = make_long_order(data)

    #     if data['open_order_type'] == 'long':
    #         if data['to_order'] == 'short':
    #             if data['orders_list'][7]['pl'] < 0:
    #                 data['open_order'] = 8
    #                 data = make_short_order(data)

    # if data['open_order'] == 8:
    #     if data['open_order_type'] == 'short':
    #         if data['to_order'] == 'long':                
    #             if data['orders_list'][8]['pl'] < 0:
    #                 data['open_order'] = 9
    #                 data = make_long_order(data)

    #     if data['open_order_type'] == 'long':
    #         if data['to_order'] == 'short':
    #             if data['orders_list'][8]['pl'] < 0:
    #                 data['open_order'] = 9
    #                 data = make_short_order(data)

    # if data['open_order'] == 9:
    #     if data['open_order_type'] == 'short':
    #         if data['to_order'] == 'long':                
    #             if data['orders_list'][9]['pl'] < 0:
    #                 data['open_order'] = 10
    #                 data = make_long_order(data)

    #     if data['open_order_type'] == 'long':
    #         if data['to_order'] == 'short':
    #             if data['orders_list'][9]['pl'] < 0:
    #                 data['open_order'] = 10
    #                 data = make_short_order(data)
    # # -----------------------------------------------------------------

    return(data)
#...............................................................................................
def close_all_orders(data):
    
    if data['open_order'] > 1:
        if data['orders_list']['total_pl'] >= 0.0001:            
            for i in range(1, data['open_order']+1):
                if data['orders_list'][i]['open_order_type'] == 'long':   
                    data['pl'] = data['orders_list'][i]['pl']
                    data['close_type_val'] = ('all_close')
                    data['i'] = i
                    data = close_long_order(data)

                elif data['orders_list'][i]['open_order_type'] == 'short':
                    data['pl'] = data['orders_list'][i]['pl']
                    data['i'] = i
                    data['close_type_val'] = ('all_close')
                    data = close_short_order(data)

            data['open_order'] = 0
            data['orders_list'] = {}

    return(data)
#...............................................................................................
# def close_half_orders(data):

#     if data['open_order'] > 1:
#         if data['orders_list']['total_pl'] >= 0.0001:            
#             data['before_orders_list'] = data['orders_list']
#             for i in range(1, data['open_order']+1):
#                 if data['orders_list'][i]['pl'] < 0:
#                     if data['orders_list'][i]['open_order_type'] == 'long':   
#                         data['pl'] = data['orders_list'][i]['pl']
#                         data['close_type_val'] = ('all_close')
#                         data['open_order'] = i
#                         data = close_long_order(data)

#                     elif data['orders_list'][i]['open_order_type'] == 'short':
#                         data['pl'] = data['orders_list'][i]['pl']
#                         data['close_type_val'] = ('all_close')
#                         data['open_order'] = i
#                         data = close_short_order(data)

#             data['positions_half_closed'] = True
#             data = get_open_direction(data)
#             data['slema_check_flag'] =  True
                
#     return(data)

# #...............................................................................................
# def half_slema_positive_check(data):
#     if data['positions_half_closed']:
#         if data['slema_check_flag']:
#             if data['open_direction'] == 'long':
#                 if data['sema'] > data['slema']:
#                     data['slema_positive'] = True
#                     data['slema_check_flag'] = False
#                 else:
#                     data['slema_positive'] = False

#             if data['open_direction'] == 'short':
#                 if data['sema'] < data['slema']:
#                     data['slema_positive'] = True
#                     data['slema_check_flag'] = False
#                 else:
#                     data['slema_positive'] = False

#     return(data)
# #...............................................................................................

# def half_slema_move_close(data):
#     if data['positions_half_closed']:
#         if data['slema_positive']: 
#             if data['open_direction_pl'] > 0:        

#                 if data['open_direction'] == 'long':
#                     if data['sema'] < data['slema']:
#                         data['close_type_val'] = ('half_slema_move_close')              
            
#                         for i in range(1, data['open_order']+1):
#                             if data['orders_list'][i]['status'] == 'open':
#                                 data['pl'] = data['orders_list'][i]['pl']
#                                 data['open_order'] = i
#                                 data = close_long_order(data)
#                         data['open_order'] = 0
#                         data['positions_half_closed'] = False

#                 if data['open_direction'] == 'short':
#                     if data['sema'] > data['slema']:                
#                         data['close_type_val'] = ('half_slema_move_close')
#                         for i in range(1, data['open_order']+1):
#                             if data['orders_list'][i]['status'] == 'open':
#                                 data['pl'] = data['orders_list'][i]['pl']
#                                 data['open_order'] = i
#                                 data = close_long_order(data)
#                         data['open_order'] = 0
#                         data['positions_half_closed'] = False

#     return(data) 
# #...............................................................................................


# #...............................................................................................

#...............................................................................................
def slema_positive_check(data):
    if data['open_order'] == 1:
        if data['slema_check_flag']:
            if data['orders_list'][1]['open_order_type'] == 'long':
                if data['sema'] > data['slema']:
                    data['slema_positive'] = True
                    data['slema_check_flag'] = False
                else:
                    data['slema_positive'] = False

            if data['orders_list'][1]['open_order_type'] == 'short':
                if data['sema'] < data['slema']:
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
                    if data['sema'] < data['slema']:
                        data['close_type_val'] = ('simple_slema_move_close')
                        data['i'] = 1
                        data = close_long_order(data)       
            
                if data['orders_list'][1]['open_order_type'] == 'short':
                    if data['sema'] > data['slema']:                
                        data['close_type_val'] = ('simple_slema_move_close')
                        data['i'] = 1
                        data = close_short_order(data)  

    return(data) 
#...............................................................................................
def calculate_pl(data):
    data['orders_list']['total_pl'] = []
    data['orders_list']['pl_list'] = []

    for i in range(1, data['open_order']+1):
        if i == 1:
            data['order_size'] = 1
        else:
            # data['order_size'] = 2
            data['order_size'] = i

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

#...............................................................................................
def make_long_order(data):
    data['order_ask_price'] = data['ask']
    data['start_prices'][data['open_order']] = data['ask']
    data['open_order_type'] = 'long'
    data['start_dt_list'].append(data['dt_val'])
    data['slema_check_flag'] = True
    data['orders_list'][data['open_order']] = {}
    data['orders_list'][data['open_order']]['open_order_type'] = data['open_order_type']
    data['orders_list'][data['open_order']]['ask'] = data['ask'] 
    # data['orders_list'][data['open_order']]['status'] = 'open'
    data['long_start']	= False
    data['short_start']	= False
    data['to_order']	= None
    data['delay_counter']	= 0
    
    if data["plot"]:
        data['buy_markers_x'].append(data['i_list'][-1])
        data['buy_markers_y'].append(data['ask'])
    return(data)


def make_short_order(data):
    data['order_bid_price'] = data['bid']
    data['start_prices'][data['open_order']] = data['bid']
    data['open_order_type'] = 'short'
    data['start_dt_list'].append(data['dt_val'])
    data['slema_check_flag'] = True
    data['orders_list'][data['open_order']] = {}
    data['orders_list'][data['open_order']]['open_order_type'] = data['open_order_type']
    data['orders_list'][data['open_order']]['bid'] = data['bid'] 
    # data['orders_list'][data['open_order']]['status'] = 'open'
    data['long_start']	= False
    data['short_start']	= False
    data['to_order']	= None
    data['delay_counter']	= 0

    if data["plot"]:
        data['buy_markers_x'].append(data['i_list'][-1])
        data['buy_markers_y'].append(data['bid'])
    return(data)


def close_long_order(data):
    data['pl_list'].append(data['pl'])
    data['start_price'].append(data['start_prices'][data['i']])
    data['end_price'].append(data['bid'])
    data['num_orders'].append(data['i'])
    data['dt_list'].append(data['dt_val'])
    data['close_type'].append(data['close_type_val'])
    data['ord_types'].append('long')
    # data['ll_angle'].append(data['ordered_llema_angle'])
    # data['take_profit_flag'] = False
    # data['dir_change']	= False
    # data['orders_list'][data['i']]['status'] = 'closed' 
    data['open_order'] = 0
    data['slema_check_flag'] = False
    data['long_start']	= False
    data['short_start']	= False
    data['to_order']	= None
    data['delay_counter']	= 0
    
    if data["plot"]:
        data['sell_markers_x'].append(data['i_list'][-1])
        data['sell_markers_y'].append(data['bid'])   

    create_report(data)    
    return(data)


def close_short_order(data):
    data['pl_list'].append(data['pl'])
    # data['start_price'].append(data['order_bid_price'])
    data['start_price'].append(data['start_prices'][data['i']])
    data['end_price'].append(data['ask'])
    data['num_orders'].append(data['i'])
    data['dt_list'].append(data['dt_val'])
    data['close_type'].append(data['close_type_val'])
    data['ord_types'].append('short')
    # data['ll_angle'].append(data['ordered_llema_angle'])
    # data['take_profit_flag'] = False
    # data['dir_change']	= False
    # data['orders_list'][data['i']]['status'] = 'closed'
    data['open_order'] = 0
    data['slema_check_flag'] = False
    data['long_start']	= False
    data['short_start']	= False
    data['delay_counter']	= 0
    data['to_order']	= None
    
    if data["plot"]:
        data['sell_markers_x'].append(data['i_list'][-1])
        data['sell_markers_y'].append(data['ask'])  
    
    create_report(data)
    return(data)

#...............................................................................................
def get_order_details(data):
    data['no_of_orders'] = len(list(data['orders_list'])[1:])
    last_key = list(data['orders_list'])[-1]
    data['last_order'] = data['orders_list'][last_key]

    # data['open_orders_list'] = data['orders_list'].copy()

    # for i in data['orders_list']:
    #     if type(i) == int:
    #         if data['orders_list'][i]['status'] == 'closed':
    #             del data['open_orders_list'][i]

    return(data)
#...............................................................................................
def get_order_list(data):
    if data['first_type'] == 'long':
        data['forward_order_list'] = ['']
        data['forward_order_list'] = data['forward_order_list'] + [data['first_type']]
        data['forward_order_list'] = data['forward_order_list'] + ['short'] * 5
        data['forward_order_list'] = data['forward_order_list'] + ['long'] * 5
        data['forward_order_list'] = data['forward_order_list'] + ['short'] * 5
        data['forward_order_list'] = data['forward_order_list'] + ['long'] * 3
    elif data['first_type'] == 'short':
        data['forward_order_list'] = ['']
        data['forward_order_list'] = data['forward_order_list'] + [data['first_type']]
        data['forward_order_list'] = data['forward_order_list'] + ['long'] * 5
        data['forward_order_list'] = data['forward_order_list'] + ['short'] * 5
        data['forward_order_list'] = data['forward_order_list'] + ['long'] * 5
        data['forward_order_list'] = data['forward_order_list'] + ['short'] * 3
    return(data)
#...............................................................................................
def get_order_list(data):
    if data['first_type'] == 'long':
        data['forward_order_list'] = ['']
        data['forward_order_list'] = data['forward_order_list'] + [data['first_type']]
        for i in range(1,21):
            if i%2 == 0:
                data['forward_order_list'] = data['forward_order_list'] + ['long']
            else:
                data['forward_order_list'] = data['forward_order_list'] + ['short']


    elif data['first_type'] == 'short':
        data['forward_order_list'] = ['']
        data['forward_order_list'] = data['forward_order_list'] + [data['first_type']]
        for i in range(1,21):
            if i%2 == 0:
                data['forward_order_list'] = data['forward_order_list'] + ['short']
            else:
                data['forward_order_list'] = data['forward_order_list'] + ['long']
    return(data)
#...............................................................................................
#...............................................................................................
#...............................................................................................
#...............................................................................................
#...............................................................................................
#...............................................................................................
#...............................................................................................
#...............................................................................................