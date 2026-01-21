import os
import json
import re

def clean_html(text):
    text = re.sub(r'# [A-Z]', '', text)
    text = re.sub(r'#### \d+', '', text)
    text = text.replace('\n', ' ').strip()
    text = re.sub(r'\s+', ' ', text)
    return f"<p>{text}</p>"

def parse_md_section(content, start_tag, end_tag, item_type):
    # More robust section extraction
    items = []
    section_match = re.search(f"{re.escape(start_tag)}.*?(?={re.escape(end_tag)}|\\Z)", content, re.DOTALL | re.IGNORECASE)
    if not section_match: return []
    
    text = section_match.group(0)
    
    # Pattern for items in the summary
    # Matches: **NAME** (opt: sub) \n [Requirements: ...] \n Description
    pattern = r"\*\*([^*]+)\*\*\s*(?:\(([^)]+)\))?\s*\n\s*(?:\*\*Requirements:\*\*|\*\*Requisitos:\*\*)?\s*(.*?)\n\s*(.*?)(?=\n\s*\*\*|\n\s*##|\Z)"
    
    matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
    
    for match in matches:
        name = match.group(1).strip()
        sub = match.group(2)
        reqs = match.group(3).strip()
        desc = match.group(4).strip()
        
        # If reqs is empty but desc starts with "Your ...", we might have missed reqs
        # In summary sometimes reqs are missing
        
        items.append({
            "name": name,
            "sub": sub,
            "reqs": reqs if reqs else "None",
            "desc": desc,
            "type": item_type
        })
    return items

def save_items(items, output_dir, lang):
    os.makedirs(output_dir, exist_ok=True)
    for item in items:
        swid = item['name'].lower().replace(" ", "-").replace("!", "").replace("(", "").replace(")", "").replace(".", "")
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
        
        with open(os.path.join(output_dir, f"{swid}.json"), 'w', encoding='utf-8') as out:
            json.dump(foundry_item, out, indent=2, ensure_ascii=False)

def main():
    root = r"d:\Rol\FoundryVTT\Data\modules\swade-setting-iz3\src"
    
    # English
    with open(r"d:\Rol\SWADE\IZ3_Setting_Summary_EN.md", 'r', encoding='utf-8') as f: en = f.read()
    save_items(parse_md_section(en, "MODIFIED HINDRANCES", "EDGES", "hindrance"), os.path.join(root, "en", "hindrances"), "en")
    save_items(parse_md_section(en, "NEW HINDRANCES", "EDGES", "hindrance"), os.path.join(root, "en", "hindrances"), "en")
    save_items(parse_md_section(en, "NEW EDGES", "ZEEKS", "edge"), os.path.join(root, "en", "edges"), "en")
    
    # Spanish
    with open(r"d:\Rol\SWADE\IZ3_Setting_Summary_ES.md", 'r', encoding='utf-8') as f: es = f.read()
    # Note: Spanish markers might be different
    save_items(parse_md_section(es, "## VENTAJAS Y DESVENTAJAS", "## ZEEKS", "edge"), os.path.join(root, "es", "edges"), "es")
    # Need to find where Hindrances are in ES
    
    print("Generation complete.")

if __name__ == "__main__":
    main()
