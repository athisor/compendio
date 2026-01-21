# Documentación de Desarrollo de Compendios: Interface Zero 3.0 (SWADE)

Esta guía documenta el flujo de trabajo "Profesional" para Foundry VTT V13+, utilizando LevelDB y la CLI de Foundry.

## 1. Arquitectura del Proyecto

Adoptamos una estrategia de **Fuente (JSON) vs. Distribución (LevelDB)** para permitir el control de versiones y la edición legible por humanos, mientras cumplimos con los estándares de rendimiento de Foundry V13.

### ⚠️ Problema Resuelto: Separación Local/Remoto

**Problema Original**: Trabajar directamente en la carpeta del módulo de Foundry causaba conflictos entre:
- Archivos compilados localmente (LevelDB)
- Archivos sincronizados con Git remoto
- Bloqueos de archivos cuando Foundry está abierto

**Solución**: Separación completa en tres capas:
1. **Repositorio Git** (`src/`): Solo archivos fuente (JSONs) y configuración
2. **Carpeta de Compilación Temporal** (`dist/`): Archivos compilados temporales (NO se sube a Git)
3. **Módulo de Foundry** (`FoundryVTT/Data/modules/...`): Solo recibe archivos compilados finales (NO se sincroniza con Git)

### Estructura de Directorios

```
SWADE/
├── src/
│   └── packs/              # ✅ ARCHIVOS FUENTE (se suben a Git)
│       ├── iz3-edges/
│       │   └── *.json
│       └── iz3-hindrances/
│           └── *.json
├── dist/                    # ⚠️ TEMPORAL (NO se sube a Git)
│   └── packs/               # Carpeta de compilación intermedia
├── .gitignore               # Excluye dist/ y archivos compilados
├── compile_packs.py         # Script de compilación mejorado
└── module.json              # Manifiesto (se sube a Git)

FoundryVTT/Data/modules/swade-setting-iz3/
└── packs/                   # ⚠️ SOLO archivos compilados (NO se sincroniza con Git)
    ├── iz3-edges/
    │   ├── *.ldb           # Archivos LevelDB compilados
    │   └── *.log
    └── ...
```

**Reglas Importantes**:
*   **`src/packs/[pack-name]/`**: Contiene los archivos fuente en formato JSON. **Estos SÍ se suben a Git.**
*   **`dist/packs/[pack-name]/`**: Carpeta temporal para compilación. **NO se sube a Git** (está en `.gitignore`).
*   **`FoundryVTT/Data/modules/.../packs/`**: Contiene los archivos binarios compilados (LevelDB). **NO se sincroniza con Git.**
*   **`module.json`**: El manifiesto que apunta a las carpetas en `packs/`. **SÍ se sube a Git.**

## 2. Requisitos Previos

*   **Node.js**: Instalado en el sistema.
*   **Foundry VTT CLI (`fvtt`)**: `npm install -g @foundryvtt/foundryvtt-cli`
*   **Configuración Inicial**: `fvtt configure set dataPath "d:\Rol\FoundryVTT\Data"`

## 3. Flujo de Trabajo (Workflow) - MEJORADO

### Paso 1: Generación de Contenido (Python)
Ejecutamos scripts de Python para "hidratar" la carpeta `src/packs`.
```powershell
python d:\Rol\SWADE\create_poc.py
```
**Nota**: Asegúrate de que los scripts escriban en `src/packs/`, NO directamente en la carpeta del módulo de Foundry.

### Paso 2: Compilación (Packing) - NUEVO MÉTODO
Usa el script de compilación mejorado que separa fuente de compilados:

```powershell
# Opción 1: Script completo (recomendado)
python d:\Rol\SWADE\compile_packs.py

# Opción 2: Script simplificado (sin dependencias extras)
python d:\Rol\SWADE\compile_packs_simple.py
```

**¿Qué hace el script?**
1. ✅ Lee los JSONs desde `src/packs/`
2. ✅ Crea una estructura temporal en `dist/packs/` con subcarpetas `_source`
3. ✅ Compila usando `fvtt package pack` desde `dist/` a `dist/`
4. ✅ Copia SOLO los archivos compilados (`.ldb`, `.log`) al módulo de Foundry
5. ✅ Limpia los archivos temporales de `dist/`

**Ventajas**:
- ✅ No modifica `src/` (permanece limpio para Git)
- ✅ No trabaja directamente en la carpeta de Foundry (evita bloqueos)
- ✅ Los archivos compilados nunca entran en conflicto con Git

### Paso 3: Despliegue (Git) - MEJORADO
Subimos SOLO los archivos fuente al repositorio:

