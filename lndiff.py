import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.offline as offline

data = pd.read_excel('data/JSTdatasetR4.xlsx', sheet_name='Data').set_index(['year', 'iso'])
all_countries = data.index.get_level_values('iso').unique().to_list()


def calculateLn(variable: str, country: str) -> pd.Series:
    """
    ln(rgdpmad)x - ln(rgdpmad)usa
    """

    ln_base = np.log(data.xs(country, level='iso')[variable])
    res = data.groupby(level='iso', group_keys=False).apply(lambda x: np.log(x[variable]) - ln_base)
    return res


def plot_ln(fig_data,xlabel,ylabel):
    ln_fig = go.Figure(layout={'xaxis_title':xlabel,'yaxis_title':ylabel})
    trace_list = []
    fig_data.groupby(level='iso')\
        .apply(lambda x: trace_list.append(go.Scatter(x=x.index.get_level_values('year'),y=x.values,name=x.index[0][1])))
    ln_fig.add_traces(trace_list)
    offline.plot(ln_fig,filename='lndiff.html')


lndiff = calculateLn(variable='rgdpmad',country='USA')
plot_ln(lndiff, 'year', 'lndiff')