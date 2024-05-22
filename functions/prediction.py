import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
import logging

class ProductivityPredictModel: 
    """
    Class that performs the prediction of productivity with XgBoost model.  
    """
    def __init__(self, max_depth=None, n_estimators=100, learning_rate=0.1):
        self.model = XGBRegressor(max_depth=max_depth, n_estimators=n_estimators, learning_rate=learning_rate)
        self.lag_features = None
        logging.info("Initialized TimeSeriesRegressionTree with max_depth={}, n_estimators={}, learning_rate={}",
                    max_depth, n_estimators, learning_rate)

    def create_lag_features(self, data, features, lags):
        """
        Creates lag features for specific features in the time series data.
        
        Parameters:
        data (pd.DataFrame): The input time series data.
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

    
    def fit(self, data, features, lags, target, split_date, date_column):
        """
        Fits the regression tree model on the time series data with lag features.
        
        Parameters:
        data (pd.DataFrame): The input time series data.
        features (list): The list of feature names to create lag features for.
        lags (int): The number of lag features to create.
        target (str): The name of the target column.
        split_date (str): The date to split the data into train and test sets.
        """
        df_lagged = self.create_lag_features(data, features, lags)
        train = df_lagged[df_lagged[date_column] < split_date]
        test = df_lagged[df_lagged[date_column] >= split_date]

        X_train = train.drop(columns=[target, date_column])
        y_train = train[target]
        X_test = test.drop(columns=[target, date_column])
        y_test = test[target]

        self.model.fit(X_train, y_train)
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        logging.info("Model trained with R^2 score on training data: {:.4f}", train_score)
        logging.info("Model trained with R^2 score on test data: {:.4f}", test_score)

        self.X_test = X_test
        self.y_test = y_test


    def predict(self):
        """
        Makes predictions on the test data.
        
        Returns:
        np.ndarray: Array of predictions.
        """
        if self.lag_features is None or self.X_test is None:
            logging.error("The model has not been fitted yet or test data is not available.")
            raise ValueError("The model has not been fitted yet or test data is not available.")
        
        predictions = self.model.predict(self.X_test)
        logging.info("Made predictions on the test data")

        df_predictions = self.X_test.copy()
        df_predictions['actual'] = self.y_test
        df_predictions['predicted'] = predictions

        logging.info("Made predictions on the test data")
        return df_predictions

    def evaluate(self): 
        pass

    