'''
    Callbacks - Callback functions for Dash app
    Sandeep Venkataram
    Jan 2023
'''

from dash import Input, Output, State, callback, MATCH
from dash.exceptions import PreventUpdate


import Plots
import Table


@callback(
    Output('primary', 'figure'),
    Input("selected-mut-table","selected_rows"),
    Input({'type': 'figure-checkboxes', 'index': 'primary'}, 'value'),
    Input({'type': 'axis-dropdown-X', 'index': 'primary'}, 'value'),
    Input({'type': 'axis-scale-radio-X', 'index': 'primary'}, 'value'),
    Input({'type': 'axis-dropdown-Y', 'index': 'primary'}, 'value'),
    Input({'type': 'axis-scale-radio-Y', 'index': 'primary'}, 'value'),
    State("selected-mut-table","data"),
)
def update_primary(selected_rows, checkboxes, xcol, xscale, ycol, yscale, data,):
    ''' Callback to update primary scatterplot '''
    R = "R" in checkboxes
    YX = "YX" in checkboxes
    Errorbars = "Errorbars" in checkboxes

    selected_genes = []
    if len(selected_rows)>0:
        selected_genes = [data[i]["Gene"] for i in selected_rows]

    selected_barcodes = []

    return Plots.generate_scatter_chart(
        selected_barcodes,
        selected_genes,
        R,
        YX,
        xcol,
        ycol,
        xscale,
        yscale,
        Errorbars,
    )


@callback(
    Output({'type': 'figure', 'index': MATCH}, 'figure'),
    Input('primary', 'selectedData'),
    Input('selected-mut-table',"data"),
    Input('selected-mut-table',"selected_rows"),
    Input({'type': 'figure-checkboxes', 'index': MATCH}, 'value'),
    Input({'type': 'axis-dropdown-X', 'index': MATCH}, 'value'),
    Input({'type': 'axis-scale-radio-X', 'index': MATCH}, 'value'),
    Input({'type': 'axis-dropdown-Y', 'index': MATCH}, 'value'),
    Input({'type': 'axis-scale-radio-Y', 'index': MATCH}, 'value'),
)
def update_scatter(selectedData, data, selected_rows, checkboxes, xcol, xscale, ycol, yscale,):
    ''' Flexible callback to update secondary scatterplots '''
    R = "R" in checkboxes
    YX = "YX" in checkboxes
    Errorbars = "Errorbars" in checkboxes

    selected_genes = []
    if len(selected_rows)>0:
        selected_genes = [data[i]["Gene"] for i in selected_rows]

    selected_barcodes = []
    if selectedData is not None:
        selected_barcodes = [point['hovertext'] for point in selectedData['points']]


    return Plots.generate_scatter_chart(
        selected_barcodes,
        selected_genes,
        R,
        YX,
        xcol,
        ycol,
        xscale,
        yscale,
        Errorbars,
    )

@callback(
    Output("selected-mut-table","data"),
    Input("primary", "selectedData"),
)
def update_selected_mut_list(selectedData):
    ''' Callback to update list of adaptive loci based on selected clones '''
    my_barcodes = []
    if selectedData is not None:
        my_barcodes = [point['hovertext'] for point in selectedData['points']]
    return Table.generate_subset_table(my_barcodes)

@callback(
    Output("hover-mut-table","data"),
    Input("primary", "hoverData"),
)
def update_hover_mut_list(hoverData):
    ''' Callback to update list of mutations in hovered clone '''
    if "hovertext" in hoverData['points'][0]:
        return Table.generate_hover_table(hoverData['points'][0]['hovertext'])
    raise PreventUpdate

@callback(
    Output("selected-mut-table", "selected_rows"),
    Input("clear", "n_clicks"),
)
def clear(n_clicks):
    ''' Callback to clear selected genes '''
    return []