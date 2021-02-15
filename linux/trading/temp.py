from utils.packages import *
warnings.filterwarnings('ignore')
import pickle
import joblib
import xgboost

temp_file = 'config/access_keys.yaml'
    
#model_jl = joblib.load('data/model/model_xg.pkl')  

#with open('data/model/model_xg.pkl', 'rb') as f:
#    model_pk = pickle.load(f)

#model_pk = pickle.load(open('data/model/model_xg.pkl', 'rb'))
filename = 'data/model/xgb.model'
loaded_model = xgboost.XGBClassifier(tree_method='gpu_hist', gpu_id=0)
loaded_model.load_model(filename)

#print(f'model_jl : {model_jl}')
#print(f'model_pk : {model_pk}')
print(f'loaded_model : {loaded_model}')

live_df = pd.read_csv('temp_test.csv')

pred = loaded_model.predict(live_df)
print(pred)
