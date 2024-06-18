"""
Render the preferences page of the app.

Author: Lucas Bicalho
"""

from dash import html, dcc
import plotly.express as px
import pandas as pd


def geraDFContagemTags():
    df = pd.read_pickle("datasets/preferences.pkl")

    dictAux = dict()

    for linha in range(len(df)):
        if df["tags"][linha] is None:
            continue

        for tag in df["tags"][linha]:
            if tag not in dictAux:
                dictAux[tag] = dict()
                dictAux[tag]["Jogos"] = 0
                dictAux[tag]["Jogadores Agora"] = 0
                dictAux[tag]["Jogadores registrados (milhões)"] = 0

            dictAux[tag]["Jogos"] += 1
            dictAux[tag]["Jogadores Agora"] += df["peak24h"][linha]
            dictAux[tag]["Jogadores registrados (milhões)"] += df["allTimePeak"][linha]

    dictAux2 = dict()
    dictAux2["tag"] = []
    dictAux2["Jogos"] = []
    dictAux2["Jogadores Agora"] = []
    dictAux2["Jogadores registrados (milhões)"] = []

    for tag in dictAux:
        dictAux2["tag"].append(tag)
        dictAux2["Jogos"].append(dictAux[tag]["Jogos"])
        dictAux2["Jogadores Agora"].append(dictAux[tag]["Jogadores Agora"])
        dictAux2["Jogadores registrados (milhões)"].append(
            dictAux[tag]["Jogadores registrados (milhões)"]
        )

    return pd.DataFrame(dictAux2)


def render_preferences(**kwargs):
    fig = px.scatter(
        geraDFContagemTags(),
        x="Jogadores registrados (milhões)",
        y="Jogos",
        size="Jogadores Agora",
        hover_name="tag",
        log_y=False,
        log_x=False,
        size_max=50,
    )

    return html.Div(
        [
            html.H1(children="A indústria de jogos moderna"),
            html.Div(
                children="""
            Entendendo as preferências de consumidores em um mercado cada vez mais competitivo.
        """
            ),
            html.Hr(),
            dcc.Graph(id="preferences", figure=fig),
        ]
    )

    return fig
