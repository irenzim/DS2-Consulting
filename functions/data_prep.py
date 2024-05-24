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

        if not missing_cols.empty: 
            return missing_cols
        else: 
            return None

    def impute_missing_data(self, missing_cols, impute_option: str): 
        """Complementary function - takes column name from the previous function and imputes."""
        if missing_cols is not None: 
            for col in missing_cols:
                if impute_option == 'median': 
                    self.df[col] = self.df[col].fillna(self.df[col].median())
                elif impute_option == 'zero': 
                    self.df[col] = self.df[col].fillna(0)

        return self.df

    def transform_data(self): 
        """Any other corrections on data."""
        self.df['department'] = self.df['department'].str.strip()
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df['day'] = self.df['date'].dt.day
        self.df['month'] = self.df['date'].dt.month
        self.df['num_week'] = self.df['date'].dt.isocalendar().week.astype(int)

        return self.df










