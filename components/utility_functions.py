from fractions import Fraction

from dash import html
import re
from flask import request

def get_api_base_url():
    """Get the API base URL dynamically based on the current host"""
    # Get the host from the request
    host = request.host.split(':')[0]  # Remove port if present
    
    # For development
    if host in ['127.0.0.1', 'localhost']:
        return "http://127.0.0.1:8000/summary"
    
    # For production - use the same host as the app

    print(f"http://{host}:8000/summary")
    return f"http://{host}:8000/summary"

def format_formula_charge(formula_string: str) -> str:
    """
    Convert formula charge strings into proper superscript format.
    Examples:
        Li+ -> Li⁺
        O2- -> O²⁻
        P5+ -> P⁵⁺
    """
    # Dictionary for superscript numbers
    superscript_numbers = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
    }
    
    # Dictionary for superscript plus and minus
    superscript_symbols = {
        '+': '⁺',
        '-': '⁻'
    }

    # Find the position where the charge starts
    charge_start = -1
    for i, char in enumerate(formula_string):
        if char in '+-' or (char.isdigit() and i > 0):
            charge_start = i
            break
    
    if charge_start == -1:
        return formula_string
    
    # Split into formula and charge
    formula = formula_string[:charge_start]
    charge = formula_string[charge_start:]
    
    # Convert charge to superscript
    superscript_charge = ''
    for char in charge:
        if char.isdigit():
            superscript_charge += superscript_numbers[char]
        else:
            superscript_charge += superscript_symbols[char]
    
    return formula + superscript_charge

def format_chemical_formula(formula_str: str) -> html.Span:
    """
    Convert chemical formula string to formatted HTML with subscripts.
    Handles various formats:
    - Spaced elements: "A2 B3 O4"
    - Unspaced elements: "A2B3O4"
    - Decimal subscripts: "A1.4B3.5"
    - Spaced decimals: "A1.4 B3.5"
    - Variable subscripts: "Na_x Cl_y"
    - Complex subscripts: "Na_{1-1.4}ClO4"
    - Parentheses groups: "Ca(OH)2", "Zn(HCO3)2"
    - Hydrates with dot: "CuSO4·5H2O"
    - Coefficients with hydrates: "2KAl(SO4)2·12H2O"
    
    Args:
        formula_str: Chemical formula string
        
    Returns:
        html.Span: Formatted chemical formula with proper subscripts
    """
    
    def format_number(num_str: str) -> html.Sub:
        """Format a number/expression as subscript"""
        # Handle curly braces
        num_str = num_str.strip('{}')
        return html.Sub(num_str)

    def parse_formula(formula: str, is_start: bool = True) -> list:
        """Parse chemical formula recursively"""
        result = []
        i = 0
        # Handle leading coefficient at the start of the formula
        if is_start and formula[0].isdigit():
            coefficient = ''
            while i < len(formula) and (formula[i].isdigit() or formula[i] in '._{}-'):
                coefficient += formula[i]
                i += 1
            if coefficient:
                result.append(coefficient)
        
        while i < len(formula):
            # Handle dot operator for hydrates
            if formula[i] in ['·', '•']:
                result.append(html.Span('·', style={'margin': '0 2px'}))
                i += 1
                # Handle leading coefficient at the start of the formula
                if formula[0].isdigit():
                    coefficient = ''
                    while i < len(formula) and (formula[i].isdigit() or formula[i] in '._{}-'):
                        coefficient += formula[i]
                        i += 1
                    if coefficient:
                        result.append(coefficient)
                continue
                
            if formula[i] == '(':
                # Find matching parenthesis
                paren_count = 1
                j = i + 1
                while j < len(formula) and paren_count > 0:
                    if formula[j] == '(':
                        paren_count += 1
                    elif formula[j] == ')':
                        paren_count -= 1
                    j += 1
                
                # Parse inside parentheses
                inner_formula = formula[i+1:j-1]
                inner_result = parse_formula(inner_formula, False)
                
                # Look for subscript after parentheses
                k = j
                subscript = ''
                while k < len(formula) and (formula[k].isdigit() or formula[k] in '._{}-'):
                    subscript += formula[k]
                    k += 1
                
                result.extend(['(', *inner_result, ')'])
                if subscript:
                    result.append(format_number(subscript))
                
                i = k
                continue
            
            # Match element symbol (capital letter followed by optional lowercase letter)
            if formula[i].isupper():
                element = formula[i]
                i += 1
                if i < len(formula) and formula[i].islower():
                    element += formula[i]
                    i += 1
                
                # Look for subscript
                subscript = ''
                while i < len(formula) and (formula[i].isdigit() or formula[i] in '._{}-'):
                    subscript += formula[i]
                    i += 1
                
                result.append(element)
                if subscript:
                    result.append(format_number(subscript))
                continue
            
            i += 1
        
        return result

    # Pre-process the formula
    formula_str = formula_str.replace('_', '')  # Remove underscores
    
    # Handle spaced formulas
    if ' ' in formula_str:
        parts = formula_str.split()
        result = []
        for i, part in enumerate(parts):
            result.extend(parse_formula(part))
        return html.Span(result)
    
    return html.Span(parse_formula(formula_str))

def format_decimal_to_fraction(decimal_value: float) -> html.Span:
    """
    Convert decimal to fraction format with HTML superscript and subscript.
    If the fraction differs from decimal by more than 0.0001, returns decimal format.
    
    Args:
        decimal_value: float value to convert
        
    Returns:
        html.Span: Formatted fraction or decimal
        
    Examples:
        0.25 -> ¹/₄
        0.333333 -> ¹/₃
        0.0634921 -> ⁴/₆₃ 
        0.12345678 -> 0.123 (if no close simple fraction exists)
    """
    # Handle zero or very small numbers
    if abs(decimal_value) < 1e-10:
        return html.Span("0")
        
    # Handle whole numbers
    if abs(decimal_value - round(decimal_value)) < 1e-10:
        return html.Span(str(int(round(decimal_value))))

    # Convert to fraction
    frac = Fraction(decimal_value).limit_denominator(1000)
    
    # Check if the fraction is close enough to original value
    if abs(float(frac) - decimal_value) > 0.0001:
        return html.Span(f"{decimal_value:.3f}")
    
    # Format the fraction
    return html.Span([
        html.Sup(str(abs(frac.numerator))),
        "/",
        html.Sub(str(frac.denominator))
    ])

# Test function
if __name__ == "__main__":
    test_formulas = [
        "2KAl(SO4)2·12H2O",    # Potassium alum with coefficient
        "3CuSO4·5H2O",         # Copper sulfate pentahydrate with coefficient
        "0.5CaSO4·2H2O",       # Gypsum with decimal coefficient
        "2.5Na2CO3·10H2O",     # Sodium carbonate decahydrate with decimal coefficient
        "MgSO4·7H2O",          # Epsom salt without coefficient
        # Previous test cases
        "A2 B3 O4",
        "2A2B3O4",
        "1.5A1.4B3.5",
        "2Na_x Cl_y",
        "3Na_{1-1.4}ClO4",
        "4Ca(OH)2",
        "2.5Zn(HCO3)2",
    ]
    
    from dash import Dash
    import dash_bootstrap_components as dbc
    
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    
    test_layout = html.Div([
        html.Div([
            html.Span(f"{formula}: "),
            format_chemical_formula(formula),
            html.Br(),
            format_decimal_to_fraction(0.19047619047619047)
        ]) for formula in test_formulas
    ], style={'padding': '20px', 'font-size': '18px'})
    
    app.layout = test_layout
    app.run_server(debug=True, port=9994)