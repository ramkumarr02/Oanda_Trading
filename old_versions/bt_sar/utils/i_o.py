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
    data['df_ohlc']['month_val'] = [x.month for x in data['df_ohlc']['DateTime_frmt']]
    data['df_ohlc']['date_val'] = [x.day for x in data['df_ohlc']['DateTime_frmt']]
    data['df_ohlc']['hour_val'] = [x.hour for x in data['df_ohlc']['DateTime_frmt']]

    data['df_ohlc']['long_profit'] = np.nan
    data['df_ohlc']['long_loss'] = np.nan
    data['df_ohlc']['short_profit'] = np.nan
    data['df_ohlc']['short_loss'] = np.nan

    data['df_ohlc']['long_profit'][data['df_ohlc']['pl'] > 0] = data['df_ohlc']['long_close']
    data['df_ohlc']['long_loss'][data['df_ohlc']['pl'] < 0] = data['df_ohlc']['long_close']

    data['df_ohlc']['short_profit'][data['df_ohlc']['pl'] > 0] = data['df_ohlc']['short_close']
    data['df_ohlc']['short_loss'][data['df_ohlc']['pl'] < 0] = data['df_ohlc']['short_close']

    data['df_ohlc'].loc[data['df_ohlc']['up'].notnull(), 'order_side'] = 'long'
    data['df_ohlc'].loc[data['df_ohlc']['down'].notnull(), 'order_side'] = 'short'

    del data['df_ohlc']['long_close']
    del data['df_ohlc']['short_close']

    # data['df_ohlc'] = data['df_ohlc'][data['final_columns_list']]
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

    print(np.sum(data['df_ohlc'][['pl']]))
    print('--------------------------------------')
    print(data['df_ohlc'][data['df_ohlc']['pl'].notnull()][['DateTime_frmt', 'order_side','close_type', 'pl']].tail(15))

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
    print('PL Split')
    p = data['report_df']['pl'][data['report_df']['pl'] > 0]
    print(f"{p.count()} Positive trans with total pl : {p.sum()}")

    n = data['report_df']['pl'][data['report_df']['pl'] < 0]
    print(f"{n.count()} Negative trans with total pl : {n.sum()}")
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

def get_report_df(data):
    
    cols = ['DateTime_frmt', 'month_val', 'date_val', 'hour_val','open', 'high', 'low', 'close', 'candle_size', 'ask',
           'bid', 'lema', 'lema_angle', 'lema_angle_2', 'lema_angle_0', 'slema',
           'slema_angle', 'slema_angle_2', 'sema', 'sema_angle', 'sema_angle_2',
           'BBand_upper', 'BBand_middle', 'BBand_lower', 'BBand_width',
           'avg_BBand_width', 'adx', 'order_side', 'order_size', 'up', 'down', 'long_open', 'long_profit', 'long_loss', 'short_open',
           'short_profit', 'short_loss', 'close_type', 'pl', 'close_diff', 'tip','lema_match',  'lema_max',  'lema_min',  'lema_gap', 'lema_diff']

    data['df_small'] = data['df_ohlc'][cols][data['df_ohlc'][['long_open', 'short_open', 'pl']].notnull().any(axis=1)].reset_index(drop=True)

    data['df_small']['pl_type'] = np.nan

    for i in tqdm(range(1, len(data['df_small']))):
        if data['df_small']['pl'][i] > 0:
            data['df_small'].loc[i-1, 'pl_type']        = 'positive'
            data['df_small'].loc[i-1, 'long_profit']    = data['df_small'].loc[i, 'long_profit']
            data['df_small'].loc[i-1, 'short_profit']   = data['df_small'].loc[i, 'short_profit']
            data['df_small'].loc[i-1, 'pl']             = data['df_small'].loc[i, 'pl']
            data['df_small'].loc[i-1, 'close_type']     = data['df_small'].loc[i, 'close_type']
            data['df_small'].drop(i, inplace=True)

        elif data['df_small']['pl'][i] < 0:
            data['df_small']['pl_type'][i-1]            = 'negative'
            data['df_small'].loc[i-1, 'long_loss']      = data['df_small'].loc[i, 'long_loss']
            data['df_small'].loc[i-1, 'short_loss']     = data['df_small'].loc[i, 'short_loss']
            data['df_small'].loc[i-1, 'pl']             = data['df_small'].loc[i, 'pl']
            data['df_small'].loc[i-1, 'close_type']     = data['df_small'].loc[i, 'close_type']        
            data['df_small'].drop(i, inplace=True)

        elif data['df_small']['pl'][i] == 0:
            data['df_small']['pl_type'][i-1] = 'zero'        

    data['df_small']['weekday'] = data['df_small']['DateTime_frmt'].dt.weekday

    data['df_small'].loc[data['df_small']['up'].notnull(),'order_side'] = 'long'
    data['df_small'].loc[data['df_small']['down'].notnull(),'order_side'] = 'short'
        
    return(data)

