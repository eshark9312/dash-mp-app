import dash_mp_components
import dash
from dash import dcc, html, Input, Output, callback
from components.app_header import create_page_header
import dash_bootstrap_components as dbc
import requests
import crystal_toolkit.components as ctc
from urllib.parse import urlparse, parse_qs 

API_base_url = "http://127.0.0.1:8000/summary"


# Register the page with a dynamic parameter
dash.register_page(
    __name__,
    path='/materials/:material_id',  # :material_id is a path parameter
    path_template='/materials/<material_id>',  # Alternative syntax
    title='Material Details - Materials Project',
    name='Material Details'
)

def get_material_summary(material_id):
    response = requests.get(f"{API_base_url}/{material_id}")
    response.raise_for_status()
    return response.json()


structure_viewer = ctc.StructureMoleculeComponent(id='ctc_structure_viewer')
structure_viewer_layout = structure_viewer.layout()



breadcrumb_items = [
    {"label": "Home", "href": "/", "external_link": True},
    {"label": "Apps", "href": "/apps", "external_link": True},
    {"label": "Materials Explorer", "href": "/materials", "external_link": True},
    {"label": "", "active": True},
]


breadcrumb = dbc.Breadcrumb(
            items = breadcrumb_items,
            class_name = "mb-0 fw-bold",
            style = {
                "marginLeft": "2.5rem", 
                "marginTop": "1rem"
            },
            id = "_breadcrumb_explorer"
        )
page_header = create_page_header("Materials Explorer")
app_header = html.Div([
        html.Div([breadcrumb, page_header], className="app-content")
    ])

scrollspy_layout = html.Div(className='scrollspy app-content', children=[
# html.H1(material_summary.get("formula_pretty"), className="mb-4 menu-label"),
dash_mp_components.Scrollspy(
    menuGroups=[{'label': 'Table of Contents', 'items': [{'label': 'One', 'targetId': 'one'}, {'label': 'Two', 'targetId': 'two'}, {'label': 'Three', 'targetId': 'three'}]}],
    menuClassName="menu",
    menuItemContainerClassName="menu-list",
    activeClassName="is-active",
    offset=0
),
html.Div(className='content', children=[
    html.Div(id='one', children=[
        html.H1('One'),
        structure_viewer_layout
    ]),
    html.Div(id='two', children=[
        html.H1('Two'),
        html.P('lorem ipsum'),
    ]),
    html.Div(id='three', children=[
        html.H1('Three'),
        html.P('lorem ipsum'),
    ]),
])
], style={'backgroundColor': '#f5f5f5'})

layout = html.Div([
    app_header, 
    scrollspy_layout])

ctc.register_crystal_toolkit(app = dash.get_app(), layout = layout)

def get_url_query_params(search_string):
    if not search_string:
        return {}
    return {k: v[0] for k, v in parse_qs(search_string.replace('?', '')).items()}

@callback(
    Output(structure_viewer.id(), 'data'),
    Output('_breadcrumb_explorer', 'items'),
    Input('url', 'pathname'),
    Input('url', 'search')
)
def update_structure(pathname, search):
    query_params = get_url_query_params(search)
    material_id = urlparse(pathname).path.split('/')[-1]
    material_summary = get_material_summary(material_id)
    print(material_id)

    breadcrumb_items = [
    {"label": "Home", "href": "/", "external_link": True},
    {"label": "Apps", "href": "/apps", "external_link": True},
    {"label": "Materials Explorer", "href": "/materials", "external_link": True},
    {"label": material_id, "active": True},
]
    return material_summary.get("structure"), breadcrumb_items