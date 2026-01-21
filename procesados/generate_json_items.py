import os
import json
import re

def clean_html(text):
    text = text.replace('\n', ' ').strip()
    text = re.sub(r'\s+', ' ', text)
    return f"<p>{text}</p>"

def parse_md_to_json(md_path, category_map, output_dir, item_type="edge"):
    if not os.path.exists(md_path):
        return
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple regex to find items like **NAME** followed by Requirements and Description
    # Matches: **NAME** (opt: (MINOR/MAJOR)) \n Requirements: ... \n Description
    pattern = r"\*\*([^*]+)\*\*\s*(?:\(([^)]+)\))?\s*\n\s*\*\*Requirements:\*\*\s*(.*?)\n\s*(.*?)(?=\n\s*\*\*|\n\s*##|\Z)"
    
    matches = re.finditer(pattern, content, re.DOTALL | re.IGNORECASE)
    
    for match in matches:
        name = match.group(1).strip()
        sub_type = match.group(2) # Minor/Major
        requirements_str = match.group(3).strip()
        description_raw = match.group(4).strip()
        
        full_name = name
        if sub_type:
            full_name = f"{name} ({sub_type})"
            
        # Determine category based on headers or simple logic
        # For now, we'll try to find which section it's in by position
        pos = match.start()
        category = "Background"
        if "COMBAT EDGES" in content[:pos]: category = "Combat"
        if "HACKING EDGES" in content[:pos]: category = "Professional"
        if "PROFESSIONAL EDGES" in content[:pos]: category = "Professional"
        if "SOCIAL EDGES" in content[:pos]: category = "Social"
        if "NEW HINDRANCES" in content[:pos] and item_type == "hindrance": category = ""

        # Construct JSON structure
        item = {
            "name": full_name,
            "type": item_type,
            "system": {
                "category": category,
                "description": clean_html(description_raw),
                "notes": f"Requirements: {requirements_str}",
                "isArcaneBackground": False,
                "requirements": [], # Complex to parse automatically, leaving for user
                "swid": name.lower().replace(" ", "-").replace("!", ""),
                "source": "Interface Zero 3.0",
            },
            "img": f"systems/swade/assets/icons/{item_type}.svg",
            "effects": [],
            "flags": {}
        }
        
        filename = f"{item['system']['swid']}.json"
        with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as out:
            json.dump(item, out, indent=2, ensure_ascii=False)
        print(f"Generated {filename}")

def main():
    en_md = r"d:\Rol\SWADE\IZ3_Setting_Summary_EN.md"
    edges_dir = r"d:\Rol\FoundryVTT\Data\modules\swade-setting-iz3\src\edges"
    hindrances_dir = r"d:\Rol\FoundryVTT\Data\modules\swade-setting-iz3\src\hindrances"
    
    # Create dirs if they don't exist
    os.makedirs(edges_dir, exist_ok=True)
    os.makedirs(hindrances_dir, exist_ok=True)
    
    print("Parsing English Edges...")
    # We need a more specific regex for the summary file as it has some artifacts
    parse_md_to_json(en_md, {}, edges_dir, "edge")
    
    # Hindrances are slightly different in formatting sometimes, let's see
    # Actually most use **NAME** \n # Y(Intro) \n Description
    # The summary has **NAME (MAJOR)** \n Description
    
if __name__ == "__main__":
    main()
