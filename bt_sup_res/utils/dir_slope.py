from utils.packages import *


#...............................................................................................
def get_position(data):

    if data['sema'] >= data['df']['h_trend_calc_spot'].loc[data['i']]:
        data['position'] = 'up'

    elif data['sema'] <= data['df']['l_trend_calc_spot'].loc[data['i']]:
        data['position'] = 'down'

    else:
        data['position'] = 'middle'

    data["df"]['position'][data['i']] = data['position']
    
    return(data)
#...............................................................................................

#...............................................................................................
def get_cross_dir(data):   
    
    data['dir_list'].popleft()
    data['dir_list'].append(data['position'])   
    
    data['pos_1'] = data['dir_list'][0]
    data['pos_2'] = data['dir_list'][1]

    if data['pos_1'] == 'up' and data['pos_2'] == 'middle':    
        if data["df"]['h_line_angle'][data['i']] < 0 and data["df"]['l_line_angle'][data['i']] < 0:
            data["df"]['to_order'][data['i']] = 'short'

    elif data['pos_1'] == 'down' and data['pos_2'] == 'middle':
        if data["df"]['h_line_angle'][data['i']] > 0 and data["df"]['l_line_angle'][data['i']] > 0:
            data["df"]['to_order'][data['i']] = 'long'
        
    else:
        data['dir_change'] = False
        data['direction'] = ''


    return(data)    
#................................................................................................


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
def get_trend_fwd_skip(data):
    line_types      = ['h', 'l']
    
    for line_type in line_types:
        line_var        = f'{line_type}_line'
        angle_var       = f'{line_type}_line_angle'
        trend_calc_spot = f'{line_type}_trend_calc_spot'
        line_index  = data['df'][data['i']-data['line_length']+1 : data['i']+1].index
        temp_df     = data['df'].loc[line_index]
        x           = temp_df[line_type][temp_df[line_type].notnull()].index
        y           = temp_df[line_type][temp_df[line_type].notnull()].values 

        if len(x) >= data['min_line_points']:
            slope_tick, intercept, _, _, _                  = linregress(x, y)
            line_tick_val                                   = (slope_tick * data['i']) + intercept

            if line_type == 'h' and line_tick_val >= data['df']['lema'][data['i']]:                
                data['df'][trend_calc_spot].loc[data['i']]  = (slope_tick * data['i']) + intercept
                data['df'][angle_var].loc[data['i']]        = math.degrees(math.atan(slope_tick)) * 10**6
            
            elif line_type == 'l' and line_tick_val <= data['df']['lema'][data['i']]:                
                data['df'][trend_calc_spot].loc[data['i']]  = (slope_tick * data['i']) + intercept
                data['df'][angle_var].loc[data['i']]        = math.degrees(math.atan(slope_tick)) * 10**6

    if np.isnan(data['df']['h_trend_calc_spot'].loc[data['i']]) or np.isnan(data['df']['l_trend_calc_spot'].loc[data['i']]):
        data['df']['h_trend_calc_spot'].loc[data['i']] = np.nan
        data['df']['l_trend_calc_spot'].loc[data['i']] = np.nan
        data['df']['h_line_angle'].loc[data['i']] = np.nan
        data['df']['l_line_angle'].loc[data['i']] = np.nan

    return(data)

#...............................................................................................     


#...............................................................................................    
def get_trend_fwd(data):

    if data['i'] >= data['line_length']:

        line_index  = data['df'][data['i']-data['line_length']+1 : data['i']+1].index
        temp_df     = data['df'].loc[line_index]

        x           = temp_df['h'][temp_df['h'].notnull()].index
        y           = temp_df['h'][temp_df['h'].notnull()].values 

        if len(x) >= data['min_line_points']:
            slope_tick, intercept, _, _, _                  = linregress(x, y)
            data['df']['h_trend_calc_spot'].loc[data['i']]      = (slope_tick * data['i']) + intercept
            data['df']['h_line_angle'].loc[data['i']]           = math.degrees(math.atan(slope_tick)) * 10**6

    # ----------------------------------------------------------------------------------

        x           = temp_df['l'][temp_df['l'].notnull()].index
        y           = temp_df['l'][temp_df['l'].notnull()].values 

        if len(x) >= data['min_line_points']:
            slope_tick, intercept, _, _, _                  = linregress(x, y)
            data['df']['l_trend_calc_spot'].loc[data['i']]      = (slope_tick * data['i']) + intercept
            data['df']['l_line_angle'].loc[data['i']]           = math.degrees(math.atan(slope_tick)) * 10**6

        data["df"]['sup_res_gap'].loc[data['i']] = data['df']['h_trend_calc_spot'].loc[data['i']] - data['df']['l_trend_calc_spot'].loc[data['i']]

    return(data)

#...............................................................................................   

#...............................................................................................     
def trend_angle_check(data):

    if data["df"]['h_line_angle'][data['i']] >= data['trend_angle'] and data["df"]['l_line_angle'][data['i']] >= data['trend_angle']:
        data["df"]['trend_angle'][data['i']] = 'up'

    elif data["df"]['h_line_angle'][data['i']] <= -data['trend_angle'] and data["df"]['l_line_angle'][data['i']] <= -data['trend_angle']:
        data["df"]['trend_angle'][data['i']] = 'down'
    
    return(data)

#...............................................................................................
