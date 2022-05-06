from utils.packages import *


#...............................................................................................
def get_position(data):

    data['short'] = data['sema']
    data['long'] = data['lema']

    if data['sema'] == data['lema']:
        data['position'] = 0

    elif data['sema'] - data['lema'] >= 0.00001:
        data['position'] = 1

    elif data['lema'] - data['sema'] >= 0.00001:
        data['position'] = -1
    
    return(data)
#...............................................................................................

#...............................................................................................
def get_cross_dir(data):   
    
    data['dir_list'].popleft()
    data['dir_list'].append(data['position'])   
    
    data['pos_1'] = data['dir_list'][0]
    data['pos_2'] = data['dir_list'][1]

    data = dir_switch_check(data)

    return(data)    
#................................................................................................

def dir_switch_check(data):

    if data['direction'] == 'straight':
        if data['pos_1'] != data['pos_2'] and data['pos_2'] == -1:
            data['dir_change'] = True    
            data['to_order'] = 'short'

        elif data['pos_1'] != data['pos_2'] and data['pos_2'] == 1:
            data['dir_change'] = True    
            data['to_order'] = 'long'   
        
        else:
            data['dir_change'] = False
            data['to_order'] = None
            data['sema_close_flag'] = False        

    #-------------------------

    if data['direction'] == 'reverse':
        if not data['open_order']:
            if data['pos_1'] != data['pos_2'] and data['pos_2'] == 1:
                data['dir_change'] = True    
                data['to_order'] = 'short'

            elif data['pos_1'] != data['pos_2'] and data['pos_2'] == -1:
                data['dir_change'] = True    
                data['to_order'] = 'long'   
            
            else:
                data['dir_change'] = False
                data['to_order'] = None
                data['sema_close_flag'] = False        


        if data['open_order']:
            if data['open_order_type'] == 'long':
                if data['pos_1'] != data['pos_2'] and data['pos_2'] == 1:
                    data['dir_change'] = True    
                    data['to_order'] = 'long'

                elif data['pos_1'] != data['pos_2'] and data['pos_2'] == -1:
                    data['dir_change'] = True    
                    data['to_order'] = 'short'   
                    
                else:
                    data['dir_change'] = False
                    data['to_order'] = None
                    data['sema_close_flag'] = False
            
            if data['open_order_type'] == 'short':    
                if data['pos_1'] != data['pos_2'] and data['pos_2'] == 1:
                    data['dir_change'] = True    
                    data['to_order'] = 'long'

                elif data['pos_1'] != data['pos_2'] and data['pos_2'] == -1:
                    data['dir_change'] = True    
                    data['to_order'] = 'short'   
                    
                else:
                    data['dir_change'] = False
                    data['to_order'] = None
                    data['sema_close_flag'] = False

    return(data)    

#...............................................................................................

#...............................................................................................

def get_slope(data):
    
    data['y_axis'] = list(np.round(data['y_axis'],data['pip_decimal_num']))
    ma_len = len(data['y_axis'])
    
    x_axis = []
    for i in range(ma_len):
        x_axis.append(1 + ((i+1) * 10**(-data['pip_decimal_num'])))
    
    slope_tick, intercept, _, _, _ = linregress(x_axis, data['y_axis'])
    
    data['llema_angle'] = math.degrees(math.atan(slope_tick))        

    return(data)    
#...............................................................................................    

def get_tick_time(data):
    data['df']['sno'] = data['df'].index

    data['df']['tick']      = (data["df"]['Ask'] + data["df"]['Bid'])/2
    data['df']['DateTime_frmt']   = [dt.datetime.strptime(x,"%Y%m%d %H:%M:%S.%f") for x in data["df"]['DateTime']]
    # data['df']['DateTime_frmt']   = [dt.datetime.strptime(x.split(".")[0],"%Y%m%d %H:%M:%S") for x in data["df"]['DateTime']]
    # data['df'] = data['df'].set_index('DateTime_frmt')
    return(data)

#...............................................................................................    

