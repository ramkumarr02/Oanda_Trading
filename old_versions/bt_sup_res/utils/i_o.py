from utils.packages import *
from utils.variables import *


#...............................................................................................
def read_data(data):   
    data['source_file_path'] = f'data/{data["input_file_name"]}'
    # source_file_path = f'../data/products/{data["product"]}/{data["input_file_name"]}'

    if data['input_rows'] is None:
        data["df"] = pd.read_csv(data['source_file_path'])
        print(f'Read dataframe with {len(data["df"])} records.')
    else:
        data["df"] = pd.read_csv(data['source_file_path'], nrows=data['input_rows'])
        print(f'Read dataframe with {len(data["df"])} records.')
        
    data["df"] = data["df"][data["df"]['DateTime'].str.contains('|'.join(data['date_list']))]
    print(f'Dataframe has {len(data["df"])} records between {data["start_date"], data["end_date"]}.')

    data["df"]['tick']  = np.float()
    data['df']['DateTime_frmt'] = np.nan
    del data['df']['Volume']

    data["df"]['sema'] = np.nan
    data["df"]['slema'] = np.nan
    data["df"]['lema'] = np.nan

    data["df"]['position'] = np.nan
    data["df"]['to_order'] = np.nan
    data["df"]['h_line_angle'] = np.nan
    data["df"]['l_line_angle'] = np.nan
    data["df"]['h_trend_calc_spot'] = np.nan
    data["df"]['l_trend_calc_spot'] = np.nan
    data["df"]['small_h_trend_calc_spot'] = np.nan
    data["df"]['small_l_trend_calc_spot'] = np.nan
    data["df"]['sup_res_gap'] = np.nan
    data["df"]['stop_text'] = np.nan
    
    data['df']['stop_loss_pip'] = np.nan
    data['df']['pl_move_trail_trigger'] = np.nan
    data['df']['pl_move_min'] = np.nan
    # data["df"]['direction'] = np.nan
    # data["df"]['trend_angle'] = np.nan

    data['df']['h'] = np.nan
    data['df']['l'] = np.nan
    data['df']['small_h'] = np.nan
    data['df']['small_l'] = np.nan
    
    # data['df']['h_line'] = np.nan
    # data['df']['l_line'] = np.nan
    data['df']['long_open'] = np.nan
    data['df']['long_close'] = np.nan
    data['df']['short_open'] = np.nan
    data['df']['short_close'] = np.nan
    data['df']['pl'] = np.nan

    if data['df_subset_size'] is not None:
        data["df"] = data["df"][0:data['df_subset_size']]
        print(f'Subsetted dataframe with {len(data["df"])} records.')

    data["df"] = data["df"].reset_index(drop = True)
    print(f'Record num : {len(data["df"])}')        

    data['df_len'] = len(data["df"])

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

