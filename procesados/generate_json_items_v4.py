import os
import json
import re

def clean_html(text):
    text = re.sub(r'# [A-Z]', '', text)
    text = re.sub(r'#### \d+', '', text)
    text = text.replace('\n', ' ').strip()
    text = re.sub(r'\s+', ' ', text)
    return f"<p>{text}</p>"

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', '-', name.lower().replace(" ", "-")).replace("--", "-").strip("-")

def parse_md_section(content, start_tag, end_tag, item_type):
    items = []
    # Use re.escape but allow for some flexibility in whitespace
    start_pattern = re.escape(start_tag)
    end_pattern = re.escape(end_tag)
    
    # Try to find a section between tags
    match = re.search(f"{start_pattern}(.*?)(?={end_pattern}|\\Z)", content, re.DOTALL | re.IGNORECASE)
    if not match: return []
    
    text = match.group(1)
    
    # Updated pattern to catch items correctly even if requirements are slightly differently formatted
    pattern = r"\*\*([^*]+)\*\*\s*(?:\(([^)]+)\))?\s*\n\s*(?:\*\*Requirements:\*\*|\*\*Requisitos:\*\*)?\s*(.*?)\n\s*(.*?)(?=\n\s*\*\*|\n\s*##|\Z)"
    
    matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
    
    for m in matches:
        items.append({
            "name": m.group(1).strip(),
            "sub": m.group(2).strip() if m.group(2) else None,
            "reqs": m.group(3).strip() if m.group(3) else "None",
            "desc": m.group(4).strip(),
            "type": item_type
        })
    return items

def save_items(items, output_dir, lang):
    if not items: return
    os.makedirs(output_dir, exist_ok=True)
    for item in items:
        swid = sanitize_filename(item['name'])
        full_name = item['name']
        if item['sub']:
            full_name = f"{item['name']} ({item['sub']})"
            
        foundry_item = {
            "name": full_name,
            "type": item['type'],
            "system": {
                "category": "Background" if item['type'] == "edge" else "",
                "description": clean_html(item['desc']),
                "notes": f"Requirements: {item['reqs']}",
                "swid": swid,
                "source": "Interface Zero 3.0",
            },
            "img": f"systems/swade/assets/icons/{item['type']}.svg",
            "effects": [],
            "flags": {"iz3": {"lang": lang}}
        }
        
        filepath = os.path.join(output_dir, f"{swid}.json")
        with open(filepath, 'w', encoding='utf-8') as out:
            json.dump(foundry_item, out, indent=2, ensure_ascii=False)
        print(f"Saved {filepath}")

def main():
    root = r"d:\Rol\FoundryVTT\Data\modules\swade-setting-iz3\src"
    
    # English
    en_path = r"d:\Rol\SWADE\IZ3_Setting_Summary_EN.md"
    if os.path.exists(en_path):
        with open(en_path, 'r', encoding='utf-8') as f: en = f.read()
        print("Parsing EN Hindrances...")
        save_items(parse_md_section(en, "MODIFIED HINDRANCES", "NEW HINDRANCES", "hindrance"), os.path.join(root, "en", "hindrances"), "en")
        save_items(parse_md_section(en, "NEW HINDRANCES", "EDGES", "hindrance"), os.path.join(root, "en", "hindrances"), "en")
        print("Parsing EN Edges...")
        save_items(parse_md_section(en, "NEW EDGES", "ZEEKS", "edge"), os.path.join(root, "en", "edges"), "en")
    
    # Spanish
    es_path = r"d:\Rol\SWADE\IZ3_Setting_Summary_ES.md"
    if os.path.exists(es_path):
        with open(es_path, 'r', encoding='utf-8') as f: es = f.read()
        print("Parsing ES Edges...")
        save_items(parse_md_section(es, "## VENTAJAS Y DESVENTAJAS", "SUMARIO DE DESVENTAJAS", "edge"), os.path.join(root, "es", "edges"), "es")
        # For ES Hindrances, they are in the table mostly, but let's see if we can find them
        print("Parsing ES Hindrances (from summary table or sections if any)...")
        # Spanish manual usually lists them in a table, might need separate logic or just create shells
        
    print("Generation complete.")

if __name__ == "__main__":
    main()
