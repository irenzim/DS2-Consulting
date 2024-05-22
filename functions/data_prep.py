# Defining a separate class for data preprocessing. 
import pandas as pd
class DataPreparation: 
    """
    Class that allows to verify missing data and impute NAs, based on the selected option. 
    """
    def __init__(self, df): 
        self.df = df 

    def check_missing_data(self): 
        """Verify if missing data is persistent - if yes, returns column name."""
        missing_cols = self.df.columns[self.df.isnull().any()]

        if missing_cols.empty: 
            return None
        else: 
            return missing_cols

    def impute_missing_data(self, missing_cols, impute_option:str): 
        """Complementary function - takes column name from the previous function and imputes."""

        if missing_cols is not None: 

            if impute_option == 'median': 
                self.df[missing_cols] = self.df[missing_cols].fillna(self.df[missing_cols].median())

            elif impute_option == 'zero': 
                self.df[missing_cols] = self.df[missing_cols].fillna(0)

        return self.df

    def correct_column_value(self): 
        """Any other corrections on data."""
        self.df['department'] = self.df['department'].str.strip()
        self.df = pd.get_dummies(self.df, columns=['department'], drop_first=True)
        # self.df = pd.get_dummies(self.df, columns=['department'])
        self.df['day'] = pd.to_datetime(self.df['date']).apply(lambda x: x.day)
        self.df['month'] = pd.to_datetime(self.df['date']).apply(lambda x: x.month)
        self.df['num_week'] = pd.to_datetime(self.df['date']).apply(lambda x: x.weekofyear)
        self.df.drop(['quarter'], axis=1, inplace=True)

        return self.df









