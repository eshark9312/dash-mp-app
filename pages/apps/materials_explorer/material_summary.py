import dash_mp_components
import dash
from dash import dcc, html, Input, Output, callback
from components.app_header import create_page_header
from components.data_box import DataBox
import dash_bootstrap_components as dbc
import requests
import crystal_toolkit.components as ctc
from urllib.parse import urlparse, parse_qs 

from crystal_toolkit.helpers.layouts import (
    Box,
    Column,
    Columns,
    Container,
    Loading,
    MessageBody,
    MessageContainer,
    MessageHeader,
    Reveal,
)


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
page_header = create_page_header("Materials Explorer", "fas fa-search")
app_header = html.Div([
        html.Div([breadcrumb, page_header], className="app-content")
    ])

summary_data = {
    "material_id": 1,
    "material_name": "Material 1",
    "material_formula": "Fe2O3",
    "material_structure": "BCC",
    "material_description": "This is a sample material.",
}

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
        Columns([
            Column([structure_viewer_layout]),
            Column([DataBox(title="Summary", data=summary_data)]),
            ]),
        Columns([
            Column([dash_mp_components.DataBlock(
        className="box",
        columns=[
          {
            'title': 'Material ID',
            'selector': 'material_id',
            'formatType': 'LINK',
            'formatOptions': {
              'baseUrl': 'https://lbl.gov',
              'target': '_blank',
            },
            'isTop': True,
          },
          {
            'title': 'Formula',
            'selector': 'formula_pretty',
            'formatType': 'FORMULA',
            'isTop': True,
          },
          {
            'title': 'Description',
            'selector': 'description',
            'isBottom': True,
          },
        ],
        data={
          'material_id': 'mp-777',
          'formula_pretty': 'MnO2',
          'volume': 34.88345346,
          'description': 'Ab-initio electronic transport database for inorganic materials. Here are reported the\naverage of the eigenvalues of conductivity effective mass (mₑᶜᵒⁿᵈ), the Seebeck coefficient (S),\nthe conductivity (σ), the electronic thermal conductivity (κₑ), and the Power Factor (PF) at a\ndoping level of 10¹⁸ cm⁻³ and at a temperature of 300 K for n- and p-type. Also, the maximum\nvalues for S, σ, PF, and the minimum value for κₑ chosen among the temperatures [100, 1300] K,\nthe doping levels [10¹⁶, 10²¹] cm⁻³, and doping types are reported. The properties that depend\non the relaxation time are reported divided by the constant value 10⁻¹⁴. The average of the\neigenvalues for all the properties at all the temperatures, doping levels, and doping types are\nreported in the tables for each entry. A legend of the columns of the table is provided below.',
        }
      ),])
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
    ],)

layout = html.Div([
    app_header, 
    html.Section([
        scrollspy_layout
    ], style={
        'backgroundColor': '#f5f5f5',
        'display': 'flex',
        'justifyContent': 'center',
        'width': '100%',
        'padding': '30px'
    })
    ])

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