# Restrict prices to 4 decimal places (pips)
def restrict_to_pips(num):
    numstring = str(num)
    num = float(numstring[:numstring.find('.')+5])
    return(num)



# Add prices into chunks for direction identification
def get_chunks(i, val, chunk_size, small_list,size_flag,change_position):   
    
    if len(small_list) < chunk_size: #Keep adding prices until we reach chunk size
        small_list.append(val)  
               
    if size_flag == 'reached_chunk_size':        
        if small_list[-1] != val: 
            small_list.popleft()   #Remove the left most (first) price
            small_list.append(val) #Add current value to right most position

                
        change_position -= 1  #Price allocation in small list happens right to left so change position goes from chunk size to zero
        if change_position < 0: 
            change_position = chunk_size - 1 #If position reaches zero, it needs to be reset to chunk size - 1 (for index position)

            
    if len(small_list) == chunk_size: #check if small list has reached chunk size
        size_flag = 'reached_chunk_size'  
    
    return(chunk_size, small_list,size_flag,change_position)



# Identify directions
def find_direction(lst):
    list_size = len(lst)
    diff = {}
    dir_flag = 'Error : not calculated'
   
    for i in range(list_size-1): #write the list into a dictionary 
        diff[i] = lst[i+1] - lst[i]       
        
    if list(diff.values())[-1] == 0:
        dir_flag = 'flat'        
        
    elif all(x>0 for x in diff.values()):
        dir_flag = 'positive'
    
    elif all(x<0 for x in diff.values()):
        dir_flag = 'negative'

    elif list(diff.values())[-2] >= 0 and list(diff.values())[-1] < 0:
        dir_flag = 'dir_change_negative'      

    elif list(diff.values())[-2] <= 0 and list(diff.values())[-1] > 0:
        dir_flag = 'dir_change_positive'      
        
    else:
        dir_flag = 'no_single_direction'
        
    return(dir_flag)



def write_price_dict(price_details, tick_price, truncated_tick_price, direction):
    price_details['tick_price'].append(tick_price)
    price_details['truncated_tick_price'].append(truncated_tick_price)
    price_details['direction'].append(direction)
    return(price_details)