```powershell
# Verificar qué se va a subir (debe mostrar solo src/ y module.json)
git status

# Agregar solo archivos fuente
git add src/
git add module.json
git add .gitignore

# Commit y push
git commit -m "Update compendiums: [descripción de cambios]"
git push origin main
```

**⚠️ IMPORTANTE**: 
- NO hagas `git add .` sin revisar primero con `git status`
- El `.gitignore` debe excluir `dist/` y las carpetas de Foundry
- Los archivos compilados (LevelDB) NUNCA deben subirse a Git

## 4. Troubleshooting (Errores Críticos & Soluciones)

### Error: "The pack ... is currently in use by Foundry VTT"
**Síntoma**: Al ejecutar `fvtt package pack`, el proceso falla inmediatamente.
**Causa**: Foundry VTT mantiene bloqueados los archivos de base de datos (LevelDB) mientras está abierto.
**Solución**: 
1. **Cierra Foundry VTT completamente**. (Verifica que no esté en la barra de tareas).
2. Ejecuta el comando de empaquetado.

### Error: El Compendio Aparece Vacío (Pero el JSON existe)
**Síntoma**: Has generado nuevos JSONs en `src/packs/`, ejecutaste `compile_packs.py` sin errores, pero al abrir Foundry, el ítem no aparece.
**Causa**: La CLI de Foundry a veces realiza actualizaciones incrementales y no detecta archivos nuevos si la base de datos binaria ya existe, o si los nombres de archivo no coinciden con los IDs.
**Solución: "Build Limpio" (Force Rebuild)**
1. Cierra Foundry completamente.
2. **Borra** los archivos compilados (`.ldb`, `.log`) de la carpeta de destino en Foundry (`FoundryVTT/Data/modules/swade-setting-iz3/packs/[pack-name]/`). **OJO: NO BORRES LA CARPETA `src/`**.
3. Ejecuta `python compile_packs.py` nuevamente. Esto obliga a reconstruir la DB desde cero.

### Error: Conflictos entre Local y Remoto en Git
**Síntoma**: Al hacer `git pull` o `git push`, aparecen conflictos con archivos `.ldb`, `.log`, o carpetas `packs/`.
**Causa**: Los archivos compilados están siendo rastreados por Git, o estás trabajando directamente en la carpeta del módulo de Foundry.
**Solución**:
1. Verifica que `.gitignore` incluya:
   ```
   dist/
   *.ldb
   *.log
   FoundryVTT/Data/modules/*/packs/
   ```
2. Si los archivos ya están en Git, elimínalos del índice:
   ```powershell
   git rm --cached -r dist/
   git rm --cached FoundryVTT/Data/modules/*/packs/
   git commit -m "Remove compiled files from Git"
   ```
3. Usa siempre `compile_packs.py` en lugar de trabajar directamente en la carpeta de Foundry.

### Error: 404 Not Found al Instalar
**Causas**:
1. Repositorio Privado (Debe ser Público).
2. URL Incorrecta (Debe ser `raw.githubusercontent.com`).
3. Rama Incorrecta (Usar `master` en lugar de `main` si esa es la rama por defecto).

### Reglas de Oro para Desarrollo

1. **Separación de Responsabilidades**:
   - ✅ **Solo edita archivos en `src/packs/`** (archivos fuente JSON)
   - ✅ **Usa `compile_packs.py` para compilar** (nunca edites directamente en Foundry)
   - ✅ **Solo sube `src/` y `module.json` a Git** (nunca archivos compilados)

2. **Version Bump**: Siempre incrementa la versión en `module.json` (ej. `1.1.4` -> `1.1.5`) antes de hacer Push. Si no, Foundry no detecta la actualización.

3. **Nombres de Archivo Estrictos**: Los archivos JSON en `src/packs/[pack-name]/` deben seguir el formato `Nombre_ID.json` (ej. `Gun_Fu_1a8cfd60...json`) o simplemente `ID.json`. El `_id` dentro del JSON debe coincidir con el del nombre del archivo.

4. **Flujo de Trabajo Correcto**:
   ```
   Editar JSONs en src/packs/ 
   → Ejecutar compile_packs.py 
   → Verificar en Foundry 
   → Git add src/ module.json 
   → Git commit & push
   ```

5. **Ingeniería Inversa**: Si tienes dudas del formato JSON, crea el ítem en Foundry manualmente, cierra Foundry, y ejecuta `fvtt package unpack --in "ruta/al/pack" --out "./src/packs/[pack-name]"`. Copia ese JSON como plantilla.

6. **Antes de Compilar**: Siempre cierra Foundry VTT completamente. Los archivos LevelDB se bloquean mientras Foundry está abierto.
