# ### Packages
from utils.packages import *

# ### Slope
#--------------------------------------------------------------------------------------------------------------------------
def get_slope(y_axis, data):
    #global data
    ma_len = len(y_axis)
    
    x_axis = []
    for i in range(ma_len):
        x_axis.append(1 + ((i+1) * 0.0001 * 0.1))
    
    slope_tick, intercept, _, _, _ = linregress(x_axis, y_axis)
    slope_tick = math.degrees(math.atan(slope_tick))
    
    return(slope_tick)
#==========================================================================================================================


# ### Class Mapping
#--------------------------------------------------------------------------------------------------------------------------
def map_predictions(data):
    #global data
    
    if data['prediction'] == 'same':
        data['order_create'] = None
    
    elif data['prediction'] == 'increase':
        data['order_create'] = 'long'
        
    elif data['prediction'] == 'decrease':
        data['order_create'] = 'short'
        
    return(data)
#==========================================================================================================================