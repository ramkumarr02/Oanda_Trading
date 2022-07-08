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
    data['df']['hour_val'] = [x.hour for x in data['df']['DateTime_frmt']]

    data['df']['long_profit'] = np.nan
    data['df']['long_loss'] = np.nan
    data['df']['short_profit'] = np.nan
    data['df']['short_loss'] = np.nan

    data['df']['long_profit'][data['df']['pl'] > 0] = data['df']['long_close']
    data['df']['long_loss'][data['df']['pl'] < 0] = data['df']['long_close']

    data['df']['short_profit'][data['df']['pl'] > 0] = data['df']['short_close']
    data['df']['short_loss'][data['df']['pl'] < 0] = data['df']['short_close']

    del data['df']['long_close']
    del data['df']['short_close']

    # data['df'] = data['df'][data['final_columns_list']]
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
    print(data['df'][data['df']['pl'].notnull()][['DateTime_frmt', 'order_side','close_type', 'pl']].tail(15))

#...............................................................................................    

#...............................................................................................    
def send_telegram_message(message_text):     
    data['telegram_url'] = "https://api.telegram.org/bot"
    data['url_for_Chat_id'] = f'{data["telegram_url"]}{keys.tester_bot_token}/getUpdates'   
    
    send_message_url = f'{data["telegram_url"]}{keys.tester_bot_token}/sendMessage?chat_id={keys.chat_id}/&text={message_text}'
    requests.get(send_message_url)
#...............................................................................................    

#...............................................................................................
def generate_result_report(data):
    data['report_df'] = data['df'][data['df']['pl'].notnull()]

    winsound.PlaySound('C:\\Windows\\Media\\tada.wav', winsound.SND_ASYNC)
    data["daily_pl"] = pd.DataFrame(data['report_df'].groupby(['date_val'])['pl'].sum())
    data["monthly_pl"] = pd.DataFrame(data['report_df'].groupby(['month_val'])['pl'].sum())
    data["net_pl"] = data['report_df']['pl'].sum().round(4)

    if data['send_message_to_phone']:
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
    print('Daily PL')
    print(f'{data["daily_pl"]}')
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

    if data['to_csv']:
        data['report_df'].to_csv('data/result.csv')
#...............................................................................................

#...............................................................................................
#...............................................................................................
def plot_graph(data):
    if data["plot"]:
        if data['reduce_plot']:
            data['plot_df'] = data['df'][(data['df']['DateTime_frmt'] > data['plot_start']) & (data['df']['DateTime_frmt'] < data['plot_stop'])]
        else:
            data['plot_df'] = data['df']

        # Plot Layout --------------------------------
        chart_name = f"Trade Chart"
        layout = go.Layout(title = chart_name,
                        xaxis = dict(title="DateTime"),
                        xaxis2 = dict(title= 'x', side= 'top'),
                        
                        yaxis = dict(title="PIP"),
                        yaxis2 = dict(title= 'Trend Angle', overlaying="y", side="right",)
                        )
        fig = go.Figure(layout = layout)
        # -------------------------------------------------------------------


        # -------------------------------------------------------------------
        if 'tick' in data['things_to_plot']:
            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                    y=data['plot_df']['tick'],
                                    mode='lines',
                                    name='tick',
                                    line=dict(color='lightgrey', width=1),
                                )
                        )

        if 'lema' in data['things_to_plot']:
            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                y=data['plot_df']['lema'],
                                mode='lines',
                                name='lema',
                                line=dict(color='blue', width=1),
                            )
                    )                                                     
        # -------------------------------------------------------------------


        # -------------------------------------------------------------------
        if 'h_l' in data['things_to_plot']:
            fig.add_scatter(x = data['df']['DateTime_frmt'], 
                            y = data['df']['h'], 
                            mode = 'markers', 
                            name = 'high',
                            marker_symbol = 'circle',
                            marker=dict(color='red',
                                        size=data['marker_size'],
                                        line=dict(
                                            color='red',
                                            width=5
                                        )),                            
                            opacity=1)

            fig.add_scatter(x = data['df']['DateTime_frmt'], 
                            y = data['df']['l'], 
                            mode = 'markers', 
                            name = 'low',
                            marker_symbol = 'circle',
                            marker=dict(color='blue',
                                        size=data['marker_size'],
                                        line=dict(
                                            color='blue',
                                            width=5
                                        )),
                            opacity=1)                             
        # -------------------------------------------------------------------


        # -------------------------------------------------------------------
        if 'h_l_lema' in data['things_to_plot']:
            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                y=data['plot_df']['h_lema'],
                                mode='lines',
                                name='h_lema',
                                line=dict(color='red', width=1, dash = 'dot'),
                            )
                    )   

            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                y=data['plot_df']['l_lema'],
                                mode='lines',
                                name='l_lema',
                            line=dict(color='blue', width=1, dash = 'dot'),
                            )
                    )   

            # fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
            #                     y=data['plot_df']['h_lema_2'],
            #                     mode='lines',
            #                     name='h_lema_2',
            #                     line=dict(color='red', width=1, dash = 'dash'),
            #                 )
            #         )   

            # fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
            #                     y=data['plot_df']['l_lema_2'],
            #                     mode='lines',
            #                     name='l_lema_2',
            #                 line=dict(color='blue', width=1, dash = 'dash'),
            #                 )
            #         )                       
        # -------------------------------------------------------------------


        # -------------------------------------------------------------------
        if 'tick_angle' in data['things_to_plot']:
            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                y=data['plot_df']['tick_angle'],
                                mode='lines',
                                name='tick_angle',
                                yaxis='y2',
                            line=dict(color='grey', width=0.5, dash = 'dot'),
                            )
                    )   

            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                y=[0] * len(data['plot_df']['tick_angle']),
                                mode='lines',
                                name='angle_0',
                                yaxis='y2',
                            line=dict(color='grey', width=1),
                            )
                    )   
        # -------------------------------------------------------------------


        # -------------------------------------------------------------------
        if 'positions' in data['things_to_plot']:
            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                                y = data['plot_df']['long_open'], 
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

            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                        y = data['plot_df']['short_open'], 
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

            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                        y = data['plot_df']['long_profit'], 
                        mode = 'markers', 
                        name = 'long_profit',
                        marker_symbol = 'triangle-up',
                        marker=dict(color='cadetblue',
                                    size=10,
                                    line=dict(
                                        color='black',
                                        width=1
                                    )),
                        opacity=1)

            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                        y = data['plot_df']['long_loss'], 
                        mode = 'markers', 
                        name = 'long_loss',
                        marker_symbol = 'triangle-up',
                        marker=dict(color='red',
                                    size=10,
                                    line=dict(
                                        color='red',
                                        width=1
                                    )),
                        opacity=1)


            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                        y = data['plot_df']['short_profit'], 
                        mode = 'markers', 
                        name = 'short_profit',
                        marker_symbol = 'triangle-down',
                        marker=dict(color='cadetblue',
                                    size=10,
                                    line=dict(
                                        color='black',
                                        width=1
                                    )),
                        opacity=1)




            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                        y = data['plot_df']['short_loss'], 
                        mode = 'markers', 
                        name = 'short_loss',
                        marker_symbol = 'triangle-down',
                        marker=dict(color='red',
                                    size=10,
                                    line=dict(
                                        color='red',
                                        width=1
                                    )),
                        opacity=1)                        
        # -------------------------------------------------------------------


        # -------------------------------------------------------------------
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