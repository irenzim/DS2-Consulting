# The main python code that reads the data and calls all necessary transformations, preparing predictions and saving it 
# Import packages 
import pandas as pd 
import numpy as np 
import logging

# Though in real, we would probably make a query from SQL database, here we are limited with csv file
file_path = 'data/garments_worker_productivity.csv'


def run_preprocessing(): 
    """Function that returns a client-ready dataset for the Power-BI dashboard"""
    pass 

if __name__ == '__main__': 
    """When the code is executed, the dataframe is preprocessed and saved to csv"""
    final_df = run_preprocessing()
    # final_df.to_csv('final_df.csv', index=False)
    logging.info('preprocessed data is saved to csv')

