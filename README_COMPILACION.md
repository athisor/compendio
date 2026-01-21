# 🔧 Solución al Problema de Conflictos Local/Remoto

## Problema Identificado

Trabajar directamente en la carpeta del módulo de Foundry (`FoundryVTT/Data/modules/swade-setting-iz3`) causaba conflictos entre:
- ✅ Archivos compilados localmente (LevelDB)
- ✅ Archivos sincronizados con Git remoto
- ✅ Bloqueos de archivos cuando Foundry está abierto

## Solución Implementada

Separación completa en **tres capas**:

1. **`src/packs/`** → Archivos fuente (JSON) → ✅ Se sube a Git
2. **`dist/packs/`** → Compilación temporal → ❌ NO se sube a Git
3. **`FoundryVTT/Data/modules/.../packs/`** → Archivos compilados finales → ❌ NO se sincroniza con Git

## Uso Rápido

### 1. Editar Contenido
Edita o genera archivos JSON en `src/packs/[pack-name]/`:
```powershell
python create_poc.py
```

### 2. Compilar
Ejecuta el script de compilación:
```powershell
# Opción recomendada (con verificaciones)
python compile_packs.py

# Opción simple (sin dependencias extras)
python compile_packs_simple.py
```

El script automáticamente:
- ✅ Compila desde `src/` a `dist/`
- ✅ Copia archivos compilados a Foundry
- ✅ Limpia archivos temporales

### 3. Verificar en Foundry
1. Abre Foundry VTT
2. Activa el módulo `swade-setting-iz3`
3. Verifica que los compendios aparezcan correctamente

### 4. Subir a Git
```powershell
git status                    # Verifica que solo aparezcan src/ y module.json
git add src/ module.json
git commit -m "Update compendiums"
git push origin main
```

## Archivos Importantes

- **`.gitignore`**: Excluye `dist/` y archivos compilados
- **`compile_packs.py`**: Script de compilación completo
- **`compile_packs_simple.py`**: Versión simplificada sin dependencias

## Estructura de Carpetas

```
SWADE/
├── src/packs/           ← ✅ EDITA AQUÍ (se sube a Git)
│   ├── iz3-edges/
│   └── iz3-hindrances/
├── dist/packs/          ← ⚠️ Temporal (NO se sube a Git)
├── .gitignore           ← ✅ Configuración Git
├── compile_packs.py     ← ✅ Script de compilación
└── module.json          ← ✅ Manifiesto (se sube a Git)

FoundryVTT/Data/modules/swade-setting-iz3/
└── packs/               ← ⚠️ Solo archivos compilados (NO se sincroniza)
```

## Reglas de Oro

1. ✅ **Solo edita** archivos en `src/packs/`
2. ✅ **Solo sube** `src/` y `module.json` a Git
3. ✅ **Cierra Foundry** antes de compilar
4. ✅ **Usa `compile_packs.py`** en lugar de trabajar directamente en Foundry

## Troubleshooting

### Error: "The pack ... is currently in use"
**Solución**: Cierra Foundry VTT completamente antes de compilar.

### Error: Conflictos en Git con archivos `.ldb`
**Solución**: Verifica que `.gitignore` incluya `dist/` y `*.ldb`. Si ya están en Git:
```powershell
git rm --cached -r dist/
git commit -m "Remove compiled files"
```

### Error: El compendio aparece vacío
**Solución**: Borra los archivos compilados en Foundry y recompila:
```powershell
# Borra manualmente los .ldb y .log en FoundryVTT/Data/modules/swade-setting-iz3/packs/[pack-name]/
python compile_packs.py
```

## Documentación Completa

Ver `documentacion-compendios.md` para detalles completos del flujo de trabajo.
