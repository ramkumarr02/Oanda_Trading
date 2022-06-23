from utils.packages import *
from utils.variables import *


#...............................................................................................
def read_data(data):   
    source_file_path = f'data/{data["input_file_name"]}'
    # source_file_path = f'../data/products/{data["product"]}/{data["input_file_name"]}'

    if data['input_rows'] is None:
        data["df"] = pd.read_csv(source_file_path)
    else:
        data["df"] = pd.read_csv(source_file_path, nrows=data['input_rows'])
        
    data["df"] = data["df"][data["df"]['DateTime'].str.contains('|'.join(data['date_list']))]
    
    data['df']['i'] = np.int()
    data["df"]['tick'] = np.float()
    data["df"]['sema'] = np.float()
    data["df"]['lema'] = np.float()

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
    # print(f'date_val          : {data["date_list"]}')    
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
def plot_graph(data):
    linestyle = (0, (1, 2))
    
    fig, ax1 = plt.subplots(figsize=(150,30))
    ax2 = ax1.twinx()

    x_axis = np.arange(0,len(data["df"]['tick']))

    ax1.plot(x_axis, data["df"]['tick'], label='tick', color='gray', linestyle='dotted')
    ax1.plot(x_axis, data["df"]['sema'], label='sema', color='red')
    ax1.plot(x_axis, data["df"]['slema'], label='slema', color='darkblue')
    ax1.plot(x_axis, data["df"]['lema'], label='lema', color='black')
    ax2.plot(x_axis, data["df"]['tick_angle'], label='tick_angle', color='black', linestyle=linestyle)
    ax2.plot(x_axis, [0] * len(data["df"]['tick_angle']), label='Angle 0', color='black')
    # ax2.plot(x_axis, data["df"]['lema_angle'], label='lema_angle', color='black', linestyle=linestyle)

    data = get_date_lines(data)

    for i, x_val in enumerate(data['line_list']):
        plt.axvline(x=x_val, color='black')
        plt.text(x=x_val, y=0, s=data['date_list'][i], rotation=90, fontsize = 15)

    ax1.scatter(data['buy_markers_x'], data['buy_markers_y'], s=300, c='blue', marker=10)
    ax1.scatter(data['sell_markers_x'], data['sell_markers_y'], s=300, c='red', marker=11)

    legend = ax1.legend(loc='upper left', fontsize='xx-large')
    legend = ax2.legend(loc='upper right', fontsize='xx-large')
    
    ax1.tick_params(axis='x', colors='red', labelsize = 25)
    ax1.tick_params(axis='y', colors='red', labelsize = 25)
    ax2.tick_params(axis='y', colors='red', labelsize = 25)


    plt.xlabel('tick num')
    plt.ylabel('prices')
    plt.title('trade chart')
    plt.grid()
    plt.show()    
    try:
        data['chart_name'] = f'{data["file_name"].split(".")[0]}.png'
        fig.savefig(data['chart_name'])
    except:        
        fig.savefig('temp.png')
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
        'start_date':list(data['start_dt_list'])[:len(data['dt_list'])],
        'date':data['dt_list'],
        'start_price':data['start_price'],
        'end_price':data['end_price'],
        'num_orders':data['num_orders'],
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

    data['report_df']['duration'] = data['report_df']['date'] - data['report_df']['start_date']

    data['report_df'] = data['report_df'][[
        'start_date','date', 'year_val', 'month_val', 'date_val', 'hour_val','minute_val', 
        'close_type', 'start_price', 'end_price', 'num_orders','pls', 'ord_types', 
        # 'llema_angle', 'llema_len',
        'sema_len', 'slema_len', 'lema_len', 
        'pl_move_trail_trigger' ,'stop_loss_pip', 'duration']]

    data["report_df"] = data["report_df"].reset_index(drop = True)    
        
    try:
        os.system('clear')
    except:
        pass
    
    try:
        display.clear_output(wait = True)
        # print('------------------------------')
    except:
        pass
    
    try:    
        os.system('cls')    
    except: 
        pass

    print(np.sum(data['report_df'][['pls']]))
    print('--------------------------------------')
    print(data['report_df'][['start_date', 'ord_types', 'close_type', 'pls']].tail(15))
    # print(data['report_df'][['date', 'ord_types', 'close_type', 'pls']])
    
    # print(data['report_df'][['date', 'ord_types', 'llema_angle','close_type', 'pls']].tail(15))
    # print(data['report_df'][['date', 'ord_types', 'llema_angle','close_type', 'pls']])
#...............................................................................................    

