"""Render the overview page of the app."""

from dash import html, dash_table
import pandas as pd

def render_overview(**kwargs):
    df = pd.read_pickle("datasets/overview.pkl")

    return html.Div([
        html.H1(children='A indústria de jogos moderna'),
        html.Div(children='''
            Entendendo as preferências de consumidores em um mercado cada vez mais competitivo.
        '''),
        html.Hr(),
        html.H2(children='Explore a base de dados', style={'textAlign':'center'}),
        dash_table.DataTable(
            id='interactive_datatable',
            data=df.to_dict('records'),
            columns=[
                {
                    "name": i,
                    "id": i,
                    "deletable": True,
                    "selectable": True
                }
                for i in df.columns
            ],
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            page_size= 50
        )
    ])
