import pandas as pd
import requests as req
import tabula
import boto3

class DataExtractor:

    header_details = {
        "x-api-key": "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"
    }

    def __init__(self):
        pass

    def list_number_of_stores(self, endpoint, header_details):
        response = req.get(endpoint, headers = header_details)
        return response.json()['number_stores']

    def read_rds_table(self, engine, table_name):
        '''Query the database table into a Pandas DataFrame'''
        query = f'SELECT * FROM {table_name};'
        df = pd.read_sql_query(query, engine)

        return df
    
    def retrieve_stores_data(self, endpoint):
        '''Retrieve stores data from endpoint'''
        list_of_frames = []
        store_number = self.list_number_of_stores('https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores', self.header_details)
        for i in range(store_number):
            response = req.get(f'{endpoint}{i}',headers=self.header_details)
            list_of_frames.append(pd.json_normalize(response.json()))

        return pd.concat(list_of_frames)
    
    def retrieve_pdf_data(self, link):
        '''Retreive pdf data and convert to DataFrame'''
        return pd.concat(tabula.read_pdf(link, pages='all'))
    
    def extract_from_s3(self, address):
        '''Extract CSV using s3 address'''
        s3 = boto3.client('s3')
        bucket, key = address.replace("s3://", "").split("/", 1)
        s3.download_file(bucket, key, key)
        df = pd.read_csv(key)
        print(df)
        return df
    
    def extract_json(self, address):
        '''Extract json with link'''
        response = req.get(address) 
        json = response.json()
        df = pd.DataFrame(json)
        return df


if __name__ == '__main__':

    data_extractor = DataExtractor()
    data_extractor.extract_from_s3('s3://data-handling-public/products.csv')

    '''
    db_connector = DatabaseConnector()
    data_extractor = DataExtractor()
    data_extractor.read_rds_table(db_connector)
    

    data_extractor = DataExtractor()
    print(data_extractor.header_details)
    count = data_extractor.list_number_of_stores('https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores', data_extractor.header_details)
    print(count)
    '''