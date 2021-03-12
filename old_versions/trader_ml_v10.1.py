# # ML Trader
# ### Packages
from utils.packages import *
from utils.engine import *
from utils.fixed_variables import *
warnings.filterwarnings('ignore')

#--------------------------------------------------------------------------------------------------------------------------
# ### Inputs and Parameters

temp_file = 'config/access_keys.yaml'
with open(temp_file) as temp_file:
    config = yaml.load(temp_file)     
    
logging.basicConfig(filename='traderrun.log', level=logging.ERROR)

data['access_token'] = config['oanda_demo_hedge']['token']
data['accountID'] = config['oanda_demo_hedge']['account_id']
data['params'] = {'instruments': data['instrument']}

data['api'] = API(access_token = data['access_token'])
request_stream_data = pricing.PricingStream(accountID=data['accountID'], params=data['params'])
response_stream = data['api'].request(request_stream_data)
#==========================================================================================================================



#--------------------------------------------------------------------------------------------------------------------------
# Prep
data = check_for_open_orders(data)
data = check_for_open_orders(data)
data = check_for_open_orders(data)

data = reset_data(data)

data['start_ts'] = (datetime.now() + timedelta(hours=8, minutes=0)).strftime("%Y-%b-%d, %I:%M:%S (%p)")
data["start_ts_internal"] = time.time()

#data['start_ts'] = (datetime.now() + timedelta(hours=8, minutes=0)).strftime("%Y-%b-%d, %I:%M:%S (%p)")
#==========================================================================================================================


#--------------------------------------------------------------------------------------------------------------------------
# Run

if data['run_type'] == 'single':
    data, live_df_full = run_engine(data, live_df_full)        

elif data['run_type'] == 'loop':
    while data["run_flg"] ==  True:
        try:        
            data, live_df_full = run_engine(data, live_df_full)        
        
        except KeyboardInterrupt:
            print("Run manually stopped")
            ts = dt.datetime.now()
            err_msg = 'KeyboardInterrupt'
            logging.error(f'--- Timestamp-{ts}, Error-{err_msg}')
            break           
        
        except Exception as err_msg:
            data['error_count'] = data['error_count'] + 1
            ts = dt.datetime.now()
            logging.error(f'--- Timestamp-{ts}, Error-{err_msg}')
#==========================================================================================================================            