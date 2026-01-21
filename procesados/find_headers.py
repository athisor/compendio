headers = ["RACES", "EDGES AND HINDRANCES", "MALMART CATALOG", "AUGMENTATIONS", "WEAPONS", "SIMULACRUM", "ZEEKS"]

md_file = r"d:\Rol\SWADE\Interface-Zero-30-players-guide-to-2095-v13.md"

with open(md_file, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        for h in headers:
            if h in line.upper() and ("## " in line or "### " in line):
                print(f"Found {h} at line {i+1}: {line.strip()}")
