from utils.packages import *
from utils.i_o import *

#...............................................................................................  

def encode_x_y_split(data):
    
    temp_df = data["df_ohlc"].loc[:, data["df_ohlc"].columns != "DateTime_frmt"]

    if len(data['remove_cols']) > 0:
        for col_name in data['remove_cols']:
            del temp_df[col_name]

    data["x"] = temp_df.loc[:, temp_df.columns != data["target_col"]]
    data["y"] = temp_df[data["target_col"]]

    data["encoder"] = LabelEncoder()
    data["encoder"].fit(data["y"])
    data["y_encoded"] = data["encoder"].transform(data["y"])
    data["y_map"] = dict(zip(data["encoder"].transform(data["encoder"].classes_),data["encoder"].classes_))

    data["train_x"], data["valid_x"], data["train_y"], data["valid_y"] = train_test_split(data["x"], data["y_encoded"],train_size = 0.8,random_state = 1)

    print(f'encode_x_y_split    : Completed')
    
    return(data)

#...............................................................................................  

def train_model(data):    
    data["clf"] = data['classifier'].fit(data["train_x"], data["train_y"])
    data["predictions"] = data["clf"].predict(data["valid_x"])    
    data["acc"] = metrics.accuracy_score(data["predictions"], data["valid_y"])  

    print(f'train_model         : Completed')

    return (data)

#...............................................................................................  

def print_classification_report(data):

    print('-------------------------------------')
    print(f"Overall Accuracy : {data['acc']}")
    print('-------------------------------------')
    
    target_names = list(data['y_map'].values())
    print(classification_report(data["valid_y"], data['predictions'], target_names=target_names))
    
    return(data)
#...............................................................................................     