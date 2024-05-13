from numpy import inf
import pandas as pd
import plotly.graph_objs as go

from analysis_utils.feature_pair_analysis import bin_metric_by_quantiles


def plot_deciles(df
                 , grouping_column
                 , metric_column
                 , title
                 , xaxis_title
                 , output_file=None
                 , top_val=inf):
    deciles_column = grouping_column + '_deciles'
    deciles_df = generate_deciles(df=df
                                  , grouping_column=grouping_column
                                  , deciles_column=deciles_column
                                  , top_val=top_val)
    deciles_df = deciles_df.sort_values(deciles_column)

    return plot_groups(deciles_df
                 , grouping_column=deciles_column
                 , metric_column=metric_column
                 , title=title
                 , xaxis_title=xaxis_title
                 , output_file=output_file)

def generate_deciles(df : pd.DataFrame
                     , grouping_column : str
                     , deciles_column: str
                     , top_val=inf):

    return bin_metric_by_quantiles(df
                                   , grouping_column
                                   , deciles_column
                                   , bins=10
                                   , top_val=top_val
                                   )


def plot_groups(df
                 , grouping_column
                 , metric_column
                 , title
                 , xaxis_title
                 , output_file=None):

    fig = go.Figure()
    item = 0
    for cur_group in df[grouping_column].unique():
        color = 'blue' # 'rgb(' +str(20*item +1) + ',' + str(100 + 10*item) +',' + str(254 - 15*item) + ')'
        if str(cur_group).find(',') > 0:
            name = '<=' + str(cur_group)[str(cur_group).find(',')+1:-1]
        else:
            name = str(cur_group)
        trace = go.Box(
            y=df[df[grouping_column] == cur_group][metric_column].tolist(),
            name=name,
            marker=dict(
                color=color,
            ),
            boxpoints=False,
            boxmean=True
        )
        fig.add_trace(trace)

        item += 1

    fig.update_layout(
        title=title.replace("_", " "),
        xaxis_title=xaxis_title.replace("_", " "),
        yaxis_title=metric_column.replace("_", " "),
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="black"
        )
    )
    fig.update_layout(showlegend=False)

    if output_file:
        fig.write_image(output_file)

    return fig

def get_cdf_quantile_value(cdf
                           , quantile
                           , value_column
                           , cdf_column='cdf'):
    return cdf[cdf[cdf_column] > quantile][value_column].min()