import re

def main():
    spanish_md = r"d:\Rol\SWADE\SWIZ-01-Interface-Zero-3-digital-whkhpj.md"
    
    with open(spanish_md, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    targets = [
        "## RAZAS",
        "## VENTAJAS Y DESVENTAJAS",
        "## ARQUETIPOS",
        "## CATÁLOGO MALMART",
        "## ZEEKS",
        "### RAZAS",
        "### ARQUETIPOS", # Just in case
        "## TRASFONDOS",
        "#### **RAZAS**"
    ]
    
    for i, line in enumerate(lines):
        for target in targets:
            if target.upper() in line.upper():
                print(f"Found {target} at line {i+1}: {line.strip()}")

if __name__ == "__main__":
    main()
