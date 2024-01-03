# Multinational Retail Data Centralisation

This app gets different data from various sources and cleans them. Then upload to the local SQL database created using PostgreSQL.

Some technologies and libraries used; Python, PostgreSQL, AWS, pandas, numpy, sqlalchemy, requests, tabula, boto3

## Installation
Download te project and install required python libraries to run the project.

## Usage
Use main.py to download, clean and upload data. Other files are including helper classes. You can find examples in files.

## File Structure
### Database Utils
Includes DatabaseConnector class to retrieve data, read credentials and initialise database engine.

### Data Extraction
Includes DataEctractor class to get list of stores, read tables and retrieve relevant data from sources.

### Data Cleaning
Includes DataCleaning class to clean various data. Use the relevant method for the data you want to clean.

### Main
The main file includes the methods to upload tables to the database. Usually methods first download data, then clean data and lastly upload this clean data to the database.

### Queries
Queries folder includes sql files for different purposes.For better organization, they have been gathered under this folder.

#### Update DB
This sql file includes queries to update or change tables. Also there are display data queries to decide what has to be updated exactly.
