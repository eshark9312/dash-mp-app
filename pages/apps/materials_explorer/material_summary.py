import dash_mp_components
import dash
from dash import dcc, html
from components.app_header import create_app_header
import requests
import crystal_toolkit.components as ctc
from pymatgen.core import Structure

API_base_url = "http://127.0.0.1:8000/summary"

# Register the page with a dynamic parameter
dash.register_page(
    __name__,
    path='/apps/materials/:material_id',  # :material_id is a path parameter
    path_template='/apps/materials/<material_id>',  # Alternative syntax
    title='Material Details - Materials Project',
    name='Material Details'
)

def get_material_summary(material_id):
    response = requests.get(f"{API_base_url}/{material_id}")
    response.raise_for_status()
    return response.json()

def layout(material_id):
    material_summary = get_material_summary(material_id)
    pymat_structure = Structure.from_dict(material_summary.get("structure"))

    structure_viewer = ctc.StructureMoleculeComponent(pymat_structure, id=f"structure-viewer-{material_id}")
    structure_viewer_layout = structure_viewer.layout()
    breadcrumb_items = [
        {"label": "Home", "href": "/", "external_link": True},
        {"label": "Apps", "href": "/apps", "external_link": True},
        {"label": "Materials Explorer", "href": "/apps/materials", "external_link": True},
        {"label": material_id, "active": True},
    ]
    app_header = create_app_header(breadcrumb_items, "Materials Explorer", "fas fa-search")
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

    layout = html.Div([app_header, scrollspy_layout])
    ctc.register_crystal_toolkit(app=dash.get_app(), layout=structure_viewer_layout)
    print("structure_viewer_layout registered")
    return layout

