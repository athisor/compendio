import os
import json
import re

def clean_text(text):
    text = re.sub(r'# [A-Z]', '', text)
    text = re.sub(r'#### \d+', '', text)
    text = text.replace('\n', ' ').strip()
    text = re.sub(r'\s+', ' ', text)
    return text

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', '-', name.lower().replace(" ", "-")).replace("--", "-").strip("-")

def parse_origins(text, lang):
    print(f"Parsing {lang} origins...")
    origins = []
    # Identify items by **NAME**
    name_matches = list(re.finditer(r"\*\*([A-ZÁÉÍÓÚÑ ]+)\*\*", text))
    
    for i in range(len(name_matches)):
        name = name_matches[i].group(1).strip()
        # Filter out common bold terms that aren't titles
        if len(name.split()) > 5 or name.upper() in ["TRASFONDOS", "ORIGINS", "HABIIDADES", "EQUIPO", "SKILLS", "GEAR", "RAZAS", "SUMARIO DE TRASFONDOS"]: 
            continue
        
        start_pos = name_matches[i].end()
        end_pos = name_matches[i+1].start() if i+1 < len(name_matches) else len(text)
        
        chunk = text[start_pos:end_pos]
        
        quote_match = re.search(r"_(.*?)_", chunk, re.DOTALL)
        quote = quote_match.group(1).strip() if quote_match else ""
        
        if lang == "en":
            skills_match = re.search(r"Skills:\*\*\s*(.*?)(?=\n\s*\n|\n\s*-|\*\*Gear|\Z)", chunk, re.DOTALL | re.IGNORECASE)
            gear_match = re.search(r"Gear:\*\*\s*(.*?)(?=\n\s*\n|\Z)", chunk, re.DOTALL | re.IGNORECASE)
        else:
            skills_match = re.search(r"Habilidades:\*\*\s*(.*?)(?=\s*\*\*|\n\s*\n|\Z)", chunk, re.DOTALL | re.IGNORECASE)
            gear_match = re.search(r"Equipo:\*\*\s*(.*?)(?=\s*\*\*|\n\s*\n|\Z)", chunk, re.DOTALL | re.IGNORECASE)
            
        skills = skills_match.group(1).strip() if skills_match else ""
        gear = gear_match.group(1).strip() if gear_match else ""
        
        desc_start = quote_match.end() if quote_match else 0
        desc_end = skills_match.start() if skills_match else (gear_match.start() if gear_match else len(chunk))
        desc = chunk[desc_start:desc_end].strip()
        
        if name and (skills or gear):
            print(f"Found origin: {name}")
            origins.append({
                "name": name,
                "quote": quote,
                "desc": desc,
                "skills": skills,
                "gear": gear,
                "lang": lang
            })
            
    return origins

def save_origin_json(origin, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    swid = sanitize_filename(origin['name'])
    
    html_desc = f"<blockquote>{origin['quote']}</blockquote>{clean_text(origin['desc'])}"
    html_desc += f"<p><strong>Skills:</strong> {clean_text(origin['skills'])}</p>"
    html_desc += f"<p><strong>Gear:</strong> {clean_text(origin['gear'])}</p>"
    
    foundry_item = {
        "name": origin['name'].title(),
        "type": "item",
        "system": {
            "description": html_desc,
            "notes": f"Origin: {origin['name']}",
            "swid": swid,
            "source": "Interface Zero 3.0"
        },
        "img": "icons/sundries/books/book-open-purple.svg",
        "flags": {"iz3": {"lang": origin['lang'], "type": "origin"}}
    }
    
    filepath = os.path.join(output_dir, f"{swid}.json")
    with open(filepath, 'w', encoding='utf-8') as out:
        json.dump(foundry_item, out, indent=2, ensure_ascii=False)

def main():
    root = r"d:\Rol\FoundryVTT\Data\modules\swade-setting-iz3\src"
    
    # English
    en_path = r"d:\Rol\SWADE\IZ3_Setting_Summary_EN.md"
    if os.path.exists(en_path):
        with open(en_path, 'r', encoding='utf-8') as f: en = f.read()
        en_match = re.search(r"## ORIGINS.*?(?=\n## |\Z)", en, re.DOTALL | re.IGNORECASE)
        if en_match:
            en_origins = parse_origins(en_match.group(0), "en")
            for o in en_origins:
                save_origin_json(o, os.path.join(root, "en", "origins"))
            
    # Spanish
    es_full_path = r"d:\Rol\SWADE\SWIZ-01-Interface-Zero-3-digital-whkhpj.md"
    if os.path.exists(es_full_path):
        with open(es_full_path, 'r', encoding='utf-8') as f: es = f.read()
        es_match = re.search(r"\*\*TRASFONDOS\*\*.*?(?=\*\*SUMARIO DE TRASFONDOS\*\*|\Z)", es, re.DOTALL | re.IGNORECASE)
        if es_match:
            es_origins = parse_origins(es_match.group(0), "es")
            for o in es_origins:
                save_origin_json(o, os.path.join(root, "es", "origins"))

if __name__ == "__main__":
    main()
