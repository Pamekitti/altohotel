import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from pages import home, custom, package

server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dbc.Row([
            dbc.Col([
                dbc.NavbarSimple(
                    children=[
                        dbc.NavItem(dbc.NavLink("Home", id='index/home-href', href="/"),
                                    style={'margin-right': '40px'}),
                        dbc.NavItem(dbc.NavLink("Benchmark", id='index/custom-href', href="/custom"),
                                    style={'margin-right': '40px'}),
                        dbc.NavItem(dbc.NavLink("Solution", id='index/solution-href', href="/solution"),
                                    style={'margin-right': '380px'}),
                        html.Img(src="../assets/altologo.png",
                                 style={'width': '40px', 'margin-left': '50px', 'float': 'left'}),
                    ],
                    id='index/navbar',
                    brand="Hotel Benchmarking Tool",
                    brand_href="/",
                    color="white",
                    dark=False,
                    sticky="top",
                    brand_style={'font-size': '20px', 'font-weight': 'bold'},
                    style={'background-color': '#f8f9fa', 'border-bottom': '1px solid #dee2e6'},
                    className="navbar"
                )
            ])
        ])
    ]),
    html.Div(id='page-content', children=[])
])


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page_content(pathname):
    """
    Display the page content based on the pathname
    Args:
        pathname (str): The pathname of the url
    Returns:
        page_content (dash_html_components.Div): The page content
    """
    path = app.strip_relative_path(pathname)
    if path == "custom":
        return custom.serve_layout()
    elif path == "solution":
        return package.serve_layout()
    else:
        return home.serve_layout()


if __name__ == "__main__":
    app.run_server(debug=False, host='0.0.0.0', port=80)
