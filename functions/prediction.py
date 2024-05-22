class ProductivityPredictModel: 
    """
    Class that performs the prediction of productivity with XgBoost model.  
    """
    def __init__(self, df, dep_var): 
        self.df = df 
        self.dep_var = dep_var

    