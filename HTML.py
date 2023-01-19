'''
    HTML - Module to generate HTML for Dash app
    Sandeep Venkataram
    Jan 2023
'''

from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import Data
import Table


def generate_header():
    """ Generate HTML header """
    header = html.H3(
        "Yeast adaptation in a community context", className="bg-primary text-white p-2 mb-2 text-center"
    )
    return header

def generate_subheader():
    """ Generate HTML subheader """
    subheader = html.H6(
        html.Div([
            "Data from ",
            dcc.Link("Venkataram et al.", href="https://www.nature.com/articles/s41559-022-01923-8"),
            html.I(" Nature Ecology and Evolution"),
            " (2023)"
        ]),
        className = "bg-secondary text-white p-2 mb-2 text-center"
    )
    return subheader

def generate_axis_selector(my_id: str, axis: str, default_val: str):
    """ Generate HTML DIV for axis selector dropdown """
    my_div = html.Div(
        [
            dcc.Dropdown(
                options = [{"label" : Data.master_name_map[x], "value" : x} for x in Data.master_name_map],
                value = default_val,
                id={
                    'type': 'axis-dropdown-'+axis,
                    'index': my_id,
                },
                clearable=False,
            ),
        ],
        className="mb-4",
    )
    return(my_div)

def generate_scale_radio(my_id: str, axis: str):
    """ Generate HTML DIV for scale radio buttons """
    my_div = html.Div(
        [
            dcc.RadioItems(
                ["linear","log"],
                "linear",
                id={
                    'type': 'axis-scale-radio-'+axis,
                    'index': my_id,
                },
                inputStyle={"margin-right": "5px", "margin-left": "5px", "margin-top" : "13px"},
            ),
        ],
        className="mb-4",
    )
    return(my_div)

def generate_plot_checkboxes(my_id: str):
    """ Generate HTML DIV for plot checkboxes """
    my_div = html.Div(
        [
            dcc.Checklist(
                options = [
                    {"label": "R", "value" : "R"},
                    {"label": "Errorbars", "value" : "Errorbars"},
                    {"label": "Y=X", "value" : "YX"},
                ],
                value = ["R","Errorbars"],
                id= {
                    'type': 'figure-checkboxes',
                    'index': my_id,
                },
                inline=True,
                inputStyle={"margin-right": "5px", "margin-left": "20px"},
            ),
        ],
        className="mb-4",
    )
    return(my_div)


def get_figure_id(my_id):
    """ Generate ID for dcc Graph"""
    if my_id == "primary": # Make primary plot different from other plots so that they can be handled with separate callbacks
        return my_id
    return {'type': "figure", 'index': my_id,}

def generate_scatter_col(my_id: str, defaultx: str, defaulty: str):
    """ Generate HTML column including graph, X and Y dropdown and scale selector, and plot checkboxes """
    result = dbc.Col(
        [
            dcc.Graph(
                id = get_figure_id(my_id),
                hoverData={'points': [{'hovertext': 'A1_243081'}]}
            ),
            dbc.Row(
                [
                dbc.Col(dbc.Label("X: ", width=1),width=1),
                dbc.Col(generate_axis_selector(my_id, "X", defaultx),width=8),
                dbc.Col(generate_scale_radio(my_id, "X"),width=3),
                ]
            ),
            dbc.Row(
                [
                dbc.Col(dbc.Label("Y: ", width=1),width=1),
                dbc.Col(generate_axis_selector(my_id, "Y", defaulty),width=8),
                dbc.Col(generate_scale_radio(my_id, "Y"),width=3),
                ]
            ),
            generate_plot_checkboxes(my_id),
        ],
        width=4,
    )
    return result

def generate_selected_table():
    """ Generate HTML Column for table of adaptive loci """
    result = dbc.Col(
        [
            dbc.Label("Adaptive Loci", className='text-center'),
            dash_table.DataTable(
                id = "selected-mut-table",
                columns = [{'id': x, 'name': x} for x in Table.Subset_Columns],
                editable = False,
                row_selectable="multi",
                selected_rows = [],
                style_table={'overflowX': 'scroll', 'overflowY': 'scroll'},
                fixed_columns={'headers':True, "data": 1},
                sort_action="native",
                sort_mode="multi",
                page_size = 10,
                page_current =0,
                page_action="native",

            ),
            dbc.Button("Clear selection", id="clear"),
        ],
        width=4,
    )
    return result

def generate_highlighted_table():
    """ Generate HTML Column for table of mutations in clone """
    result = dbc.Col(
        [
            dbc.Label("Mutations in Isolate", className='text-center'),
            dash_table.DataTable(
                id = "hover-mut-table",
                columns = [{'id': Table.Hover_Column_Map[x], 'name': Table.Hover_Column_Map[x]} for x in Table.Hover_Columns],
                editable = False,
                style_table={'overflowX': 'scroll'},
                fixed_columns={'headers':True, "data": 1},
                page_size = 10,
                page_current =0,
                page_action="native",
            ),

        ],
        width=4,
    )

    return result
