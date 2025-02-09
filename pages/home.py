import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', name='Materials Project')

layout = html.Div([
    # Banner Section
    html.Div(
        style={'backgroundColor': '#2c3e50', 'color': 'white', 'padding': '50px', 'textAlign': 'center'},
        children=[
            html.H1("Harnessing the power of supercomputing"),
            html.P("The Materials Project provides open web-based access to computed information on known and predicted materials as well as powerful analysis tools to inspire and design novel materials."),
            dbc.Button("Start Exploring Materials", color="primary", className="mr-2"),
            dbc.Button("See a Random Material", color="secondary"),
        ]
    ),
    
    # Statistics Section
    html.Div(
        className="container mt-5",
        children=[
            html.H2("The Materials Project by the numbers", className="text-center"),
            dbc.Row([
                dbc.Col(html.Div([
                    html.H3("Materials"),
                    html.H1("169,385", className="display-1"),
                ]), width=3),
                dbc.Col(html.Div([
                    html.H3("Registered Users"),
                    html.H1("560,000+", className="display-1"),
                ]), width=3),
                dbc.Col(html.Div([
                    html.H3("Citations"),
                    html.H1("42,000+", className="display-1"),
                ]), width=3),
                dbc.Col(html.Div([
                    html.H3("CPU Hours/Year"),
                    html.H1("100 million", className="display-1"),
                ]), width=3),
            ]),
        ]
    ),
]) 