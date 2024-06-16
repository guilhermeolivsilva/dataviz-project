"""Main source file for the Plotly Dash app."""

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

from src import *


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


sidebar = html.Div(
    [
        dbc.Nav(
            [
                dbc.NavLink("Início", href="/", active="exact"),
                dbc.NavLink("Visão geral", href="/overview", active="exact"),
                dbc.NavLink("Preferências", href="/preferences", active="exact"),
                dbc.NavLink("Jogos pagos vs. gratuitos", href="/free_to_play", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    pages = {
        "/": render_home,
        "/overview": render_overview,
        "/preferences": render_preferences,
        "/free_to_play": render_free_to_play
    }

    handler = pages.get(pathname, render_not_found)

    return handler(pathname=pathname)   


if __name__ == '__main__':
    app.run(port=10000, host="0.0.0.0")
