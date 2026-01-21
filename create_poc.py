import os
import json
import uuid

# Configuration
MODULE_ID = "iz3v2"
SRC_BASE = r"d:\Rol\FoundryVTT\Data\modules\iz3v2\packs"

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_swade_item(item_data):
    # Use 16-char ID similar to Foundry
    item_id = str(uuid.uuid4().hex)[:16]
    folder_name = item_data["folder"]
    
    # Construct "System" data matching SWADE 5.1.1 structure (Reverse Engineered)
    system_data = {
        "description": item_data["system"]["description"],
        "notes": "",
        "requirements": item_data["system"]["requirements_structured"], # Use structured list
        "source": "Interface Zero 3.0 PoC",
        "swid": item_data["name"].lower().replace(" ", ""), # Guessing
        "isArcaneBackground": False,
        "actions": {},
        "category": item_data["system"]["category"] # e.g. "Combat"
    }

    final_data = {
        "name": item_data["name"],
        "type": item_data["type"],
        "_id": item_id,
        "img": item_data["img"],
        "system": system_data,
        "effects": [],
        "flags": {
             "core": {
                "sourceId": f"Compendium.{MODULE_ID}.{folder_name}.{item_id}"
             }
        },
        "_stats": {
            "systemId": "swade",
            "systemVersion": "5.1.1", # Matches what we saw
            "coreVersion": "13.351"
        }
    }
    return final_data

def main():
    print("Generating PoC Data...")

    # Define Content: Gun Fu!
    # Requirements: Novice, Martial Artist, Fighting d6+, Shooting d6+
    poc_edge = {
        "name": "Gun Fu!",
        "type": "edge",
        "folder": "iz3-edges",
        "img": "icons/svg/target.svg",
        "system": {
            "description": "<p>Heavily trained in close quarters gunplay, you know gun fu. When using pistols against a target’s Parry, she has +2 to Shooting and +2 to pistol damage. This benefit only applies to such close range combat, not to attacks from further than adjacent.</p>",
            "category": "Combat",
            # Hardcoded structured requirements for PoC
            "requirements_structured": [
                { "type": "rank", "value": 0, "combinator": "and" }, # Novice
                { "type": "edge", "label": "Martial Artist", "combinator": "and" }, # Martial Artist (Placeholder type)
                { "type": "skill", "label": "Fighting", "selector": "fighting", "value": 6, "combinator": "and" }, # d6
                { "type": "skill", "label": "Shooting", "selector": "shooting", "value": 6, "combinator": "and" }  # d6
            ] 
        }
    }

    # Generate
    for item in [poc_edge]: 
        folder_path = os.path.join(SRC_BASE, item["folder"], "_source")
        ensure_dir(folder_path)
        
        json_content = create_swade_item(item)
        
        # KEY FIX: Filename format Name_ID.json (Sanitized)
        safe_name = item['name'].replace(' ', '_').replace('!', '').replace('(', '').replace(')', '')
        file_name = f"{safe_name}_{json_content['_id']}.json"
        
        file_path = os.path.join(folder_path, file_name)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(json_content, f, indent=2, ensure_ascii=False) # indent 2 matches example
        
        print(f"Created {file_path}")

    print("\nPoC Generation Complete. Run 'fvtt package pack swade-setting-iz3' to compile.")

if __name__ == "__main__":
    main()
