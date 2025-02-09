import dash
from dash import html

dash.register_page(
    __name__,
    path='/apps',
    title='Apps - Materials Project',
    name='Apps Overview'
)

layout = html.Div([
    html.H1("Apps Overview"),
    # Your layout here  
], className="main-content") 