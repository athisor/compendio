import os

# List of files to remove that are clearly parsing artifacts
junk_files = [
    r"d:\Rol\FoundryVTT\Data\modules\swade-setting-iz3\src\es\edges\ventajas-extraordinarias.json",
    r"d:\Rol\FoundryVTT\Data\modules\swade-setting-iz3\src\es\edges\ventajas-profesionales.json",
    r"d:\Rol\FoundryVTT\Data\modules\swade-setting-iz3\src\es\edges\ventajas-sociales.json",
    r"d:\Rol\FoundryVTT\Data\modules\swade-setting-iz3\src\es\edges\rango-del.json",
    r"d:\Rol\FoundryVTT\Data\modules\swade-setting-iz3\src\es\edges\de-rondas.json",
]

for f in junk_files:
    if os.path.exists(f):
        os.remove(f)
        print(f"Removed junk: {f}")
