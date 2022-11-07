import pandas as pd
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt 

def filter_bulk(mode:pd.Series,freq:str='10T',smoothing_duration:str='2D',stds:float=1.5,lag:int=288):

    """Post filter after tracking 
    """
    mode_res = deepcopy(mode)
    m=mode.rolling(smoothing_duration).median().resample(freq).mean()[mode.index]
    s=mode.rolling(smoothing_duration).std().resample(freq).mean()[mode.index]

    mask = np.abs(mode-m) >stds*s  
 #   mask = (np.abs(mode-m.shift(lag)) >stds*s.shift(lag)) & mask
    mask = (np.abs(mode-m.shift(-lag)) >stds*s.shift(-lag))  & mask

    mode_res[mask]=np.nan
    return mode_res
    
def plot_bulk(mode:pd.Series,freq:str='10T',smoothing_duration:str='2D',stds:float=1.5,lag:int=288):
    mode_res = deepcopy(mode)
    m=mode.rolling(smoothing_duration).median().resample(freq).mean()[mode.index]
    s=mode.rolling(smoothing_duration).std().resample(freq).mean()[mode.index]

    mask = np.abs(mode-m) >stds*s  
 #   mask = (np.abs(mode-m.shift(lag)) >stds*s.shift(lag)) & mask
    mask = (np.abs(mode-m.shift(-lag)) >stds*s.shift(-lag))  & mask

    mode_res[mask]=np.nan

    fig,ax=plt.subplots(ncols=2,figsize=(28,8))
    print(mask.sum())
    ax[0].plot(m)
    ax[0].fill_between(mode.index, m+s, m-s,alpha=0.5)
    ax[0].fill_between(mode.index,m.shift(lag)+s.shift(lag),(m.shift(lag))-s.shift(lag),alpha=0.5)
    ax[0].set_title('past')
    ax[1].plot(m)
    ax[1].fill_between(mode.index, m+s, m-s,alpha=0.5)
    ax[1].fill_between(mode.index,m.shift(-lag)+s.shift(lag),(m.shift(-lag))-s.shift(lag),alpha=0.5)
    ax[1].set_title('future')
    fig.show()
