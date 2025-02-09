import dash
import dash_mp_components
from dash import html, callback, Output, Input

import json
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

dash.register_page(
    __name__,

    path='/apps/materials/explorer',
    title='Materials Explorer - Materials Project',
    name='Materials Explorer'
)

with open('pages/apps/materials_explorer/columns.json','r') as fp:
  columns = json.load(fp)


with open('pages/apps/materials_explorer/filterGroups.json','r') as fp:
  filterGroups = json.load(fp)


layout = html.Div(children=[
  html.Div(id="selected-rows"),
  html.Div(id="clicked-filter-groups"),
  dash_mp_components.SearchUIContainer(
    [
      dash_mp_components.SearchUISearchBar(
              periodicTableMode="toggle",
              placeholder="e.g. Li-Fe or Li,Fe or Li3Fe or mp-19017",
              errorMessage="Please enter a valid formula (e.g. CeZn5), list of elements (e.g. Ce, Zn or Ce-Zn), or Material ID (e.g. mp-394).",
              chemicalSystemSelectHelpText="Select elements to search for materials with **only** these elements",
              elementsSelectHelpText="Select elements to search for materials with **at least** these elements",
              allowedInputTypesMap={
                                      "chemical_system": { "field": 'chemsys' },
                                      "elements": { "field": 'elements' },
                                      "formula": { "field": 'formula' },
                                      "mpid": { "field": 'material_ids' }
                                    },
              helpItems=[
                    { "label": 'Search Examples' },
                    {
                      "label": 'Include at least elements',
                      "examples": ['Li,Fe', 'Si,O,K']
                    },
                    {
                      "label": 'Include only elements',
                      "examples": ['Li-Fe', 'Si-O-K']
                    },
                    {
                      "label": 'Include only elements plus wildcard elements',
                      "examples": ['Li-Fe-*-*', 'Si-Fe-*-*-*']
                    },
                    {
                      "label": 'Has exact formula',
                      "examples": ['Li3Fe', 'Eu2SiCl2O3']
                    },
                    {
                      "label": 'Has formula with wildcard atoms',
                      "examples": ['LiFe*2*', 'Si*']
                    },
                    {
                      "label": 'Has Material ID',
                      "examples": ['mp-149', 'mp-19326']
                    },
                    {
                      "label": 'Additional search options available in the filters panel.'
                    }
                  ]
          ),
      dash_mp_components.SearchUIGrid()
    ],
    view="table",
    columns=columns,
    filterGroups=filterGroups,
    apiEndpoint="http://127.0.0.1:8000/summary/",
    autocompleteFormulaUrl="https://api.materialsproject.org/materials/formula_autocomplete/",
    apiKey="os.environ['MP_API_KEY']",
    resultLabel="material",
    hasSortMenu=True,
    selectableRows=True,
    sortFields=['-energy_above_hull', 'formula_pretty'],
    conditionalRowStyles=[
      {
        'selector': 'is_stable',
        'value': True,
        'style': {
          'backgroundColor': '#DBE2FA',
          'boxShadow': '4px 0px 0px 0px #000 inset',
        },
      },
    ]
  )
], className="app-content")

@callback(
    Output('selected-rows', 'children'),
    Input('search-ui-demo', 'selectedRows')
)

def showNumberOfSelectedRows(selectedRows):
    if not selectedRows:
      raise PreventUpdate
    return f"Selected rows: {str(len(selectedRows))}"

@callback(
    Output('clicked-filter-groups', 'children'),
    Input('materials-input', 'submitButtonClicks')
)
def click_filter_group(n_clicks):
    print(n_clicks)
    return n_clicks

# use True to load a dev build of react
if __name__ == '__main__':
    app.run_server(debug=False)