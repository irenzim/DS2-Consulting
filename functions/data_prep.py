# Defining a separate class for data preprocessing. 

class DataPreparation: 
    """
    Class that allows to verify missing data and impute NAs, based on the selected option. 
    """
    def __init__(self, df): 
        self.df = df 

    def check_missing_data(self): 
        """Verify if missing data is persistent - if yes, returns column name."""
        pass 

    def impute_missing_data(self, impute_option:str): 
        """Complementary function - takes column name from the previous function and imputes."""

        if impute_option == 'median': 
            pass 

        elif impute_option == 'zero': 
            pass 

    def correct_column_value(self, column_name:str): 
        """Any other corrections on data."""
        pass







