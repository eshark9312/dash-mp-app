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