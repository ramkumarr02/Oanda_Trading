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
    print('Date List Created')
    return(data)
#...............................................................................................



#...............................................................................................
def split_date_col(data):
    data['df']['month_val'] = [x.month for x in data['df']['DateTime_frmt']]
    data['df']['date_val'] = [x.day for x in data['df']['DateTime_frmt']]
    data['df'] = data['df'][['DateTime_frmt', 'month_val', 'date_val', 'Bid', 'Ask', 'tick', 'lema', 'h_l_gap', 'h_lema', 'l_lema', 'long_open', 'long_close', 'short_open', 'short_close','close_type', 'pl']]
    return(data)
#...............................................................................................


#...............................................................................................
def create_report(data):    
        
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

    print(np.sum(data['df'][['pl']]))
    print('--------------------------------------')
    print(data['df'][data['df']['pl'].notnull()][['DateTime_frmt', 'close_type', 'pl']].tail(15))

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
def plot_graph(data):
    if data["plot"]:
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
                            line=dict(color='blue', width=1),
                        )
                )                            

        # fig.add_trace(go.Scatter(x=data['df']['DateTime_frmt'],
        #                     y=data['df']['slema'],
        #                     mode='lines',
        #                     name='slema',
        #                     line=dict(color='black', width=1),
        #                 )
        #         )                            

        # fig.add_trace(go.Scatter(x=data['df']['DateTime_frmt'],
        #                     y=data['df']['sema'],
        #                     mode='lines',
        #                     name='sema',
        #                     line=dict(color='red', width=1),
        #                 )
        #         )                            

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

        # fig.add_trace(go.Scatter(x=data['df']['DateTime_frmt'],
        #                     y=data['df']['tick_angle'],
        #                     mode='lines',
        #                     name='tick_angle',
        #                     yaxis='y2',
        #                 line=dict(color='darkcyan', width=0.5, dash = 'dot'),
        #                 )
        #         )   

        # fig.add_trace(go.Scatter(x=data['df']['DateTime_frmt'],
        #                     y=[0] * len(data['df']['tick_angle']),
        #                     mode='lines',
        #                     name='angle_0',
        #                     yaxis='y2',
        #                 line=dict(color='black', width=1),
        #                 )
        #         )   

        fig.add_scatter(x = data['df']['DateTime_frmt'], 
                            y = data['df']['long_open'], 
                            mode = 'markers', 
                            name = 'long_open',
                            marker_symbol = 'triangle-up',
                            marker=dict(color='blue',
                                        size=10,
                                        line=dict(
                                            color='blue',
                                            width=1
                                        )),
                            opacity=1)

        fig.add_scatter(x = data['df']['DateTime_frmt'], 
                    y = data['df']['long_close'], 
                    mode = 'markers', 
                    name = 'long_close',
                    marker_symbol = 'triangle-up',
                    marker=dict(color='red',
                                size=10,
                                line=dict(
                                    color='red',
                                    width=1
                                )),
                    opacity=1)


        fig.add_scatter(x = data['df']['DateTime_frmt'], 
                    y = data['df']['short_open'], 
                    mode = 'markers', 
                    name = 'short_open',
                    marker_symbol = 'triangle-down',
                    marker=dict(color='blue',
                                size=10,
                                line=dict(
                                    color='blue',
                                    width=1
                                )),
                    opacity=1)

        fig.add_scatter(x = data['df']['DateTime_frmt'], 
                    y = data['df']['short_close'], 
                    mode = 'markers', 
                    name = 'short_close',
                    marker_symbol = 'triangle-down',
                    marker=dict(color='red',
                                size=10,
                                line=dict(
                                    color='red',
                                    width=1
                                )),
                    opacity=1)

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
def generate_result_report(data):
    data['report_df'] = data['df'][data['df']['pl'].notnull()]

    winsound.PlaySound('C:\\Windows\\Media\\tada.wav', winsound.SND_ASYNC)
    data["monthly_pl"] = pd.DataFrame(data['report_df'].groupby(['month_val'])['pl'].sum())
    data["net_pl"] = data['report_df']['pl'].sum().round(4)

    send_telegram_message(f'Run Complete: \n------------\n {data["df_name"]}')
    send_telegram_message(f'Net PL: \n------------\n {data["net_pl"]} pips')
    send_telegram_message(f'Monthly PL: \n------------\n {data["monthly_pl"]}')

    print('--------------------------------------')
    print(f'Run Complete : {data["df_name"]}')
    print('--------------------------------------\n\n')

    print('--------------------------------------')
    print('Net PL')
    print(f'{data["net_pl"]}')
    print('--------------------------------------\n\n')

    print('--------------------------------------')
    print('Monthly PL')
    print(f'{data["monthly_pl"]}')
    print('--------------------------------------\n\n')

    print('--------------------------------------')
    print('Count of transactions by Close Type')
    print('..................')
    print(pd.DataFrame(data['report_df'].groupby(['close_type'])['pl'].count()))
    print('--------------------------------------\n\n')

    print('--------------------------------------')
    print('Mean value of transactions by Close Type')
    print('..................')
    print(pd.DataFrame(data['report_df'].groupby(['close_type'])['pl'].mean()))
    print('--------------------------------------\n\n')

    print('--------------------------------------')
    print('Sum by Close Type')
    print('..................')
    print(pd.DataFrame(data['report_df'].groupby(['close_type'])['pl'].sum()))
    print('--------------------------------------\n\n')

    print('--------------------------------------')
    x = np.round(data['report_df'].groupby(['month_val', 'date_val'])['pl'].sum().values.mean(),4)
    print(f'Average pips per day : {x}')
    print('--------------------------------------\n\n')

    print('--------------------------------------')
    x = data['report_df'].groupby(['month_val', 'date_val'])['pl'].count().values.mean()
    print(f'Average orders per day : {x}')
    print('--------------------------------------\n\n')

    plot_graph(data)
#...............................................................................................