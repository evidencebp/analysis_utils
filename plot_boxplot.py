import os
import plotly.graph_objs as go




def plot_all_metrics(df
                 , grouping_column
                 , metrics
                 , figure_path):

    df = df.sort_values(grouping_column)

    for metric_column in metrics:
        plot_boxplot(df
                     , grouping_column=grouping_column
                     , metric_column=metric_column
                     , output_file=os.path.join(figure_path, metric_column + '.png'))


def plot_boxplot(df
                 , grouping_column
                 , metric_column
                 , output_file=None):

    fig = go.Figure()
    item = 0;
    for cur_group in sorted(df[grouping_column].unique()):
        color = 'rgb(' +str(20*item +1) + ',' + str(100 + 10*item) +',' + str(254 - 15*item) + ')'
        trace = go.Box(
            y=df[df[grouping_column] == cur_group][metric_column].tolist(),
            name=str(cur_group),
            marker=dict(
                color=color,
            ),
            boxpoints=False,
            boxmean=True
        )
        fig.add_trace(trace)
        item += 1

    fig.update_layout(
        title= grouping_column + " vs. " + metric_column,
        xaxis_title=grouping_column,
        yaxis_title=metric_column,
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        )
    )
    fig.show()
    if output_file:
        fig.write_image(output_file)

    return fig

