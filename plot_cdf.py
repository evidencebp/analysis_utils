"""
CDF of CCP per language figure
"""

import pandas as pd
import plotly.graph_objs as go

def get_cdf(df : pd.DataFrame
            , column_name : str):
    return df[column_name].value_counts(normalize=True).sort_index().cumsum()


def weighted_cdf(df: pd.DataFrame
                 , column_name : str
                 , weight_column: str
                 , subsets=False
                 , prob_col: str = 'prob'):

    if subsets:
        g = df.groupby(column_name).agg({weight_column: 'sum'})
    else:
        g = df
    weight_sum = g[weight_column].sum()
    g[prob_col] = g[weight_column] / weight_sum
    cdf = g[prob_col].sort_index().cumsum()

    return cdf

# data, name, limit
def plot_cdf(df : pd.DataFrame
                , column_name : str
                , title : str
                , output_file : str = None
                , subsets =[]
                , weight_column=None
                , underscore_to_space=True
                , limit=None):

    prob_col = 'prob'
    data = []

    local = df.copy()
    if limit:
        local = local[local[column_name] <= limit]

    if weight_column:
        cdf = weighted_cdf(df=local
            , column_name=column_name
            , weight_column=weight_column
            , subsets = subsets
            , prob_col=prob_col)
    else:
        cdf = get_cdf(df=local
                        , column_name=column_name)

    cdf = pd.DataFrame(cdf)
    cdf = cdf.reset_index()
    cdf.columns = [column_name, 'cdf']

    if underscore_to_space:
        column_to_present = column_name.replace("_", " ")
        title_to_present = title.replace("_", " ")
    else:
        column_to_present = column_name
        title_to_present = title

    data.append(go.Scatter(
        x=cdf[column_name],
        y=cdf.cdf,
        mode='lines',
        name=column_to_present
    ))

    for i in subsets:
        if underscore_to_space:
            val_to_present = str(i['value']).replace("_", " ")
        else:
            val_to_present = str(i['value'])

        if weight_column:
            cdf = weighted_cdf(df=local[local[i['column']] == i['value']]
                               , column_name=column_name
                               , weight_column=weight_column
                               , subsets=subsets
                               , prob_col=prob_col)
        else:
            cdf = get_cdf(df=local[local[i['column']] == i['value']]
                          , column_name=column_name)


        cdf = pd.DataFrame(cdf)
        cdf = cdf.reset_index()
        cdf.columns = [column_name, 'cdf']

        data.append(go.Scatter(
            x=cdf[column_name],
            y=cdf.cdf,
            mode='lines',
            name=val_to_present
        ))

    layout = go.Layout(
        title=title_to_present,
        xaxis=dict(
            title=column_to_present,
            titlefont=dict(
                family='Courier New, monospace',
                size=24,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='CDF of ' + column_to_present,
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

    return fig


def plot_cdf_by_column(df : pd.DataFrame
                , column_name : str
                , title : str
                , output_file : str
                , subsets_column : str
                , weight_column=None
                , underscore_to_space=True
                , limit=None):
    subsets = []
    subset_values = df[subsets_column].unique()

    for i in subset_values:
        subsets.append({'column' :subsets_column
                           , 'value' : i})

    return plot_cdf(df=df
        , column_name=column_name
        , title=title
        , output_file=output_file
        , subsets=subsets
        , weight_column=weight_column
        , underscore_to_space=underscore_to_space
        , limit=limit)

