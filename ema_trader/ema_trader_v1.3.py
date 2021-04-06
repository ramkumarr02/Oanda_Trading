from utils.packages import *
from utils.time_tick import *
from utils.variables import *
from utils.i_o import *
from utils.dir_slope import *
from utils.engine import *
from utils.loops import *
from utils.order import *
warnings.filterwarnings('ignore')


#--------------------------------------------------------------------------------------------------------------------------
# ### Inputs and Parameters

temp_file = 'config/access_keys.yaml'
with open(temp_file) as temp_file:
    config = yaml.load(temp_file)     
    
logging.basicConfig(filename='traderrun.log', level=logging.ERROR)

data['access_token'] = config[data['account']]['token']
data['accountID'] = config[data['account']]['account_id']
data['params'] = {'instruments': data['instrument']}

data['api'] = API(access_token = data['access_token'])
data['request_stream_data'] = pricing.PricingStream(accountID=data['accountID'], params=data['params'])
data['response_stream'] = data['api'].request(data['request_stream_data'])
data["start_ts"] = dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d-%H-%M')

data = get_invest_details(data)

data = check_for_open_orders(data)
data = check_for_open_orders(data)
data = check_for_open_orders(data)
#--------------------------------------------------------------------------------------------------------------------------



#--------------------------------------------------------------------------------------------------------------------------
# Run

if data['run_type'] == 'single':
    data = run_engine(data)        

elif data['run_type'] == 'loop':
    while data["run_flg"] ==  True:
        try:        
            data = run_engine(data)        
        
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