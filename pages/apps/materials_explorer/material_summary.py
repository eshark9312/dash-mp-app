from typing import List
import dash_mp_components
import dash
from pybtex.database.input import bibtex

from dash import dcc, html, Input, Output, callback
from components.app_header import create_page_header
from components.bibtex_list import BibList
from components.data_box import DataBox
from components.utility_functions import format_formula_charge, format_chemical_formula, format_decimal_to_fraction
import dash_bootstrap_components as dbc
import requests
import crystal_toolkit.components as ctc
from urllib.parse import urlparse, parse_qs 

from dash_mp_components import (
    Tabs,
)

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


# app header with breadcrumb
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

# scrollspy_menu
scrollspy_menu = dash_mp_components.Scrollspy(
        menuGroups=[{'label': 'Table of Contents', 
                     'items': [
                         {'label': 'Summary', 'targetId': 'summary_box'}, 
                         {'label': 'Crystal Structure', 'targetId': 'crystal_structure_details'},
                         {'label': 'Properties', 'targetId': 'properties_section'},
                         {'label': 'Literature References', 'targetId': 'literature_references'},
                         ]}],
        menuClassName="menu",
        menuItemContainerClassName="menu-list",
        activeClassName="is-active",
        offset=-100,
    )

def properties_tab_layout():
    phase_stability_tab = Tabs(
        labels=['Thermodynamic Stability'],
        children=[
            html.Div([
                html.H4('Thermodynamic Stability'),
                Columns([
                    Column([
                        html.Div(id='phase_stability_databox')
                    ]),
                    Column([dbc.Card([
                        dbc.CardHeader(
                            "Major update to the thermodynamic data",
                            className="text-white bg-primary",
                            style={"font-size": "1.2rem"}
                        ),
                        dbc.CardBody([
                            html.P([
                                "The formation energies have now been calculated with the r2SCAN metaGGA functional, which improves the accuracy of reported thermodynamic data. The new scheme is the default source of data on the webpage, but the GGA/GGA+U data is still available via the API."
                            ]),
                            html.P([
                                "To further explore the impact of different mixing schemes of functionals on the phase diagrams, please go to the ",
                                html.A("Phase Diagram", href="#", className="text-primary"),
                                " App."
                            ])
                        ])
                    ], className="shadow-sm")])
                ])
            ],
            className="pl-2 pr-2 pb-2"),
        ],
        className="ml-0 mb-0 border-light-grey"
    )

    electronic_structure_tab = Tabs(
        labels=['Electronic Structure', 'Magnetic Properties'],
        children=[
            html.Div([
                html.H4('Electronic Structure'),
                Columns([
                    Column([
                        html.Div(id='electronic_structure_databox')
                        ]),
                    Column()
                ])
            ],
            className="pl-2 pr-2 pb-2"),
            html.Div([
                html.H4('Magnetic Properties'),
                Columns([
                    Column([
                        html.Div(id='magnetic_properties_databox')
                        ]),
                    Column()
                ])
            ],
            className="pl-2 pr-2 pb-2"),
        ],
        className="ml-0 mb-0 border-light-grey"
    )

    return dbc.Tabs(
        [
            dbc.Tab(phase_stability_tab, label="Phase Stability"),
            dbc.Tab(electronic_structure_tab, label="Electronic Structure"),
        ],
        className="ml-0 mb-0"
    )


