"""
Main source file for the Plotly Dash app.

Author: Guilherme Silva
"""

import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html

from src import *


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

sidebar = html.Div(
    [
        dbc.Nav(
            [
                dbc.NavLink("Início", href="/", active="exact"),
                dbc.NavLink("Visão geral", href="/overview", active="exact"),
                dbc.NavLink("Receitas", href="/revenue", active="exact"),
                dbc.NavLink("Preferências", href="/preferences", active="exact"),
                dbc.NavLink(
                    "Jogos pagos vs. gratuitos", href="/free_to_play", active="exact"
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    pages = {
        "/": render_home,
        "/overview": render_overview,
        "/revenue": render_revenue,
        "/preferences": render_preferences,
        "/free_to_play": render_free_to_play,
    }

    handler = pages.get(pathname, render_not_found)

    return handler(pathname=pathname)


@app.callback(
    Output(component_id="grafico-vendas-por-ano", component_property="figure"),
    Input(component_id="radio-buttons-barmode", component_property="value"),
    Input(component_id="dropdown-esquema-de-cores", component_property="value"),
    Input(component_id="datatable-jogos", component_property="active_cell"),
)
def on_radio_buttons_barmode_changed(barmode, esquema_de_cores, linha_selecionada):
    df = pd.read_pickle("datasets/revenue.pkl")

    # Tratando o esquema de cores
    color = "nome" if esquema_de_cores == "Por nome" else "total_vendas"

    # Tratando a linha selecionada
    if linha_selecionada is None:
        df["aux_select"] = True
    else:
        df["aux_select"] = False
        print(linha_selecionada)
        df.iloc[linha_selecionada["row"], df.columns.get_loc("aux_select")] = True

        color = "aux_select"

    fig = px.bar(
        df,
        x="ano_lancamento",
        y="total_vendas",
        hover_data=["nome", "publisher", "total_vendas", "data_lancamento"],
        color=color,
        barmode=barmode,
    )

    return fig


@app.callback(
    Output("datatable-jogos", "selected_cells"),
    Output("datatable-jogos", "active_cell"),
    Input("clear-selection-datatable-jogos", "n_clicks"),
)
def clear(n_clicks):
    return [], None


if __name__ == "__main__":
    app.run(port=10000, host="0.0.0.0")
