from sklearn.base import BaseEstimator, transformermixin
from copy import deepcopy
import pandas as pd
class Compensator(BaseEstimator,transformermixin):
    """Used for mode compensation can handle multiple modes and multiple predictor
    """
    def __init__(self,model=None,models_dict=None):
        self.model= model
        self.models_dict=models_dict
        
    def fit(self,features:pd.DataFrame,mode:pd.DataFrame):
        assert self.model is not None, ' To fit a type of model should be chosen during instanciation'

        self.models_dict={}
        for col in mode.columns:
            model_ =deepcopy(self.model)
            self.models_dict[col]=model_.fit(features,mode[col])
    
    def transform(self,features,mode):
        test_data=pd.merge(features,mode, how='inner', left_index=True, right_index=True).dropna()
        for col in mode.columns:
            test_data[col+' pred']=self.models_dict[col].predict(test_data[features.columns].values)
            test_data[col+' compensated'] =test_data[col] - test_data[col+' pred']
        return test_data[mode.columns+' compensated'] ,  test_data[mode.columns+' pred']