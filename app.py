import dash
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from components.left_navbar import create_left_navbar

navbar = dbc.NavbarSimple(
        brand=html.Div([
            html.Img(
                src="/assets/img/mp_color.png",
                style={'height': '30px'},
                className="me-2"
            ),
            "The Materials Project"
        ], className="brand", style={'display': 'flex', 'alignItems': 'center'}),
        brand_href="/",
        color="dark",
        dark=True,
        className="mb-0 navbar top-navbar",
        fluid=True,
        fixed="top",
        style={'paddingLeft': '50px', 'paddingRight': '50px', 'width': '100%'},
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/", className="nav-link")),
            dbc.NavItem(dbc.NavLink("Apps", href="/apps", className="nav-link")),
            dbc.NavItem(dbc.NavLink("About", href="/about", className="nav-link")),
            dbc.NavItem(dbc.NavLink("Community", href="/community", className="nav-link")),
            dbc.NavItem(dbc.NavLink("ML", href="/ml", className="nav-link")),
            dbc.NavItem(dbc.NavLink("API", href="/api", className="nav-link")),
        ],
    )

# Define the layout of the app
layout = html.Div([
    dcc.Location(id='url', refresh=False),  # Add Location component
    dcc.Store(id='_crystal-toolkit-layout', data=False),
    # Top Navbar
    navbar,
    # Content wrapper
    html.Div([
        # Left Navbar container
        html.Div(id='left-navbar-container'),
        # Page content
        html.Div(
            dash.page_container,
            style={"paddingTop": "56px"}
        )
    ], className="content-wrapper"),
], style={'padding': '0', 'margin': '0', 'width': '100%', 'height': '100vh'})

# Initialize the Dash app with use_pages=True
app = dash.Dash(__name__, 
                external_stylesheets=[
                    dbc.themes.BOOTSTRAP,
                    "/assets/css/bulma.css",     # Base styles
                    "/assets/css/styles.css",     # Our custom styles (overrides)
                    "/assets/css/all.min.css",     # Font Awesome
                    "/assets/css/materials_project_icons.css",     # Materials Project Icons
                    "/assets/css/scrollspy.css"     # Scrollspy
                ],
                use_pages=True, prevent_initial_callbacks=True,
                )

# Set the favicon
app.title = "Materials Project"
app._favicon = "/assets/img/favicon.ico"  
app.layout = layout
# Callback to show/hide left navbar based on URL
@callback(
    Output('left-navbar-container', 'children'),
    Input('url', 'pathname')
)
def toggle_left_navbar(pathname):
    if pathname == '/' or pathname == '':
        return None
    return create_left_navbar()

# Run the app
if __name__ == '__main__':
    app.run_server(
        host='0.0.0.0', # Accepts connections from any IP
        port=8050,       # You can change this port
        debug=True)
