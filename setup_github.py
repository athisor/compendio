"""
Script para configurar Git y preparar para GitHub.
"""

import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parent.resolve()

def run_command(cmd, check=True):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\nEjecutando: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, check=check)
        if result.stdout:
            print(result.stdout)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False
    except FileNotFoundError:
        print("Git no está instalado. Instala Git desde https://git-scm.com/")
        return False

def setup_git():
    """Configura el repositorio Git"""
    print("=" * 60)
    print("Configuración de Git para GitHub")
    print("=" * 60)
    
    # Verificar si ya es un repo
    if (REPO_ROOT / ".git").exists():
        print("\n[INFO] Ya existe un repositorio Git")
        response = input("¿Reinicializar? (s/N): ")
        if response.lower() == 's':
            run_command(["git", "init"], check=False)
    else:
        run_command(["git", "init"])
    
    # Configurar .gitignore si no existe
    gitignore = REPO_ROOT / ".gitignore"
    if not gitignore.exists():
        print("\n[ERROR] .gitignore no encontrado. Creando...")
        # El .gitignore ya debería existir, pero por si acaso
        return False
    
    # Agregar archivos
    print("\nAgregando archivos a Git...")
    run_command(["git", "add", ".gitignore"])
    run_command(["git", "add", "module.json"])
    run_command(["git", "add", "README.md"])
    run_command(["git", "add", "release/"])
    run_command(["git", "add", "src/"])
    run_command(["git", "add", "compile_packs*.py"])
    run_command(["git", "add", "prepare_release.py"])
    run_command(["git", "add", "documentacion-compendios.md"])
    run_command(["git", "add", "README_COMPILACION.md"])
    
    # Commit inicial
    print("\nCreando commit inicial...")
    if run_command(["git", "commit", "-m", "Initial release: Interface Zero 3.0 Compendiums"]):
        print("\n[OK] Repositorio Git configurado correctamente")
        return True
    else:
        print("\n[WARN] No se pudo crear el commit (puede que no haya cambios)")
        return False

def print_next_steps(github_user=None):
    """Muestra los próximos pasos"""
    print("\n" + "=" * 60)
    print("PRÓXIMOS PASOS PARA SUBIR A GITHUB")
    print("=" * 60)
    
    print("\n1. Crea un repositorio en GitHub:")
    print("   - Ve a https://github.com/new")
    print("   - Nombre: swade-setting-iz3")
    print("   - Público (para que Foundry pueda instalarlo)")
    print("   - NO inicialices con README, .gitignore o licencia")
    
    if github_user:
        repo_url = f"https://github.com/{github_user}/swade-setting-iz3.git"
    else:
        repo_url = "https://github.com/TU_USUARIO/swade-setting-iz3.git"
        print("\n⚠️ IMPORTANTE: Reemplaza TU_USUARIO con tu nombre de usuario de GitHub")
    
    print(f"\n2. Conecta el repositorio local con GitHub:")
    print(f"   git remote add origin {repo_url}")
    
    print("\n3. Actualiza module.json con tu usuario de GitHub:")
    print("   - Abre module.json")
    print("   - Reemplaza 'TU_USUARIO' con tu usuario de GitHub")
    print("   - Las URLs deben ser:")
    print(f"     - url: https://github.com/{github_user or 'TU_USUARIO'}/swade-setting-iz3")
    print(f"     - manifest: https://raw.githubusercontent.com/{github_user or 'TU_USUARIO'}/swade-setting-iz3/main/module.json")
    print(f"     - download: https://github.com/{github_user or 'TU_USUARIO'}/swade-setting-iz3/archive/refs/heads/main.zip")
    
    print("\n4. Haz commit de los cambios en module.json:")
    print("   git add module.json")
    print("   git commit -m 'Update GitHub URLs'")
    
    print("\n5. Sube a GitHub:")
    print("   git branch -M main")
    print("   git push -u origin main")
    
    print("\n6. Crea un Release en GitHub (opcional pero recomendado):")
    print("   - Ve a tu repositorio en GitHub")
    print("   - Clic en 'Releases' → 'Create a new release'")
    print("   - Tag: v1.0.0")
    print("   - Title: Interface Zero 3.0 Compendiums v1.0.0")
    print("   - Description: Primera versión de los compendios de IZ3")
    
    manifest_url = f"https://raw.githubusercontent.com/{github_user or 'TU_USUARIO'}/swade-setting-iz3/main/module.json"
    print("\n" + "=" * 60)
    print("LINK DE INSTALACIÓN PARA FOUNDRY VTT")
    print("=" * 60)
    print(f"\n{manifest_url}")
    print("\nCopia esta URL y úsala en Foundry VTT:")
    print("Configuración → Add-on Modules → Install Module → Manifest URL")

if __name__ == "__main__":
    print("¿Cuál es tu nombre de usuario de GitHub?")
    print("(Déjalo vacío si aún no lo sabes, puedes actualizarlo después)")
    github_user = input("Usuario: ").strip()
    
    if setup_git():
        print_next_steps(github_user if github_user else None)
    else:
        print("\n[ERROR] No se pudo configurar Git completamente")
        print("Revisa los mensajes de error arriba")
