from utils.packages import *



#...............................................................................................
def read_data(data):
    #source_file_path = f'..\\data\\yearly_tick_data\\{data["year"]}.csv'
    source_file_path = f'data/{data["year"]}.csv'

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
def get_date_lines(data):
    data['line_list'] = []
    
    for dt_val  in data['date_list']:    
        try:
            data['line_list'].append(data["df"][data["df"]['DateTime'].str.contains(dt_val)].index[0])
        except:
            pass
    
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
    fig, ax1 = plt.subplots(figsize=(50,10))
    ax2 = ax1.twinx()

    x_axis = np.arange(0,len(data["df"]['tick']))

    ax1.plot(x_axis, data["df"]['tick'], label='tick', color='green', linestyle='dotted')
    ax1.plot(x_axis, data["df"]['sema'], label='sema', color='black')
    ax1.plot(x_axis, data["df"]['lema'], label='lema', color='blue')

    data = get_date_lines(data)

    for x_val in data['line_list']:
        plt.axvline(x=x_val, color='black')

    ax1.scatter(data['buy_markers_x'], data['buy_markers_y'], s=300, c='b', marker=10)
    ax1.scatter(data['sell_markers_x'], data['sell_markers_y'], s=300, c='r', marker=11)

    ax2.plot(data['df']["sema_angle"], c='k', label = 'sema_angle', linestyle = 'dashed')
    ax2.plot(data['df']["lema_angle"], c='b', label = 'lema_angle', linestyle = 'dashed')

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
    data['chart_name'] = f'{data["file_name"].split(".")[0]}.png'
    fig.savefig(data['chart_name'])
#...............................................................................................



#...............................................................................................
def create_report(data):
    data['report_df'] = pd.DataFrame({'date':data['dt_list'], 'pls': data['pl_list'], 'close_type': data['close_type']})
    split_date_col(data)
    data['report_df'] = data['report_df'][['date', 'year_val', 'month_val', 'date_val', 'hour_val','minute_val', 'close_type', 'pls']]
    data["report_df"] = data["report_df"].reset_index(drop = True)    

    data['file_name'] = f'data/{data["start_date"].year}-{data["start_date"].month}-({data["start_date"].day}-{data["end_date"].day})-{data["start_ts"]}.csv'
    data['report_df'].to_csv(data['file_name'], index = False) 
    
    if data['running_in'] == 'windows':
        os.system('cls')
    elif data['running_in'] == 'linux':
        os.system('clear')
    elif data['running_in'] == 'notebook':
        display.clear_output(wait = True)

    print(np.sum(data['report_df'][['pls']]))
    print('--------------------------------------')
    print(data['report_df'][['date', 'close_type', 'pls']])
#...............................................................................................    