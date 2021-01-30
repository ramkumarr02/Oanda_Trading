from utils.packages import *
from utils.tools import *

def run_direction_engine(api, accountID, instrument, num, target_num, min_count, pip_size, pip_gap, min_count_mulitplier): 
    print(f'Finding Market Direction with min trans of {num}...')
    
    params = {'instruments': instrument}
    
    reached_targets = {'start_price' : 0,
                       'target_num' : 0,
                       'positive_val' : 0,
                       'negative_val' : 0,
                       'positive' : 0,
                       'p_duration' : '',
                       'n_duration' : '',
                       'negative' : 0}

    pos_target_flag = 'not_reached'
    neg_target_flag = 'not_reached'
    first_run_flag = 0
    pip_position = pip_gap - 1
    
    df_reached_targets = pd.DataFrame()
    tick_list = []

    
    
    r = pricing.PricingStream(accountID=accountID, params=params)
    rv = api.request(r)

    start_time = time.time()

    for i, resp in tqdm(enumerate(rv)):

        if i < num: # Check if we are within the required number of price iterations               
            resp_type = resp['type']       

            if resp_type == 'HEARTBEAT': # Heart beat response to keep the api connection alive (Avoid timeout)
                pass
                #print(resp_type)

            elif resp_type == 'PRICE': # Check whether it is a price response                 
                date_val, time_val, time_fraction = get_date_time(resp) # Get time stamp for reference            
                sell_price, buy_price, spread, tick_price = get_prices(resp) # Get prices from the response                      
                tick_list.append(tick_price)

                if first_run_flag == 0:
                    positive_targets, negative_targets = get_targets(tick_price, target_num, pip_size)
                    first_run_flag = 1
                    for j in range(target_num):
                        df_reached_targets = df_reached_targets.append(reached_targets, ignore_index = True)
                        df_reached_targets.loc[df_reached_targets.index[j], 'target_num'] = j+1
                        df_reached_targets.loc[df_reached_targets.index[j], 'start_price'] = tick_price
                        df_reached_targets.loc[df_reached_targets.index[j], 'positive_val'] = positive_targets[j]
                        df_reached_targets.loc[df_reached_targets.index[j], 'negative_val'] = negative_targets[j]

                for k in range(target_num):
                    if tick_price >= positive_targets[k]:
                        price_diff = tick_price - df_reached_targets.loc[df_reached_targets.index[k], 'start_price']
                        df_reached_targets.loc[df_reached_targets.index[k], 'positive'] += (price_diff * 10000)
                        
                        if pos_target_flag == 'not_reached':
                            end_time = time.time()    
                            duration = calc_duration(start_time, end_time)
                            df_reached_targets.loc[df_reached_targets.index[k], 'p_duration'] = duration
                            pos_target_flag = 'reached'

                    if tick_price <= negative_targets[k]:
                        price_diff = df_reached_targets.loc[df_reached_targets.index[k], 'start_price'] - tick_price
                        df_reached_targets.loc[df_reached_targets.index[k], 'negative'] += (price_diff * 10000)

                        if neg_target_flag == 'not_reached':
                            end_time = time.time()    
                            duration = calc_duration(start_time, end_time)
                            df_reached_targets.loc[df_reached_targets.index[k], 'n_duration'] = duration
                            neg_target_flag = 'reached'

        else: # Crossed the required number of price iterations
            try:
                r.terminate(message = "maxrecs records received")
            except:
                pass

    df_reached_targets =  df_reached_targets[['start_price', 'target_num', 'positive_val', 'negative_val','positive', 'negative','p_duration','n_duration']]

    df_reached_targets.loc[df_reached_targets.index[0], 'positive'] = df_reached_targets.loc[df_reached_targets.index[0], 'positive'] - df_reached_targets.loc[df_reached_targets.index[1], 'positive']
    df_reached_targets.loc[df_reached_targets.index[1], 'positive'] = df_reached_targets.loc[df_reached_targets.index[1], 'positive'] - df_reached_targets.loc[df_reached_targets.index[2], 'positive']
    df_reached_targets.loc[df_reached_targets.index[0], 'negative'] = df_reached_targets.loc[df_reached_targets.index[0], 'negative'] - df_reached_targets.loc[df_reached_targets.index[1], 'negative']
    df_reached_targets.loc[df_reached_targets.index[1], 'negative'] = df_reached_targets.loc[df_reached_targets.index[1], 'negative'] - df_reached_targets.loc[df_reached_targets.index[2], 'negative']
    
    direction = get_direction(df_reached_targets, target_num, min_count, pip_position, min_count_mulitplier)

    #winsound.PlaySound('C:\\Windows\\Media\\tada.wav', winsound.SND_ASYNC) 
    return(direction, df_reached_targets, tick_list)