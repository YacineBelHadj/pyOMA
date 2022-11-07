from typing import Optional
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score, mean_absolute_percentage_error


class TS_Compensator():
    """Performs Time series compensation using a single predictor and using a polynomial models
    """
    def __init__(self,coef=None):
        """_summary_

        Args:
            coef (List or None): give the list of the polynomial coefficient from the datasheet 
            if None, the polynomial has to be fit in a first place 
        """
        self.coef :Optional[list]= coef

    def __post_init__(self):
        if self.coef is not None:
            self.poly = np.polynomial.Polynomial(self.coef)
        else:
            self.poly = None 
    
    def _check_coef(self):
        """A function used to check the attribute of the compensator
        """
        assert (self.poly is not None), "coef has to be either instantiated, or run fit_compensator"
    
    def evaluate(self, input:pd.Series, ts:pd.Series):
        """This function evalute the performance of the compensator 

        Args:
            temp (pd.Series): The variable we are trying to remove it's
            effect on the time series
            ts (pd.Series): The variable we are trying to normalize

        Returns:
            (r2,MAPE, std_ratio): returns three commons metrics used to monitor 
            the performance of the normalizing model
        """
        self._check_coef()

        ts_predicted = self.poly(input)
        std_before_compenstation = ts.std()
        std_after_compenstation = ts_predicted.std()
        std_ratio = std_before_compenstation/std_after_compenstation

        return r2_score(ts_predicted,ts), mean_absolute_percentage_error(ts_predicted,ts) , std_ratio
        
    def fit_compensator(self, input:pd.Series, ts:pd.Series, order:int):
        """ Fit a polynomal on the data 

        Args:
            input (pd.Series): X 
            ts (pd.Series): Y
            order (int): order of the polynome 

        Returns:
            _type_: _description_
        """
        coef  = np.polyfit(input, ts, order)[::-1]
        self.poly = np.polynomial.Polynomial(coef)
        return self.evaluate(input, ts)
            
    def compensate(self,input:pd.Series, ts:pd.Series):
        """Perform the compensation of the ts variable regarding the input, you first have to fit the polynomial on healthy data

        Args:
            input (pd.Series): variable regarding which we perform the normalization
            ts (pd.Series): _description_

        Returns:
            _type_: _description_
        """
        self._check_coef()
        return ts - self.poly(input)
    def predict(self, input:pd.Series):
        """Gives the expected variation of the targeted variable based on the predictor 

        Args:
            input (pd.Series): predictor (temperature) variable
        """

        return self.poly(input)
