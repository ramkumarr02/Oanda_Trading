from utils.packages import *
from utils.loops import *
from utils.dir_slope import *
from utils.order import *


#...............................................................................................
def run_engine(data):

    data["start_ts"]        = dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d-%H-%M')
    data = get_rolling_emas(data)
    data['file_text'] = 'new_engine'
    del data['df']
    with open('data/full_df.csv') as input_file:
        for i, line in tqdm(enumerate(input_file)):
            if i > 0:
                data['df_line']     = line.split(',')                

                data['dt_val']      = dt.datetime.strptime(data['df_line'][0].split(".")[0],"%Y%m%d %H:%M:%S")
                data['bid']         = np.float(data['df_line'][1])      
                data['ask']         = np.float(data['df_line'][2])
                data['tick']        = np.float(data['df_line'][3])
                data['sema']        = np.float(data['df_line'][4])      
                data['lema']        = np.float(data['df_line'][5])      
                data['slema']       = np.float(data['df_line'][6])      
                data['llema']       = np.float(data['df_line'][7])      
                data['llema_angle'] = np.float(data['df_line'][8])

                # print(f"data['dt_val'] : {data['dt_val']}")     
                # print(data['df_line']) 
                # print(f"data['bid'] : {data['bid']}")      
                # print(f"data['ask'] : {data['ask']}")      
                # print(f"data['tick'] : {data['tick']}")      
                # print(f"data['sema'] : {data['sema']}")      
                # print(f"data['lema'] : {data['lema']}")      
                # print(f"data['slema'] : {data['slema']}")      
                # print(f"data['llema'] : {data['llema']}")      
                # print(f"data['llema_angle'] : {data['llema_angle']}")      
                    
                if data["plot"]:     
                    data['i_list'].append(i)
                    data["df_tick_list"].append(data['tick'])
                    data["df_sema_list"].append(data['sema'])
                    data["df_slema_list"].append(data['slema'])
                    data["df_lema_list"].append(data['lema'])
                    data["df_llema_list"].append(data['llema'])
                    data['df_llema_angle_list'].append(data['llema_angle'])

                data = get_position(data)           
                data = calculate_pl(data)
                data = take_profit(data)        
                data = slema_positive_check(data)
                data = simple_slema_move_close(data)
                data = sema_close(data)
                data = stop_loss(data)             
                data = make_order(data)    
            
    return(data)
#...............................................................................................    


#...............................................................................................
def run_old_engine(data):

    data["start_ts"] = dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d-%H-%M')
    data = get_rolling_emas(data)
    data['file_text'] = 'old_engine'
    data['dt_val_series']   = [dt.datetime.strptime(x.split(".")[0],"%Y%m%d %H:%M:%S") for x in data["df"]['DateTime']]

    for i in tqdm(range(0, data['df_len'])):
        data['bid'] = data["df"]['Bid'][i]        
        data['ask'] = data["df"]['Ask'][i]
        data['tick'] = data['df']['tick'][i]        
        data['dt_val'] = data['dt_val_series'][i]   
        data['sema'] = data['df']['sema'][i]      
        data['slema'] = data['df']['slema'][i]      
        data['lema'] = data['df']['lema'][i]      
        data['llema'] = data['df']['llema'][i]      
        data['llema_angle'] = data['df']['llema_angle'][i]      
        # data['lema_angle'] = data['lema_angle'][i]      
        # data['slema_angle'] = data['slema_angle'][i]      
        # data['sema_angle'] = data['sema_angle'][i]      
        # data['tick_angle'] = data['tick_angle'][i]  
        
        if data["plot"]:     
            data['i_list'].append(i)
            data["df_tick_list"].append(data['tick'])
            data["df_sema_list"].append(data['sema'])
            data["df_slema_list"].append(data['slema'])
            data["df_lema_list"].append(data['lema'])
            data["df_llema_list"].append(data['llema'])
            data['df_llema_angle_list'].append(data['llema_angle'])

        data = get_position(data)
        # if data['position'] == None:
        #     continue
        
        # # Get Dirs --------------------------------
        # if len(data['dir_list']) < 2:
        #     data['dir_list'].append(data['position'])   
        #     continue

        # elif len(data['dir_list']) == 2:
        #     data = get_cross_dir(data)
        # # ----------------------------------------------------------  
        
        data = calculate_pl(data)
        data = take_profit(data)        
        data = slema_positive_check(data)
        data = simple_slema_move_close(data)
        data = sema_close(data)
        data = stop_loss(data)             
        data = make_order(data)    
        
    return(data)
#...............................................................................................    