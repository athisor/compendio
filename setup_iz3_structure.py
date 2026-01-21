import os

def create_structure():
    base_dir = r"d:\Rol\FoundryVTT\Data\modules\swade-setting-iz3"
    
    # Packs list matches module.json
    packs = [
        "iz3-rules",       # JournalEntry
        "iz3-ancestries",  # Item
        "iz3-origins",     # Item
        "iz3-edges",       # Item
        "iz3-hindrances",  # Item
        "iz3-gear",        # Item
        "iz3-hacking",     # Item
        "iz3-bestiary"     # Actor
    ]
    
    print(f"Initializing directory structure in: {base_dir}")
    
    # 1. Create src/packs folders (Source data - Individual JSONs)
    src_packs_dir = os.path.join(base_dir, "src", "packs")
    for pack in packs:
        path = os.path.join(src_packs_dir, pack)
        try:
            os.makedirs(path, exist_ok=True)
            print(f"[OK] Source dir: {path}")
        except Exception as e:
            print(f"[ERROR] Creating {path}: {e}")

    # 2. Create packs folders (Distribution data - Foundry read-only folders)
    dist_packs_dir = os.path.join(base_dir, "packs")
    for pack in packs:
        path = os.path.join(dist_packs_dir, pack)
        try:
            os.makedirs(path, exist_ok=True)
            print(f"[OK] Dist dir: {path}")
        except Exception as e:
            print(f"[ERROR] Creating {path}: {e}")
            
    # 3. Verify module.json exists
    module_json = os.path.join(base_dir, "module.json")
    if os.path.exists(module_json):
        print(f"[OK] module.json found at {module_json}")
    else:
        print(f"[WARNING] module.json NOT found at {module_json}")

if __name__ == "__main__":
    create_structure()
