from utils.packages import *
from utils.variables import *


#...............................................................................................
def read_data(data):   
    data['source_file_path'] = f'data/{data["input_file_name"]}'
    # source_file_path = f'../data/products/{data["product"]}/{data["input_file_name"]}'

    if data['input_rows'] is None:
        data["df"] = pd.read_csv(data['source_file_path'])
    else:
        data["df"] = pd.read_csv(data['source_file_path'], nrows=data['input_rows'])
        
    data["df"] = data["df"][data["df"]['DateTime'].str.contains('|'.join(data['date_list']))]

    data['df']['i'] = np.int()
    data["df"]['tick'] = np.float()
    data["df"]['sema'] = np.float()
    data["df"]['slema'] = np.float()
    data["df"]['lema'] = np.float()
    data['df']['long_open'] = ''
    data['df']['long_close'] = ''
    data['df']['short_open'] = ''
    data['df']['short_close'] = ''


    if data['df_subset_size'] is not None:
        data["df"] = data["df"][0:data['df_subset_size']]

    data["df"] = data["df"].reset_index(drop = True)
    print(f'Record num : {len(data["df"])}')        

    return(data)
#...............................................................................................



#...............................................................................................
def get_date_list(data):
    
    data['start_date'] = dt.datetime(year=data['start_date']['year'],
                      month=data['start_date']['month'],
                      day=data['start_date']['date'])

    data['end_date'] = dt.datetime(year=data['end_date']['year'],
                      month=data['end_date']['month'],
                      day=data['end_date']['date'])

    
    date_list = list(pd.date_range(data['start_date'],data['end_date'],freq='d').values)
    data['date_list'] = [str(x).split('T')[0].replace('-','') for x in date_list]
    return(data)
#...............................................................................................



#...............................................................................................
def split_date_col(data):
    data['report_df']['year_val'] = [x.year for x in data['report_df']['date']]
    data['report_df']['month_val'] = [x.month for x in data['report_df']['date']]
    data['report_df']['date_val'] = [x.day for x in data['report_df']['date']]
    data['report_df']['hour_val'] = [x.hour for x in data['report_df']['date']]
    data['report_df']['minute_val'] = [x.minute for x in data['report_df']['date']]
#...............................................................................................



#...............................................................................................
def print_report(data):
    pl_list = list(data['pl_list'])
    net_pl = round(np.sum(pl_list),5)

    positive_pls = [i for i in pl_list if i > 0]
    negative_pls = [i for i in pl_list if i < 0]

    num_positive = len(positive_pls)
    num_negative = len(negative_pls)

    sum_positive = round(np.sum(positive_pls),5)
    sum_negative = round(np.sum(negative_pls),5)
    sum_total    = round(sum_positive + abs(sum_negative),5) 

    avg_positive = round(np.mean(positive_pls),5)
    avg_negative = round(np.mean(negative_pls),5)

    data['file_name'] = f'data/{data["start_date"].year}-({data["start_date"].month}-{data["end_date"].month})-({data["start_date"].day}-{data["end_date"].day})-{data["start_ts"]}.csv'
    # data['df'].to_csv(f"data/full_df_{data['file_name'].split('/')[1]}", index = False) 
    # data['df'].to_csv(f"data/full_df_{data['angle_len']}.csv", index = False) 
    data['report_df'].to_csv(data['file_name'], index = False) 
    
    print('==============================')
    print(f'date_val          : {data["date_list"]}')    
    print(f'Total PL : {sum(data["pl_list"])}')
    print('-------------')
    print(f'net_pl            : {net_pl}/{sum_total}')  
    print('-------------')
    print(f'+ve               : num= {num_positive}    sum= +{sum_positive}    avg= +{avg_positive}')
    print(f'-ve               : num= {num_negative}    sum= {sum_negative}    avg= {avg_negative}')
    print('==============================')  
#...............................................................................................

#............................................................................................... 
def adjust_plot_list_lengths(data):
    # Adjust df len to lema(shortest) len
    data['df_len'] = len(data["df_llema_list"])

    data["df"] = data['df'][-data['df_len']:]   
    data["df"] = data["df"].reset_index(drop = True)    
    
    # data["df"]['llema_angle'] = data["df_llema_angle_list"][-data['df_len']:]            
    # data["df"]['llema'] = data["df_llema_list"][-data['df_len']:]            
    data["df"]['lema'] = data["df_lema_list"][-data['df_len']:]            
    data["df"]['slema'] = data["df_slema_list"][-data['df_len']:]            
    data["df"]['sema'] = list(data["df_sema_list"])[-data['df_len']:]    
    data['df']["tick"] = list(data["df_tick_list"])[-data['df_len']:]
            
    # Adjust buy sell markers to the shortened df
    # data['len_to_subtract'] = data['df_len']
    # data['len_to_subtract'] = data['df_len'] + data['angle_len']
    # data['len_to_subtract'] = data['llema_len'] + data['angle_len']
    data['len_to_subtract'] = 0

    data['buy_markers_x'] = list(np.array(data['buy_markers_x']) - data['len_to_subtract'])
    data['sell_markers_x'] = list(np.array(data['sell_markers_x']) - data['len_to_subtract'])    
    data["df"] = data["df"].reset_index(drop = True)
    return(data)

#............................................................................................... 

