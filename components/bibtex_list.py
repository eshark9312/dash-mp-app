from dash import html
import dash_bootstrap_components as dbc
from typing import Dict, Optional, Union, List
from pybtex.database import parse_string

class BibList(html.Div):
    """A Dash component to display formatted bibliography references"""
    
    def __init__(
        self,
        data: Union[str, List[str]],
        className: str = "",
        id: Optional[str] = None,
    ):
        """
        Initialize BibList component
        
        Args:
            data: Single BibTeX string or list of BibTeX strings
            className: Additional CSS classes
            id: Component ID
        """
        # Convert single string to list
        if isinstance(data, str):
            self.data = [data]
        else:
            self.data = data
            
        # Process BibTeX entries
        children = self._process_references()
        
        # Initialize parent div with processed children
        super().__init__(
            children=children,
            className=f"bibliography-list {className}".strip(),
            id=id if id else f"bib-list-{hash(str(data))}",
            style={
                'max-width': '1000px',
                'margin': '20px auto',
                'font-family': 'Arial, sans-serif'
            }
        )

    def _format_reference(self, entry, index: int) -> dict:
        """Format a single reference entry into component parts"""
        try:
            entry_type = entry.type.lower()
            # Extract fields
            authors = entry.persons.get('author', [])
            title = entry.fields.get('title', '').strip('{}')
            journal = entry.fields.get('journal', '')
            volume = entry.fields.get('volume', '')
            pages = entry.fields.get('pages', '')
            year = entry.fields.get('year', '')
            url = entry.fields.get('url', '')
            # Format authors
            author_names = [str(author) for author in authors]
            if len(author_names) > 1:
                authors_str = ", ".join(author_names[:-1]) + ", and " + author_names[-1]
            else:
                authors_str = author_names[0] if author_names else ""

            return {
                'type': entry_type,
                'authors': authors_str,
                'title': title,
                'journal': journal,
                'volume': volume,
                'pages': pages,
                'year': year,
                'url': url
            }
        except Exception as e:
            return {'error': f"Error formatting reference {index}: {str(e)}"}

    def _create_reference_component(self, ref_data: dict, index: int) -> html.Div:
        """Create a formatted reference component"""
        if 'error' in ref_data:
            return html.Div(ref_data['error'], 
                          style={'color': 'red', 'padding': '1em'})
        if ref_data['type'] == 'misc':
            return html.Div([
                # Reference number
                html.Span(
                    f"{index}",
                    style={
                        'color': '#0066cc',
                        'font-weight': 500,
                        'margin-right': '0.5em'
                    }
                ),
                # Title
                html.Span(
                    ref_data['title'],
                    style={'color': '#333'}
                ),
                html.Span(". "),
                # Authors
                html.Span(
                    ref_data['authors'],
                    style={'color': '#666'}
                ),
                html.Span(". "),
                html.A(
                    ref_data['url'],
                    href=ref_data['url'],
                    target="_blank",
                    style={'color': '#0066cc'}
                )
            ])

        return html.Div([
            # Reference number
            html.Span(
                f"{index}",
                style={
                    'color': '#0066cc',
                    'font-weight': 500,
                    'margin-right': '0.5em'
                }
            ),
            # Authors
            html.Span(
                ref_data['authors'],
                style={'color': '#666'}
            ),
            html.Span(". "),
            # Title
            html.Span(
                ref_data['title'],
                style={'color': '#333'}
            ),
            html.Span(". "),
            # Journal and details
            html.Span(
                ref_data['journal'],
                style={'font-style': 'italic'}
            ),
            html.Span(
                f", {ref_data['volume']}:{ref_data['pages']}, {ref_data['year']}."
            )
        ], style={
            'margin-bottom': '1em',
            'text-indent': '-2em',
            'padding-left': '2em',
            'line-height': '1.6'
        })

    def _process_references(self) -> List[html.Div]:
        """Process all BibTeX entries and create components"""
        try:
            references = []
            
            # Process each reference
            for i, bib_str in enumerate(self.data, 1):
                # Parse BibTeX string
                bib_data = parse_string(bib_str, 'bibtex')
                
                # Get the first (and should be only) entry
                key, entry = next(iter(bib_data.entries.items()))
                
                # Format and create component
                ref_data = self._format_reference(entry, i)
                ref_component = self._create_reference_component(ref_data, i)
                references.append(ref_component)

            return references

        except Exception as e:
            return [html.Div(
                f"Error processing references: {str(e)}",
                style={'color': 'red', 'padding': '1em'}
            )]

# Example usage:
if __name__ == "__main__":
    import dash

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    # Example BibTeX entries
    example_refs = [
        """@article{Janssen2013,
            author = "Yuri Janssen and Dhamodaran Santhanagopalan and Danna Qian and Miaofang Chi and Xiaoping Wang and Christina Hoffmann and Ying Shirley Meng and Peter G. Khalifah",
            title = "Reciprocal salt flux growth of li fe p o4 single crystals with controlled defect concentrations",
            journal = "Chemistry of Materials",
            volume = "25",
            pages = "4574--4584",
            year = "2013"
        }""",
        """@article{Pang2014,
            author = "Wei Kong Pang and Vanessa K. Peterson and Neeraj Sharma and Je-Jang Shiu and She-huang Wu",
            title = "Lithium migration in li4 ti5 o12 studied using in situ neutron powder diffraction",
            journal = "Chemistry of Materials",
            volume = "26",
            pages = "2318--2326",
            year = "2014"
        }"""
    ]

    app.layout = html.Div([
        BibList(data=example_refs, id="bibliography")
    ])

    app.run_server(debug=True)