def get_ohlc(data):
    data['df']['o'] = np.nan
    data['df']['h'] = np.nan
    data['df']['l'] = np.nan
    data['df']['c'] = np.nan    
    
    data['rolled_index'] = data['df'].resample(data['candle_size']).tick.first().index

    for i in np.arange(1,len(data['rolled_index'])):
        
        timestamp_val = data['df'].loc[data['rolled_index'][i-1]:data['rolled_index'][i]]['tick'].index[0]
        tick_val      = data['df'].loc[data['rolled_index'][i-1]:data['rolled_index'][i]]['tick'].values[0]
        data['df']['o'].loc[timestamp_val] = tick_val
        
        row_num       = np.argmax(data['df'].loc[data['rolled_index'][i-1]:data['rolled_index'][i]]['tick'])
        timestamp_val = data['df'].loc[data['rolled_index'][i-1]:data['rolled_index'][i]]['tick'].index[row_num]
        tick_val      = data['df'].loc[data['rolled_index'][i-1]:data['rolled_index'][i]]['tick'].values[row_num]
        data['df']['h'].loc[timestamp_val] = tick_val
        
        row_num       = np.argmin(data['df'].loc[data['rolled_index'][i-1]:data['rolled_index'][i]]['tick'])
        timestamp_val = data['df'].loc[data['rolled_index'][i-1]:data['rolled_index'][i]]['tick'].index[row_num]
        tick_val      = data['df'].loc[data['rolled_index'][i-1]:data['rolled_index'][i]]['tick'].values[row_num]
        data['df']['l'].loc[timestamp_val] = tick_val

        timestamp_val = data['df'].loc[data['rolled_index'][i-1]:data['rolled_index'][i]]['tick'].index[-1]
        tick_val      = data['df'].loc[data['rolled_index'][i-1]:data['rolled_index'][i]]['tick'].values[-1]
        data['df']['c'].loc[timestamp_val] = tick_val        
    
    data['df'] = data['df'][['sno', 'i', 'DateTime','Ask', 'Bid', 'tick', 'sema', 'lema', 'slema', 'o', 'h', 'l', 'c', ]].round(6)
    data['df_len'] = len(data["df"])

    return(data)

#...............................................................................................    

#...............................................................................................    
def consolidate_points_to_bigger_switch_points(data):
    for switch_point in list(set(data['df']['switch_point'])):

        temp = data['df'][data['df']['switch_point'] == switch_point]
        high_points_num = len(set(temp['h'][temp['h'].notnull()]))
        low_points_num = len(set(temp['l'][temp['l'].notnull()]))
        tot_points_num = high_points_num + low_points_num

        print(f'switch_point    : {switch_point}')
        print(f'high_points_num : {high_points_num}')
        print(f'low_points_num  : {low_points_num}')
        print(f'tot_points_num  : {tot_points_num}')
        print('-----------------------------------------')
        

        if tot_points_num < data['min_points_for_line']:
            data['df']['switch_point'][data['df']['switch_point'] == switch_point] = switch_point + 1

    
    return(data)
#...............................................................................................    

#...............................................................................................    
def consolidate_points_to_bigger_switch_points(data):
    switch_point_list = list(set(data['df']['switch_point']))
    switch_points_no = len(switch_point_list)
    print(f'switch_point_list : {switch_point_list}')
    print(f'switch_points_no : {switch_points_no}')

    for i in np.arange(switch_points_no):
        print(switch_point_list[i])

        temp = data['df'][data['df']['switch_point'] == switch_point_list[i]]
        high_points_num = len(set(temp['h'][temp['h'].notnull()]))
        low_points_num = len(set(temp['l'][temp['l'].notnull()]))
        tot_points_num = high_points_num + low_points_num

        print(f'switch_point    : {switch_point_list[i]}')
        print(f'high_points_num : {high_points_num}')
        print(f'low_points_num  : {low_points_num}')
        print(f'tot_points_num  : {tot_points_num}')
        print('-----------------------------------------')
        

        if tot_points_num < data['min_points_for_line'] and i != switch_points_no - 1:
            data['df']['switch_point'][data['df']['switch_point'] == switch_point_list[i]] = switch_point_list[i+1]

        if tot_points_num < data['min_points_for_line'] and i == switch_points_no - 1:
            data['df']['switch_point'][data['df']['switch_point'] == switch_point_list[i]] = switch_point_list[i-1]

        
    return(data)
#...............................................................................................  
