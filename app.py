import numpy as np

def main():
    # ==============================================================================
    # ENCABEZADO ACADÉMICO OFICIAL UACH
    # ==============================================================================
    print("\n" + "=" * 75)
    print(" " * 21 + "UNIVERSIDAD AUTÓNOMA DE CHIHUAHUA")
    print(" " * 23 + "Facultad de Ciencias Químicas")
    print("-" * 75)
    print(" MATERIA:    Operaciones Unitarias II")
    print(" ACTIVIDAD:  Participación #4 (Unidad #3)")
    print(" PROYECTO:   Simulador de Absorbedor de CO₂ en una Torre Empacada")
    print(" CATEDRÁTICO: Dr. Ildebrando Pérez Reyes")
    print(" ALUMNO:     Gerardo Emiliano Palma Chávez")
    print("=" * 75)

    # ==============================================================================
    # INSTRUCCIONES DE OPERACIÓN PARA EL USUARIO
    # ==============================================================================
    print("\n[ BIENVENIDO AL SIMULADOR DE TORRE DE ABSORCIÓN ]")
    print("Por favor, introduce los datos de diseño que se te solicitan a continuación.")
    print("Nota: Los valores numéricos deben ingresarse en formato decimal estándar (Ejemplo: 30 o 0.058).")
    print("Si deseas utilizar los datos por defecto del ejercicio (U3-P4), escríbelos tal como se sugieren.")
    print("-" * 75)

    # 1. ENTRADAS MODIFICABLES POR EL USUARIO
    print("\n[ PASO 1: Ingresa la concentración de la solución absorbente ]")
    C_MEA = float(input("-> Concentración de la solución de MEA (% en peso) [Sugerido: 30] → "))

    print("\n[ PASO 2: Ingresa la composición del gas que entra por el fondo (G1) ]")
    print("Recuerda que la suma de los tres componentes debe dar el 100% de la mezcla gaseosa.")
    y1_CO2_pct = float(input("   - Porcentaje de CO₂ (% en volumen)               [Sugerido: 15] → "))
    y1_O2_pct  = float(input("   - Porcentaje de O₂  (% en volumen)               [Sugerido: 6]  → "))
    y1_N2_pct  = float(input("   - Porcentaje de N₂  (% en volumen)               [Sugerido: 79] → "))

    print("\n[ PASO 3: Parámetros operativos y condiciones límite del sistema ]")
    x2_input = float(input("   - Concentración del líquido en el domo (mol CO2/mol sol) [Sugerido: 0.058] → "))
    factor_min = float(input("   - Multiplicador de la relación Ls-min/Gs (Exceso)        [Sugerido: 1.2]   → "))
    y2_CO2_pct = float(input("   - Concentración de CO₂ deseada en el gas de salida (%)   [Sugerido: 2]     → "))

    print("\n" + "." * 75)
    print(" CALCULANDO PROPIEDADES, BALANCES DE MATERIA Y RELACIONES MOLARES...")
    print("." * 75)

    # Conversión de porcentajes a fracciones molares (y)
    y1_CO2 = y1_CO2_pct / 100.0
    y2_CO2 = y2_CO2_pct / 100.0

    # 2. CONSTANTES FÍSICAS (Ajustadas a los decimales exactos de Excel)
    T_K = 25.0 + 273.15          # 298.15 K
    R = 0.0820574614             # L·atm/(mol·K)

    PM_CO2 = 44.009
    PM_MEA = 61.080
    PM_O2  = 31.999
    PM_N2  = 28.013
    PM_H2O = 18.015

    # 3. TABLA DE EQUILIBRIO (25°C, MEA 30%)
    x_table = np.array([0.058, 0.060, 0.062, 0.064, 0.066, 0.068, 0.070])
    P_table = np.array([5.6, 12.8, 29.0, 56.0, 98.7, 155.0, 232.0])

    # 4. RELACIONES MOLARES DE OPERACIÓN
    Y1 = y1_CO2 / (1.0 - y1_CO2)
    Y2 = y2_CO2 / (1.0 - y2_CO2)
    X2 = x2_input

    # Presión parcial en el fondo del absorbedor
    PT_mmHg = 1.2 * 760.0025
    P_CO2_fondo = y1_CO2 * PT_mmHg

    # Interpolación para hallar X1* de equilibrio
    X1_star = float(np.interp(P_CO2_fondo, P_table, x_table))

    # Relaciones Líquido/Gas (Mínima y Real de operación)
    LsGs_min = (Y1 - Y2) / (X1_star - X2)
    LsGs_real = LsGs_min * factor_min

    # ==============================================================================
    # 5. ALGORITMO MATEMÁTICO DE FLUJOS Y DENSIDADES
    # ==============================================================================
    # Corriente de operación real (Presión del sistema = 1.2 atm)
    n_total_m3_real = (1.2 * 1000.0) / (R * T_K)
    Gs_real = n_total_m3_real * (1.0 - y1_CO2)
    Ls_real = Gs_real * LsGs_real

    # Corriente de referencia estándar (Presión estándar = 1.0 atm)
    n_total_m3_1atm = (1.0 * 1000.0) / (R * T_K)
    Gs_1atm = n_total_m3_1atm * (1.0 - y1_CO2)

    # Peso molecular de la solución absorbente (Media armónica real)
    w_MEA = C_MEA / 100.0
    w_H2O = 1.0 - w_MEA
    moles_por_gramo = (w_MEA / PM_MEA) + (w_H2O / PM_H2O)
    PM_sol_g_mol = 1.0 / moles_por_gramo
    PM_sol_kg_mol = PM_sol_g_mol / 1000.0

    # Variables de masa y cantidad de sustancia finales
    kg_solucion_m3 = Ls_real * PM_sol_kg_mol
    moles_CO2_L2 = Ls_real * X2

    # 6. VARIABLES AUXILIARES DE LA INTERFAZ DE EXCEL
    PM_sol_visual = (w_MEA * PM_MEA) + (w_H2O * PM_H2O)

    g1_co2_visual = y1_CO2 / (1.0 - y1_CO2)
    g1_n2_visual = (y1_N2_pct / 100.0) / ((y1_N2_pct / 100.0) + 1.0)
    g1_o2_visual = (y1_O2_pct / y1_N2_pct) * 7.9

    g2_co2_visual = y2_CO2
    g2_n2_visual = 1.0 - y2_CO2
    g2_o2_visual = 1.0 - y2_CO2

    # ==========================================================================
    # DESPLIEGUE SECCIÓN 1: SECCIÓN DE DATOS DE LOS COMPONENTES
    # ==========================================================================
    print("\n" + "=" * 34 + " [ DATOS ] " + "=" * 30)
    print("A continuación se muestran los pesos moleculares y las presiones parciales calculadas:")
    print(f" PM A (CO2)      (g/mol) : {PM_CO2:.3f}")
    print(f" PM B (MEA)      (g/mol) : {PM_MEA:.3f}")
    print(f" PM C (O2)       (g/mol) : {PM_O2:.3f}")
    print(f" PM D (N2)       (g/mol) : {PM_N2:.3f}")
    print(f" PM H2O          (g/mol) : {PM_H2O:.3f}")
    print(f" PM sol          (g/mol) : {PM_sol_visual:.3f}   <- Peso molecular promedio")
    print(f" PT              (atm)   : 1.200")
    print(f" PT              (mmHg)  : {PT_mmHg:.3f}   <- Presión total en milímetros de mercurio")
    print(f" PCO2            (mmHg)  : {P_CO2_fondo:.3f}   <- Presión parcial de CO2 en el fondo")
    print(f" G1 CO2                  : {g1_co2_visual:.6f}")
    print(f" G1 N2                   : {g1_n2_visual:.6f}")
    print(f" G1 O2                   : {g1_o2_visual:.3f}")
    print(f" G2 CO2                  : {g2_co2_visual:.3f}")
    print(f" G2 N2                   : {g2_n2_visual:.3f}")
    print(f" G2 O2                   : {g2_o2_visual:.3f}")

    # ==========================================================================
    # DESPLIEGUE SECCIÓN 2: CÁLCULOS DE BALANCES INTERMEDIOS
    # ==========================================================================
    print("\n" + "=" * 24 + " [ CÁLCULOS INTERMEDIOS ] " + "=" * 25)
    print("Valores intermedios del balance líquido-gas y flujos calculados por volumen:")
    print(f" X1                      : {X1_star:.6f}   <- Composición de equilibrio")
    print(f" X2                      : {X2:.6f}")
    print(f" Y1                      : {Y1:.6f}")
    print(f" Y2                      : {Y2:.6f}")
    print(f" (Ls/Gs)_min             : {LsGs_min:.6f}   <- Relación Líquido/Gas mínima")
    print(f" (Ls/Gs)_real            : {LsGs_real:.6f}   <- Relación Líquido/Gas real de operación")
    print(f" nT 1.0 atm      (mol)   : {n_total_m3_1atm:.6f}   <- Moles totales a condiciones estándar")
    print(f" Gs 1.0 atm      (mol/m³): {Gs_1atm:.6f}")
    print(f" nT 1.2 atm      (mol)   : {n_total_m3_real:.6f}   <- Moles totales a presión de operación")
    print(f" Gs 1.2 atm      (mol/m³): {Gs_real:.6f}")
    print(f" Ls              (mol)   : {Ls_real:.6f}   <- Flujo molar del líquido inerte")
    print(f" mT              (Kg)    : {kg_solucion_m3:.6f}   <- Masa total de solución por m³")

    # ==========================================================================
    # DESPLIEGUE SECCIÓN 3: RESPUESTAS FORMALES EN FORMATO DECIMAL
    # ==========================================================================
    print("\n" + "=" * 75)
    print(" " * 20 + "RESULTADOS FINALES")
    print("=" * 75)
    print("Todos los resultados se presentan en notación decimal estándar para su lectura:")
    print(f" A) Relación líquido/gas mínima (Ls/Gs)_min   : {LsGs_min:.6f} mol/mol")
    print(f" B) Relación molar en el domo de la torre (Y₂): {Y2:.6f} mol CO2/mol inerte")
    print(f" C) Relación molar en el domo de la torre (X₂): {X2:.6f} mol CO2/mol sol")
    print(f" D) Relación molar en el fondo de la torre (Y₁): {Y1:.6f} mol CO2/mol inerte")
    print(f" E) Relación molar de equilibrio en fondo (X₁*): {X1_star:.6f} mol CO2/mol sol")
    print(f" F) Flujo de gas inerte Gs (mol/m³) [1 m³ de G₁]: {Gs_real:.6f} mol/m³")
    print(f" G) Masa de solución por m³ (a {factor_min:<3} veces)   : {kg_solucion_m3:.6f} kg/m³")
    print(f" H) Moles de CO₂ transportados en la corriente L₂: {moles_CO2_L2:.6f} mol/m³")
    print("=" * 75)

    input("\n[Simulación terminada con éxito] Presiona Enter para cerrar la ventana...")

if __name__ == "__main__":
    main()
