# Import Libraries
import pandas as pd
import numpy as np
import logging
from functions.data_prep import DataPreparation
from functions.prediction import PredictProductivityModel

# Though in real, we would probably make a query from SQL database, here we are limited with a CSV file
file_path = '/Users/irenaz/Desktop/Masters - DSBA/SEM4/CONSULTING/project/DS2-Consulting/data/garments_worker_productivity.csv'

def run_preprocessing(file_path):
    """Function that reads the data, applies preprocessing, prediction, and returns the final DataFrame."""
    
    # Step 1: Data Cleaning & Transformations
    logging.info('Reading data from CSV file')
    df = pd.read_csv(file_path)

    df_prep = DataPreparation(df=df)

    missing_cols = df_prep.check_missing_data()
    logging.info(f'Columns with NA: {missing_cols.values}')

    df_imputed = df_prep.impute_missing_data(missing_cols=missing_cols, impute_option='zero')
    df_transformed = df_prep.transform_data()
    logging.info('Transformed data info:')
    df_transformed.info()

    # Step 2: Predicting Productivity with XGBoost
    logging.info('Initializing PredictProductivityModel')
    model = PredictProductivityModel()

    logging.info('Creating lag features')
    model.create_lag_features(data=df_transformed, features=['actual_productivity', 'targeted_productivity', 'over_time'], lags=2).info()

    logging.info('Fitting the model')
    model.fit(data=df_transformed, features=['actual_productivity', 'targeted_productivity', 'over_time'],
              lags=2,
              target='actual_productivity',
              split_date='2015-03-04',
              date_column='date')

    logging.info('Making predictions')
    final_df = model.predict()

    return final_df

if __name__ == '__main__':
    """When the code is executed, the DataFrame is preprocessed and saved to CSV"""
    final_df = run_preprocessing(file_path)
    final_df.to_csv('final_df.csv', index=False)
    logging.info('Preprocessed data is saved to CSV')
