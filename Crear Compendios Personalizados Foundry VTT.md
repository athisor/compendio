# **Informe Técnico: Arquitectura, Desarrollo y Despliegue de Compendios Modulares para Savage Worlds en Foundry VTT V13**

## **1\. Resumen Ejecutivo y Alcance del Análisis**

La gestión de contenido en entornos de rol virtual (VTT) ha trascendido el almacenamiento local para convertirse en una disciplina de ingeniería de datos, especialmente con la llegada de la Versión 13 (V13) de Foundry VTT. Este informe aborda la solicitud técnica de diseñar, implementar y distribuir compendios personalizados ("Shared Compendiums") para el sistema *Savage Worlds Adventure Edition* (SWADE). El objetivo es proporcionar una documentación exhaustiva que sirva tanto de guía de implementación como de referencia arquitectónica para la creación de un repositorio modelo.

El análisis se centra en la transición estructural de los datos en V13, el uso de la API de paquetes para garantizar la modularidad, y las especificidades del sistema SWADE (como la gestión de *Edges*, *Hindrances* y *Powers*). Se examina la necesidad crítica de desacoplar el contenido del "Mundo" de juego para encapsularlo en "Módulos" transferibles, permitiendo que un Director de Juego (DJ) mantenga una biblioteca persistente de activos a través de múltiples campañas y actualizaciones del software núcleo.1

Se desglosa la anatomía de un repositorio de GitHub ideal que funcione como un *Add-on* instalable, detallando la configuración del manifiesto module.json bajo los estrictos estándares de validación de V13, y se exploran las herramientas de línea de comandos (CLI) necesarias para la compilación de bases de datos LevelDB, el estándar de almacenamiento actual de Foundry.3

## ---

**2\. Arquitectura de Datos en Foundry VTT V13**

Para comprender cómo crear un compendio personalizado que funcione como un módulo independiente, es imperativo analizar primero cómo Foundry VTT gestiona la persistencia de datos y cómo esto ha evolucionado en la Versión 13\.

### **2.1. El Paradigma de la Modularidad: Mundos vs. Módulos**

En la arquitectura de Foundry, un "Mundo" (*World*) actúa como un contenedor aislado de datos. Los actores, objetos y escenas creados dentro de un mundo se almacenan en la base de datos local de esa instancia. Históricamente, esto presentaba un desafío significativo para la portabilidad: si un usuario creaba un bestiario personalizado para una campaña de *Deadlands* (un entorno de SWADE), esos datos quedaban atrapados en ese mundo específico.

La solución arquitectónica es el "Módulo de Contenido" o *Shared Compendium*. Técnicamente, un módulo es un paquete de software que se inyecta en el tiempo de ejecución de Foundry. A diferencia de los módulos que alteran la interfaz o añaden lógica (scripts), un módulo de contenido se dedica a "montar" bases de datos adicionales en el sistema de archivos virtual de Foundry.1

Al encapsular el contenido en un módulo:

1. **Persistencia Agnostica:** Los datos existen independientemente de cualquier mundo.  
2. **Control de Versiones:** El módulo puede gestionarse mediante Git, permitiendo revertir cambios y colaborar en equipos.  
3. **Optimización de Recursos:** Los compendios no se cargan en la memoria RAM hasta que se solicitan, a diferencia de los items que residen en la barra lateral del mundo, mejorando el rendimiento del servidor.4

### **2.2. Evolución del Almacenamiento: De NeDB a LevelDB**

Hasta la versión 10, Foundry utilizaba NeDB, un sistema que almacenaba los compendios como archivos de texto legibles (JSON-lines) con extensión .db. Sin embargo, desde la versión 11 y consolidándose en la V13, Foundry ha migrado a **LevelDB** (a través de classic-level).

Esta transición tiene implicaciones profundas para el desarrollo de compendios personalizados:

