from .utils import modes_condition
import pandas as pd
import numpy as np
class Tracker: 
    """this class allows for tracking modes present in a dataFrame, you first have to set the mode config. Like this :
    mode_config_dict={'mode 1':{'f_ref':3.9,'lfb':3.8,'ufb':4,'min_size':20,'ldb':0.025,'udb':2.49},
                  'mode 2':{'f_ref':4.4,'lfb':4.3,'ufb':4.5,'min_size':10,'ldb':0.019,'udb':6.33},
                  'mode 3':{'f_ref':4.9,'lfb':4.7,'ufb':5.1,'min_size':10,'ldb':0.026,'udb':3.015},
                  'mode 4': {'f_ref':28,'lfb':27.2,'ufb':28.5,'min_size':10,'ldb':0.026,'udb':3.015},
                  'mode 5' : {'f_ref':33.6,'lfb':33,'ufb':34,'min_size':10,'ldb':0.026,'udb':3.015}}
    then we have different strategy to track (since sometimes there is mutliple modes in frequency range at one timestamp)

    different type of tracking are defined are implimented
                  """
    mode_config_dict: dict
        
    def frequency_tracker_max(self,mpe_list,config):
        track_list = modes_condition(mpe_list,config)
        if not isinstance(track_list,list): return np.nan
        return max(track_list,key= lambda mode:mode['frequency'])['frequency']
                                        
    
    def frequency_tracker_ref(self,mpe_list,config):
        if 'ref_freq'not in config.keys():
            raise ValueError('ref_freq is missing in the config dictionnary')

        track_list = modes_condition(mpe_list,config) 
        if not isinstance(track_list,list): return np.nan
        return min(track_list, key= lambda x:np.abs(x['frequency']-config['ref_freq']))['frequency']
                                        
    def frequency_tracker_single(self,mpe_list,config):
        track_list = modes_condition(mpe_list,config)
        if not isinstance(track_list,list): return np.nan
        if len(track_list) !=1  : return np.nan
        return track_list[0]['frequency']
                                        

    def frequency_tracker_all(self,mpe_list, config):
        track_list = modes_condition(mpe_list,config)
        if not isinstance(track_list,list): return np.nan
        return [i['frequency'] for i in track_list]
    
    def track(self,df,columns,strategy='frequency_ref'):
        TRACKERS= {'frequency_ref':self.frequency_tracker_ref,
                     'frequency_max':self.frequency_tracker_max,
                     'frequency_single':self.frequency_tracker_single,
                     'frequency_all':self.frequency_tracker_all}
                     
        if strategy not in TRACKERS.keys():
            print(f'strategy not available, please choose from the following {TRACKERS.keys()}')
        
        tracker_func = TRACKERS[strategy]        
        all_tracked_mode={}
        
        if isinstance(columns,str): columns=[columns] 
        for col in columns:
            tracked_mode={}
            for mode_name,mode_config in self.mode_config_dict.items():
                mode=df[col].apply(tracker_func,args=(mode_config,))
                tracked_mode[mode_name]=mode
        
            all_tracked_mode[col]=pd.DataFrame(tracked_mode)

        return all_tracked_mode