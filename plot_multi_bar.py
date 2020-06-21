import pandas as pd
import plotly.graph_objects as go

def plot_multi_bar(df : pd.DataFrame
                   , grouping_column : str
                   , metrics: list):
    """
    Plots a bar per metric
    :param df:
    :param grouping_column:
    :param metrics:
    :return:
    """

    data = []
    for i in metrics:
        data.append(go.Bar(name=i['name']
                           , x=df[grouping_column]
                           , y=df[i['content']]
                           , textposition='outside'
                           ))

    fig = go.Figure(data=data)
    # Change the bar mode
    fig.update_layout(barmode='group')
    fig.update_traces(textposition='auto')

    return fig
