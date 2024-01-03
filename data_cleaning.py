import pandas as pd
import numpy as np
import re

class DataCleaning:

    def __init__(self):
        pass

    def clean_user_data(self, user_data_df):
        '''Drop null values and clean date data in user data'''
        # Drop NULL values
        user_data_df.dropna(subset=['user_uuid'], how='any', axis=0, inplace=True)

        # Handle date errors
        user_data_df['date_of_birth'] = pd.to_datetime(user_data_df['date_of_birth'], errors='coerce')
        user_data_df['join_date'] = pd.to_datetime(user_data_df['join_date'], errors='coerce')

        return user_data_df
    
    def clean_card_data(self, card_data_df):
        '''Drop null values and clean date data in card data'''
        # Drop NULL values
        card_data_df.dropna(inplace=True) 

        # Handle date errors
        card_data_df['date_payment_confirmed'] = pd.to_datetime(card_data_df['date_payment_confirmed'], errors='coerce')
        card_data_df.dropna(subset=['date_payment_confirmed'], inplace=True)

        return card_data_df

    def called_clean_store_data(self, df):
        # Drop unnecessary column
        df.drop(columns='lat', inplace=True)
        # Remove the data if staff number is not valid                    
        df['staff_numbers'] = pd.to_numeric( df['staff_numbers'].apply(self.remove_char_from_string),errors='coerce', downcast="integer") 
        df.dropna(subset = ['staff_numbers'],how='any',inplace= True)
        return df
    
    def remove_char_from_string(self,value):
        return re.sub(r'\D', '',value)
    
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
        # Handle typo
        df['removed'] = df['removed'].str.replace('Still_avaliable', 'Still_available')
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
    
    def clean_date_times(self,df,column_name):
        df[column_name] = pd.to_datetime(df[column_name], format='%Y-%m-%d', errors='ignore')
        df[column_name] = pd.to_datetime(df[column_name], format='%Y %B %d', errors='ignore')
        df[column_name] = pd.to_datetime(df[column_name], format='%B %Y %d', errors='ignore')
        df[column_name] = pd.to_datetime(df[column_name], errors='coerce')
        df.reset_index(inplace=True)
        return df