* **Estructura de Carpetas:** Un compendio ya no es un solo archivo. Ahora es un directorio que contiene archivos binarios y logs de transacciones.  
* **Inviabilidad de Edición Manual:** Ya no es posible abrir un archivo de compendio en un editor de texto para corregir un error tipográfico o cambiar un ID. Se requiere el uso de herramientas de CLI (*Command Line Interface*) para "desempaquetar" la base de datos a archivos JSON editables y volver a "empaquetarla" para su distribución.3  
* **Rendimiento:** LevelDB ofrece un rendimiento superior en operaciones de lectura/escritura y soporta carpetas anidadas dentro de los compendios, una característica muy solicitada para organizar las complejas jerarquías de ventajas y poderes de SWADE.5

### **2.3. Estándares de Validación en V13**

La Versión 13 introduce un rigor mayor en la validación de los manifiestos de los módulos. El archivo module.json actúa como el contrato entre el módulo y el núcleo de software. En V13, campos que anteriormente eran opcionales o laxos ahora provocan que el módulo no se cargue si están mal formados.

El cambio más crítico es el objeto compatibility. Anteriormente se usaban campos planos como minimumCoreVersion. En V13, esto se ha encapsulado en un objeto estructurado que define los límites de compatibilidad (minimum, verified, maximum). Ignorar esta estructura resultará en advertencias de deprecación o fallos críticos en la carga del módulo.6

## ---

**3\. Anatomía del Manifiesto module.json para SWADE**

El núcleo de la solicitud del usuario es obtener un "manifiesto que se instale como un Addon". A continuación, se presenta la especificación técnica completa de un archivo module.json optimizado para SWADE en Foundry V13, con un análisis detallado de cada campo.

### **3.1. Estructura de Referencia del Manifiesto**

Este código representa el estado del arte para un módulo de compendio en 2026 (V13). Debe residir en la raíz del directorio del módulo.

JSON

{  
  "id": "swade-arsenal-personalizado",  
  "title": "Arsenal y Bestiario Personalizado SWADE",  
  "description": "Compendio compartido de armas, vehículos y PNJs para campañas de Savage Worlds.",  
  "version": "1.0.0",  
  "compatibility": {  
    "minimum": "13",  
    "verified": "13.341",  
    "maximum": "13.999"  
  },  
  "authors":,  
  "relationships": {  
    "systems": \[  
      {  
        "id": "swade",  
        "type": "system",  
        "manifest": "https://github.com/pinnacle/swade/releases/latest/download/system.json",  
        "compatibility": {  
          "minimum": "3.2.0"  
        }  
      }  
    \]  
  },  
  "packs":,  
  "url": "https://github.com/usuario/swade-arsenal-personalizado",  
  "manifest": "https://github.com/usuario/swade-arsenal-personalizado/releases/latest/download/module.json",  
  "download": "https://github.com/usuario/swade-arsenal-personalizado/releases/latest/download/module.zip",  
  "media": \[  
    {  
      "type": "cover",  
      "url": "modules/swade-arsenal-personalizado/assets/cover.webp"  
    }  
  \]  
}

### **3.2. Análisis de Campos Críticos**

#### **3.2.1. El Bloque relationships y la Dependencia del Sistema**

Para un compendio de SWADE, es fundamental declarar la relación con el sistema de juego.

* **Propósito:** El campo relationships (anteriormente dependencies en versiones antiguas) asegura que el módulo solo se active si el sistema SWADE está presente.  
* **Implicación Técnica:** Al especificar "type": "system" y "id": "swade", Foundry valida que la estructura de datos interna de los items (por ejemplo, system.attributes.agility) coincida con lo que el motor de juego espera. Si se intenta cargar este módulo en D\&D 5e, Foundry bloqueará la activación o los items aparecerán corruptos debido a la discrepancia de esquemas de datos.8  
* **Compatibilidad Cruzada:** Es posible definir compatibilidad mínima del sistema ("minimum": "3.2.0"). Dado que SWADE actualiza frecuentemente sus modelos de datos (por ejemplo, cambios en cómo se gestionan los modificadores de daño), fijar una versión mínima previene errores de "Data Model Mismatch".

#### **3.2.2. Definición de packs**

Este array define qué bases de datos expone el módulo.

