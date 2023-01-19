'''
    Plots - Module to generate plotly plots for dashboard
    Sandeep Venkataram
    Jan 2023
'''

import plotly.express as px
import plotly.graph_objects as go
import Data
import math
import numpy as np

def generate_scatter_chart(
        selected_bcs: list,
        selected_genes: list,
        R: bool,
        xy: bool,
        xcol: str,
        ycol: str,
        scalex: str,
        scaley: str,
        err: bool,
        ):
    """ Generate scatter plot used in Dash dashboard"""

    my_data = Data.master_df.loc[:,[xcol,ycol]]
    my_data = Data.master_df[my_data.notnull().all(axis=1)]
    bcs_to_highlight = Data.get_barcodes_to_highlight(selected_bcs, selected_genes)
    bcs_to_highlight = list(set(bcs_to_highlight).intersection(set(list(my_data.index))))

    error_x = [0] * len(my_data)
    error_y = [0] * len(my_data)
    if err:
        error_x = my_data.loc[:,Data.master_err_map[xcol]]
        error_y = my_data.loc[:,Data.master_err_map[ycol]]


    all_x_data = my_data.loc[:,xcol]
    all_y_data = my_data.loc[:,ycol]

    xname_prefix = ""
    yname_prefix = ""
    if scalex == "log":
        all_x_data = np.log2(all_x_data)
        xname_prefix = "Log2 "
    if scaley == "log":
        all_y_data = np.log2(all_y_data)
        yname_prefix = "Log2 "

    fig_all = None

    initial_opacity = 0.5
    if len(bcs_to_highlight)>0:
        initial_opacity = 0.3

    if R:
        trend_type = "trace"
        if len(all_x_data)- all_x_data.isna().sum() < 100:
            trend_type = "overall"
        fig_all = px.scatter(
            x=all_x_data,
            y=all_y_data,
            color=my_data.loc[:, "populationType"],
            hover_name = my_data.index,
            labels = {
                "populationType" : "",
            },
            error_x = error_x,
            error_y = error_y,
            trendline="ols",
            trendline_scope = trend_type,
        )
    else:
        fig_all = px.scatter(
            x=all_x_data,
            y=all_y_data,
            color=my_data.loc[:, "populationType"],
            hover_name = my_data.index,
            labels = {
                "populationType" : "",
            },
            error_x = error_x,
            error_y = error_y,
        )

    fig_all.update_traces(marker=dict(opacity = initial_opacity, size = 10))
    fig_all.update_traces(error_x=dict(color = "rgba(255,255,255,0.1)", width=0))
    fig_all.update_traces(error_y=dict(color = "rgba(255,255,255,0.1)", width=0))


    fig = go.Figure()

    if xy:
        my_dat1 = filter(lambda x: not math.isnan(x), list(map(abs,all_x_data.values.tolist())))
        my_dat2 = filter(lambda x: not math.isnan(x), list(map(abs,all_y_data.values.tolist())))
        my_val = min(max(my_dat1), max(my_dat2))
        xy_line = px.line(
            x=[-my_val,my_val],
            y=[-my_val,my_val]
        )
        xy_line.update_traces(line_color="#FFFFFF")
        xy_line.update_layout(showlegend=False)
        fig.add_trace(xy_line.data[0])
    for trace in fig_all.data:
        fig.add_trace(trace)

    if len(bcs_to_highlight)>0:
        highlight_x_data = my_data.loc[bcs_to_highlight,xcol]
        highlight_y_data = my_data.loc[bcs_to_highlight,ycol]
        fig_highlight = px.scatter(
            x=highlight_x_data,
            y=highlight_y_data,
            color=my_data.loc[bcs_to_highlight, "populationType"],
            hover_name = highlight_x_data.index,
            labels = {
                "populationType" : "",
            }
        )
        fig_highlight.update_traces(showlegend=False)
        fig_highlight.update_traces(marker=dict(opacity = 1, size = 14))
        for trace in fig_highlight.data:
            fig.add_trace(trace)

    fig.update_xaxes(
        range = [min(all_x_data) * 0.5, max(all_x_data) * 1.1],
        title = {"text" : xname_prefix + Data.master_name_map[xcol]},
    )
    fig.update_yaxes(
        range = [min(all_y_data) * 0.5, max(all_y_data) * 1.1],
        title = {"text" : yname_prefix + Data.master_name_map[ycol]},
    )
    fig.update_layout(template="plotly_dark")



    return fig
