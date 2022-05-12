from utils.packages import *


#...............................................................................................
def get_position(data):

    if data['sema'] == data['lema']:
        data['position'] = 0

    elif data['sema'] - data['lema'] >= 0.00001:
        data['position'] = 1

    elif data['lema'] - data['sema'] >= 0.00001:
        data['position'] = -1

    if data["plot"]:
        data["df"]['position'][data['i']] = data['position']
    
    return(data)
#...............................................................................................

#...............................................................................................
def get_cross_dir(data):   
    
    data['dir_list'].popleft()
    data['dir_list'].append(data['position'])   
    
    data['pos_1'] = data['dir_list'][0]
    data['pos_2'] = data['dir_list'][1]

    if data['pos_1'] != data['pos_2'] and data['pos_2'] == -1:
        data['dir_change'] = True    
        data['to_order'] = 'short'

    elif data['pos_1'] != data['pos_2'] and data['pos_2'] == 1:
        data['dir_change'] = True    
        data['to_order'] = 'long'   
        
    else:
        data['dir_change'] = False
        data['to_order'] = ''

    data["df"]['to_order'][data['i']] = data['to_order']

    return(data)    
#................................................................................................


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

    if data['i'] % data['candle_size'] == 0 and data['i'] > 0:        
        data['tick_list'] = data['df']['tick'].loc[data['i'] - data['candle_size'] : data['i']]
        max_index = data['tick_list'].idxmax()
        min_index = data['tick_list'].idxmin()
        data['df']['h'].loc[max_index] = max(data['tick_list'])
        data['df']['l'].loc[min_index] = min(data['tick_list'])

    return(data)

#...............................................................................................    

#...............................................................................................    
def get_trend_lines(data):
    line_types = ['h', 'l']
    for line_type in line_types:
        line_index = data['df'][data['i']-data['line_length'] : data['i']].index
        temp_df = data['df'].loc[line_index]
        x = temp_df[line_type][temp_df[line_type].notnull()].index
        y = temp_df[line_type][temp_df[line_type].notnull()].values 
        if len(x) > data['min_line_points']:
            # print(x,y)
            slope_tick, intercept, _, _, _ = linregress(x, y)
            data['df'][f'{line_type}_line'].loc[line_index] = (slope_tick * line_index) + intercept
    
            x_axis = []
            y_len = len(y)
            for i in range(y_len):
                x_axis.append(1 + ((i+1) * 10**(-data['pip_decimal_num'])))
            
            slope_tick, intercept, _, _, _ = linregress(x_axis, y)
            data['df'][f'{line_type}_line_angle'].loc[line_index] = math.degrees(math.atan(slope_tick)) 
            
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
