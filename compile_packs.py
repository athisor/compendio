"""
Script de compilación mejorado para compendios de Foundry VTT V13+
Separa completamente el código fuente del código compilado para evitar conflictos con Git.

Flujo:
1. Compila desde src/packs/ a dist/packs/ (usando CLI de Foundry)
2. Copia los archivos compilados al módulo de Foundry
3. Mantiene src/ limpio y sincronizable con Git
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

# Lista de packs a compilar (debe coincidir con module.json)
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

def check_foundry_cli():
    """Verifica que la CLI de Foundry esté instalada"""
    import platform
    try:
        # En Windows, intentar fvtt.cmd primero
        if platform.system() == "Windows":
            try:
                result = subprocess.run(
                    ["fvtt.cmd", "--version"],
                    capture_output=True,
                    text=True,
                    check=True
                )
            except FileNotFoundError:
                # Fallback a fvtt normal
                result = subprocess.run(
                    ["fvtt", "--version"],
                    capture_output=True,
                    text=True,
                    check=True
                )
        else:
            result = subprocess.run(
                ["fvtt", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
        print(f"[OK] Foundry CLI encontrada: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[ERROR] Foundry CLI (fvtt) no encontrada.")
        print("  Instala con: npm install -g @foundryvtt/foundryvtt-cli")
        return False

def check_foundry_closed():
    """Verifica que Foundry VTT esté cerrado"""
    import psutil
    foundry_processes = [
        p for p in psutil.process_iter(['name'])
        if 'foundry' in p.info['name'].lower() or 'electron' in p.info['name'].lower()
    ]
    if foundry_processes:
        print("[WARN] ADVERTENCIA: Parece que Foundry VTT está abierto.")
        print("  Cierra Foundry completamente antes de compilar.")
        response = input("  ¿Continuar de todos modos? (s/N): ")
        if response.lower() != 's':
            return False
    return True

def prepare_source_for_cli(pack_name):
    """
    Prepara los archivos fuente para la CLI de Foundry.
    La CLI espera los JSONs en una subcarpeta _source dentro del pack.
    """
    src_pack_dir = SRC_DIR / pack_name
    temp_pack_dir = DIST_DIR / pack_name
    
    if not src_pack_dir.exists():
        print(f"[WARN] Pack fuente no encontrado: {src_pack_dir}")
        return False
    
    # Crear estructura temporal con _source
    temp_source_dir = temp_pack_dir / "_source"
    temp_source_dir.mkdir(parents=True, exist_ok=True)
    
    # Copiar JSONs a _source
    json_files = list(src_pack_dir.glob("*.json"))
    if not json_files:
        print(f"[WARN] No hay archivos JSON en {src_pack_dir}")
        return False
    
    for json_file in json_files:
        shutil.copy2(json_file, temp_source_dir / json_file.name)
    
        print(f"  [OK] Preparados {len(json_files)} archivos JSON para {pack_name}")
    return True

def compile_pack_with_cli(pack_name):
    """
    Compila un pack usando la CLI de Foundry.
    Usa el modo 'workon' para trabajar directamente con la carpeta.
    """
    pack_dir = DIST_DIR / pack_name
    
    if not pack_dir.exists():
        print(f"✗ Carpeta de pack no encontrada: {pack_dir}")
        return False
    
    try:
        # En Windows, usar fvtt.cmd o shell=True
        import platform
        if platform.system() == "Windows":
            try:
                cmd = [
                    "fvtt.cmd", "package", "pack",
                    "--in", str(pack_dir),
                    "--out", str(pack_dir)
                ]
            except:
                cmd = [
                    "fvtt", "package", "pack",
                    "--in", str(pack_dir),
                    "--out", str(pack_dir)
                ]
        else:
            cmd = [
                "fvtt", "package", "pack",
                "--in", str(pack_dir),
                "--out", str(pack_dir)
            ]
        
        print(f"  Ejecutando: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True
        )
        
        print(f"  [OK] Compilado exitosamente: {pack_name}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error al compilar {pack_name}:")
        print(f"  {e.stderr}")
        return False

def copy_to_foundry(pack_name):
    """
    Copia los archivos compilados al módulo de Foundry.
    Solo copia los archivos LevelDB (.ldb, .log, etc.), no los JSONs fuente.
    """
    dist_pack_dir = DIST_DIR / pack_name
    foundry_pack_dir = FOUNDRY_PACKS_DIR / pack_name
    
    if not dist_pack_dir.exists():
        print(f"[ERROR] Carpeta de distribución no encontrada: {dist_pack_dir}")
        return False
    
    # Crear carpeta de destino si no existe
    foundry_pack_dir.mkdir(parents=True, exist_ok=True)
    
    # Limpiar carpeta de destino (excepto _source si existe)
    for item in foundry_pack_dir.iterdir():
        if item.name != "_source":
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
    
    # Copiar archivos compilados (LevelDB)
    copied = 0
    for item in dist_pack_dir.iterdir():
        if item.name == "_source":
            continue  # No copiar la carpeta fuente
        
        if item.is_file():
            shutil.copy2(item, foundry_pack_dir / item.name)
            copied += 1
        elif item.is_dir() and item.name != "_source":
            shutil.copytree(item, foundry_pack_dir / item.name, dirs_exist_ok=True)
            copied += 1
    
    print(f"  [OK] Copiados {copied} archivos a Foundry para {pack_name}")
    return True

def cleanup_temp_files():
    """Limpia archivos temporales después de la compilación"""
    # Eliminar carpetas _source temporales de dist/
    for pack_dir in DIST_DIR.iterdir():
        if pack_dir.is_dir():
            source_dir = pack_dir / "_source"
            if source_dir.exists():
                shutil.rmtree(source_dir)
                print(f"  [OK] Limpiado {source_dir}")

def main():
    print("=" * 60)
    print("Compilador de Compendios - Foundry VTT V13+")
    print("=" * 60)
    print()
    
    # Verificaciones previas
    if not check_foundry_cli():
        sys.exit(1)
    
    # Verificar que Foundry esté cerrado (opcional, requiere psutil)
    try:
        if not check_foundry_closed():
            sys.exit(1)
    except ImportError:
        print("[INFO] psutil no instalado, omitiendo verificación de procesos")
        print("  Instala con: pip install psutil")
    
    # Crear directorios necesarios
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    FOUNDRY_PACKS_DIR.mkdir(parents=True, exist_ok=True)
    
    print()
    print("Iniciando compilación...")
    print()
    
    success_count = 0
    failed_packs = []
    
    for pack in PACKS:
        print(f"[{pack}]")
        
        # Paso 1: Preparar fuente
        if not prepare_source_for_cli(pack):
            failed_packs.append(pack)
            continue
        
        # Paso 2: Compilar con CLI
        if not compile_pack_with_cli(pack):
            failed_packs.append(pack)
            continue
        
        # Paso 3: Copiar a Foundry
        if not copy_to_foundry(pack):
            failed_packs.append(pack)
            continue
        
        success_count += 1
        print()
    
    # Limpieza
    print("Limpiando archivos temporales...")
    cleanup_temp_files()
    
    # Resumen
    print()
    print("=" * 60)
    print("Resumen de compilación")
    print("=" * 60)
    print(f"[OK] Packs compilados exitosamente: {success_count}/{len(PACKS)}")
    
    if failed_packs:
        print(f"[ERROR] Packs con errores: {', '.join(failed_packs)}")
        sys.exit(1)
    else:
        print("[OK] ¡Compilación completada exitosamente!")
        print()
        print("Próximos pasos:")
        print("1. Abre Foundry VTT")
        print("2. Activa el módulo 'swade-setting-iz3'")
        print("3. Verifica que los compendios aparezcan correctamente")

if __name__ == "__main__":
    main()
