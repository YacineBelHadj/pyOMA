import numpy as np 

def modes_condition(mpe_list:dict,config:list):
    """utils func :: used to select the modes that respect certain config"""
    track_list=[]
    if mpe_list is None: return np.nan
    for i in mpe_list:
        if (i['size']>config['min_size'] and \
            i['frequency']>config['lfb'] and i['frequency']<config['ufb'] and\
            i['damping']>config['ldb'] and i['damping']<config['udb']):                                                                                                                       
                                                                                                                                   
            track_list.append(i)                                                                 
    #check if the list is empty                                    
    if len(track_list) != 0 : return track_list
    else: return np.nan