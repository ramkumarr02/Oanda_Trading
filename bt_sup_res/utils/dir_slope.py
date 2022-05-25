from utils.packages import *

#...............................................................................................
#...............................................................................................    

def get_tick_time(data):
    data['df']['sno'] = data['df'].index

    data['df']['tick']      = (data["df"]['Ask'] + data["df"]['Bid'])/2
    data['df']['DateTime_frmt']   = [dt.datetime.strptime(x,"%Y%m%d %H:%M:%S.%f") for x in data["df"]['DateTime']]
    # data['df']['DateTime_frmt']   = [dt.datetime.strptime(x.split(".")[0],"%Y%m%d %H:%M:%S") for x in data["df"]['DateTime']]
    # data['df'] = data['df'].set_index('DateTime_frmt')
    return(data)

#...............................................................................................    

#...............................................................................................    
def get_ohlc_small(data):
    
    if data['i'] % data['small_candle_size'] == 0 and data['i'] > 0:        
        data['tick_list'] = data['df']['tick'].loc[data['i'] - data['small_candle_size'] : data['i']]
        max_index = data['tick_list'].idxmax()
        min_index = data['tick_list'].idxmin()
        data['df']['small_h'].loc[max_index] = max(data['tick_list'])
        data['df']['small_l'].loc[min_index] = min(data['tick_list'])

    return(data)
#...............................................................................................    

#...............................................................................................    
def get_trend_fwd_small(data):
    
    if data['i'] >= data['small_line_length']:
    
        line_index  = data['df'][data['i']-data['small_line_length']+1 : data['i']+1].index
        temp_df     = data['df'].loc[line_index]

        x           = temp_df['small_h'][temp_df['small_h'].notnull()].index
        y           = temp_df['small_h'][temp_df['small_h'].notnull()].values 

        if len(x) >= data['min_line_points']:
            slope_tick, intercept, _, _, _                  = linregress(x, y)
            data['df']['small_h_trend_calc_spot'].loc[data['i']]      = (slope_tick * data['i']) + intercept
            # data['df']['small_h_line_angle'].loc[data['i']]           = math.degrees(math.atan(slope_tick)) * 10**6

    # ----------------------------------------------------------------------------------

        x           = temp_df['small_l'][temp_df['small_l'].notnull()].index
        y           = temp_df['small_l'][temp_df['small_l'].notnull()].values 

        if len(x) >= data['min_line_points']:
            slope_tick, intercept, _, _, _                  = linregress(x, y)
            data['df']['small_l_trend_calc_spot'].loc[data['i']]      = (slope_tick * data['i']) + intercept
            # data['df']['small_l_line_angle'].loc[data['i']]           = math.degrees(math.atan(slope_tick)) * 10**6

        #data['sup_res_gap'] = data['df']['small_h_trend_calc_spot'].loc[data['i']] - data['df']['small_l_trend_calc_spot'].loc[data['i']]        
        #data["df"]['sup_res_gap'].loc[data['i']]                = data['sup_res_gap']

    return(data)

#...............................................................................................   

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

        
        data['sup_res_gap'] = data['df']['h_trend_calc_spot'].loc[data['i']] - data['df']['l_trend_calc_spot'].loc[data['i']]        
        data["df"]['sup_res_gap'].loc[data['i']]                = data['sup_res_gap']

    return(data)

#...............................................................................................   

def get_position(data):
    
    if data['sema'] >= data['df']['h_trend_calc_spot'].loc[data['i']] - data['sup_res_buffer']:
        data['position'] = 'up'

    elif data['sema'] <= data['df']['l_trend_calc_spot'].loc[data['i']] + data['sup_res_buffer']:
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

    if data["df"]['sup_res_gap'].loc[data['i']] >= data['min_sup_res_gap']:
        if data["df"]['h_line_angle'][data['i']] < 0 and data["df"]['l_line_angle'][data['i']] < 0:
            if data['pos_1'] == 'up' and data['pos_2'] == 'middle':    
                data["df"]['to_order'][data['i']] = 'short'
                data = build_sup_res_gap_list(data)

        elif data["df"]['h_line_angle'][data['i']] > 0 and data["df"]['l_line_angle'][data['i']] > 0:
            if data['pos_1'] == 'down' and data['pos_2'] == 'middle':
                data["df"]['to_order'][data['i']] = 'long'        
                data = build_sup_res_gap_list(data)

    return(data)    
#................................................................................................

def capture_pl_data(data):
    data['stop_loss_pip']                                   = -data['avg_sup_res_gap'] * 0.8
    data['pl_move_trail_trigger']                           = data['avg_sup_res_gap'] * 0.8
    data['df']['stop_loss_pip'].loc[data['i']]              = data['stop_loss_pip'] 
    data['df']['pl_move_trail_trigger'].loc[data['i']]      = data['pl_move_trail_trigger'] 
    return(data)
#................................................................................................

def build_sup_res_gap_list(data):
    if len(data['sup_res_gap_list']) < 4:
        data['sup_res_gap_list'].append(data['sup_res_gap'])

    elif len(data['sup_res_gap_list']) == 4:
        data['sup_res_gap_list'].popleft()
        data['sup_res_gap_list'].append(data['sup_res_gap'])

    if np.isnan(np.mean(data['sup_res_gap_list'])):
        data['avg_sup_res_gap'] = data['min_sup_res_gap']
    else:
        data['avg_sup_res_gap'] = np.mean(data['sup_res_gap_list'])

    return(data)

#...............................................................................................     
def trend_angle_check(data):
    
    if data["df"]['h_line_angle'][data['i']] >= data['trend_angle'] and data["df"]['l_line_angle'][data['i']] >= data['trend_angle']:
        data["df"]['trend_angle'][data['i']] = 'up'

    elif data["df"]['h_line_angle'][data['i']] <= -data['trend_angle'] and data["df"]['l_line_angle'][data['i']] <= -data['trend_angle']:
        data["df"]['trend_angle'][data['i']] = 'down'
    
    return(data)

#...............................................................................................