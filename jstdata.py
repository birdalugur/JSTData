#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import plotly.graph_objects as go
import plotly.offline as offline

data = pd.read_excel('data/JSTdatasetR4.xlsx', sheet_name='Data')

all_countries = data['iso'].unique().tolist()

data = data.set_index(['year', 'iso'])

# ## Oran hesaplama


# imports/gdp
data_ig = data.groupby(level=1).apply(lambda x: x['imports'] / x['gdp']).droplevel(2)

# exports/gdp
data_eg = data.groupby(level=1).apply(lambda x: x['exports'] / x['gdp']).droplevel(2)

# ## Dünya ortalaması


mean_ig = data_ig.groupby(level=1).mean()
mean_eg = data_eg.groupby(level=1).mean()

mean_ig.name = 'mean_ig'
mean_eg.name = 'mean_eg'

mean_series = pd.concat([mean_ig, mean_eg], axis=1)


def fill_scatter(d):
    sclist = []
    for country in all_countries:
        _data = d[country].sort_index()
        sclist.append(go.Scatter(x=_data.index, y=_data.values, name=country))
    return sclist


ig_layout = {
    'title': 'imports/gdp',
    'xaxis_title': 'Year',
    'yaxis_title': 'Rate'
}

eg_layout = {
    'title': 'exports/gdp',
    'xaxis_title': 'Year',
    'yaxis_title': 'Rate'
}
mean_layout = {
    'title': 'mean',
    'xaxis_title': 'Year',
    'yaxis_title': 'mean'
}

fig_ig = go.Figure(layout=ig_layout)
fig_eg = go.Figure(layout=eg_layout)
fig_mean = go.Figure(layout=mean_layout)

s_1 = go.Scatter(x=mean_series.index, y=mean_series['mean_eg'].values, name='mean_eg')
s_2 = go.Scatter(x=mean_series.index, y=mean_series['mean_ig'].values, name='mean_ig')

fig_ig.add_traces(fill_scatter(data_ig))
fig_eg.add_traces(fill_scatter(data_eg))

fig_mean.add_traces([s_1, s_2])

offline.plot(fig_ig, filename='output/ig.html')

offline.plot(fig_eg, filename='output/eg.html')

offline.plot(fig_mean, filename='output/mean.html')
