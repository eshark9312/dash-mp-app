import dash
from dash import html
import dash_bootstrap_components as dbc

# Define your app sections and routes
APP_SECTIONS = [
    {
        "name": "Apps Overview",
        "items": [
            {"icon": "fas fa-atom", "label": "Apps Overview", "href": "/apps"},
        ]
    },
    {
        "name": "EXPLORE AND SEARCH",

        "items": [
            {"icon": "fas fa-search", "label": "Materials Explorer", "href": "/apps/materials"},
            {"icon": "fas fa-atom", "label": "Molecules Explorer", "href": "/apps/molecules"},
            {"icon": "fas fa-atom", "label": "JCESR Molecules", "href": "/apps/jcesr"},
            {"icon": "fas fa-battery-full", "label": "Battery Explorer", "href": "/apps/battery"},
            {"icon": "fas fa-mortar-pestle", "label": "Synthesis Explorer", "href": "/apps/synthesis"},
            {"icon": "fas fa-microscope", "label": "Catalysis Explorer", "href": "/apps/catalysis"},
            {"icon": "fas fa-cube", "label": "MOF Explorer", "href": "/apps/mof"},
        ]
    },
    {
        "name": "ANALYSIS TOOLS",
        "items": [
            {"icon": "fas fa-chart-area", "label": "Phase Diagram", "href": "/apps/phase"},
            {"icon": "fas fa-chart-line", "label": "Pourbaix Diagram", "href": "/apps/pourbaix"},
            {"icon": "fas fa-cubes", "label": "Crystal Toolkit", "href": "/apps/crystal"},
            {"icon": "fas fa-flask", "label": "Reaction Calculator", "href": "/apps/reaction"},
            {"icon": "fas fa-project-diagram", "label": "Interface Reactions", "href": "/apps/interface"},
        ]
    },
    {
        "name": "CHARACTERIZATION",
        "items": [
            {"icon": "fas fa-wave-square", "label": "X-ray Absorption Spectra", "href": "/apps/xas"},
        ]
    },
    {
        "name": "CONTRIBUTED DATA",
        "items": [
            {"icon": "fas fa-database", "label": "MPContribs Explorer", "href": "/apps/mpcontribs"},
            {"icon": "fas fa-table", "label": "GNoME Explorer", "href": "/apps/gnome"},
            {"icon": "fas fa-puzzle-piece", "label": "Contributed Apps", "href": "/apps/contributed"},
        ]
    }
]

def create_left_navbar():
    return html.Div(
        [
            html.Div(
                [
                    html.Div([
                        html.Div(
                            [
                                html.I(className="fas fa-minus"),
                                html.Span(
                                    section["name"],
                                    className="ms-3 nav-text"
                                )
                            ],
                            className="left-nav-header"
                        ) if i > 0 else None,
                        dbc.Nav(
                            [
                                dbc.NavLink(
                                    [
                                        html.I(className=item["icon"]),
                                        html.Span(item["label"], className="ms-2 nav-text")
                                    ],
                                    href=item["href"],
                                    className="left-nav-link"
                                ) for item in section["items"]
                            ],
                            vertical=True,
                            className="left-nav"
                        )
                    ]) for i, section in enumerate(APP_SECTIONS)
                ],
                className="left-navbar-content"
            )
        ],
        className="left-navbar",
        id="left-navbar"
    ) 