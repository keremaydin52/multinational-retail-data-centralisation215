from database_utils import DatabaseConnector 
from data_extraction import DataExtractor 
from data_cleaning import DataCleaning

class Main:

    def __init__(self):
        pass
    
    def upload_dim_users(self):

        # Create instances
        data_extractor = DataExtractor()
        db_connector = DatabaseConnector()
        data_cleaning = DataCleaning()

        # Connect to the database and get list of tables
        creds = db_connector.read_db_creds("db_creds.yaml") 
        engine = db_connector.init_db_engine(creds)
        engine.connect()
        tables_list = db_connector.list_db_tables(engine)

        # Clean the data
        df_name = tables_list[1]
        df = data_cleaning.clean_user_data(data_extractor.read_rds_table(engine, df_name))
        print(df.head())

        # Upload to the local db
        creds = db_connector.read_db_creds("local_db_creds.yaml") 
        engine = db_connector.init_db_engine(creds)
        engine.connect()
        db_connector.upload_to_db(df,'dim_users',engine)

    def upload_dim_card_details(self):

        # Create instances
        data_extractor = DataExtractor()
        db_connector = DatabaseConnector()
        data_cleaning = DataCleaning() 

        # Get data from pdf
        df = data_extractor.retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')
        
        # Clean the data
        df = data_cleaning.clean_card_data(df)
        print(df.head())
        
        # upload to the db
        creds = db_connector.read_db_creds("local_db_creds.yaml") 
        engine = db_connector.init_db_engine(creds)

        db_connector.upload_to_db(df,'dim_card_details',engine)

    def upload_dim_store_details(self):
        
        # Create instances
        data_extractor = DataExtractor()
        db_connector = DatabaseConnector()
        data_cleaning = DataCleaning()

        # Get data
        df = data_extractor.retrieve_stores_data('https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/')

        # Clean data 
        df = data_cleaning.called_clean_store_data(df)
        
        # Upload to db 
        cred = db_connector.read_db_creds("local_db_creds.yaml") 
        engine = db_connector.init_db_engine(cred)
        engine.connect()
        db_connector.upload_to_db(df,'dim_store_details', engine)

    def upload_dim_products(self):

        # Create instances
        data_extractor = DataExtractor()
        db_connector = DatabaseConnector()
        data_cleaning = DataCleaning()  

        # Get data from s3
        df = data_extractor.extract_from_s3('s3://data-handling-public/products.csv')
        df = data_cleaning.convert_product_weights(df)

        # Clean data 
        df =  data_cleaning.clean_products_data(df)
        print(df)
        
        # Upload to db 
        creds = db_connector.read_db_creds("local_db_creds.yaml") 
        engine = db_connector.init_db_engine(creds)
        engine.connect()
        db_connector.upload_to_db(df, 'dim_products', engine)

    def upload_orders_table(self):

        # Create instances
        data_extractor = DataExtractor()
        db_connector = DatabaseConnector()
        data_cleaning = DataCleaning()

        # Connect to db
        creds = db_connector.read_db_creds("db_creds.yaml") 
        engine = db_connector.init_db_engine(creds)
        tables_list = db_connector.list_db_tables(engine)

        # Get frame name and download
        df_name = tables_list[2]
        df = data_extractor.read_rds_table( engine, df_name)

        # Clean data 
        df = data_cleaning.clean_orders_data(df)

        # Upload to db 
        creds = db_connector.read_db_creds("local_db_creds.yaml") 
        engine = db_connector.init_db_engine(creds)
        engine.connect()
        db_connector.upload_to_db(df, 'orders_table', engine)

    def upload_dim_date_times(self):

        # Create instances
        data_extractor = DataExtractor()
        db_connector = DatabaseConnector()
        data_cleaning = DataCleaning()

        # Get data
        df = data_extractor.extract_json('https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json')
        print(df.head())

        # Clean data
        df = data_cleaning.clean_date_times(df)

        # Upload to the database
        creds = db_connector.read_db_creds("local_db_creds.yaml") 
        engine = db_connector.init_db_engine(creds)
        engine.connect()
        db_connector.upload_to_db(df,'dim_date_times', engine)

if __name__ == '__main__':
    main = Main()
    main.upload_dim_users()