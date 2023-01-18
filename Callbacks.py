'''
    Callbacks - Callback functions for Dash app
    Sandeep Venkataram
    Jan 2023
'''

from dash import Input, Output, State, callback, MATCH, ctx
from dash.exceptions import PreventUpdate


import Plots
import Table


@callback(
    Output({'type': 'figure', 'index': MATCH}, 'figure'),
    Input({'type': 'figure', 'index': MATCH}, 'figure'),
    Input({'type': 'figure', 'index': 'primary'}, 'selectedData'),
    Input("selected-mut-table","data"),
    Input("selected-mut-table","selected_rows"),
    Input({'type': 'figure-checkboxes', 'index': MATCH}, 'value'),
    Input({'type': 'axis-dropdown-X', 'index': MATCH}, 'value'),
    Input({'type': 'axis-scale-radio-X', 'index': MATCH}, 'value'),
    Input({'type': 'axis-dropdown-Y', 'index': MATCH}, 'value'),
    Input({'type': 'axis-scale-radio-Y', 'index': MATCH}, 'value'),
    State({'type': 'figure', 'index': MATCH}, 'id'),
)
def update_scatter(infig, selectedData, data, selected_rows, checkboxes, xcol, xscale, ycol, yscale, id):
    ''' Flexible callback to update scatterplots '''
    R = "R" in checkboxes
    YX = "YX" in checkboxes
    Errorbars = "Errorbars" in checkboxes

    selected_genes = []
    if len(selected_rows)>0:
        selected_genes = [data[i]["Gene"] for i in selected_rows]

    selected_barcodes = []
    if selectedData is not None:
        selected_barcodes = [point['hovertext'] for point in selectedData['points']]

    if (id['index'] == "primary") and (infig is not None) and (ctx.args_grouping[1]['triggered'] or ctx.args_grouping[3]['triggered']):
        raise PreventUpdate
    
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
        id['index'],
    )

@callback(
    Output("selected-mut-table","data"),
    Input({'type': 'figure', 'index': 'primary'}, "selectedData"),
)
def update_selected_mut_list(selectedData):
    ''' Callback to update list of adaptive loci based on selected clones '''
    my_barcodes = []
    if selectedData is not None:
        my_barcodes = [point['hovertext'] for point in selectedData['points']]
    return Table.generate_subset_table(my_barcodes)

@callback(
    Output("hover-mut-table","data"),
    Input({'type': 'figure', 'index': 'primary'}, "hoverData"),
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