from sqlalchemy import create_engine, inspect
import yaml
import tabula
import pandas as pd

class DatabaseConnector:

    def __init__(self):
        pass

    def retrieve_pdf_data(self, link):
        '''Retrieve pdf data using link'''
        dfs = tabula.read_pdf(link, pages='all')
        return dfs
    
    def read_db_creds(self, file):
        '''Read credentials from local'''
        with open(file, 'r') as stream:
            data_loaded = yaml.safe_load(stream)

        print(data_loaded['RDS_HOST'])
        return data_loaded

    def init_db_engine(self, creds):
        '''Initialise database engine using credentials'''
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}")
        return engine

    def list_db_tables(self, engine):
        inspector = inspect(engine)
        db_tables_list = inspector.get_table_names()
        print(db_tables_list)
        return db_tables_list
    
    def upload_to_db(self, df, name, engine):
        df = pd.DataFrame(df)
        df.to_sql(name, engine, if_exists='replace')

if __name__ == '__main__':
    db_connector = DatabaseConnector()
    creds = db_connector.read_db_creds("local_db_creds.yaml")
    engine = db_connector.init_db_engine(creds)
    db_connector.list_db_tables(engine)