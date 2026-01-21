import os

def main():
    player_md = r"d:\Rol\SWADE\Interface-Zero-30-players-guide-to-2095-v13.md"
    output_md = r"d:\Rol\SWADE\IZ3_Summary.md"
    
    if not os.path.exists(player_md):
        print("Player manual not found yet.")
        return

    with open(player_md, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    origins_start = -1
    origins_end = -1
    races_start = -1
    races_end = -1
    edges_start = -1
    edges_end = -1
    hacking_start = -1
    
    for i, line in enumerate(lines):
        if "#### **ACTIVIST**" in line:
            if origins_start == -1: origins_start = i
        if "ORIGIN SUMMARY TABLE" in line:
            # We want to include the table too
            pass
        if "#### **RACES**" in line:
            if origins_end == -1: origins_end = i
            races_start = i
        if "#### **EDGES AND HINDRANCES**" in line:
            races_end = i
            edges_start = i
        if "## MALMART CATALOG" in line:
            edges_end = i
        if "#### **ZEEKS**" in line:
            hacking_start = i

    sections = [
        ("ARQUETIPOS (ORIGINS)", origins_start, origins_end),
        ("RAZAS (RACES)", races_start, races_end),
        ("VENTAJAS Y DESVENTAJAS (EDGES & HINDRANCES)", edges_start, edges_end),
        ("ZEEKS & HACKING", hacking_start, hacking_start + 1000 if hacking_start != -1 else -1)
    ]

    with open(output_md, 'w', encoding='utf-8') as f:
        f.write("# Interface Zero 3.0 - Resumiendo para Compendio\n")
        f.write("> [!NOTE]\n")
        f.write("> Este documento contiene una extracción estructurada para facilitar la creación de los compendios en Foundry VTT.\n\n")
        
        for name, start, end in sections:
            if start != -1:
                f.write(f"## {name}\n\n")
                if end != -1:
                    f.writelines(lines[start:end])
                else:
                    f.writelines(lines[start:])
                f.write("\n\n---\n\n")

    print(f"Detailed summary written to {output_md}")

if __name__ == "__main__":
    main()
