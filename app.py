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
    Output(component_id='grafico-vendas-por-ano', component_property='figure'),
    Input(component_id='radio-buttons-barmode', component_property='value'),
    Input(component_id='dropdown-esquema-de-cores', component_property='value'),
    Input(component_id='range-slider-unidades', component_property='value'),
    Input(component_id='radio-buttons-escala', component_property='value'),
    Input(component_id='datatable-jogos', component_property='derived_virtual_selected_rows'),
)
def gerar_grafico_vendas_por_ano(barmode, esquema_de_cores, valores_range, escala, linhas_selecionadas):
    # Filtrando os dados
    df = pd.read_pickle("datasets/revenue.pkl")
    filtered_df = df.query(f"total_vendas >= {valores_range[0]} and total_vendas <= {valores_range[1]}")
    
    # Tratando o esquema de cores
    #color = 'nome' if esquema_de_cores == 'Por nome' else 'total_vendas'
    color = list(filtered_df['cor']) if esquema_de_cores == 'Por nome' else 'total_vendas'
    
    # Tratando as linhas selecionadas
    if linhas_selecionadas is not None and len(linhas_selecionadas) != 0:
        color = ['#7FDBFF' if i in linhas_selecionadas else '#0074D9' for i in range(len(filtered_df))]
    
    fig = px.bar(
        filtered_df, 
        x="ano_lancamento", 
        y="total_vendas",
        hover_data=['nome', 'publisher', 'total_vendas', 'data_lancamento'],
        color=color, 
        barmode=barmode,
        labels={'ano_lancamento':'Ano de lançamento', 'total_vendas':'Unidades vendidas (mi)'}
    )
    
    fig.update_layout(showlegend=False)
    fig.update_yaxes(type='linear' if escala == 'Linear' else 'log')
    fig.update_traces(width=1)

    return fig


@app.callback(
    Output(component_id='datatable-jogos', component_property='data'),
    Input(component_id='range-slider-unidades', component_property='value')
)
def gerar_dataset_tabela(valores_range):
    df = pd.read_pickle("datasets/revenue.pkl")
    filtered_df = df.query(f"total_vendas >= {valores_range[0]} and total_vendas <= {valores_range[1]}")
    return filtered_df.to_dict('records')


@app.callback(
    Output("datatable-jogos", "selected_rows"),
    Input("clear-selection-datatable-jogos", "n_clicks"),    
)
def clear_selection_datatable(n_clicks):
    return []


if __name__ == "__main__":
    app.run(port=10000, host="0.0.0.0")
