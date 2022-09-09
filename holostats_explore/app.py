import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

from holostats_explore.details import layout_details
from holostats_explore.subscribers import layout_subscribers

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Holostats", className="display-4"),
        html.Hr(),
        html.P(
            "Real number for real anons", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Subscribers", href="/", active="exact"),
                dbc.NavLink("Community", href="/community", active="exact"),
                dbc.NavLink("VTuber stats details", href="/details", active="exact"),
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
    if pathname == "/":
        return layout_subscribers
    elif pathname == "/details":
        return layout_details
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(port=8888)
