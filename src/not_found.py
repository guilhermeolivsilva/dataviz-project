"""
Render the 404 error handler.

Author: Guilherme Silva
"""

from dash import html


def render_not_found(pathname):
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )
