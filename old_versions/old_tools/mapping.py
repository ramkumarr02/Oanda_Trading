from utils.packages import *

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