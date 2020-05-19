"""
CDF of CCP per language figure
"""

import pandas as pd
import plotly.graph_objs as go

# data, name, limit
def plot_cdf(df : pd.DataFrame
                , column_name : str
                , title : str
                , output_file : str = None
                , subsets =[]):

    data = []

    cdf = df[column_name].value_counts(normalize=True).sort_index().cumsum()
    cdf = pd.DataFrame(cdf)
    cdf = cdf.reset_index()
    cdf.columns = [column_name, 'cdf']

    data.append(go.Scatter(
        x=cdf[column_name],
        y=cdf.cdf,
        mode='lines',
        name=column_name
    ))

    for i in subsets:
        cdf = df[df[i['column']] == i['value']][column_name].value_counts(normalize=True).sort_index().cumsum()
        cdf = pd.DataFrame(cdf)
        cdf = cdf.reset_index()
        cdf.columns = [column_name, 'cdf']

        data.append(go.Scatter(
            x=cdf[column_name],
            y=cdf.cdf,
            mode='lines',
            name=str(i['value'])
        ))

    layout = go.Layout(
        title=title,
        xaxis=dict(
            title='CCP',
            titlefont=dict(
                family='Courier New, monospace',
                size=24,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='CDF of ' + column_name,
            titlefont=dict(
                family='Courier New, monospace',
                size=24,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=data
                    , layout=layout)

    fig.show()
    if output_file:
        fig.write_image(output_file)


def plot_cdf_by_column(df : pd.DataFrame
                , column_name : str
                , title : str
                , output_file : str
                , subsets_column : str):
    subsets = []
    subset_values = df[subsets_column].unique()

    for i in subset_values:
        subsets.append({'column' :subsets_column
                           , 'value' : i})

    plot_cdf(df
        , column_name
        , title
        , output_file
        , subsets)

