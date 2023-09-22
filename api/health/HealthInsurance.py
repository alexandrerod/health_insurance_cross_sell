import pickle
import inflection
import pandas as pd


class HealthInsurance(object):
    def __init__(self):
        self.home_path = '/home/alexandrerod/Documentos/repos/health_insurance_cross_sell/'
        self.age_scaler = pickle.load(open(self.home_path + 'parameters/age_scaler.pkl','rb'))
        self.annual_premium_scaler = pickle.load(open(self.home_path + 'parameters/annual_premium.pkl','rb'))
        self.policy_chanel_scaler = pickle.load(open(self.home_path + 'parameters/policy_chanel_scaler.pkl','rb'))
        self.region_scaler = pickle.load(open(self.home_path + 'parameters/region_scaler.pkl','rb'))
        self.vintage_scaler = pickle.load(open(self.home_path + 'parameters/vintage_scaler.pkl','rb'))
        self.vehicle_age_encoding = pickle.load(open(self.home_path + 'parameters/vehicle_age_encoding.pkl','rb'))

    def cleanind_data (self, df1):

        #old columns
        cols_old = list(df1.columns)
        #creating function
        rename_columns = lambda x: inflection.underscore(x)
        #new columns
        cols_new = list(map(rename_columns, cols_old))
        #renaming columns 
        df1.columns = cols_new

        return df1
    
    def feature_engineering (self, df2):
        return df2
    
    def data_preparation(self, df5):

        #gender train
        df5 = pd.get_dummies(df5, prefix=['gender'], columns=['gender']  ,dtype='int64')
        

        #vehicle_damage train
        df5 = pd.get_dummies(df5, prefix=['vehicle_damage'], columns=['vehicle_damage'] ,dtype='int64' )
        

        df5['vehicle_age'] = self.vehicle_age_encoding.transform(df5[['vehicle_age']].values)
        
        #age train
        df5['age'] = self.age_scaler.transform(df5[['age']].values)
    
        #region_code train
        df5['region_code'] = self.region_scaler.transform(df5[['region_code']].values)

        #annual_premium train
        df5['annual_premium'] = self.annual_premium_scaler.transform(df5[['annual_premium']].values)

        #policy_sales_channel train
        df5['policy_sales_channel'] = self.policy_chanel_scaler.transform(df5[['policy_sales_channel']].values)
        
        #vintage train
        df5['vintage'] = self.vintage_scaler.transform(df5[['vintage']].values)

        cols_selected = ['age','driving_license', 'region_code','previously_insured',
                            'vehicle_age', 'annual_premium', 'policy_sales_channel',
                            'gender_Female','gender_Male', 'vehicle_damage_No',
                            'vehicle_damage_Yes']
                            
        return df5[cols_selected]
    
    
    def get_prediction(self ,model, original_data, test_data):
        #prediction
        pred = model.predict_proba(test_data)
        
        # join pred into the original data
        original_data['prediction'] = pred
        
        return original_data.to_json( orient='records', date_format='iso' )