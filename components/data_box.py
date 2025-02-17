from dash import html
import dash_bootstrap_components as dbc
from typing import Dict, Optional

class DataBox(html.Div):
    """A component for displaying key-value pairs in a styled box."""
    
    def __init__(
        self,
        data: Dict[str, str],
        title: Optional[str] = None,
        className: str = "",
        id: Optional[str] = None
    ):
        """
        Initialize a DataBox component.
        
        Args:
            data (Dict[str, str]): Dictionary of key-value pairs to display
            title (str, optional): Title of the data box
            className (str, optional): Additional CSS classes
            id (str, optional): The ID used to identify this component
        """
        rows = []
        for key, value in data.items():
            rows.append(
                html.Div([
                    html.Div(key, className="property-label"),
                    html.Div(value, className="property-value")
                ], className="property-row")
            )

        children = rows
        if title:
            children.insert(0, html.H3(title, className="data-box-title mb-3"))

        # Initialize parent class (html.Div)
        super().__init__(
            children=children,
            className=f"data-box {className}",
            id=id if id else f"data-box-{hash(str(data))}"
        )

    @property
    def data(self):
        """Get the current data."""
        return {
            row.children[0].children: row.children[1].children
            for row in self.children
            if isinstance(row, html.Div) and "property-row" in row.className
        }

    def update_data(self, new_data: Dict[str, str]):
        """
        Update the data in the box.
        
        Args:
            new_data (Dict[str, str]): New key-value pairs to display
        """
        rows = []
        for key, value in new_data.items():
            rows.append(
                html.Div([
                    html.Div(key, className="property-label"),
                    html.Div(value, className="property-value")
                ], className="property-row")
            )
        
        # Preserve title if it exists
        if self.children and isinstance(self.children[0], html.H3):
            rows.insert(0, self.children[0])
            
        self.children = dbc.Card(children=rows)