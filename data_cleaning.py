import pandas as pd
import numpy as np

class DataCleaning:

    def __init__(self):
        pass

    def clean_user_data(self, user_data_df):
        '''Drop null values and clean date data in user data'''
        # Drop NULL values
        user_data_df.dropna(inplace = True) 

        # Handle date errors
        user_data_df['date_of_birth'] = pd.to_datetime(user_data_df['date_of_birth'], errors='coerce')
        user_data_df['join_date'] = pd.to_datetime(user_data_df['join_date'], errors='coerce')

        return user_data_df
    
    def clean_card_data(self, card_data_df):
        '''Drop null values and clean date data in card data'''
        # Drop NULL values
        card_data_df.dropna(inplace = True) 

        # Handle date errors
        card_data_df['expiry_date'] = pd.to_datetime(card_data_df['expiry_date'], format='%m/%Y', errors='coerce')

        return card_data_df

    def called_clean_store_data(self, df):
        # Drop NULL values
        df.dropna(inplace = True) 
        # Handle date errors
        df['opening_date'] = pd.to_datetime(df['opening_date'], errors='coerce')
        return df
    
    def convert_product_weights(self, df):
        '''Convert all weights to gram in weight column'''
        df['weight'] = df['weight'].apply(self.convert_to_grams)
        return df
    
    def convert_to_grams(self, value):
        '''Get every weight in grams'''
        value = str(value).replace(' .', '')
        if value.endswith('kg'):
            value = self.replace_strings('kg', value, 1000)
        elif value.endswith('g'):   
            value = self.replace_strings('g', value)
        elif value.endswith('ml'):   
            value = self.replace_strings('ml', value)
        elif value.endswith('l'):   
            value = self.replace_strings('l', value, 1000)
        elif value.endswith('oz'):   
            value = self.replace_strings('oz', value, 28.35)
        else:
            value = np.nan
        return value
        
    def replace_strings(self, end, value, factor = 1):
        '''Calculate the result if there's multiply'''
        value = value.replace(end, '')
        result = 0
        if 'x' in value:
            value = value.replace(' ','')
            numbers = value.split('x')
            result = str(float(numbers[0]) * float(numbers[1]) * factor)
        else:
            result = float(value) * factor
        return result
    
    def clean_products_data(self, df):
        '''Drop null values and clean date data in products data'''
        # Drop NULL values
        df.dropna(inplace = True)
        # Handle date errors
        df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
        return df
    
    def clean_orders_data(self, df):
        '''Drop null values and clean date data in orders data'''
        # Drop unnecessary fields
        df.drop(columns='first_name',inplace = True)
        df.drop(columns='last_name',inplace = True)
        df.drop(columns='1',inplace = True)
        df.drop(columns='level_0',inplace = True)
        # Drop NULL values
        df.dropna(inplace = True)
        return df
    
    def clean_date_times(self, df):
        '''Convert date strings to integers and correct format'''
        # Handle date errors
        df['month'] = pd.to_numeric( df['month'],errors='coerce', downcast="integer")
        df['year'] = pd.to_numeric( df['year'], errors='coerce', downcast="integer")
        df['day'] = pd.to_numeric( df['day'], errors='coerce', downcast="integer")
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M:%S', errors='coerce')
        # Drop NULL values
        df.dropna(how='any',inplace= True)
        df.reset_index(inplace=True)       
        return df