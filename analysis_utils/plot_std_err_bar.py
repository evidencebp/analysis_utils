from math import sqrt
import pandas as pd
import plotly.graph_objects as go

def plot_std_err_bar(df : pd.DataFrame
                     , x_column: str
                     , y_avg: str
                     , y_std: str
                     , y_count: str
                     , title: str
                     , x_title: str
                     , y_title: str
                     , grouping_column: str = None
                     , text_digits: int = None):
    if grouping_column:
        grouping_values = df[grouping_column].unique()
        data = []
        for i in grouping_values:
            x = df[df[grouping_column] == i][x_column]
            y = df[df[grouping_column] == i][y_avg]
            error = df.apply(lambda x: x[y_std] / sqrt(x[y_count])
                             , axis=1)
            if text_digits:
                data.append(go.Bar(
                    x=x,
                    y=y,
                    name=i,
                    text=round(y, text_digits),
                    error_y=dict(
                        type='data',
                        array=error,
                        visible=True
                    )))
            else:
                data.append(go.Bar(
                    x=x,
                    y=y,
                    name=i,
                    error_y=dict(
                        type='data',
                        array=error,
                        visible=True
                    )))

    else:
        x = df[x_column]
        y = df[y_avg]
        error = df.apply(lambda x: x[y_std] / sqrt(x[y_count])
                         , axis=1)

        if text_digits:
            data = [go.Bar(
                x=x,
                y=y,
                text=round(y, text_digits),
                name=title,
                error_y=dict(
                    type='data',
                    array=error,
                    visible=True
                )
            )]
        else:
            data = [go.Bar(
                x=x,
                y=y,
                name=title,
                error_y=dict(
                    type='data',
                    array=error,
                    visible=True
                )
            )]


    layout = go.Layout(
        barmode='group',
        title=title,
        xaxis=dict(
            title=x_title,
            type='category',
            titlefont=dict(
                family='Courier New, monospace',
                size=32,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title=y_title,
            titlefont=dict(
                family='Courier New, monospace',
                size=32,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=data
                    , layout=layout)

    return fig