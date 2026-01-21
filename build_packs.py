import os
import shutil
import json

def build_packs():
    base_dir = r"d:\Rol\FoundryVTT\Data\modules\swade-setting-iz3"
    src_dir = os.path.join(base_dir, "src", "packs")
    dist_dir = os.path.join(base_dir, "packs")
    
    packs = [
        "iz3-rules",
        "iz3-ancestries",
        "iz3-origins",
        "iz3-edges",
        "iz3-hindrances",
        "iz3-gear",
        "iz3-hacking",
        "iz3-bestiary"
    ]
    
    print("Building Packs...")
    
    for pack in packs:
        src_pack = os.path.join(src_dir, pack)
        dist_pack = os.path.join(dist_dir, pack)
        
        # 1. Clear dist folder
        if os.path.exists(dist_pack):
            for file in os.listdir(dist_pack):
                file_path = os.path.join(dist_pack, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Error clearing {file_path}: {e}")
        else:
            os.makedirs(dist_pack, exist_ok=True)
            
        # 2. Copy files from src to dist
        # We can implement processing here later (e.g. minification, validation)
        if os.path.exists(src_pack):
            files = [f for f in os.listdir(src_pack) if f.endswith('.json')]
            print(f"Building {pack}: {len(files)} items")
            
            for f in files:
                src_file = os.path.join(src_pack, f)
                dist_file = os.path.join(dist_pack, f)
                
                # Simple copy for now. Could load/dump to validate JSON.
                try:
                    shutil.copy2(src_file, dist_file)
                except Exception as e:
                    print(f"Error copying {f}: {e}")
        else:
            print(f"Warning: Source pack {pack} not found at {src_pack}")

    print("Build complete.")

if __name__ == "__main__":
    build_packs()
