from utils.packages import *

#...............................................................................................
def print_report(data):
       
    if data['os'] == 'windows':
        os.system('cls')
    elif data['os'] == 'linux':
        os.system('clear')
    elif data['os'] == 'notebook':        
        display.clear_output(wait = True)    

    print('---------------------------')
    print(f"Bot             : EMA - {data['instrument']}")
    print('---------------------------')
    print(f"iter            : {data['iter']}")
    print(f"time            : {data['disp_ts']}")
    print(f"time_diff       : {data['time_diff']}")
    print(f"tick            : {data['tick']}")
    print(f"lema len        : {len(data['lema_tick_list'])}/{data['lema_len']}")
    print(f"lema            : {data['lema']}")    
    print(f"position        : {data['position']}")  
    print(f"candle_swing    : {data['candle_swing']}")    
    print(f"to_order        : {data['to_order']}")    
    print(f"take_profit_flg : {data['take_profit_flg']}")  
    print(f"sema angle      : {data['sema_angle']}")
    print(f"lema angle      : {data['lema_angle']}")
    print(f"pl              : {data['pl']}")
    print(f"error_count     : {data['error_count']}")
    print(f"num_orders      : {data['num_orders']}")
    print('---------------------------')    
#...............................................................................................  

def capture_in_df(data):
    data['df'] = data['df'][-1000:]
    data['df'].loc[data['iter'], ['DateTime_frmt']] = data['tot_ts_2']
    data['df'].loc[data['iter'], ['bid']] = data['bid']
    data['df'].loc[data['iter'], ['ask']] = data['ask']
    data['df'].loc[data['iter'], ['tick']] = data['tick']
    data['df'].loc[data['iter'], ['lema']] = data['lema']
    return(data)
   
#...............................................................................................    

def plot_plotly_graph(data):
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
    fig.show()