* **path**: En V13, esto apunta a una *carpeta* (packs/equipo) en lugar de un archivo (packs/equipo.db), reflejando la arquitectura LevelDB.  
* **type**: Define la clase de Documento. Para SWADE:  
  * **Item**: Cubre *Edges*, *Hindrances*, *Weapons*, *Powers*, *Gear*.  
  * **Actor**: Cubre *Characters*, *NPCs*, *Vehicles*.  
  * **JournalEntry**: Para reglas de la casa y descripciones de ambientación.  
* **system**: **Crucial**. Debe establecerse en "swade". Esto permite que el sistema de juego indexe el contenido para sus buscadores internos y aplique filtros específicos (como filtrar poderes por Rango).4

#### **3.2.3. Control de Acceso (ownership)**

Una característica potente en V13 es definir permisos por defecto en el manifiesto.

* Configurar "PLAYER": "OBSERVER" en un compendio de equipo permite que los jugadores vean las estadísticas de las armas sin necesidad de que el DJ configure los permisos manualmente cada vez que inicia una partida. Esto es ideal para "Manuales de Jugador" personalizados.1

## ---

**4\. Estrategias de Implementación: Flujos de Trabajo**

Existen dos metodologías principales para crear estos compendios: el enfoque de interfaz gráfica (GUI) y el enfoque de ingeniería de software (CLI). Para satisfacer la solicitud de un "repositorio de ejemplo", se detallará el flujo avanzado, que es el estándar profesional.

### **4.1. Flujo de Trabajo 1: El Generador de Módulos (GUI)**

Para usuarios menos técnicos o para el prototipado rápido, Foundry V13 incluye herramientas nativas.

**Tabla 1: Proceso de Creación vía GUI**

| Fase | Acción en Foundry VTT | Detalles Técnicos |
| :---- | :---- | :---- |
| **Inicialización** | Configuración \> Add-on Modules \> "Create Module" | Genera el esqueleto del directorio y el module.json automáticamente, asegurando sintaxis válida.9 |
| **Definición** | Asignar ID, Título y Autores | El ID debe ser "kebab-case" (ej. mi-modulo). Evitar espacios y caracteres especiales. |
| **Estructura** | Pestaña "Compendium Packs" \> "Create Pack" | Se deben crear packs separados para Actores, Items y Tablas. Asignar el sistema "swade" es obligatorio. |
| **Población** | Entrar a un Mundo \> Activar Módulo | Los compendios aparecen vacíos. Se debe quitar el bloqueo de edición ("Toggle Edit Lock").10 |
| **Migración** | Arrastrar y Soltar / Exportar Carpeta | Usar "Export to Compendium" en carpetas del mundo preserva la estructura de carpetas anidadas dentro del compendio.4 |

**Limitación:** Este método crea un módulo que reside solo en su máquina local. No es fácilmente compartible sin comprimir manualmente la carpeta y enviarla, lo cual dificulta las actualizaciones.

### **4.2. Flujo de Trabajo 2: Repositorio y CLI (Estándar Profesional)**

Este enfoque responde a la necesidad del usuario de un "repositorio de ejemplo". Implica tratar el contenido de rol como código fuente.

#### **4.2.1. Preparación del Entorno**

Se requiere la instalación de **Node.js** y la herramienta oficial **Foundry VTT CLI**.

1. Instalar Node.js (versión LTS compatible con su sistema operativo).  
2. Instalar la CLI: Ejecutar npm install \-g @foundryvtt/foundryvtt-cli en la terminal.  
3. Esta herramienta permite interactuar con los formatos de datos de Foundry sin abrir la aplicación.3

#### **4.2.2. Arquitectura del Repositorio de Ejemplo**

Un repositorio de GitHub para un compendio de SWADE debe tener la siguiente estructura de archivos. Esta estructura separa el código fuente (JSONs editables) de los archivos compilados (LevelDB).

mi-repo-swade/  
├──.github/  
│ └── workflows/  
│ └── release.yml \# Automatización para crear el ZIP  
├── src/  
│ ├── packs/ \# Aquí viven los archivos JSON (Fuente)  
│ │ ├── bestiario/  
│ │ │ ├── orco\_guerrero.json  
│ │ │ └── dragon\_joven.json  
│ │ └── ventajas/  
│ │ ├── ambidiestro.json  
│ │ └── trasfondo\_arcano.json  
│ └── assets/ \# Imágenes originales (Iconos, Tokens)  
├── dist/ \# Carpeta de salida (Generada, no se sube a git)  
├── module.json \# El manifiesto maestro  
├── package.json \# Configuración de NPM y scripts  
├── README.md \# Instrucciones de instalación  
└──.gitignore \# Ignorar carpeta 'dist' y 'node\_modules'

