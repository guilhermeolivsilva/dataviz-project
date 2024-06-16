"""Render the home page of the app."""

from dash import html


def render_home(**kwargs):
    return html.Div([
        html.H1(children='A indústria de jogos moderna'),
        html.Div(
            children=(
                "Entendendo as preferências de consumidores em um mercado cada"
                " vez mais competitivo"
            )
        ),
        html.Hr(),
        html.H4(
            "Projeto final para a disciplina DCC831 - Visualização de Dados"
        ),
        html.H5("Resumo"),
        html.P(
            "Neste projeto, analisamos as tendências do mercado de jogos de" 
            " computador a partir de uma base de dados da plataforma Steam."
        ),
        html.P(
            "Dentre os achados, destacamos a ascensão de jogos gratuitos para"
            " jogar (free-to-play), jogos independentes (indie) e jogos"
            " competitivos."
        ),
        html.H5("Grupo"),
        html.Ul(
            children=[
                html.P("Guilherme Barboza Mendonça"),
                html.P("Guilherme de Oliveira Silva"),
                html.P("Lucas Rios Bicalho"),
                html.P("Kael Soares Augusto")
            ]
        )
    ])
