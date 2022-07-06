from utils.packages import *


#...............................................................................................
def get_position(data):
    
    if data['tick'] >= data['h_lema']:
        data['position'] = -1

    elif data['tick'] <= data['l_lema']:
        data['position'] = 1
    
    else:
        data['position'] = 0

    return(data)
#...............................................................................................

#...............................................................................................
def get_cross_dir(data):   
    
    data['dir_list'].popleft()
    data['dir_list'].append(data['position'])   
    
    data['pos_1'] = data['dir_list'][0]
    data['pos_2'] = data['dir_list'][1]

    if data['pos_1'] != data['pos_2'] and data['pos_2'] == -1:
        if data['h_l_gap'] > data['min_hl_gap']:
            data['touched_line'] = 'h_lema'
            data['to_order'] = 'short'      

    elif data['pos_1'] != data['pos_2'] and data['pos_2'] == 1:
        if data['h_l_gap'] > data['min_hl_gap']:
            data['touched_line'] = 'l_lema'
            data['to_order'] = 'long'            
    else:
        data['to_order'] = None
        data['touched_line'] = None

    return(data)    

#...............................................................................................
def get_cross_dir_rl(data):   
    
    data['dir_list'].popleft()
    data['dir_list'].append(data['position'])   
    
    data['pos_1'] = data['dir_list'][0]
    data['pos_2'] = data['dir_list'][1]

    if data['pos_1'] != data['pos_2'] and data['pos_2'] == -1:
        if data['h_l_gap'] > data['min_hl_gap']:
            data['touched_line'] = 'h_lema'
            # data['to_order'] = 'short'      
            data = r_l_dir_selection(data)

    elif data['pos_1'] != data['pos_2'] and data['pos_2'] == 1:
        if data['h_l_gap'] > data['min_hl_gap']:
            data['touched_line'] = 'l_lema'
            # data['to_order'] = 'long'            
            data = r_l_dir_selection(data)
    else:
        data['to_order'] = None
        data['touched_line'] = None

    return(data)    
#................................................................................................

def r_l_dir_selection(data):
    data['df_h_lema'] = data['df'][(data['df']['pl'].notnull()) & (data['df']['touched_line'] == 'h_lema')][['touched_line', 'order_side','pl']].tail(1)
    data['df_h_lema'] = data['df_h_lema'].reset_index(drop=True) 

    data['df_l_lema'] = data['df'][(data['df']['pl'].notnull()) & (data['df']['touched_line'] == 'l_lema')][['touched_line', 'order_side','pl']].tail(1)
    data['df_l_lema'] = data['df_l_lema'].reset_index(drop=True) 

    if data['touched_line'] == 'h_lema':
        if len(data['df_h_lema']) > 0:
            if data['df_h_lema']['pl'][0] > 0:
                if data['df_h_lema']['order_side'][0] == 'short':
                    data['to_order'] = 'short'      
                elif data['df_h_lema']['order_side'][0] == 'long':
                    data['to_order'] = 'long'
            elif data['df_h_lema']['pl'][0] < 0:
                if data['df_h_lema']['order_side'][0] == 'long':
                    data['to_order'] = 'short'      
                elif data['df_h_lema']['order_side'][0] == 'short':
                    data['to_order'] = 'long'
        else:
            data['to_order'] = 'short'      

    if data['touched_line'] == 'l_lema':
        if len(data['df_l_lema']) > 0:
            if data['df_l_lema']['pl'][0] > 0:
                if data['df_l_lema']['order_side'][0] == 'short':
                    data['to_order'] = 'short'      
                elif data['df_l_lema']['order_side'][0] == 'long':
                    data['to_order'] = 'long'
            elif data['df_l_lema']['pl'][0] < 0:
                if data['df_l_lema']['order_side'][0] == 'long':
                    data['to_order'] = 'short'      
                elif data['df_l_lema']['order_side'][0] == 'short':
                    data['to_order'] = 'long'
        else:
            data['to_order'] = 'long'   

    return(data)

# #...............................................................................................
# def get_cross_dir(data):   
    
#     data['dir_list'].popleft()
#     data['dir_list'].append(data['position'])   
    
#     data['pos_1'] = data['dir_list'][0]
#     data['pos_2'] = data['dir_list'][1]

#     if -20 <= data['tick_angle'] <= 20:
#         if data['pos_1'] != data['pos_2'] and data['pos_2'] == -1:
#             if data['h_l_gap'] > data['min_hl_gap']:
#                 data['to_order'] = 'short'      

#         elif data['pos_1'] != data['pos_2'] and data['pos_2'] == 1:
#             if data['h_l_gap'] > data['min_hl_gap']:
#                 data['to_order'] = 'long'            
#         else:
#             data['to_order'] = None

#     else:
#         if data['pos_1'] != data['pos_2'] and data['pos_2'] == -1:
#             if data['h_l_gap'] > data['min_hl_gap']:
#                 data['to_order'] = 'long'      

#         elif data['pos_1'] != data['pos_2'] and data['pos_2'] == 1:
#             if data['h_l_gap'] > data['min_hl_gap']:
#                 data['to_order'] = 'short'            
#         else:
#             data['to_order'] = None

#     return(data)    
# #................................................................................................