#### **4.2.3. El Ciclo de Desarrollo "Unpack/Pack"**

Para mantener este repositorio, el desarrollador sigue un ciclo continuo:

1. **Creación en Foundry:** Crea los items en el mundo de juego y expórtalos al compendio del módulo.  
2. **Extracción (Unpack):** Usa la CLI para convertir la base de datos binaria de Foundry en JSONs legibles en la carpeta src.  
   * Comando: fvtt package unpack \--in "Ruta/A/Foundry/Data/modules/mi-modulo/packs/bestiario" \--out "./src/packs/bestiario".3  
3. **Versionado:** Haz *commit* y *push* de los archivos JSON a GitHub. Esto permite ver exactamente qué cambió (ej. "Aumentada la fuerza del Orco de d6 a d8").  
4. **Distribución (Pack):** Cuando estés listo para liberar una versión, usa la CLI para compilar los JSONs de nuevo a LevelDB y generar el ZIP.  
   * Comando: fvtt package pack \--in "./src/packs/bestiario" \--out "./dist/packs/bestiario".3

## ---

**5\. Especificidades del Sistema SWADE en Compendios**

El sistema *Savage Worlds* tiene particularidades que afectan cómo se deben construir los compendios para asegurar su funcionalidad completa.

### **5.1. Gestión de IDs y Enlaces Cruzados**

Uno de los problemas más comunes en SWADE es la ruptura de enlaces. Un "Poder" en SWADE a menudo hace referencia a una "Ventaja" (Arcane Background). Si estos elementos se crean en un mundo y luego se mueven a un compendio, sus identificadores únicos (UUID) cambian de Actor.id a Compendium.pack.id.

**Insight Técnico:** Al crear contenido para un compendio compartido, **nunca** se deben arrastrar items directamente a la hoja de personaje o a un diario si se pretende exportar después. Se debe utilizar la sintaxis de enlace dinámico de Foundry.

* **Incorrecto:** Arrastrar una ventaja desde la barra de items del mundo a la descripción de un actor. Esto crea un enlace duro al mundo (@Item\[xyz\]).  
* **Correcto:** Referenciar el item una vez que está en el compendio (@UUID\[Compendium.mi-modulo.ventajas.abc\]).

Para facilitar esto, módulos como *SWADE Tools* o *Compendium Browser* (mencionado en 12) son esenciales, ya que permiten buscar y arrastrar contenido directamente desde los compendios, generando los enlaces correctos automáticamente.

### **5.2. Imágenes y Rutas Relativas (Assets)**

Un compendio profesional debe ser autocontenido. Si un arma en el compendio apunta a worlds/mi-mundo/imagenes/espada.png, el usuario que instale el módulo verá un enlace roto.

**Estrategia de Assets:**

1. Crear una carpeta assets dentro del directorio del módulo (modules/mi-modulo/assets).  
2. Colocar todas las imágenes (iconos de ventajas, tokens de monstruos) allí.  
3. Al editar el item en Foundry, seleccionar la imagen desde esta ruta. Foundry guardará la ruta como modules/mi-modulo/assets/imagen.png.  
4. Esta ruta es universal para cualquier usuario que instale el módulo.

### **5.3. Active Effects y Automatización**

En V13 y SWADE moderno, muchos objetos tienen "Efectos Activos" (Active Effects) que modifican estadísticas automáticamente (ej. una armadura que reduce la Agilidad).

* Al exportar a un compendio, asegúrese de que los efectos no dependan de macros almacenadas en el mundo. Si el efecto llama a una macro (Macro.execute), esa macro también debe estar en un compendio de Macros dentro del módulo, y la llamada debe referenciarla por UUID o nombre dentro del compendio.13

## ---

**6\. Integración de Referencias y Repositorios Ejemplo**