def print_results(data):
    try:
        display.clear_output(wait = True)
    except:
        pass

    pl_list = data['df']['pl'][data['df']['pl'].notnull()]
    print(f'Sum : {sum(pl_list)}')
    print('-----------------------------')
    print(data['df'][['DateTime','pl']][data['df']['pl'].notnull()])
    return(data)

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
def plot_graph(data):
    # Plot Layout --------------------------------
    chart_name = f"Trade Chart -- sema-lema:{data['sema_len']}-{data['lema_len']}, candle_size:{data['candle_size']}, line_len:{data['line_length']}, min_pts:{data['min_line_points']}, small_candle_size:{data['small_candle_size']}, line_len:{data['small_line_length']}"
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

    if 'sema' in data['included_loops']:
        fig.add_trace(go.Scatter(x=data['df']['DateTime_frmt'],
                                y=data['df']['sema'],
                                mode='lines',
                                name='sema',
                                line=dict(color='grey', width=1),
                            )
                    )    

    if 'slema' in data['included_loops']:
        fig.add_trace(go.Scatter(x=data['df']['DateTime_frmt'],
                            y=data['df']['slema'],
                            mode='lines',
                            name='slema',
                            line=dict(color='burlywood', width=1),
                        )
                )       


    if 'lema' in data['included_loops']:
        fig.add_trace(go.Scatter(x=data['df']['DateTime_frmt'],
                            y=data['df']['lema'],
                            mode='lines',
                            name='lema',
                            line=dict(color='blue', width=1),
                        )
                )                                                
    # --------------------------------
    if data['plot_std']:
        fig.add_trace(go.Scatter(x=data['df']['DateTime_frmt'],
                            y=data['df']['std_up'],
                            mode='lines',
                            name='std_up',
                            line=dict(color='grey', width=1),
                        )
                )       


        fig.add_trace(go.Scatter(x=data['df']['DateTime_frmt'],
                            y=data['df']['std_down'],
                            mode='lines',
                            name='std_down',
                            line=dict(color='grey', width=1),
                        )
                )                                                
    # --------------------------------


    # Tip points --------------------------------
    if data['plot_tip_points']:
        fig.add_scatter(x = data['df']['DateTime_frmt'], 
                    y = data['df']['h'], 
                    mode = 'markers', 
                    name = 'high',
                    marker_symbol = 'circle',
                    marker=dict(color='red',
                                size=data['marker_size'],
                                line=dict(
                                    color='crimson',
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
                                    color='darkblue',
                                    width=5
                                )),
                    opacity=1)
    #  --------------------------------
    if data['plot_transactions']:
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

    # Trend lines --------------------------------
    if data['plot_trend_lines']:

        fig.add_trace(go.Scatter(x=data['df']['DateTime_frmt'],
                                y=data['df']['h_line'],
                                mode='lines',
                                name='high_line',
                                line=dict(color='red', width=2, dash = 'dot'),                        
                                )
                    )

        fig.add_trace(go.Scatter(x=data['df']['DateTime_frmt'],
                                y=data['df']['l_line'],
                                mode='lines',
                                name='low_line',
                                line=dict(color='blue', width=2, dash = 'dot'),                        
                                )
                    )
    #  --------------------------------

    
    #  --------------------------------
    if data['plot_trend_calc_lines']:
        fig.add_scatter(x = data['df']['DateTime_frmt'], 
                    y = data['df']['h_trend_calc_spot'], 
                    mode = 'markers', 
                    name = 'Resistance',
                    marker_symbol = 'circle',
                    marker=dict(color='red',
                                size=data['marker_size'],
                                line=dict(
                                    color='red',
                                    width=0.5
                                )),
                    opacity=1)

        fig.add_scatter(x = data['df']['DateTime_frmt'], 
                    y = data['df']['l_trend_calc_spot'], 
                    mode = 'markers', 
                    name = 'Support',
                    marker_symbol = 'circle',
                    marker=dict(color='blue',
                                size=data['marker_size'],
                                line=dict(
                                    color='blue',
                                    width=0.5
                                )),
                    opacity=1)
        
        # fig.add_scatter(x = data['df']['DateTime_frmt'], 
        #             y = data['df']['small_h_trend_calc_spot'], 
        #             mode = 'markers', 
        #             name = 'Resistance',
        #             marker_symbol = 'circle',
        #             marker=dict(color='orange',
        #                         size=data['marker_size'],
        #                         line=dict(
        #                             color='orange',
        #                             width=0.5
        #                         )),
        #             opacity=1)

        # fig.add_scatter(x = data['df']['DateTime_frmt'], 
        #             y = data['df']['small_l_trend_calc_spot'], 
        #             mode = 'markers', 
        #             name = 'Support',
        #             marker_symbol = 'circle',
        #             marker=dict(color='purple',
        #                         size=data['marker_size'],
        #                         line=dict(
        #                             color='purple',
        #                             width=0.5
        #                         )),
        #             opacity=1)
    #  --------------------------------    
    
    
    # Angle line --------------------------------
    if data['plot_angle_line']:
        fig.add_trace(go.Scatter(x=data['df']['DateTime_frmt'],
                                y=data['df']['h_line_angle'],
                                mode='lines',
                                name='Resistance_angle',
                                line=dict(color='red', width=1, dash = 'dot'),yaxis='y2'),
                    )

        fig.add_trace(go.Scatter(x=data['df']['DateTime_frmt'],
                            y=data['df']['l_line_angle'],
                            mode='lines',
                            name='Support_angle',
                            line=dict(color='blue', width=1, dash = 'dot'),yaxis='y2'),
                )

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
def send_telegram_message(message_text):     
    data['telegram_url'] = "https://api.telegram.org/bot"
    data['url_for_Chat_id'] = f'{data["telegram_url"]}{keys.tester_bot_token}/getUpdates'   
    
    send_message_url = f'{data["telegram_url"]}{keys.tester_bot_token}/sendMessage?chat_id={keys.chat_id}/&text={message_text}'
    requests.get(send_message_url)
#...............................................................................................    