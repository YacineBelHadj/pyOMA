
import numpy as np
from typing import Optional

from typing import Union ,Optional
from dataclasses import dataclass
from sklearn.metrics import r2_score, mean_absolute_percentage_error

@dataclass
class SG_Compensator():
    coef :Optional[list]= None
    
    def __post_init__(self):
        self.poly = np.polynomial.Polynomial(self.coef)
    
    def evaluate(self,temp:pd.Series, sg:pd.Series):
        sg_predicted = self.poly(temp)
        return r2_score(sg_predicted,sg), mean_absolute_percentage_error(sg_predicted,sg)
        
    def _check_coef(self):
        assert (self.poly is not None), "coef has to be either instantiated, or run fit_compensator"
        
    def fit_compensator(self,temp:pd.Series, sg:pd.Series,order:int):
        coef  = np.polyfit(temp,sg,order)[::-1]
        self.poly = np.polynomial.Polynomial(coef)
        return self.evaluate(temp,sg)
            
    def compensate(self,temp,sg):
        self._check_coef()
        return sg - self.poly(temp)
    
    def plot_prediction(self,temp:pd.Series,sg:pd.Series):
        sg_predicted=self.poly(temp)
        fig,ax=plt.subplots(ncols=2,figsize=(28,12))
        ax[0].scatter(temp,sg,color='steelblue',label='data')
        ax[0].scatter(temp,sg_predicted,color='red',label='model')
        ax[0].set_ylabel('Strain')
        ax[0].set_xlabel('Temperature °C')
        
        ax[1].hist((sg-sg.mean()),color='steelblue',label='data')
        ax[1].hist((sg_predicted-sg_predicted.mean()),color='red',label='compensated')
        ax[1].set_xlabel('Strain')

        plt.legend()
        return ax 