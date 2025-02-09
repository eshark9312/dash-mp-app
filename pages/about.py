import dash
from dash import html

dash.register_page(__name__, path='/about', name='Materials Project')

layout = html.Div([
    html.H1("About The Materials Project"),
    html.P("This is the about page content. Add your content here.")
]) 