Para satisfacer la solicitud de "repositorios de ejemplo", analizamos patrones de repositorios reales de la comunidad SWADE que pueden servir como plantilla.

### **6.1. Análisis del Repositorio "Savage Rifts Compendium Browser"**

El snippet 12 hace referencia a un repositorio que, aunque es un módulo de código, ilustra la estructura de empaquetado para SWADE.

* **Lección:** Nótese el uso de un module.json que declara dependencias y la estructura de carpetas. Este módulo en particular añade una capa de interfaz sobre los compendios, demostrando cómo se pueden extender las funcionalidades básicas.

### **6.2. Análisis del Repositorio "SWADE NPC Importer"**

El snippet 14 muestra herramientas para importar bloques de estadísticas. Esto es relevante para el flujo de trabajo: en lugar de crear actores manualmente, se puede usar este importador para generar los datos en el mundo y luego exportarlos al compendio compartido siguiendo el flujo descrito en la Sección 4.1.

### **6.3. Plantilla de Referencia "Scene Packer"**

Aunque enfocado en escenas, el "Module Generator" de Scene Packer 15 es citado recurrentemente como la herramienta estándar *de facto* para usuarios que no desean lidiar con la CLI.

* **Recomendación:** Para el usuario que busca una "guía", el uso del generador online de Scene Packer (o su equivalente integrado en Foundry V11+) es el punto de partida ideal para generar el module.json inicial sin errores de sintaxis.

## ---

**7\. Guía de Instalación y Distribución**

Una vez creado y empaquetado el módulo, el paso final es hacerlo instalable "como un Addon".

### **7.1. El Enlace de Manifiesto (Manifest URL)**

Para que otros usuarios instalen el módulo sin que este figure en la lista oficial de Foundry, necesitan el **Manifest URL**.

1. Alojamiento del archivo module.json: Este archivo debe estar accesible públicamente en internet (usualmente en la sección "Releases" de GitHub o en un servidor web).  
2. El campo download dentro del module.json debe apuntar al archivo .zip del módulo.

**Proceso de Instalación para el Usuario Final:**

1. Abrir Foundry VTT \> Add-on Modules \> Install Module.  
2. Pegar la URL del module.json en el campo inferior "Manifest URL".  
3. Hacer clic en Install. Foundry leerá el manifiesto, validará la compatibilidad (V13/SWADE) y descargará el ZIP automáticamente.17

## ---

**8\. Conclusiones y Recomendaciones Estratégicas**

La creación de compendios personalizados para SWADE en Foundry VTT V13 no es solo una tarea de entrada de datos, sino un ejercicio de arquitectura de sistemas. La transición a V13 impone un rigor técnico mediante la validación estricta del manifiesto y el uso de LevelDB, lo que, aunque eleva la barrera de entrada, garantiza una mayor estabilidad y rendimiento a largo plazo.

**Recomendaciones Finales:**

1. **Adopción del Estándar CLI:** Para cualquier proyecto que pretenda ser duradero o compartido, es imperativo abandonar la edición manual de archivos y adoptar el flujo de trabajo unpack/pack con la CLI oficial. Esto asegura la integridad de los datos LevelDB.  
2. **Modularidad Granular:** Se recomienda no crear un único "Mega-Módulo". Es preferible segmentar el contenido temáticamente (ej. "SWADE \- Reglas Caseras", "SWADE \- Campaña Fantasía"), aprovechando el sistema de relaciones del module.json para gestionar dependencias.  
3. **Higiene de Datos:** Antes de empaquetar, se debe realizar una auditoría de enlaces y assets. Un compendio con imágenes rotas o referencias a actores inexistentes degrada la experiencia del usuario y genera errores en la consola.

Este informe proporciona la hoja de ruta técnica completa para transformar una colección de notas y estadísticas dispersas en un producto de software robusto, instalable y profesional dentro del ecosistema Foundry VTT.

#### **Obras citadas**

