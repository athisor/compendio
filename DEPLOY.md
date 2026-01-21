# Guía de Despliegue a GitHub

## Pasos para Subir el Módulo a GitHub

### 1. Preparar Release
```powershell
python prepare_release.py
```

### 2. Configurar Git y GitHub

Ejecuta el script interactivo:
```powershell
python setup_github.py
```

O sigue estos pasos manualmente:

#### 2.1. Inicializar Git
```powershell
git init
```

#### 2.2. Actualizar module.json
Abre `module.json` y reemplaza `TU_USUARIO` con tu nombre de usuario de GitHub en estas líneas:
- `"url": "https://github.com/TU_USUARIO/swade-setting-iz3"`
- `"manifest": "https://raw.githubusercontent.com/TU_USUARIO/swade-setting-iz3/main/module.json"`
- `"download": "https://github.com/TU_USUARIO/swade-setting-iz3/archive/refs/heads/main.zip"`

#### 2.3. Agregar archivos
```powershell
git add .gitignore
git add module.json
git add README.md
git add release/
git add src/
git add compile_packs*.py
git add prepare_release.py
git add documentacion-compendios.md
git add README_COMPILACION.md
```

#### 2.4. Commit inicial
```powershell
git commit -m "Initial release: Interface Zero 3.0 Compendiums"
```

### 3. Crear Repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre del repositorio: `swade-setting-iz3`
3. Descripción: "Compendios de Interface Zero 3.0 para SWADE en Foundry VTT"
4. **IMPORTANTE**: Marca como **Público** (necesario para que Foundry pueda instalarlo)
5. **NO** marques "Add a README file", "Add .gitignore", ni "Choose a license"
6. Haz clic en "Create repository"

### 4. Conectar y Subir

```powershell
git remote add origin https://github.com/TU_USUARIO/swade-setting-iz3.git
git branch -M main
git push -u origin main
```

**Nota**: Reemplaza `TU_USUARIO` con tu usuario de GitHub.

### 5. Verificar Instalación

Una vez subido, el link de instalación será:

```
https://raw.githubusercontent.com/TU_USUARIO/swade-setting-iz3/main/module.json
```

Para instalar en Foundry VTT:
1. Abre Foundry VTT
2. Ve a **Configuración** → **Add-on Modules** → **Install Module**
3. Pega la URL del manifest
4. Haz clic en **Install**

## Actualizaciones Futuras

Para actualizar el módulo:

1. **Compilar cambios**:
   ```powershell
   python compile_packs_simple.py
   ```

2. **Preparar release**:
   ```powershell
   python prepare_release.py
   ```

3. **Actualizar versión en module.json**:
   - Incrementa el número de versión (ej: `1.0.0` → `1.0.1`)

4. **Commit y push**:
   ```powershell
   git add .
   git commit -m "Update to v1.0.1"
   git push
   ```

## Estructura del Repositorio

```
swade-setting-iz3/
├── module.json          # Manifiesto del módulo (instalable)
├── README.md            # Documentación principal
├── .gitignore           # Excluye archivos compilados
├── release/             # Archivos compilados para distribución
│   ├── module.json
│   └── packs/           # Packs compilados (LevelDB)
├── src/                 # Código fuente (JSONs editables)
│   └── packs/
└── compile_packs*.py    # Scripts de compilación
```