# main layout
scrollspy_layout = html.Div(className='scrollspy', children=[
    html.Div(className='menu', children=[
            html.Div(className='mb-3', id='scrollspy_menu_title'),
            scrollspy_menu
        ]),
    html.Div(className='content', children=[
        Columns([
            Column([structure_viewer_layout]),
            Column([
                html.Div(id="summary_box", className="mb-3"),
                dash_mp_components.DataBlock(
                    id="robocrys_box",
                    className='box',
                    columns=[
                        {'selector':'title', 'isTop': True},
                        {'selector':'description', 'isBottom': True, 'minHeight': '200px'}
                        ],
                    data={'title':'Robocrys', 'description': "Description about the structure generated by robocrys"},
                ),
                ]),
            ]),
        html.Div(id='crystal_structure_details', children=[
            html.H3('Crystal Structure')
        ]),
        Columns([
            Column([
                html.Div(id="lattice_constants", className="mb-3"),
                html.Div(id="symmetry_details", className="mb-3"),
                html.Div(id="chem_env", className="mb-3"),
            ]),
            Column([
                html.Div(id="atomic_positions", className="mb-3"),
                html.Div(id="more_details", className="mb-3"),
            ]),
            ]),
        html.Div(id='properties_section', children=[
            html.H3('Properties')
        ]),
        properties_tab_layout(),
        html.Div(id='literature_references', children=[
            html.H3('Literature References'),
            html.Div(id='literature_list'),
            ], 
            className='mt-3'
        ),
    ])
    ],)

layout = html.Div([
    app_header, 
    html.Section([
        html.Div([  # Added container div with max-width
            scrollspy_layout
        ], style={
            'maxWidth': '1280px',
            'width': '100%',
            'margin': '0 auto',  # Center the container
        })
    ], style={
        'backgroundColor': '#f5f5f5',
        'display': 'flex',
        'justifyContent': 'center',
        'width': '100%',
        'padding-left': '70px'
    })
    ])

ctc.register_crystal_toolkit(app = dash.get_app(), layout = layout)

def get_url_query_params(search_string):
    if not search_string:
        return {}
    return {k: v[0] for k, v in parse_qs(search_string.replace('?', '')).items()}

def generate_lattice_constants_box(lattice_data):
    lattice_constants ={
        'a': f"{lattice_data['a']:.2f} Å",
        'b': f"{lattice_data['b']:.2f} Å",
        'c': f"{lattice_data['c']:.2f} Å",
        'α': f"{lattice_data['alpha']:.2f} º",
        'β': f"{lattice_data['beta']:.2f} º",
        'ɣ': f"{lattice_data['gamma']:.2f} º",
        'Volume': f"{lattice_data['volume']:.2f} Å³",
    }
    return DataBox(title="Lattice", data=lattice_constants).children

def generate_summary_box(mpr_response):
    magnetic_ordering = {
        'NM': 'Non-magnetic', 
        'FM': 'Ferro-magnetic', 
        'FiM': 'Ferrimagnetic'
    }
    summary_data = {
      'Energy Above Hull': f"{mpr_response.get('energy_above_hull'):.3f} eV/atom",
      'Space Group': f"{mpr_response.get('symmetry')['symbol']}",
      'Band Gap': f"{mpr_response.get('band_gap'):.2f} eV",
      'Predicted Formation Energy': f"{mpr_response.get('formation_energy_per_atom'):.3f} eV/atom",
      'Magnetic Ordering': magnetic_ordering[mpr_response.get('ordering')],
      'Total Magnetization': f"{mpr_response.get('total_magnetization'):.2f} µB/f.u.",
      'Experimentally Observed': 'No' if mpr_response.get('theoretical') else 'Yes',
    }
    return DataBox(data=summary_data).children

def generate_symmetry_box(sym_data):
    return DataBox(title="Symmetry", data=sym_data).children

def generate_atomic_posistions_box(wyckoff_sites_data):
    return DataBox(title="Atomic Positions", data=wyckoff_sites_data).children

def generate_scrollspy_menu_title(mp_id, formula_pretty):
    return [
        html.Div(format_chemical_formula(formula_pretty), style={"font-size": "2.5rem"}),
        html.Span(mp_id, style={"fontSize":"1.5rem", "fontWeight": 400}), 
        ]

def generate_chemical_environment(chem_env_data):
    chem_env_table = []
    for ce in chem_env_data:
        chem_env_table.append({
                "Wyckoff": ce['Wyckoff'],
                "Species": format_formula_charge(ce['Species']),
                "Environment": ce['Environment'],
                "IUPAC": ce['IUPAC'],
                "CSM": ce['CSM'],
        })
    return DataBox(title="Chemical Environment", data=chem_env_table).children