1. Introduction to Module Development | Foundry Virtual Tabletop, fecha de acceso: enero 20, 2026, [https://foundryvtt.com/article/module-development/](https://foundryvtt.com/article/module-development/)  
2. Foundry new user perplexed about compendium and module : r/FoundryVTT \- Reddit, fecha de acceso: enero 20, 2026, [https://www.reddit.com/r/FoundryVTT/comments/1kjyb4a/foundry\_new\_user\_perplexed\_about\_compendium\_and/](https://www.reddit.com/r/FoundryVTT/comments/1kjyb4a/foundry_new_user_perplexed_about_compendium_and/)  
3. foundryvtt/foundryvtt-cli: The official Foundry VTT CLI \- GitHub, fecha de acceso: enero 20, 2026, [https://github.com/foundryvtt/foundryvtt-cli](https://github.com/foundryvtt/foundryvtt-cli)  
4. Compendium Packs | Foundry Virtual Tabletop, fecha de acceso: enero 20, 2026, [https://foundryvtt.com/article/compendium/](https://foundryvtt.com/article/compendium/)  
5. Release 11.293 \- Foundry Virtual Tabletop, fecha de acceso: enero 20, 2026, [https://foundryvtt.com/releases/11.293](https://foundryvtt.com/releases/11.293)  
6. Publishing a Module | Foundry VTT Community Wiki, fecha de acceso: enero 20, 2026, [https://foundryvtt.wiki/en/development/guides/local-to-repo](https://foundryvtt.wiki/en/development/guides/local-to-repo)  
7. Release 13.341 | Foundry Virtual Tabletop, fecha de acceso: enero 20, 2026, [https://foundryvtt.com/releases/13.341](https://foundryvtt.com/releases/13.341)  
8. Introduction to System Development | Foundry Virtual Tabletop, fecha de acceso: enero 20, 2026, [https://foundryvtt.com/article/system-development/](https://foundryvtt.com/article/system-development/)  
9. Module Maker | Foundry Virtual Tabletop, fecha de acceso: enero 20, 2026, [https://foundryvtt.com/article/module-maker/](https://foundryvtt.com/article/module-maker/)  
10. How to make compendium in a module? : r/FoundryVTT \- Reddit, fecha de acceso: enero 20, 2026, [https://www.reddit.com/r/FoundryVTT/comments/1ipvpey/how\_to\_make\_compendium\_in\_a\_module/](https://www.reddit.com/r/FoundryVTT/comments/1ipvpey/how_to_make_compendium_in_a_module/)  
11. How to Share Content Between Worlds \- Foundry \- The Forge, fecha de acceso: enero 20, 2026, [https://forums.forge-vtt.com/t/how-to-share-content-between-worlds/5653](https://forums.forge-vtt.com/t/how-to-share-content-between-worlds/5653)  
12. 1337mith/swrifts-compendium-browser \- GitHub, fecha de acceso: enero 20, 2026, [https://github.com/1337mith/swrifts-compendium-browser](https://github.com/1337mith/swrifts-compendium-browser)  
13. SalieriC/SWIM: A collection of macros for the SWADE ... \- GitHub, fecha de acceso: enero 20, 2026, [https://github.com/SalieriC/SWIM](https://github.com/SalieriC/SWIM)  
14. arnonram/swade-npc-importer: Savage Worlds Stat-block importer for FoundryVTT \- GitHub, fecha de acceso: enero 20, 2026, [https://github.com/arnonram/swade-npc-importer](https://github.com/arnonram/swade-npc-importer)  
15. Module Generator release : r/FoundryVTT \- Reddit, fecha de acceso: enero 20, 2026, [https://www.reddit.com/r/FoundryVTT/comments/pexynh/module\_generator\_release/](https://www.reddit.com/r/FoundryVTT/comments/pexynh/module_generator_release/)  
16. Library: Scene Packer | Foundry Virtual Tabletop, fecha de acceso: enero 20, 2026, [https://foundryvtt.com/packages/scene-packer](https://foundryvtt.com/packages/scene-packer)  
17. Content Packaging Guide | Foundry Virtual Tabletop, fecha de acceso: enero 20, 2026, [https://foundryvtt.com/article/packaging-guide/](https://foundryvtt.com/article/packaging-guide/)  
18. My Shared Compendia | Foundry Virtual Tabletop, fecha de acceso: enero 20, 2026, [https://foundryvtt.com/packages/My-Shared-Compendia](https://foundryvtt.com/packages/My-Shared-Compendia)