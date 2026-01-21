# Documentación de Desarrollo de Compendios: Interface Zero 3.0 (SWADE)

Esta guía documenta el flujo de trabajo "Profesional" para Foundry VTT V13+, utilizando LevelDB y la CLI de Foundry.

## 1. Arquitectura del Proyecto

Adoptamos una estrategia de **Fuente (JSON) vs. Distribución (LevelDB)** para permitir el control de versiones y la edición legible por humanos, mientras cumplimos con los estándares de rendimiento de Foundry V13.

### ⚠️ Problema Crítico Descubierto: La CLI de Foundry NO Funciona

**Problema**: La CLI oficial de Foundry (`fvtt package pack`) crea archivos LevelDB vacíos. Los archivos `.log` tienen 0 bytes y no se insertan datos.

**Evidencia**:
- Packs compilados con `fvtt`: archivos `.log` de 0 bytes, sin archivos `.ldb`
- Packs del sistema SWADE oficial: archivos `.ldb` de 28KB con datos reales
- Error al hacer unpack: `Iterator is not open: cannot call next() after close()`

**Solución**: Usar `classic-level` directamente (como hace el sistema SWADE oficial) en lugar de la CLI de Foundry.

### Estructura de Directorios

```
SWADE/
├── src/
│   └── packs/              # ✅ ARCHIVOS FUENTE (se suben a Git)
│       ├── iz3-edges/
│       │   └── *.json
│       └── iz3-hindrances/
│           └── *.json
├── packs/                   # ✅ ARCHIVOS COMPILADOS (se suben a Git para GitHub)
│   ├── iz3-edges/
│   │   ├── *.ldb           # Archivos LevelDB con datos reales
│   │   └── *.log
│   └── iz3-hindrances/
├── build-packs.js           # ✅ Script de compilación (usa classic-level)
├── package.json             # ✅ Dependencias de Node.js
├── .gitignore               # Excluye node_modules/ y dist/
└── module.json              # Manifiesto (se sube a Git)
```

**Reglas Importantes**:
*   **`src/packs/[pack-name]/`**: Archivos fuente JSON. **SÍ se suben a Git.**
*   **`packs/[pack-name]/`**: Archivos LevelDB compilados. **SÍ se suben a Git** (necesarios para instalación desde GitHub).
*   **`build-packs.js`**: Script Node.js que compila usando `classic-level`.
*   **`module.json`**: Manifiesto que apunta a `packs/`. **SÍ se sube a Git.**

## 2. Requisitos Previos

*   **Node.js**: Instalado en el sistema (v18+ recomendado).
*   **classic-level**: `npm install classic-level`
*   **NO usar**: La CLI de Foundry (`fvtt`) para compilar packs (tiene bugs).

## 3. Flujo de Trabajo (Workflow) - CORREGIDO

### Paso 1: Generación de Contenido (Python o manual)
Crea archivos JSON en `src/packs/[pack-name]/`:

```json
{
    "name": "Nombre del Item",
    "type": "edge",
    "_id": "16caracteres1234",
    "img": "icons/svg/item-bag.svg",
    "system": {
        "description": "<p>Descripción del item.</p>",
        "source": "Interface Zero 3.0",
        "requirements": "",
        "actions": {},
        "isArcaneBackground": false
    },
    "effects": [],
    "flags": {},
    "_stats": {
        "systemId": "swade",
        "systemVersion": "4.1.0",
        "coreVersion": "13.341"
    }
}
```

### Paso 2: Compilación (Node.js con classic-level)

```powershell
cd D:\Rol\SWADE
node build-packs.js
```

**¿Qué hace el script?**
1. ✅ Lee los JSONs desde `src/packs/`
2. ✅ Crea bases de datos LevelDB en `packs/` usando `classic-level`
3. ✅ Inserta los documentos con las claves correctas (`!items!<id>`)
4. ✅ Genera archivos `.ldb` con datos reales

### Paso 3: Despliegue (Git)

```powershell
git add packs/ src/ module.json build-packs.js package.json
git commit -m "Update compendiums"
git push origin main
```

**Nota**: Los archivos compilados (`packs/`) SÍ se suben a Git porque son necesarios para la instalación desde GitHub.

## 4. Troubleshooting (Errores Críticos & Soluciones)

### Error: "Compendium containing 0 entries"
**Síntoma**: Foundry muestra "Constructed index of ... containing 0 entries".
**Causa**: Los archivos LevelDB están vacíos (compilados con la CLI de Foundry).
**Solución**:
1. Usa `node build-packs.js` en lugar de `fvtt package pack`.
2. Verifica que los archivos `.log` tengan más de 0 bytes.
3. Verifica que existan archivos `.ldb`.

### Error: "Iterator is not open: cannot call next() after close()"
**Síntoma**: Al hacer `fvtt package unpack`, aparece este error.
**Causa**: La base de datos LevelDB está corrupta o vacía.
**Solución**: Recompila con `node build-packs.js`.

### Error: "The pack ... is currently in use by Foundry VTT"
**Síntoma**: Al compilar, el proceso falla.
**Causa**: Foundry VTT tiene los archivos bloqueados.
**Solución**: Cierra Foundry VTT completamente antes de compilar.

### Error: 404 Not Found al Instalar
**Causas**:
1. Repositorio Privado (Debe ser Público).
2. URL Incorrecta (Debe ser `raw.githubusercontent.com`).
3. Rama Incorrecta (Usar `main` si esa es la rama por defecto).

## 5. Comparación: CLI de Foundry vs classic-level

| Aspecto | CLI de Foundry (`fvtt`) | classic-level directo |
|---------|-------------------------|----------------------|
| **Resultado** | ❌ LevelDB vacío | ✅ LevelDB con datos |
| **Archivos .ldb** | ❌ No se crean | ✅ Se crean con datos |
| **Archivos .log** | ❌ 0 bytes | ✅ Con contenido |
| **Usado por SWADE oficial** | ❌ No | ✅ Sí |
| **Documentación** | ✅ Oficial | ⚠️ Requiere código |

## 6. Reglas de Oro para Desarrollo

1. **NO usar la CLI de Foundry** para compilar packs. Usar `node build-packs.js`.

2. **Formato de JSON correcto**:
   - `_id`: 16 caracteres alfanuméricos
   - `type`: `edge`, `hindrance`, `power`, `skill`, etc.
   - `system`: Objeto con datos específicos del sistema SWADE
   - `effects`: Array (puede estar vacío)

3. **Claves LevelDB**:
   - Items: `!items!<id>`
   - Actors: `!actors!<id>`
   - Journals: `!journal!<id>`

4. **Flujo de Trabajo Correcto**:
   ```
   Editar JSONs en src/packs/ 
   → Ejecutar node build-packs.js 
   → Verificar en Foundry 
   → Git add packs/ src/ module.json 
   → Git commit & push
   ```

5. **Ingeniería Inversa**: Para obtener el formato JSON correcto:
   - Crea el ítem manualmente en Foundry
   - Exporta desde el compendio
   - Usa ese JSON como plantilla

## 7. Link de Instalación

```
https://raw.githubusercontent.com/athisor/compendio/main/module.json
```

Para instalar en Foundry VTT:
1. Configuración → Add-on Modules → Install Module
2. Pega la URL del manifest
3. Install
4. Activa el módulo en tu mundo
