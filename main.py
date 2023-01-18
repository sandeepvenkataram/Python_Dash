
'''
    Main - main module to build layout and run Dash app
    Sandeep Venkataram
    Jan 2023
'''

from dash import Dash
import dash_bootstrap_components as dbc

import HTML
import Callbacks

my_theme = dbc.themes.DARKLY
# stylesheet with the .dbc class
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[my_theme, dbc_css])



app.layout = dbc.Container(
    [
        HTML.generate_header(),
        HTML.generate_subheader(),
        dbc.Row(
            [
                HTML.generate_scatter_col("primary", "Alone_fitness", "Community_fitness"),
                HTML.generate_selected_table(),
                HTML.generate_highlighted_table(),
            ]
        ),
        dbc.Row(
            [
                HTML.generate_scatter_col("fig1", "YYC_avg_rescaled", "AYC_avg_rescaled"),
                HTML.generate_scatter_col("fig2", "r_Avg_rescaled", "K_Avg_rescaled"),
                HTML.generate_scatter_col("fig3", "K_Avg_rescaled", "Community_fitness"),
            ]
        ),
    ],
    fluid=True,
    className="dbc",
)







if __name__ == "__main__":
    app.run_server(debug=True)