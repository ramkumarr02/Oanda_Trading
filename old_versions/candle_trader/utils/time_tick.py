from utils.packages import *

#--------------------------------------------------------------------------------------------------------------------------
# Get timestamp of the price and segregate it
def get_date_time(data):
    time_stamp = data['resp']['time']
    
    # Convert Timestamp to python timestamp form
    # --------------------------------------------------------
    data['ts_date_val'], full_time = time_stamp.split(sep = 'T')
    data['ts_time_val'], _ = full_time.split(sep = '.')
    data['ts_date_val'] = dt.datetime.strptime(data['ts_date_val'], '%Y-%m-%d')
    data['ts_time_val'] = dt.datetime.strptime(data['ts_time_val'], '%H:%M:%S')
    tot_ts = dt.datetime.combine(dt.datetime.date(data['ts_date_val']), dt.datetime.time(data['ts_time_val']))
    # --------------------------------------------------------
    # if data['os'] != 'linux':
    #     tot_ts = tot_ts + timedelta(hours=8)   
    #     disp_ts = tot_ts             
    # else:
    #     disp_ts = tot_ts + timedelta(hours=8)
    # --------------------------------------------------------
    data['tot_ts']  = tot_ts.strftime("%Y-%b-%d, %I:%M:%S (%p)")      
    data['disp_ts'] = data['tot_ts']
        
    t2 = dt.datetime.utcnow()    
        
    data['time_diff'] = (t2 - tot_ts).total_seconds()

    return(data)
#==========================================================================================================================



#--------------------------------------------------------------------------------------------------------------------------
# Get bid and ask prices
def get_prices(data):    
    data['bid']     = float(data['resp']['bids'][0]['price'])    
    data['ask']     = float(data['resp']['asks'][0]['price'])
    data['spread']  = data['ask'] - data['bid']
    data['tick']    = (data['ask'] + data['bid']) / 2

    # data['bid']     = np.round(data['bid'],5) 
    # data['ask']     = np.round(data['ask'],5) 
    # data['spread']  = np.round(data['spread'],5) 
    # data['tick']    = np.round(data['tick'],5) 

    return(data)
#==========================================================================================================================



#--------------------------------------------------------------------------------------------------------------------------
# sleep over weekend
def sleep_check():
    curr_time = dt.datetime.utcnow()

    if curr_time.weekday() >= 4:

        if curr_time.weekday() == 4:
            start_ts = datetime(year   = curr_time.year, 
                                month  = curr_time.month, 
                                day    = curr_time.day, 
                                hour   = 21, 
                                minute = 0, 
                                second = 1)

            end_ts = datetime(year   = curr_time.year, 
                              month  = curr_time.month, 
                              day    = curr_time.day, 
                              hour   = 21, 
                              minute = 59, 
                              second = 59) + timedelta(days = 2)        


            if curr_time > start_ts:
                start_ts = curr_time
                end_ts = datetime(year   = curr_time.year, 
                                  month  = curr_time.month, 
                                  day    = curr_time.day, 
                                  hour   = 21, 
                                  minute = 59, 
                                  second = 59) + timedelta(days = 2)        



        if curr_time.weekday() == 5:
            start_ts = curr_time
            end_ts = datetime(year   = curr_time.year, 
                              month  = curr_time.month, 
                              day    = curr_time.day, 
                              hour   = 21, 
                              minute = 59, 
                              second = 59) + timedelta(days = 1)        

        if curr_time.weekday() == 6:
            start_ts = curr_time
            end_ts = datetime(year   = curr_time.year, 
                              month  = curr_time.month, 
                              day    = curr_time.day, 
                              hour   = 21, 
                              minute = 59, 
                              second = 59)


        if end_ts > curr_time >= start_ts:
            duration_secs = np.floor((end_ts - curr_time).total_seconds())
            print('---------------------------------------------------')
            print('SLEEPING')
            print(f"Sleep start time  : {curr_time}")        
            print(f'Sleeping duration : {int(duration_secs)} seconds')
            print(f"Wake up time      : {end_ts}")
            time.sleep(duration_secs)
            print('---------------------------------------------------')    
    return()
#==========================================================================================================================    