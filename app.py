# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

app = Dash(__name__)


# View 1: placeholder

def get_placeholder_fig():
    placeholder = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })

    fig_placeholder = px.bar(placeholder, x="Fruit", y="Amount", color="City", barmode="group")

    return fig_placeholder

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=get_placeholder_fig()
    )
])


if __name__ == '__main__':
    app.run(debug=True)
