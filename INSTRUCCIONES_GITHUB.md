# ✅ Módulo Compilado y Listo para GitHub

## Estado Actual

✅ **Compilación completada**: 2 packs compilados (iz3-edges, iz3-hindrances)  
✅ **Release preparado**: Carpeta `release/` lista  
✅ **Git inicializado**: Repositorio local creado  
✅ **Commit inicial**: Creado con todos los archivos  

## Próximos Pasos para Subir a GitHub

### Paso 1: Crear Repositorio en GitHub

1. Ve a https://github.com/new
2. **Nombre del repositorio**: `swade-setting-iz3`
3. **Descripción**: "Compendios de Interface Zero 3.0 para SWADE en Foundry VTT"
4. **IMPORTANTE**: Marca como **Público** (necesario para instalación)
5. **NO** marques ninguna opción adicional (README, .gitignore, license)
6. Haz clic en **"Create repository"**

### Paso 2: Actualizar module.json con tu Usuario de GitHub

Abre `module.json` y `release/module.json` y reemplaza `TU_USUARIO` con tu usuario real:

**Línea 119**: 
```json
"url": "https://github.com/TU_USUARIO/swade-setting-iz3",
```

**Línea 120**:
```json
"manifest": "https://raw.githubusercontent.com/TU_USUARIO/swade-setting-iz3/main/module.json",
```

**Línea 121**:
```json
"download": "https://github.com/TU_USUARIO/swade-setting-iz3/archive/refs/heads/main.zip"
```

### Paso 3: Conectar y Subir a GitHub

Ejecuta estos comandos (reemplaza `TU_USUARIO` con tu usuario):

```powershell
cd D:\Rol\SWADE

# Conectar con GitHub
git remote add origin https://github.com/TU_USUARIO/swade-setting-iz3.git

# Cambiar a rama main
git branch -M main

# Subir
git push -u origin main
```

Si te pide autenticación, usa un Personal Access Token (no tu contraseña):
- Ve a https://github.com/settings/tokens
- Crea un token con permisos `repo`
- Úsalo como contraseña

### Paso 4: Verificar Instalación

Una vez subido, tu link de instalación será:

```
https://raw.githubusercontent.com/TU_USUARIO/swade-setting-iz3/main/module.json
```

**Para instalar en Foundry VTT:**

1. Abre Foundry VTT
2. Ve a **Configuración** → **Add-on Modules** → **Install Module**
3. Pega la URL del manifest (la de arriba, reemplazando TU_USUARIO)
4. Haz clic en **Install**
5. Activa el módulo en tu mundo de juego

## Estructura del Repositorio

```
swade-setting-iz3/
├── module.json              # Manifiesto principal
├── README.md                # Documentación
├── release/                 # Archivos para distribución
│   ├── module.json          # Manifiesto (este es el que Foundry lee)
│   └── packs/               # Packs compilados (LevelDB)
│       ├── iz3-edges/
│       └── iz3-hindrances/
├── src/                     # Código fuente (JSONs editables)
│   └── packs/
└── compile_packs*.py        # Scripts de compilación
```

## Comandos Útiles

### Actualizar después de cambios:

```powershell
# 1. Compilar
python compile_packs_simple.py

# 2. Preparar release
python prepare_release.py

# 3. Actualizar versión en module.json (ej: 1.0.0 → 1.0.1)

# 4. Commit y push
git add .
git commit -m "Update to v1.0.1"
git push
```

## Notas Importantes

- ⚠️ El repositorio **DEBE ser público** para que Foundry pueda instalarlo
- ⚠️ El `module.json` en `release/` es el que Foundry lee, asegúrate de actualizarlo también
- ✅ Los archivos compilados (LevelDB) están en `release/packs/`
- ✅ Los archivos fuente (JSON) están en `src/packs/` y se suben a Git para control de versiones

## Solución de Problemas

### Error: "Repository not found"
- Verifica que el repositorio sea público
- Verifica que el nombre del repositorio coincida exactamente

### Error: "404 Not Found" al instalar
- Verifica que la URL del manifest sea correcta
- Asegúrate de que la rama sea `main` (no `master`)
- Verifica que `release/module.json` exista en el repositorio

### El módulo no aparece en Foundry
- Verifica que el sistema SWADE esté instalado
- Verifica la compatibilidad de versiones en `module.json`
- Revisa la consola de Foundry (F12) para errores
