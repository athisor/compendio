import os

def main():
    player_md = r"d:\Rol\SWADE\Interface-Zero-30-players-guide-to-2095-v13.md"
    output_md = r"d:\Rol\SWADE\IZ3_Setting_Summary_EN.md"
    
    if not os.path.exists(player_md):
        print("English Player manual not found.")
        return

    with open(player_md, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # English Markers
    origins_start = -1
    for i, line in enumerate(lines):
        if "**ACTIVIST**" in line and i < 2000:
            origins_start = i
            break
            
    races_start = -1
    for i, line in enumerate(lines):
        if "#### **RACES**" in line and i > 2000:
            races_start = i
            break
            
    edges_start = -1
    for i, line in enumerate(lines):
        if "#### **EDGES AND HINDRANCES**" in line and i > 3000:
            edges_start = i
            break
            
    catalog_start = -1
    for i, line in enumerate(lines):
        if "## MALMART CATALOG" in line and i > 4000:
            catalog_start = i
            break
            
    zeeks_start = -1
    for i, line in enumerate(lines):
        if "#### **ZEEKS**" in line and i > 10000:
             zeeks_start = i
             break

    with open(output_md, 'w', encoding='utf-8') as f:
        f.write("# Interface Zero 3.0 - Setting Summary (English)\n\n")
        f.write("> [!IMPORTANT]\n")
        f.write("> This is a compilation of key information for character creation in Interface Zero 3.0.\n\n")
        
        if origins_start != -1:
            f.write("## ORIGINS (ARCHETYPES)\n\n")
            end_origins = races_start if races_start != -1 else origins_start + 1000
            f.writelines(lines[origins_start:end_origins])
            f.write("\n\n---\n\n")
            
        if races_start != -1:
            f.write("## RACES (ANCESTRIES)\n\n")
            end_races = edges_start if edges_start != -1 else races_start + 1000
            f.writelines(lines[races_start:end_races])
            f.write("\n\n---\n\n")
            
        if edges_start != -1:
            f.write("## EDGES AND HINDRANCES\n\n")
            end_edges = catalog_start if catalog_start != -1 else edges_start + 1000
            f.writelines(lines[edges_start:end_edges])
            f.write("\n\n---\n\n")
            
        if zeeks_start != -1:
            f.write("## ZEEKS & HACKING\n\n")
            f.writelines(lines[zeeks_start:zeeks_start+600])
            f.write("\n\n---\n\n")

    print(f"English summary written to {output_md}")

if __name__ == "__main__":
    main()