#...............................................................................................
def plot_graph_old(data):
    fig = px.line(data['df'], 
                    x="DateTime_frmt", 
                    y=['tick', 'sema','slema', 'lema'], 
                    # y=['tick', 'sema', 'lema'], 
                    color_discrete_sequence = ['grey', 'red', 'blue', 'black'],
                    title='tick chart') 

    data['marker_size'] = 15

    if data['plot_transactions']:

        fig.add_scatter(x = data['df']['DateTime_frmt'] , 
                    y = data['df']['long_open'], 
                    mode = 'markers', 
                    name = 'long_open',
                    marker_symbol = 'triangle-up',
                    marker=dict(color='lightgreen',
                                size=data['marker_size'],
                                line=dict(
                                    color='green',
                                    width=2
                                )),
                    opacity=1)


        fig.add_scatter(x = data['df']['DateTime_frmt'] , 
                    y = data['df']['long_close'], 
                    mode = 'markers', 
                    name = 'long_close',
                    marker_symbol = 'triangle-up',
                    marker=dict(color='red',
                                size=data['marker_size'],
                                line=dict(
                                    color='darkred',
                                    width=2
                                )),
                    opacity=1)


        fig.add_scatter(x = data['df']['DateTime_frmt'] , 
                    y = data['df']['short_open'], 
                    mode = 'markers', 
                    name = 'short_open',
                    marker_symbol = 'triangle-down',
                    marker=dict(color='lightgreen',
                                size=data['marker_size'],
                                line=dict(
                                    color='green',
                                    width=2
                                )),
                    opacity=1)


        fig.add_scatter(x = data['df']['DateTime_frmt'] , 
                    y = data['df']['short_close'], 
                    mode = 'markers', 
                    name = 'short_close',
                    marker_symbol = 'triangle-down',
                    marker=dict(color='red',
                                size=data['marker_size'],
                                line=dict(
                                    color='darkred',
                                    width=2
                                )),
                    opacity=1)


    # for i in np.arange(len(data['dup_removed_sup_res'])):
    #     fig.add_hline(y = data['dup_removed_sup_res'][i], line_width=1, line_dash="dot", line_color="darkred")  

    for i in np.arange(len(data['dup_removed_sup_res'])):
        fig.add_shape(type = 'line', x0 = data['df']['DateTime_frmt'][0], x1 = data['sup_res_datetime'][i], y0 = data['dup_removed_sup_res'][i], y1 = data['dup_removed_sup_res'][i], line_width=1, line_dash="dot", line_color="darkred")  


    # fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")

    fig.show()


    # try:
    #     data['chart_name'] = f'{data["file_name"].split(".")[0]}.png'
    #     fig.savefig(data['chart_name'])
    # except:        
    #     fig.savefig('temp.png')
#...............................................................................................


#...............................................................................................
def plot_graph(data):
    fig = px.line(data['df'], 
                    x = data['df'].index, 
                    # y=['tick', 'sema','slema', 'lema'], 
                    # y=['tick', 'sema', 'lema'], 
                    y = ['tick'], 
                    color_discrete_sequence = ['grey', 'red', 'blue', 'black'],
                    title='tick chart') 

    data['marker_size'] = 10

    fig.add_scatter(x = data['df'].index, 
                    y = data['df']['h'], 
                    mode = 'markers', 
                    name = 'high',
                    marker_symbol = 'circle',
                    marker=dict(color='red',
                                size=data['marker_size'],
                                line=dict(
                                    color='black',
                                    width=2
                                )),
                    opacity=1)

    fig.add_scatter(x = data['df'].index, 
                    y = data['df']['l'], 
                    mode = 'markers', 
                    name = 'low',
                    marker_symbol = 'circle',
                    marker=dict(color='blue',
                                size=data['marker_size'],
                                line=dict(
                                    color='black',
                                    width=2
                                )),
                    opacity=1)

    fig.show()

#...............................................................................................


#...............................................................................................
def get_date_lines(data):
    data['line_list'] = []
    
    for dt_val in data['date_list']:    
        try:
            data['date_index'] = data["df"][data["df"]['DateTime'].str.contains(dt_val)].index[0]
            data['line_list'].append(data['date_index'])
        except:
            data['line_list'].append(data['date_index'])
    
    return(data)
#...............................................................................................



#...............................................................................................
def create_report(data):
    data['report_df'] = pd.DataFrame({
        'date':data['dt_list'],
        'pls': data['pl_list'],
        'close_type': data['close_type'], 
        'ord_types': data['ord_types'],
        # 'llema_angle':data['ll_angle'],
        'sema_len': data['sema_len'],
        'slema_len': data['slema_len'], 
        'lema_len': data['lema_len'],
        # 'llema_len': data['llema_len'], 
        'pl_move_trail_trigger': data['pl_move_trail_trigger'],
        'stop_loss_pip': data['stop_loss_pip']
        })

    split_date_col(data)

    data['report_df'] = data['report_df'][[
        'date', 'year_val', 'month_val', 'date_val', 'hour_val','minute_val', 
        'close_type', 'pls', 'ord_types', 
        # 'llema_angle', 'llema_len',
        'sema_len', 'slema_len', 'lema_len', 
        'pl_move_trail_trigger' ,'stop_loss_pip']]

    data["report_df"] = data["report_df"].reset_index(drop = True)    
        
    try:
        os.system('clear')
    except:
        pass
    
    try:
        display.clear_output(wait = True)
    except:
        pass
    
    try:    
        os.system('cls')    
    except: 
        pass

    print(np.sum(data['report_df'][['pls']]))
    print('--------------------------------------')
    print(data['report_df'][['date', 'ord_types', 'close_type', 'pls']].tail(15))
    # print(data['report_df'][['date', 'ord_types', 'close_type', 'pls']])
    
    # print(data['report_df'][['date', 'ord_types', 'llema_angle','close_type', 'pls']].tail(15))
    # print(data['report_df'][['date', 'ord_types', 'llema_angle','close_type', 'pls']])
#...............................................................................................    