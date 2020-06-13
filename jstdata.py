#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import plotly.graph_objects as go
import plotly.offline as offline
import os
from plotly.tools import make_subplots

if 'output' not in os.listdir():
    os.mkdir('output')

data = pd.read_excel('data/JSTdatasetR4.xlsx', sheet_name='Data')

all_countries = data['iso'].unique().tolist()

data = data.set_index(['year', 'iso'])

# ## Oran hesaplama

# (exports+imports)/gdp

data_ieg = (data['imports'] + data['exports']) / data['gdp']
data_ieg = data_ieg.swaplevel()

data_iex = (data['imports'] + data['exports']) * data['xrusd']
data_gx = data['gdp'] * data['xrusd']

data_gx = data_gx.swaplevel()
data_iex = data_iex.swaplevel()

total_iex = data_iex.groupby(level='year').sum()
total_gx = data_gx.groupby(level='year').sum()

rate = total_iex / total_gx
rate = rate.sort_index()


def fill_scatter(d):
    sclist = []
    for country in all_countries:
        _data = d[country].sort_index()
        sclist.append(go.Scatter(x=_data.index, y=_data.values, name=country))
    return sclist


def get_layout(title, yaxis):
    _layout = {
        'title': title,
        'xaxis_title': 'Year',
        'yaxis_title': yaxis
    }
    return _layout


# Figures


fig_ieg = go.Figure(layout=get_layout('(imports+exports)/gdp', 'rate'))
fig_ieg.add_traces(fill_scatter(data_ieg))

fig_rate = go.Figure(layout=get_layout('rate of iex/gx', 'rate'))
fig_rate.add_trace(go.Scatter(x=rate.index, y=rate.values))

offline.plot(fig_ieg, filename='output/ieg.html')

offline.plot(fig_rate, filename='output/rate.html')
