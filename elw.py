#!/usr/bin/env python
# coding: utf-8

# ## Import Packages



from math import floor

import pandas as pd
import numpy as np

import plotly.graph_objects as go
import plotly.offline as offline

from rpy2.robjects.packages import importr # Import R Library
from rpy2.robjects import FloatVector # Converting data to R format
from rpy2.robjects import r # Calling R functions

importr('LongMemoryTS')


# ## Reading Data



data = pd.read_excel('data/JSTdatasetR4.xlsx', sheet_name='Data').set_index(['year', 'iso'])
all_countries = data.index.get_level_values('iso').unique().to_list()


# ## Functions to calculate and plot ln differences.


def calculateLn(variable: str, country: str) -> pd.Series:
    """
    ln(rgdpmad)x - ln(rgdpmad)usa
    """

    ln_base = np.log(data.xs(country, level='iso')[variable])
    res = data.groupby(level='iso', group_keys=False).apply(lambda x: np.log(x[variable]) - ln_base)
    return res.drop(countryntry,level='iso')


def plot_ln(fig_data,xlabel,ylabel):
    ln_fig = go.Figure(layout={'xaxis_title':xlabel,'yaxis_title':ylabel})
    trace_list = []
    fig_data.groupby(level='iso')        .apply(lambda x: trace_list.append(go.Scatter(x=x.index.get_level_values('year'),y=x.values,name=x.index[0][1])))
    ln_fig.add_traces(trace_list)
    offline.plot(ln_fig,filename='lndiff.html')



lndiff = calculateLn(variable='rgdpmad',country='USA')
plot_ln(lndiff, 'year', 'lndiff')



# ## Reading Data


data = pd.read_csv('lndiff.csv')


data = data.set_index(['year','iso']).drop('USA',level=1)


def elw(data,start_year:int, delta:float=0.7,s2=False) -> dict:
    """
    Exact local Whittle estimator of the fractional difference parameter d
    for stationary and non-stationary long memory.
    """
    
    data = data[data.index.get_level_values('year')>=2000]
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



elw_df = lndiff.groupby(level='iso').apply(elw, start_year=2005)


elw2s_df = lndiff.groupby(level='iso').apply(elw,start_year=2005, delta=0.4, s2=True)


elwdata= pd.merge(elw_df,elw2s_df,how='outer',left_index=True,right_index=True,suffixes=('_ELW','_ELW2S'))


elwdata.to_csv('elwdata.csv')

