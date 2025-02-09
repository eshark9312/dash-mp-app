import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Initialize the Dash app with use_pages=True
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                use_pages=True)

# Set the favicon
app.title = "Materials Project"
app._favicon = "/assets/img/favicon.ico"  # Use this instead of index_string

navbar = dbc.NavbarSimple(
        brand=html.Div([
            html.Img(
                src="/assets/img/mp_color.png",
                height="30px",
                className="me-2"
            ),
            "The Materials Project"
        ], style={'display': 'flex', 'alignItems': 'center'}),
        brand_href="/",
        color="dark",
        dark=True,
        className="mb-0",
        fluid=True,
        style={'paddingLeft': '50px', 'paddingRight': '50px', 'width': '100%'},
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Apps", href="/apps")),
            dbc.NavItem(dbc.NavLink("About", href="/about")),
            dbc.NavItem(dbc.NavLink("Community", href="/community")),
            dbc.NavItem(dbc.NavLink("ML", href="/ml")),
            dbc.NavItem(dbc.NavLink("API", href="/api")),
        ],
    )
    

# Define the layout of the app
app.layout = html.Div([
    # Top Navbar
    navbar,
    # Page content
    dash.page_container
], style={'padding': '0', 'margin': '0', 'width': '100%', 'height': '100vh'})

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
