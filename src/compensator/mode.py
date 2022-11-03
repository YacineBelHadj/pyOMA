from dataclasses import dataclass
from sklearn.base import BaseEstimator


@dataclass
class Compensator(BaseEstimator,):
    model = None
    model_dict = None

    def fit(self,X:): -> None

    def predict(self):
    
    def score(self):