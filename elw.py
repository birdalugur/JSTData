#!/usr/bin/env python
# coding: utf-8

# ## Import Packages



from math import floor

import pandas as pd

from rpy2.robjects.packages import importr # Import R Library
from rpy2.robjects import FloatVector # Converting data to R format
from rpy2.robjects import r # Calling R functions

importr('LongMemoryTS')


# ## Reading Data


data = pd.read_csv('lndiff.csv')


data = data.set_index(['year','iso']).drop('USA',level=1)



def elw(data, delta=0.7,s2=False) -> dict:
    """
    Exact local Whittle estimator of the fractional difference parameter d
    for stationary and non-stationary long memory.
    """
    T = len(data)
    d = FloatVector(data)
    m = floor(1 + pow(T,delta))
    
    if s2==True:
        result = r['ELW2S'](d, m)
    else:
        result = r['ELW'](d, m)
    
    d_val = list(result.rx2('d'))[0]
    se_val = list(result.rx('s.e.')[0])[0]
    
    return {'d':d_val,'se':se_val}



elw_df = data.groupby(level='iso')['rgdpmad'].apply(elw)


elw2s_df = data.groupby(level='iso')['rgdpmad'].apply(elw,True)


elwdata= pd.concat([elw_df,elw2s_df],axis=1)


elwdata.columns = ['elw','elw2s']


elwdata.to_csv('elwdata.csv')