def generate_literature_list(literature_references):
    return BibList(data = literature_references).children

def generate_phase_stability_box(thermostability_info):
    if (thermostability_info['Predicted Stable']):
        thermostability_info['Predicted Stable'] = html.I(className="fas fa-circle-check fa-lg", style={"color": "green"})
    else:
        thermostability_info['Predicted Stable'] = html.I(className="fas fa-circle-xmark fa-lg", style={"color": "red"})
    
    if (float(thermostability_info['Energy Above Hull'].split(' ')[0]) > 0):
        thermostability_info['Energy Above Hull'] = html.Div([
            html.I(className="fas fa-circle-chevron-up fa-lg", style={"color": "red"}), html.Span('  '),
            html.Span(thermostability_info['Energy Above Hull'], style={"font-size": "1rem"})
        ])
    else:
        thermostability_info['Energy Above Hull'] = html.Div([
            html.I(className="fas fa-circle-minus fa-lg", style={"color": "green"}), html.Span('  '),
            html.Span(thermostability_info['Energy Above Hull'], style={"font-size": "1rem"})
        ])

    if (isinstance(thermostability_info['Decomposes to'], List)):
        decompose_to = []
        for i in range(len(thermostability_info['Decomposes to'])):
            component = thermostability_info['Decomposes to'][i]
            decompose_to.append(format_decimal_to_fraction(component['amount']))
            decompose_to.append(dcc.Link(format_chemical_formula(component['formula']), href=f"/materials/{component['material_id']}", className="text-primary"))
            if i != len(thermostability_info['Decomposes to']) -1:
                decompose_to.append(html.Span(' + '))
        thermostability_info['Decomposes to'] = html.Div(decompose_to, style={"font-size": "1rem"})
    else:
        thermostability_info['Decomposes to'] = 'Not predicted to decompose'
    # return html.Div()
    return DataBox(data=thermostability_info).children

@callback(
    Output(structure_viewer.id(), 'data'),
    Output('_breadcrumb_explorer', 'items'),
    Output('summary_box', 'children'),
    Output('robocrys_box', 'data'),
    Output('lattice_constants', 'children'),
    Output('symmetry_details', 'children'),
    Output('atomic_positions', 'children'),
    Output('more_details', 'children'),
    Output('scrollspy_menu_title', 'children'),
    Output('chem_env', 'children'),
    Output('literature_list', 'children'),
    Output('phase_stability_databox', 'children'),
    Input('url', 'pathname'),
    Input('url', 'search')
)
def update_structure(pathname, search):
    query_params = get_url_query_params(search)
    material_id = urlparse(pathname).path.split('/')[-1]
    material_summary = get_material_summary(material_id)
    breadcrumb_items = [
        {"label": "Home", "href": "/", "external_link": True},
        {"label": "Apps", "href": "/apps", "external_link": True},
        {"label": "Materials Explorer", "href": "/materials", "external_link": True},
        {"label": material_id, "active": True},
    ]
    robocrys_block_data = material_summary["description"]
    robocrys_block_data['title'] = "Description"

    more_details_block = DataBox(data = {
        "Number of Atoms": material_summary["nsites"],
        "Density": f"{material_summary["density"]:.2f} g·cm⁻³",
        "Possible Oxidation States": " ".join([format_formula_charge(specie) for specie in material_summary["possible_species"]]),
    }).children

    generate_literature_list(material_summary['literature'])

    return  material_summary.get("structure"), \
            breadcrumb_items, \
            generate_summary_box(material_summary), \
            robocrys_block_data, \
            generate_lattice_constants_box(material_summary["structure"]["lattice"]), \
            generate_symmetry_box(material_summary['symmetry_detail']), \
            generate_atomic_posistions_box(material_summary["wyckoff_sites"]), \
            more_details_block, \
            generate_scrollspy_menu_title(material_id, material_summary['formula_pretty']), \
            generate_chemical_environment(material_summary['chemical_environment']), \
            generate_literature_list(material_summary['literature']), \
            generate_phase_stability_box(material_summary['thermostability'])

