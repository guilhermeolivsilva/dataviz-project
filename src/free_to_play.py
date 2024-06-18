"""
Render the free_to_play data visualization.

Author: Guilherme Silva
"""

from dash import html, dcc
import plotly.graph_objs as go
import pandas as pd


def get_in_app_vs_single_purchase():
    in_app_purchases = pd.read_pickle("datasets/in_app_purchases.pkl")
    single_purchase = pd.read_pickle("datasets/single_purchase.pkl")

    def group_data(df: pd.DataFrame) -> pd.DataFrame:
        df_grp = (
            df.groupby("score", as_index=False)
            .agg({"gameID": "count"})
            .rename(columns={"gameID": "proportion"})
        )

        totals = len(df)

        df_grp["proportion"] = df_grp["proportion"] / totals * 100

        for i in range(0, 100 + 1):
            if len(df_grp[df_grp["score"] == i]) < 1:
                df_grp = df_grp._append(
                    {"score": i, "proportion": 0}, ignore_index=True
                )

        return df_grp.sort_values(by="score")

    in_app_purchases_grp = group_data(in_app_purchases)
    single_purchase_grp = group_data(single_purchase)

    in_app_purchases_bins = in_app_purchases_grp["proportion"]
    single_purchase_bins = single_purchase_grp["proportion"] * -1

    y = list(range(0, 101, 1))

    layout = go.Layout(
        yaxis=go.layout.YAxis(title="Meta Score"),
        xaxis=go.layout.XAxis(
            range=[-10, 10],
            tickvals=[-8, -5, -3, 0, 3, 5, 8],
            ticktext=[8, 5, 3, 0, 3, 5, 8],
            title="Proporção (%)",
        ),
        barmode="overlay",
        bargap=0.1,
    )

    data = [
        go.Bar(
            y=y,
            x=single_purchase_bins,
            orientation="h",
            name="Compra única",
            hoverinfo="x",
            marker=dict(color="mediumturquoise"),
        ),
        go.Bar(
            y=y,
            x=in_app_purchases_bins,
            orientation="h",
            name="Gratuitos c/ microtransações",
            hoverinfo="x",
            marker=dict(color="seagreen"),
        ),
    ]

    return go.Figure(data=data, layout=layout)


def render_free_to_play(**kwargs):
    return html.Div(
        children=[
            html.H1(children="A indústria de jogos moderna"),
            html.Div(
                children="""
            Entendendo as preferências de consumidores em um mercado cada vez mais competitivo.
        """
            ),
            dcc.Graph(id="free_to_play", figure=get_in_app_vs_single_purchase()),
        ]
    )