#...............................................................................................

#...............................................................................................
#...............................................................................................
#...............................................................................................
def plot_graph(data):
    temp_df = data['df_ohlc']

    if data["plot"]:
        if data['reduce_plot']:
            data['plot_df'] = temp_df[(temp_df['DateTime_frmt'] > data['plot_start']) & (temp_df['DateTime_frmt'] < data['plot_stop'])]
        else:
            data['plot_df'] = temp_df            

        # Plot Layout --------------------------------
        layout = go.Layout(title = 'chart_name',
                        xaxis = dict(title="DateTime"),
                        xaxis2 = dict(title= 'x', side= 'top'),
                        
                        yaxis = dict(title="PIP"),
                        yaxis2 = dict(title= 'Trend Angle', overlaying="y", side="right",)
                        )

        fig = go.Figure(layout = layout)        
        # -------------------------------------------------------------------

        if 'candles' in data['things_to_plot']:
            fig.add_trace(go.Candlestick(x=data['plot_df']['DateTime_frmt'],
                open=data['plot_df']['open'],
                high=data['plot_df']['high'],
                low=data['plot_df']['low'],
                close=data['plot_df']['close']))

        # -------------------------------------------------------------------
        if 'tick' in data['things_to_plot']:
            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                    y=data['plot_df']['tick'],
                                    mode='lines',
                                    name='tick',
                                    line=dict(color='lightgrey', width=1),
                                )
                        )

        if 'close' in data['things_to_plot']:
            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                    y=data['plot_df']['close'],
                                    mode='lines',
                                    name='close',
                                    line=dict(color='darkgrey', width=1),
                                )
                        )


        if 'lema' in data['things_to_plot']:
            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                y=data['plot_df']['lema'],
                                mode='lines',
                                name='lema',
                                line=dict(color='black', width=2),
                            )
                    ) 

        if 'sema' in data['things_to_plot']:
            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                y=data['plot_df']['sema'],
                                mode='lines',
                                name='sema',
                                line=dict(color='red', width=1),
                            )
                    )                                                                                                                                                 

        if 'slema' in data['things_to_plot']:
            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                y=data['plot_df']['slema'],
                                mode='lines',
                                name='slema',
                                line=dict(color='blue', width=1),
                            )
                    ) 

        if 'sema_lema_diff' in data['things_to_plot']:
            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                y=data['plot_df']['sema_lema_diff'],
                                mode='lines',
                                name='sema_lema_diff',
                                yaxis='y2',
                            line=dict(color='blue', width=1, dash = 'dot'),
                            )
                    )   

            # fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
            #                     y=data['plot_df']['ma'],
            #                     mode='lines',
            #                     name='ma',
            #                     line=dict(color='blue', width=0.5),
            #                 )
            #         ) 


        if 'mp' in data['things_to_plot']:
            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                y=data['plot_df']['sema_mp'],
                                mode='lines',
                                name='sema_mp',
                                line=dict(color='red', width=1),
                            )
                    ) 

            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                y=data['plot_df']['slema_mp'],
                                mode='lines',
                                name='slema_mp',
                                line=dict(color='black', width=1),
                            )
                    ) 

            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                y=data['plot_df']['lema_mp'],
                                mode='lines',
                                name='lema_mp',
                                line=dict(color='blue', width=1),
                            )
                    ) 

        if 'sema_angle' in data['things_to_plot']:
            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                y=data['plot_df']['sema_angle'],
                                mode='lines',
                                name='sema_angle',
                                yaxis='y2',
                            line=dict(color='red', width=1, dash = 'dot'),
                            )
                    )       

            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                y=data['plot_df']['sema_angle_2'],
                                mode='lines',
                                name='sema_angle_2',
                                yaxis='y2',
                            line=dict(color='red', width=1, dash = 'dash'),
                            )
                    )   

        if 'close_diff' in data['things_to_plot']:
            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                    y=data['plot_df']['close_diff'],
                                    mode='lines',
                                    name='close_diff',
                                    yaxis='y2',
                                    line=dict(color='black', width=1, dash = 'dot'),
                                )
                        )

        if 'slema_angle' in data['things_to_plot']:
            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                y=data['plot_df']['slema_angle'],
                                mode='lines',
                                name='slema_angle',
                                yaxis='y2',
                            line=dict(color='blue', width=1, dash = 'dot'),
                            )
                    )       


            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                y=data['plot_df']['slema_angle_2'],
                                mode='lines',
                                name='slema_angle_2',
                                yaxis='y2',
                            line=dict(color='blue', width=1, dash = 'dash'),
                            )
                    )   


        if 'lema_angle' in data['things_to_plot']:
            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                y=data['plot_df']['lema_angle'],
                                mode='lines',
                                name='lema_angle',
                                yaxis='y2',
                            line=dict(color='black', width=1, dash = 'dot'),
                            )
                    )       


            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                y=data['plot_df']['lema_angle_2'],
                                mode='lines',
                                name='lema_angle_2',
                                yaxis='y2',
                            line=dict(color='black', width=1, dash = 'dash'),
                            )
                    )       

        fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                            y=[0] * len(data['plot_df']['lema_angle']),
                            mode='lines',
                            name='angle_0',
                            yaxis='y2',
                        line=dict(color='grey', width=1),
                        )
                )   

        if 'rsi' in data['things_to_plot']:
            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                y=data['plot_df']['rsi'],
                                mode='lines',
                                name='rsi',
                                yaxis='y2',
                            line=dict(color='blue', width=1, dash = 'dot'),
                            )
                    )       
        if 'adx' in data['things_to_plot']:
            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                y=data['plot_df']['adx'],
                                mode='lines',
                                name='adx',
                                yaxis='y2',
                            line=dict(color='black', width=1, dash = 'dot'),
                            )
                    )       

        if 'lema_diff' in data['things_to_plot']:
            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                y=data['plot_df']['lema_diff'],
                                mode='lines',
                                name='lema_diff',
                                yaxis='y2',
                            line=dict(color='black', width=1, dash = 'dot'),
                            )
                    ) 

            # fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
            #                     y=data['plot_df']['tema_angle'],
            #                     mode='lines',
            #                     name='tema_angle',
            #                     yaxis='y2',
            #                 line=dict(color='black', width=1, dash = 'dot'),
            #                 )
            #         )  

            # fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
            #                     y=data['plot_df']['tema_angle_2'],
            #                     mode='lines',
            #                     name='tema_angle_2',
            #                     yaxis='y2',
            #                 line=dict(color='black', width=1, dash = 'dash'),
            #                 )
            #         )  


        if 'sar_line' in data['things_to_plot']:
            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                y=[data['sar_line']] * len(data['plot_df']['sar_gap']),
                                mode='lines',
                                name='sar_line',
                                yaxis='y2',
                            line=dict(color='grey', width=1),
                            )
                    )   

        # -------------------------------------------------------------------

        # -------------------------------------------------------------------

        if 'BBands' in data['things_to_plot']:
            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                y=data['plot_df']['BBand_upper'],
                                mode='lines',
                                name='BBand_upper',
                                line=dict(color='red', width=2.5, dash = 'dot'),
                            )
                    )                                                                         

            # fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
            #                     y=data['plot_df']['BBand_middle'],
            #                     mode='lines',
            #                     name='BBand_middle',
            #                     line=dict(color='black', width=2.5, dash = 'dot'),
            #                 )
            #         )                                                                         

            fig.add_trace(go.Scatter(x=data['plot_df']['DateTime_frmt'],
                                y=data['plot_df']['BBand_lower'],
                                mode='lines',
                                name='BBand_lower',
                                line=dict(color='blue', width=2.5, dash = 'dot'),
                            )
                    ) 
        # -------------------------------------------------------------------


        # -------------------------------------------------------------------
        if 'sar' in data['things_to_plot']:
            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                                y = data['plot_df']['sar'], 
                                mode = 'markers', 
                                name = 'sar',
                                marker_symbol = 'circle',
                                marker=dict(color='red',
                                            size=5,
                                            line=dict(
                                                color='black',
                                                width=1
                                            )),
                                opacity=1)

        if 'lema_change' in data['things_to_plot']:
            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                                # y = data['plot_df']['lema_change'], 
                                y = data['plot_df']['lema_change'], 
                                mode = 'markers', 
                                name = 'lema_change',
                                marker_symbol = 'circle',
                                marker=dict(color='red',
                                            size=5,
                                            line=dict(
                                                color='black',
                                                width=1
                                            )),
                                opacity=1)

        if 'close_max' in data['things_to_plot']:
            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                                # y = data['plot_df']['lema_change'], 
                                y = data['plot_df']['close_max'], 
                                mode = 'markers', 
                                name = 'close_max',
                                marker_symbol = 'circle',
                                marker=dict(color='red',
                                            size=5,
                                            line=dict(
                                                color='red',
                                                width=1
                                            )),
                                opacity=1)

        if 'close_min' in data['things_to_plot']:
            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                                # y = data['plot_df']['lema_change'], 
                                y = data['plot_df']['close_min'], 
                                mode = 'markers', 
                                name = 'close_min',
                                marker_symbol = 'circle',
                                marker=dict(color='blue',
                                            size=5,
                                            line=dict(
                                                color='blue',
                                                width=1
                                            )),
                                opacity=1)                                

        if 'lema_match' in data['things_to_plot']:
            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                                y = data['plot_df']['lema_match'], 
                                mode = 'markers', 
                                name = 'lema_match',
                                marker_symbol = 'circle',
                                marker=dict(color='black',
                                            size=5,
                                            line=dict(
                                                color='black',
                                                width=1
                                            )),
                                opacity=1)

        if 'match_max' in data['things_to_plot']:
            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                                y = data['plot_df']['match_max'], 
                                mode = 'markers', 
                                name = 'match_max',
                                marker_symbol = 'circle',
                                marker=dict(color='red',
                                            size=5,
                                            line=dict(
                                                color='red',
                                                width=1
                                            )),
                                opacity=1)

        if 'match_min' in data['things_to_plot']:
            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                                y = data['plot_df']['match_min'], 
                                mode = 'markers', 
                                name = 'match_min',
                                marker_symbol = 'circle',
                                marker=dict(color='blue',
                                            size=5,
                                            line=dict(
                                                color='blue',
                                                width=1
                                            )),
                                opacity=1)

        if 'unmatched' in data['things_to_plot']:
            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                                y = data['plot_df']['unmatched'], 
                                mode = 'markers', 
                                name = 'unmatched',
                                marker_symbol = 'circle',
                                marker=dict(color='darkgrey',
                                            size=5,
                                            line=dict(
                                                color='darkgrey',
                                                width=1
                                            )),
                                opacity=1)

        if 'cross' in data['things_to_plot']:
            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                                y = data['plot_df']['cross'], 
                                mode = 'markers', 
                                name = 'cross',
                                marker_symbol = 'circle',
                                marker=dict(color='blue',
                                            size=10,
                                            line=dict(
                                                color='black',
                                                width=1
                                            )),
                                opacity=1)

        if 'tip' in data['things_to_plot']:
            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                                y = data['plot_df']['tip'], 
                                mode = 'markers', 
                                name = 'tip',
                                marker_symbol = 'circle',
                                marker=dict(color='yellow',
                                            size=10,
                                            line=dict(
                                                color='black',
                                                width=1
                                            )),
                                opacity=1)

            # fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
            #                     y = data['plot_df']['top'], 
            #                     mode = 'markers', 
            #                     name = 'top',
            #                     marker_symbol = 'circle',
            #                     marker=dict(color='red',
            #                                 size=10,
            #                                 line=dict(
            #                                     color='red',
            #                                     width=1
            #                                 )),
            #                     opacity=1)

            # fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
            #                     y = data['plot_df']['bottom'], 
            #                     mode = 'markers', 
            #                     name = 'bottom',
            #                     marker_symbol = 'circle',
            #                     marker=dict(color='blue',
            #                                 size=10,
            #                                 line=dict(
            #                                     color='blue',
            #                                     width=1
            #                                 )),
            #                     opacity=1)

        if 'lema_max_min' in data['things_to_plot']:
            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                                y = data['plot_df']['lema_max'], 
                                mode = 'markers', 
                                name = 'lema_max',
                                marker_symbol = 'circle',
                                marker=dict(color='red',
                                            size=1,
                                            line=dict(
                                                color='red',
                                                width=1
                                            )),
                                opacity=1)

            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                                y = data['plot_df']['lema_min'], 
                                mode = 'markers', 
                                name = 'lema_min',
                                marker_symbol = 'circle',
                                marker=dict(color='blue',
                                            size=1,
                                            line=dict(
                                                color='blue',
                                                width=1
                                            )),
                                opacity=1)

        if 'sema_max_min' in data['things_to_plot']:
            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                                y = data['plot_df']['sema_max'], 
                                mode = 'markers', 
                                name = 'sema_max',
                                marker_symbol = 'circle',
                                marker=dict(color='red',
                                            size=1,
                                            line=dict(
                                                color='red',
                                                width=1
                                            )),
                                opacity=1)

            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                                y = data['plot_df']['sema_min'], 
                                mode = 'markers', 
                                name = 'sema_min',
                                marker_symbol = 'circle',
                                marker=dict(color='blue',
                                            size=1,
                                            line=dict(
                                                color='blue',
                                                width=1
                                            )),
                                opacity=1)
                                
        if 'lema_angle_0' in data['things_to_plot']:
            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                                y = data['plot_df']['lema_angle_0'], 
                                mode = 'markers', 
                                name = 'lema_angle_0',
                                marker_symbol = 'circle',
                                marker=dict(color='blue',
                                            size=1,
                                            line=dict(
                                                color='blue',
                                                width=1
                                            )),
                                opacity=1)

        # -------------------------------------------------------------------

        if 'dir' in data['things_to_plot']:
            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                                y = data['plot_df']['up'], 
                                mode = 'markers', 
                                name = 'up',
                                marker_symbol = 'triangle-up',
                                marker=dict(color='blue',
                                            size=10,
                                            line=dict(
                                                color='blue',
                                                width=1
                                            )),
                                opacity=1)

            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                                y = data['plot_df']['down'], 
                                mode = 'markers', 
                                name = 'down',
                                marker_symbol = 'triangle-down',
                                marker=dict(color='red',
                                            size=10,
                                            line=dict(
                                                color='red',
                                                width=1
                                            )),
                                opacity=1)


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

            # fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
            #             y = data['plot_df']['all_close'], 
            #             mode = 'markers', 
            #             name = 'all_close',
            #             marker_symbol = 'circle',
            #             marker=dict(color='black',
            #                         size=10,
            #                         line=dict(
            #                             color='red',
            #                             width=1
            #                         )),
            #             opacity=1)                           
        # -------------------------------------------------------------------
        # -------------------------------------------------------------------
        if 'indicators' in data['things_to_plot']:
            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                                y = data['plot_df']['cdl_hammer'], 
                                mode = 'markers', 
                                name = 'cdl_hammer',
                                marker_symbol = 'hash',
                                marker=dict(color='blue',
                                            size=10,
                                            line=dict(
                                                color='blue',
                                                width=1
                                            )),
                                opacity=1)

            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                                y = data['plot_df']['cdl_shootingstar'], 
                                mode = 'markers', 
                                name = 'cdl_shootingstar',
                                marker_symbol = 'star',
                                marker=dict(color='red',
                                            size=10,
                                            line=dict(
                                                color='red',
                                                width=1
                                            )),
                                opacity=1)

            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                                y = data['plot_df']['cdl_engulfing_up'], 
                                mode = 'markers', 
                                name = 'cdl_engulfing_up',
                                marker_symbol = 'square',
                                marker=dict(color='blue',
                                            size=10,
                                            line=dict(
                                                color='blue',
                                                width=1
                                            )),
                                opacity=1)

            fig.add_scatter(x = data['plot_df']['DateTime_frmt'], 
                                y = data['plot_df']['cdl_engulfing_down'], 
                                mode = 'markers', 
                                name = 'cdl_engulfing_down',
                                marker_symbol = 'square',
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

def lema_gap_pl_analysis(data):

    if data['lema_gap_pl_analysis_month']:
        data['temp_df'] = data['df_small'][data['df_small']['month_val'] == data['lema_gap_pl_analysis_month']]
    else:
        data['temp_df'] = data['df_small']     
    
    order_side = 'positive'
    y = pd.DataFrame(data['temp_df'][data['temp_df']['pl_type'] == order_side].lema_gap.round(3).value_counts())
    y= y.reset_index()
    y = y.rename(columns = {'lema_gap':order_side})

    t = data['temp_df'].loc[data['temp_df']['pl_type'] == order_side, ['lema_gap', 'pl']]
    t['lema_gap'] = t['lema_gap'].round(3)
    t1 = pd.DataFrame(t.groupby('lema_gap').pl.sum()).reset_index().rename(columns={'lema_gap': 'index', 'pl':f'{order_side}_sum'})

    order_side = 'negative'
    x= pd.DataFrame(data['temp_df'][data['temp_df']['pl_type'] == order_side].lema_gap.round(3).value_counts())
    x = x.reset_index()
    x = x.rename(columns = {'lema_gap':order_side})

    t = data['temp_df'].loc[data['temp_df']['pl_type'] == order_side, ['lema_gap', 'pl']]
    t['lema_gap'] = t['lema_gap'].round(3)
    t2 = pd.DataFrame(t.groupby('lema_gap').pl.sum()).reset_index().rename(columns={'lema_gap': 'index', 'pl':f'{order_side}_sum'})

    x = x.merge(y, on = 'index', how = 'outer')
    x = x.merge(t1, on = 'index', how = 'outer')
    all = x.merge(t2, on = 'index', how = 'outer')

    all = all.fillna(0)

    all['count_diff'] = all['positive'] - all['negative']
    all['sum_diff'] = all['positive_sum'] - abs(all['negative_sum'])

    # all = all.sort_values(by = ['count_diff', 'sum_diff', 'index'])
    all = all.sort_values(by = ['index'])
    all = all[['index','positive', 'negative', 'count_diff', 'positive_sum', 'negative_sum', 'sum_diff']]
    data['lema_gap_pl_report'] = all
    
    return(data)

#...............................................................................................