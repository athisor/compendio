"""
Versión simplificada del compilador (sin dependencias externas).
Usa directamente fvtt package pack con la estructura esperada.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# Configuración
REPO_ROOT = Path(__file__).parent.resolve()
SRC_DIR = REPO_ROOT / "src" / "packs"
DIST_DIR = REPO_ROOT / "dist" / "packs"
FOUNDRY_MODULE_DIR = Path(r"d:\Rol\FoundryVTT\Data\modules\swade-setting-iz3")
FOUNDRY_PACKS_DIR = FOUNDRY_MODULE_DIR / "packs"

PACKS = [
    "iz3-rules",
    "iz3-ancestries",
    "iz3-origins",
    "iz3-edges",
    "iz3-hindrances",
    "iz3-gear",
    "iz3-hacking",
    "iz3-bestiary"
]

def compile_pack(pack_name):
    """Compila un pack individual"""
    src_pack = SRC_DIR / pack_name
    dist_pack = DIST_DIR / pack_name
    foundry_pack = FOUNDRY_PACKS_DIR / pack_name
    
    if not src_pack.exists():
        print(f"[WARN] Pack fuente no encontrado: {src_pack}")
        return False
    
    # Crear estructura temporal
    dist_pack.mkdir(parents=True, exist_ok=True)
    source_dir = dist_pack / "_source"
    source_dir.mkdir(parents=True, exist_ok=True)
    
    # Copiar JSONs a _source
    json_files = list(src_pack.glob("*.json"))
    if not json_files:
        print(f"[WARN] No hay archivos JSON en {src_pack}")
        return False
    
    for json_file in json_files:
        shutil.copy2(json_file, source_dir / json_file.name)
    
    print(f"  [{pack_name}] Preparados {len(json_files)} archivos")
    
    # Compilar con CLI
    # La CLI necesita el nombre del compendio y busca archivos en _source/
    try:
        import platform
        # Usar -n para el nombre del compendio y -r para recursivo
        # La CLI buscará archivos en _source/ dentro del directorio de entrada
        if platform.system() == "Windows":
            cmd = [
                "fvtt.cmd", "package", "pack",
                "-n", pack_name,
                "--in", str(dist_pack),
                "--out", str(dist_pack),
                "-r"  # Recursivo para buscar en _source/
            ]
        else:
            cmd = [
                "fvtt", "package", "pack",
                "-n", pack_name,
                "--in", str(dist_pack),
                "--out", str(dist_pack),
                "-r"
            ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, shell=False)
        print(f"  [{pack_name}] [OK] Compilado")
    except subprocess.CalledProcessError as e:
        print(f"  [{pack_name}] [ERROR] Error: {e.stderr}")
        if e.stdout:
            print(f"  [{pack_name}] Salida: {e.stdout}")
        return False
    except FileNotFoundError:
        # Intentar con shell=True como fallback
        try:
            cmd_str = f'fvtt.cmd package pack -n "{pack_name}" --in "{dist_pack}" --out "{dist_pack}" -r'
            result = subprocess.run(cmd_str, shell=True, capture_output=True, text=True, check=True)
            print(f"  [{pack_name}] [OK] Compilado")
        except subprocess.CalledProcessError as e:
            print(f"  [{pack_name}] [ERROR] Error: {e.stderr}")
            return False
    
    # Copiar a Foundry (solo archivos compilados)
    foundry_pack.mkdir(parents=True, exist_ok=True)
    
    # Limpiar destino
    for item in foundry_pack.iterdir():
        if item.name != "_source":
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
    
    # Copiar archivos compilados
    copied = 0
    for item in dist_pack.iterdir():
        if item.name != "_source":
            if item.is_file():
                shutil.copy2(item, foundry_pack / item.name)
                copied += 1
            elif item.is_dir():
                shutil.copytree(item, foundry_pack / item.name, dirs_exist_ok=True)
                copied += 1
    
    print(f"  [{pack_name}] [OK] Copiado a Foundry ({copied} archivos)")
    
    # Limpiar temporal
    if source_dir.exists():
        shutil.rmtree(source_dir)
    
    return True

def main():
    print("Compilador de Compendios (Versión Simple)")
    print("=" * 50)
    
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    FOUNDRY_PACKS_DIR.mkdir(parents=True, exist_ok=True)
    
    success = 0
    failed = []
    
    for pack in PACKS:
        if compile_pack(pack):
            success += 1
        else:
            failed.append(pack)
        print()
    
    print("=" * 50)
    print(f"Completado: {success}/{len(PACKS)} packs")
    if failed:
        print(f"Errores: {', '.join(failed)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
