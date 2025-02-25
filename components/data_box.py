from dash import html
import dash_bootstrap_components as dbc
from typing import Dict, Optional, Union, List, Any
from dash.development.base_component import Component

class DataBox(html.Div):
    """A component for displaying data in a table format."""
    
    def __init__(
        self,
        data: Union[Dict[str, Any], List[Dict[str, Any]]],
        title: Optional[str] = None,
        className: str = "",
        id: Optional[str] = None,
        
    ):
        """
        Initialize a DataBox component.
        
        Args:
            data: Either a dictionary for key-value pairs or a list of dictionaries for table format
            title: Optional title for the box
            className: Additional CSS classes
            id: Component ID
            variant: "key_value" for dict display or "table" for list of dicts display
        """
        if isinstance(data, list) and len(data) > 0:
            table = self._create_table_variant(data)
        else:
            table = self._create_key_value_variant(data if isinstance(data, dict) else {})

        # Add title if provided
        children = []
        if title:
            children.append(html.Div([
                html.Span(
                    title,
                    style={
                        'color': '#666666',
                        'borderBottom': '1px dotted #666666',
                        'paddingBottom': '0.2rem',
                        'display': 'inline-block',
                        'fontSize': '1rem'
                    }
                )
            ], className="data-box-title mb-3"))
        children.append(table)

        # Wrap in Card component
        card = dbc.Card(
            children=children,
            className="p-3",
            style={
                'backgroundColor': 'white',
                'borderRadius': '8px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
                'border': '1px solid #eee'
            }
        )

        # Initialize parent class
        super().__init__(
            children=card,
            className=f"data-box {className}",
            id=id if id else f"data-box-{hash(str(data))}"
        )

    def _create_key_value_variant(self, data: Dict[str, Any]) -> html.Table:
        """Create a key-value pair table."""
        rows = []
        for key, value in data.items():
            rows.append(
                html.Tr([
                    html.Th(
                        key,
                        style={
                            'fontWeight': '800',
                            'color': '#333333',
                            'borderBottom': '1px solid #eee',
                            'padding': '0.4rem 2rem 0.4rem 0',
                            'width': '50%'
                        }
                    ),
                    html.Td(
                        value if isinstance(value, str) else html.Div(value),
                        style={
                            'fontFamily': 'monospace',
                            'borderBottom': '1px solid #eee',
                            'padding': '0.4rem 0',
                            'width': '50%'
                        }
                    )
                ])
            )
        
        return html.Table(
            rows,
            style={
                'width': '100%',
                'borderCollapse': 'collapse'
            }
        )

    def _create_table_variant(self, data: List[Dict[str, Any]]) -> html.Table:
        """Create a table with headers from a list of dictionaries."""
        # Get headers from the first dictionary
        headers = list(data[0].keys())
        
        # Create header row
        header_row = html.Tr([
            html.Th(
                header,
                style={
                    'fontWeight': '800',
                    'borderBottom': '2px solid #ddd',
                    'padding': '0.75rem 1rem',
                    'textAlign': 'left',
                }
            ) for header in headers
        ])
        
        # Create data rows
        data_rows = []
        for item in data:
            row = html.Tr([
                html.Td(
                    item.get(header, '') if isinstance(item.get(header, ''), str) else html.Div(item.get(header, '')),
                    style={
                        'fontFamily': 'monospace',
                        'borderBottom': '1px solid #eee',
                        'padding': '0.4rem 1rem'
                    }
                ) for header in headers
            ])
            data_rows.append(row)
        
        return html.Table(
            [header_row] + data_rows,
            style={
                'width': '100%',
                'borderCollapse': 'collapse'
            }
        )

    def update_data(self, new_data: Union[Dict[str, Any], List[Dict[str, Any]]], variant: str = "key_value"):
        """
        Update the data in the box.
        
        Args:
            new_data: New data to display (dict or list of dicts)
            variant: Ignored parameter, variant is determined by data type
        """
        if variant == "table" and isinstance(new_data, list) and len(new_data) > 0:
            table = self._create_table_variant(new_data)
        else:
            table = self._create_key_value_variant(new_data if isinstance(new_data, dict) else {})

        # Preserve title if it exists
        if len(self.children.children) > 1:
            self.children.children = [self.children.children[0], table]
        else:
            self.children.children = [table]

if __name__ == "__main__":
    # Test data for key-value variant
    kv_data = {
        "Name": "John Doe",
        "Age": 30,
        "Email": "john@example.com",
        "Status": html.Span("Active", style={"color": "green"}),
    }

    # Test data for table variant
    table_data = [
        {"ID": 1, "Name": "John Doe", "Department": "Engineering"},
        {"ID": 2, "Name": "Jane Smith", "Department": "Marketing"},
        {"ID": 3, "Name": "Bob Wilson", "Department": "Sales"},
    ]

    # Create test layout
    test_layout = html.Div([
        # Key-value variant with title
        DataBox(
            data=kv_data,
            title="User Information",
            className="mb-4",
            id="user-info-box"
        ),
        
        # Table variant with title
        DataBox(
            data=table_data,
            title="Employee List",
            className="mb-4",
            id="employee-table"
        ),
        
        # Key-value variant without title
        DataBox(
            data={"Simple": "Example", "Without": "Title"},
            className="mb-4"
        ),
        
        # Empty data handling
        DataBox(
            data={},
            title="Empty Data Box",
            className="mb-4"
        ),
    ])

    # If you want to run this as a standalone app
    from dash import Dash
    import webbrowser
    
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = html.Div(test_layout, className="container p-4")
    
    if __name__ == "__main__":
        webbrowser.open('http://127.0.0.1:8059/')
        app.run_server(debug=True, port=8059)