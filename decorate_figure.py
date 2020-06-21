import plotly.graph_objects as go

def decorate_figure(fig: go.Figure
                    , title: str = None
                    , xaxis_title: str = None
                    , yaxis_title: str = None
                    , font_dict: dict = None
                    , showlegend=True) -> go.Figure:

    if title:
        fig.update_layout(title=title)

    if title:
        fig.update_layout(title=title)

    if xaxis_title:
        fig.update_layout(xaxis_title=xaxis_title)

    if yaxis_title:
        fig.update_layout(yaxis_title=title)

    if font_dict:
        fig.update_layout(font=font_dict)

    if showlegend:
        fig.update_layout(showlegend=showlegend)


    return fig