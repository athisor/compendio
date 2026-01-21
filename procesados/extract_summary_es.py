import os

def main():
    spanish_md = r"d:\Rol\SWADE\SWIZ-01-Interface-Zero-3-digital-whkhpj.md"
    output_md = r"d:\Rol\SWADE\IZ3_Setting_Summary_ES.md"
    
    if not os.path.exists(spanish_md):
        print("Spanish manual not found.")
        return

    with open(spanish_md, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Precise markers for Spanish summary
    # 1. TRASFONDOS (Starting at activist, ending at summary table approx)
    # Actually Activist is at 8, summary table ends at 810 approx.
    trasfondos_start = 8
    trasfondos_end = 810
    
    # 2. RAZAS (Starting at Android 2763, ending at Human 2.0 approx)
    # Android 2763
    # Human 2.0 3719, ends around 3900
    razas_start = 2704 # Intro at 2704
    razas_end = 4000
    
    # 3. VENTAJAS (Start around Ratero 4004, ends after summary table 4480)
    ventajas_start = 4004
    ventajas_end = 4480
    
    # 4. ZEEKS
    zeeks_start = 8185
    zeeks_end = 8400

    with open(output_md, 'w', encoding='utf-8') as f:
        f.write("# Interface Zero 3.0 - Resumen del Escenario (Español)\n\n")
        f.write("> [!IMPORTANT]\n")
        f.write("> Esta es una recopilación de la información básica para la creación de personajes en Interface Zero 3.0.\n\n")
        
        f.write("## TRASFONDOS (ORIGINS)\n\n")
        f.writelines(lines[trasfondos_start-1:trasfondos_end])
        f.write("\n\n---\n\n")
        
        f.write("## RAZAS (ANCESTRIES)\n\n")
        f.writelines(lines[razas_start-1:razas_end])
        f.write("\n\n---\n\n")
        
        f.write("## VENTAJAS Y DESVENTAJAS\n\n")
        f.writelines(lines[ventajas_start-1:ventajas_end])
        f.write("\n\n---\n\n")
        
        f.write("## ZEEKS Y PIRATERÍA\n\n")
        f.writelines(lines[zeeks_start-1:zeeks_end])
        f.write("\n\n---\n\n")

    print(f"Precise Spanish summary written to {output_md}")

if __name__ == "__main__":
    main()
