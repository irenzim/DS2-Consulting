# Libraries import 
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
import logging

class PredictProductivityModel:
    """
    Class that performs the prediction of productivity with XGBoost model.
    """
    def __init__(self, max_depth=None, n_estimators=100, learning_rate=0.1):
        self.model = XGBRegressor(max_depth=max_depth, n_estimators=n_estimators, learning_rate=learning_rate)
        self.lag_features = None
        logging.info("Initialized PredictProductivityModel with max_depth={}, n_estimators={}, learning_rate={}",
                     max_depth, n_estimators, learning_rate)
        self.data = None  # To store the original data with predictions

    def create_lag_features(self, data, features, lags):
        """
        Creates lag features for specific features in the time series data.
        
        Parameters:
        data (pd.DataFrame): The input time series data on productivity.
        features (list): The list of feature names to create lag features for.
        lags (int): The number of lag features to create.

        Returns:
        pd.DataFrame: DataFrame with lag features.
        """
        self.lag_features = lags
        df_lagged = data.copy()
        for feature in features:
            for lag in range(1, lags + 1):
                df_lagged[f'{feature}_lag_{lag}'] = data[feature].shift(lag)
        df_lagged.dropna(inplace=True)
        logging.info("Created lag features for features={} with lags={}", features, lags)

        return df_lagged

    def fit(self, data, features:list, lags:int, target:str, split_date:str, date_column:str):
        """
        Fits the XGBoost model on the time series data with lag features.
        
        Parameters:
        data (pd.DataFrame): The input time series data.
        features (list): The list of feature names to create lag features for.
        lags (int): The number of lag features to create.
        target (str): The name of the target column.
        split_date (str): The date to split the data into train and test sets.
        date_column (str): The name of the date column.
        """
        self.data = data.copy()  # Store the original data
        df_lagged = self.create_lag_features(data, features, lags)
        df_lagged = pd.get_dummies(df_lagged, drop_first=True)

        train = df_lagged[df_lagged[date_column] < split_date]
        test = df_lagged[df_lagged[date_column] >= split_date]

        # Handle categorical columns temporarily
        categorical_columns = data.select_dtypes(include=['object', 'category']).columns.tolist()
        columns_to_exclude = [target, date_column] + categorical_columns
        
        # Ensure columns_to_exclude contains only columns that exist in the DataFrame
        columns_to_exclude = [col for col in columns_to_exclude if col in df_lagged.columns]

        X_train = train.drop(columns=columns_to_exclude)
        X_test = test.drop(columns=columns_to_exclude)
        
        y_train = train[target]
        y_test = test[target]

        # Align the train and test set to ensure they have the same dummy variables
        X_train, X_test = X_train.align(X_test, join='outer', axis=1, fill_value=0)

        self.model.fit(X_train, y_train)
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        logging.info("Model trained with R^2 score on training data: {:.4f}".format(train_score))
        logging.info("Model trained with R^2 score on test data: {:.4f}".format(test_score))

        self.X_test = X_test
        self.y_test = y_test
        self.X_train = X_train
        self.test_index = test.index  # Store the indices of the test set

    def predict(self):
        """
        Makes predictions on the test data and assigns them to the original DataFrame.
        
        Returns:
        pd.DataFrame: Original DataFrame with added 'predicted' column.
        """
        if self.lag_features is None or self.X_test is None:
            logging.error("The model has not been fitted yet or test data is not available.")
            raise ValueError("The model has not been fitted yet or test data is not available.")
        
        predictions = self.model.predict(self.X_test)
        logging.info("Made predictions on the test data")

        # Assign predictions to the original data
        self.data['predicted'] = np.nan
        self.data.loc[self.test_index, 'predicted'] = predictions

        logging.info("Predictions assigned to the original data")
        
        return self.data

    def evaluate(self):
        pass

