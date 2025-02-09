import dash
from dash import html
import dash_bootstrap_components as dbc

# Define your app sections and routes
APP_SECTIONS = [
    {
        "name": "Apps Overview",
        "items": [
            {"icon": "icon-fontastic-apps", "label": "Apps Overview", "href": "/apps"},
        ]
    },
    {
        "name": "EXPLORE AND SEARCH",
        "items": [
            {"icon": "icon-fontastic-search", "label": "Materials Explorer", "href": "/apps/materials/explorer"},
            {"icon": "icon-fontastic-molecules", "label": "Molecules Explorer", "href": "/apps/molecules/explorer"},
            {"icon": "icon-fontastic-molecules", "label": "JCESR Molecules", "href": "/apps/molecules/jcesr"},
            {"icon": "icon-fontastic-battery", "label": "Battery Explorer", "href": "/apps/battery/explorer"},
            {"icon": "icon-fontastic-synthesis", "label": "Synthesis Explorer", "href": "/apps/synthesis"},
            {"icon": "icon-fontastic-catalysis", "label": "Catalysis Explorer", "href": "/apps/catalysis"},
            {"icon": "icon-fontastic-qmof", "label": "MOF Explorer", "href": "/apps/mof"},
        ]
    },

    {
        "name": "ANALYSIS TOOLS",
        "items": [
            {"icon": "icon-fontastic-phase-diagram", "label": "Phase Diagram", "href": "/apps/analysis/phase"},
            {"icon": "icon-fontastic-pourbaix-diagram", "label": "Pourbaix Diagram", "href": "/apps/analysis/pourbaix"},
            {"icon": "icon-fontastic-toolkit", "label": "Crystal Toolkit", "href": "/apps/analysis/crystal"},
            {"icon": "icon-fontastic-reaction", "label": "Reaction Calculator", "href": "/apps/reaction"},
            {"icon": "icon-fontastic-interface", "label": "Interface Reactions", "href": "/apps/interface"},
        ]
    },
    {
        "name": "CHARACTERIZATION",
        "items": [
            {"icon": "icon-fontastic-xas", "label": "X-ray Absorption Spectra", "href": "/apps/xas"},
        ]

    },
    {
        "name": "CONTRIBUTED DATA",
        "items": [
            {"icon": "icon-fontastic-contribs", "label": "MPContribs Explorer", "href": "/apps/mpcontribs"},
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