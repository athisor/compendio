import os
import json
import re

def clean_html(text):
    # Remove markers like # Y, # T, etc. used in the PDF conversion
    text = re.sub(r'# [A-Z]', '', text)
    # Remove #### \d+ (page numbers)
    text = re.sub(r'#### \d+', '', text)
    text = text.replace('\n', ' ').strip()
    text = re.sub(r'\s+', ' ', text)
    return f"<p>{text}</p>"

def parse_items(content, section_marker, end_marker, item_type="edge"):
    items = []
    
    # Extract the relevant section
    section_start = content.find(section_marker)
    if section_start == -1: return []
    
    section_end = content.find(end_marker, section_start)
    if section_end == -1: section_end = len(content)
    
    section_text = content[section_start:section_end]
    
    # Regex for summary items: **NAME** (opt: sub) \n Reqs \n Desc
    # Note: Summary uses **NAME** then often intro text then Desc
    # Let's use a more flexible one
    pattern = r"\*\*([^*]+)\*\*\s*(?:\(([^)]+)\))?\s*\n\s*(?:\*\*Requirements:\*\*|\*\*Requisitos:\*\*)\s*(.*?)\n\s*(.*?)(?=\n\s*\*\*|\n\s*##|\Z)"
    
    matches = re.finditer(pattern, section_text, re.DOTALL | re.IGNORECASE)
    
    for match in matches:
        name = match.group(1).strip()
        sub_type = match.group(2) # Minor/Major
        reqs = match.group(3).strip()
        desc = match.group(4).strip()
        
        items.append({
            "name": name,
            "sub": sub_type,
            "reqs": reqs,
            "desc": desc,
            "type": item_type
        })
    return items

def generate_foundry_json(item_data, output_dir, lang="en"):
    os.makedirs(output_dir, exist_ok=True)
    
    for item in item_data:
        full_name = item['name']
        if item['sub']:
            full_name = f"{item['name']} ({item['sub']})"
        
        swid = item['name'].lower().replace(" ", "-").replace("!", "").replace("(", "").replace(")", "")
        
        # Determine category
        category = "Background"
        if item['type'] == "edge":
            # Simple heuristic for setting edges
            if any(x in item['name'].upper() for x in ["GUN", "WARRIOR", "FIGHTING"]): category = "Combat"
            elif any(x in item['name'].upper() for x in ["HACKER", "CYBER", "BIO", "COP"]): category = "Professional"
            elif any(x in item['name'].upper() for x in ["IDENTITY", "MULTITUD", "REPUTACIÓN", "SOCIAL"]): category = "Social"
        
        foundry_item = {
            "name": full_name,
            "type": item['type'],
            "system": {
                "category": category if item['type'] == "edge" else "",
                "description": clean_html(item['desc']),
                "notes": f"Requirements: {item['reqs']}",
                "isArcaneBackground": False,
                "requirements": [], 
                "swid": swid,
                "source": "Interface Zero 3.0",
            },
            "img": f"systems/swade/assets/icons/{item['type']}.svg",
            "effects": [],
            "flags": {
                "iz3": {
                    "lang": lang,
                    "originalName": item['name']
                }
            }
        }
        
        filename = f"{swid}.json"
        with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as out:
            json.dump(foundry_item, out, indent=2, ensure_ascii=False)

def main():
    en_md_path = r"d:\Rol\SWADE\IZ3_Setting_Summary_EN.md"
    es_md_path = r"d:\Rol\SWADE\IZ3_Setting_Summary_ES.md"
    module_root = r"d:\Rol\FoundryVTT\Data\modules\swade-setting-iz3\src"
    
    with open(en_md_path, 'r', encoding='utf-8') as f: en_content = f.read()
    with open(es_md_path, 'r', encoding='utf-8') as f: es_content = f.read()
    
    # Process English
    print("Processing English Edges...")
    en_edges = parse_items(en_content, "## ORIGINS", "## ZEEKS", "edge") # Modified to start from Origins to catch all
    # Actually Edges start at ## EDGES AND HINDRANCES
    en_edges = parse_items(en_content, "## EDGES AND HINDRANCES", "## ZEEKS", "edge")
    generate_foundry_json(en_edges, os.path.join(module_root, "en", "edges"), "en")
    
    # Process Spanish
    print("Processing Spanish Edges...")
    es_edges = parse_items(es_content, "## VENTAJAS Y DESVENTAJAS", "## ZEEKS", "edge")
    generate_foundry_json(es_edges, os.path.join(module_root, "es", "edges"), "es")
    
    print("Done generating JSON source files.")

if __name__ == "__main__":
    main()