#...............................................................................................    
def send_telegram_message(message_text):     
    data['telegram_url'] = "https://api.telegram.org/bot"
    data['url_for_Chat_id'] = f'{data["telegram_url"]}{keys.tester_bot_token}/getUpdates'   
    
    send_message_url = f'{data["telegram_url"]}{keys.tester_bot_token}/sendMessage?chat_id={keys.chat_id}/&text={message_text}'
    requests.get(send_message_url)
#...............................................................................................    '
def combine_csv_files(data):
    for i, csv_file in enumerate(data['csv_list']):
        if i == 0:
            df = pd.read_csv(f"data/{csv_file}.csv")
            print(f"{csv_file} has {len(df)} records")
        else:
            df_new= pd.read_csv(f"data/{csv_file}.csv")
            print(f"{csv_file} has {len(df_new)} records")
            df =  df.append(df_new)
            
        print(f"{data['new_file']} has {len(df)} records")
        df.to_csv(f"data/{data['new_file']}.csv")
    
    return(data)
#...............................................................................................    
#...............................................................................................
def plotly_graph(data):
    # Plot Layout --------------------------------
    chart_name = f"Trade Chart"
    layout = go.Layout(title = chart_name,
                       xaxis = dict(title="DateTime"),
                       xaxis2 = dict(title= 'x', side= 'top'),
                       
                       yaxis = dict(title="PIP"),
                       yaxis2 = dict(title= 'Trend Angle', overlaying="y", side="right",)
                      )
    

    fig = go.Figure(layout = layout)
    # --------------------------------

    # Tick  --------------------------------
    fig.add_trace(go.Scatter(x=data['df']['DateTime_frmt'],
                            y=data['df']['tick'],
                            mode='lines',
                            name='tick',
                            line=dict(color='lightgrey', width=1),
                        )
                )

    fig.add_trace(go.Scatter(x=data['df']['DateTime_frmt'],
                        y=data['df']['lema'],
                        mode='lines',
                        name='lema',
                        line=dict(color='grey', width=1),
                    )
            )                            

    fig.add_trace(go.Scatter(x=data['df']['DateTime_frmt'],
                        y=data['df']['h_lema'],
                        mode='lines',
                        name='h_lema',
                        line=dict(color='red', width=1, dash = 'dot'),
                    )
            )   

    fig.add_trace(go.Scatter(x=data['df']['DateTime_frmt'],
                        y=data['df']['l_lema'],
                        mode='lines',
                        name='l_lema',
                    line=dict(color='blue', width=1, dash = 'dot'),
                    )
            )   

    # fig.add_scatter(x = data['df']['DateTime_frmt'], 
    #                 y = data['df']['h'], 
    #                 mode = 'markers', 
    #                 name = 'high',
    #                 marker_symbol = 'circle',
    #                 marker=dict(color='red',
    #                             size=data['marker_size'],
    #                             line=dict(
    #                                 color='crimson',
    #                                 width=5
    #                             )),
    #                 opacity=1)
                                
    # fig.add_scatter(x = data['df']['DateTime_frmt'], 
    #                 y = data['df']['l'], 
    #                 mode = 'markers', 
    #                 name = 'low',
    #                 marker_symbol = 'circle',
    #                 marker=dict(color='blue',
    #                             size=data['marker_size'],
    #                             line=dict(
    #                                 color='blue',
    #                                 width=5
    #                             )),
    #                 opacity=1)
                                
    # fig.add_scatter(x = data['df']['DateTime_frmt'], 
    #                 y = data['df']['mid_point'], 
    #                 mode = 'markers', 
    #                 name = 'mid_point',
    #                 marker_symbol = 'circle',
    #                 marker=dict(color='black',
    #                             size=data['marker_size'],
    #                             line=dict(
    #                                 color='black',
    #                                 width=5
    #                             )),
    #                 opacity=1)

    fig.update_layout(legend=dict(orientation="h",
                                  yanchor="bottom",
                                  y=1.02,
                                  xanchor="right",
                                  x=1
                                 ))
    
    if data['plot_type'] == 'file':
        chart_name = str(dt.datetime.now())
        chart_name = chart_name.replace(":", "-")
        chart_name = chart_name.replace(".", "-")
        chart_name = chart_name.replace(" ", "-")
        data['chart_file_path'] = (f'{os.getcwd()}\\data\\chart-{chart_name}.html')

        fig.write_html(data['chart_file_path'])
        webbrowser.get(data['chrome_path']).open(data['chart_file_path'])
    elif data['plot_type'] == 'show':
        fig.show()
#...............................................................................................
