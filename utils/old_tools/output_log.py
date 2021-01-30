from utils.packages import *
from utils.tools import *

def get_output_data(api, accountID, instrument, make_order_log, close_order_log, iters, close_reason, dirc):
    output_data = {'date':[],
                   'time':[],
                   'instrument':[],
                   'direction':[],                   
                   'ordr_type':[],                   
                   'units':[],
                   'profit_pips':[],
                   'close_reason':[],
                   'Iterations':[],                   
                   'orderID':[]
                  }
    

    if dirc:    
        # Make_Order_Log
        #-------------------------------------------------
        make_dict_key = list(make_order_log.keys())[1]
        uni = int(make_order_log[make_dict_key]['units'])
        if uni > 0:
            output_data['ordr_type'] = 'long'
            output_data['direction'] = 'positive'
        else:
            output_data['ordr_type'] = 'short'
            output_data['direction'] = 'negative'        


        # Close_Order_Log
        #-------------------------------------------------        
        if close_order_log != 'stop_loss_trigger':    
            close_dict_key= list(close_order_log.keys())[1]
            dt, tm, _ = get_date_time(close_order_log[close_dict_key])
            output_data['date'].append(dt)  
            output_data['time'].append(tm)
            output_data['instrument'].append(close_order_log[close_dict_key]['instrument'])
            output_data['units'].append(uni)
            output_data['profit_pips'].append(close_order_log[close_dict_key]['pl'])
            output_data['orderID'].append(close_order_log[close_dict_key]['orderID'])
            output_data['close_reason'].append(close_reason)
            output_data['Iterations'].append(iters)



        # Stop_Order_Logging
        #-------------------------------------------------
        elif close_order_log == 'stop_loss_trigger':
            last_position_r = positions.PositionDetails(accountID, instrument)
            last_position_rv = api.request(last_position_r)
            last_transaction_id = last_position_rv['lastTransactionID']

            transaction_details_r = trans.TransactionDetails(accountID, transactionID=last_transaction_id)
            transaction_details_rv = api.request(transaction_details_r)

            time_stamp = transaction_details_rv['transaction']['fullPrice']['timestamp']
            dt, full_time = time_stamp.split(sep = 'T')
            tm, time_fraction = full_time.split(sep = '.')
            inst = transaction_details_rv['transaction']['instrument']
            #unts = transaction_details_rv['transaction']['units']
            prfit_pips = transaction_details_rv['transaction']['pl']
            clse_reason = transaction_details_rv['transaction']['reason']
            ordrID = transaction_details_rv['transaction']['orderID']

            output_data['date'].append(dt)  
            output_data['time'].append(tm)
            output_data['instrument'].append(inst)
            output_data['units'].append(uni)
            output_data['profit_pips'].append(prfit_pips)
            output_data['orderID'].append(ordrID)
            output_data['close_reason'].append(close_reason)
            output_data['Iterations'].append(iters)  
            
            
    elif dirc == False:
        d = datetime.datetime.utcnow()
        d_with_timezone = d.replace(tzinfo=pytz.UTC)
        time_stamp = d_with_timezone.isoformat()
        dt_now, full_time = time_stamp.split(sep = 'T')
        tm_now, time_fraction = full_time.split(sep = '.')

        output_data['date'].append(dt_now)  
        output_data['time'].append(tm_now)
        output_data['instrument'].append(instrument)
        output_data['direction'] = 'no_direction'        
        output_data['ordr_type'].append('')
        output_data['units'].append('')
        output_data['profit_pips'].append('')
        output_data['orderID'].append('')
        output_data['close_reason'].append('')
        output_data['Iterations'].append('') 

        
    # Write to Dataframe
    #-------------------------------------------------    
    output_df = pd.DataFrame()
    output_df = pd.DataFrame.from_dict(output_data)
    output_df = output_df[['date', 'time', 'instrument', 'direction', 'ordr_type','units', 'profit_pips', 'close_reason', 'Iterations','orderID']]

    return(output_df)