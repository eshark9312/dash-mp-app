from dash import html
import dash_bootstrap_components as dbc
from typing import Dict, Optional, Union, List

class DataBox(html.Div):
    """A component for displaying data in a table format."""
    
    def __init__(
        self,
        data: Union[Dict[str, str], List[Dict[str, str]]],
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
            children.append(html.H5(title, className="data-box-title mb-3", style={
                'color': '#666666',
                'borderBottom': '1px dotted #666666',
                'paddingBottom': '0.5rem'
            }))
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

    def _create_key_value_variant(self, data: Dict[str, str]) -> html.Table:
        """Create a key-value pair table."""
        print("key-value variant")
        rows = []
        for key, value in data.items():
            rows.append(
                html.Tr([
                    html.Th(
                        key,
                        style={
                            'fontWeight': '500',
                            'color': '#333333',
                            'borderBottom': '1px solid #eee',
                            'padding': '0.75rem 2rem 0.75rem 0',
                            'width': '50%'
                        }
                    ),
                    html.Td(
                        value,
                        style={
                            'color': '#485fc7',
                            'fontFamily': 'monospace',
                            'borderBottom': '1px solid #eee',
                            'padding': '0.75rem 0',
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

    def _create_table_variant(self, data: List[Dict[str, str]]) -> html.Table:
        """Create a table with headers from a list of dictionaries."""
        # Get headers from the first dictionary
        print('table variant')
        headers = list(data[0].keys())
        
        # Create header row
        header_row = html.Tr([
            html.Th(
                header,
                style={
                    'fontWeight': '600',
                    'color': '#333333',
                    'borderBottom': '2px solid #ddd',
                    'padding': '0.75rem 1rem',
                    'textAlign': 'left',
                    'backgroundColor': '#f8f9fa'
                }
            ) for header in headers
        ])
        
        # Create data rows
        data_rows = []
        for item in data:
            row = html.Tr([
                html.Td(
                    item.get(header, ''),
                    style={
                        'color': '#485fc7',
                        'fontFamily': 'monospace',
                        'borderBottom': '1px solid #eee',
                        'padding': '0.75rem 1rem'
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

    def update_data(self, new_data: Union[Dict[str, str], List[Dict[str, str]]], variant: str = "key_value"):
        """Update the data in the box."""
        if variant == "table" and isinstance(new_data, list) and len(new_data) > 0:
            table = self._create_table_variant(new_data)
        else:
            table = self._create_key_value_variant(new_data if isinstance(new_data, dict) else {})

        # Preserve title if it exists
        if len(self.children.children) > 1:
            self.children.children = [self.children.children[0], table]
        else:
            self.children.children = [table]