import dash_bootstrap_components as dbc
from dash import html

def create_breadcrumb(items):
    """
    Create a breadcrumb navigation component
    
    Args:
        items (list): List of dictionaries with keys 'label', 'href' (optional), and 'active' (optional)
        Example: [
            {"label": "Home", "href": "/"},
            {"label": "Apps", "href": "/apps"},
            {"label": "Materials Explorer", "active": True}
        ]
    """
    return html.Div([
        dbc.Breadcrumb(
            items=items,
            class_name="mb-0 fw-bold",
            style={
                "marginLeft": "2.5rem", 
                "marginTop": "1rem"
            },
        )
    ], className="breadcrumb-nav")

def create_page_header(title, icon_class="fas fa-cube", show_references=True, show_documentation=True):
    """
    Create a page header with title and optional buttons
    
    Args:
        title (str): Page title
        icon_class (str): Font Awesome icon class
        show_references (bool): Whether to show the References button
        show_documentation (bool): Whether to show the Documentation button
    """
    buttons = []
    if show_references:
        buttons.append(
            dbc.Button(
                [html.I(className="fas fa-book me-1"), "References"],
                color="light",
                className="me-2"
            )
        )
    if show_documentation:
        buttons.append(
            dbc.Button(
                [html.I(className="fas fa-question-circle me-1"), "Documentation"],
                color="light"
            )
        )

    return html.Div([
        html.Div([
            html.Div([
                html.I(className=f"{icon_class} fa-lg")
            ], className="rounded-circle p-2 text-white me-4 fw-bold", style={
                "fontSize": "1.5rem",
                "width": "50px",
                "height": "50px",
                "display": "flex",
                "alignItems": "center", 
                "justifyContent": "center",
                "backgroundColor": "#004d00"
            }),
            html.Span(title, className="mb-4 fw-bold d-inline", style={
                "fontSize": "2.5rem"
            })
        ], className="d-flex align-items-center"),
        html.Div(buttons, className="ms-auto")
    ], className="d-flex align-items-center mb-4", style={
        "marginLeft": "2.5rem"
    })





def create_app_header(breadcrumb_items, title, icon_class="fas fa-cube", 
                     show_references=True, show_documentation=True, ):
    """
    Create a standard app layout with breadcrumb, header, and optional description
    
    Args:
        breadcrumb_items (list): List of breadcrumb items
        title (str): Page title
        icon_class (str): Font Awesome icon class
        show_references (bool): Whether to show the References button
        show_documentation (bool): Whether to show the Documentation button
    """
    layout_children = [
        create_breadcrumb(breadcrumb_items),
        create_page_header(title, icon_class, show_references, show_documentation)
    ]

    return html.Div([
        html.Div(layout_children, className="app-content")
    ]) 