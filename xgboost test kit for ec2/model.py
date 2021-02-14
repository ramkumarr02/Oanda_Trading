import joblib
import xgboost
import warnings
import numpy as np
import pandas as pd
warnings.filterwarnings('ignore')
from sklearn.metrics import classification_report


test_file = '2020'
target_col = 'direction'
remove_cols = ['tick_avg', 'sema', 'ssma', 'lema', 'lsma', 'max_tick', 'min_tick', 'rs']

#test_data = 'data/yearly_tick_data/tab_'+ test_file +'.csv'
test_data = 'tab_'+ test_file +'.csv'
df1 = pd.read_csv(test_data)
df1 = df1.round(5)
df1.drop(remove_cols, axis=1, inplace=True)

x = df1.loc[:, df1.columns != target_col]
y = df1[target_col]

#clf_xg = joblib.load('data/model/model_xg.pkl')
clf_xg = joblib.load('model_xg.pkl')
predictions = clf_xg.predict(x)

print(classification_report(y, predictions))