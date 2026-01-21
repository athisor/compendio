"""
Script para preparar el módulo para distribución en GitHub.
Copia los archivos compilados y configura la estructura para instalación.
"""

import os
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).parent.resolve()
FOUNDRY_MODULE_DIR = Path(r"d:\Rol\FoundryVTT\Data\modules\swade-setting-iz3")
RELEASE_DIR = REPO_ROOT / "release"

def prepare_release():
    """Prepara la estructura de release para GitHub"""
    print("Preparando release para GitHub...")
    
    # Crear directorio de release
    if RELEASE_DIR.exists():
        shutil.rmtree(RELEASE_DIR)
    RELEASE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Copiar module.json
    if (REPO_ROOT / "module.json").exists():
        shutil.copy2(REPO_ROOT / "module.json", RELEASE_DIR / "module.json")
        print("[OK] Copiado module.json")
    
    # Copiar README.md
    if (REPO_ROOT / "README.md").exists():
        shutil.copy2(REPO_ROOT / "README.md", RELEASE_DIR / "README.md")
        print("[OK] Copiado README.md")
    
    # Crear carpeta packs
    release_packs_dir = RELEASE_DIR / "packs"
    release_packs_dir.mkdir(exist_ok=True)
    
    # Copiar packs compilados desde Foundry
    foundry_packs_dir = FOUNDRY_MODULE_DIR / "packs"
    
    if foundry_packs_dir.exists():
        packs_copied = 0
        for pack_dir in foundry_packs_dir.iterdir():
            if pack_dir.is_dir():
                # Copiar solo si tiene archivos compilados (no _source)
                has_compiled_files = False
                for item in pack_dir.iterdir():
                    if item.name != "_source" and (item.is_file() or item.is_dir()):
                        has_compiled_files = True
                        break
                
                if has_compiled_files:
                    dest_pack = release_packs_dir / pack_dir.name
                    if dest_pack.exists():
                        shutil.rmtree(dest_pack)
                    shutil.copytree(pack_dir, dest_pack)
                    # Eliminar _source si existe
                    source_dir = dest_pack / "_source"
                    if source_dir.exists():
                        shutil.rmtree(source_dir)
                    packs_copied += 1
                    print(f"[OK] Copiado pack: {pack_dir.name}")
        
        print(f"[OK] Total packs copiados: {packs_copied}")
    else:
        print(f"[WARN] No se encontró {foundry_packs_dir}")
    
    print("\n[OK] Release preparado en: release/")
    print("\nPróximos pasos:")
    print("1. Revisa y actualiza las URLs en module.json con tu usuario de GitHub")
    print("2. Inicializa Git: git init")
    print("3. Agrega archivos: git add release/ module.json README.md .gitignore")
    print("4. Commit: git commit -m 'Initial release'")
    print("5. Crea repositorio en GitHub y conecta: git remote add origin [URL]")
    print("6. Push: git push -u origin main")

if __name__ == "__main__":
    prepare_release()
