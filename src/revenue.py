"""
Render the revenue page of the app.

Author: Guilherme Barboza
"""

from dash import html, dcc, dash_table
import pandas as pd


def render_revenue(**kwargs):
    df = pd.read_pickle("datasets/revenue.pkl")

    return html.Div(
        children=[
            html.H1(children='Jogos mais vendidos ao longo dos anos', style={'textAlign':'center'}),
            html.Hr(),

            html.H4(
                children='Gráfico geral com os jogos mais vendidos a cada ano, desde 1971 a 2024',
                style={'textAlign': 'center'}
            ),

            html.Div(
                className='row',
                children=[
                    html.Div(
                        className='six columns',
                        children=[
                            html.Label('Organização das barras'),
                            dcc.RadioItems(
                                options=['overlay', 'relative'],
                                value='overlay',
                                inline=True,
                                id='radio-buttons-barmode'
                            )
                        ]
                    ),
                    html.Div(
                        className='six columns',
                        children=[
                            html.Label('Esquema de cores'),
                            dcc.Dropdown(
                                options=['Por nome', 'Por número de vendas'],
                                value='Por nome', 
                                multi=False,
                                id='dropdown-esquema-de-cores')
                        ]
                    )
                ]
            ),
            
            html.Br(),
            
            html.Div(
                className='row',
                children=[
                    html.Div(
                        className='six columns',
                        children=[
                            html.Label('Filtrar intervalo de unidades vendidas'),
                            dcc.RangeSlider(
                                min=df['total_vendas'].min(),
                                max=df['total_vendas'].max(),
                                value=[df['total_vendas'].min(), df['total_vendas'].max()],
                                tooltip={"placement": "bottom", "always_visible": True},
                                allowCross=False,
                                dots=False,
                                id='range-slider-unidades')
                        ]
                    ),
                    html.Div(
                        className='six columns',
                        children=[
                            html.Label('Escala dos dados'),
                            dcc.RadioItems(options=['Linear', 'Logarítmica'],
                                    value='Linear',
                                    inline=True,
                                    id='radio-buttons-escala')
                        ]
                    )
                ]
            ),
            
            dcc.Graph(id='grafico-vendas-por-ano', figure={}),

            html.Br(),
            html.H4(
                children='Uma tabela paginada que enumera os jogos mais vendidos a cada ano, desde 1971 a 2024',
                style={'textAlign': 'center'}
            ),

            dash_table.DataTable(
                id='datatable-jogos',
                columns=[
                    {'name': 'Nome', 'id': 'nome'},
                    {'name': 'Publisher', 'id': 'publisher'},
                    {'name': 'Total de vendas', 'id': 'total_vendas'},
                    {'name': 'Data de lançamento', 'id': 'data_lancamento'}
                ],
                data=df.to_dict('records'),
                page_size=10,
                row_selectable="single"),
            html.Button("Limpar Seleção", id="clear-selection-datatable-jogos"),
        ]
    )
