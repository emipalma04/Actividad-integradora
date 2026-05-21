import streamlit as st
import numpy as np

# Configuración de la página web
st.set_page_config(page_title="Actividad Integradora - Emiliano Palma", layout="centered") 

# ==============================================================================
# ENCABEZADO LOGOS E INSTITUCIONAL (UACH IZQUIERDA, FCQ DERECHA)
# ==============================================================================
img_col_izq, texto_col_centro, img_col_der = st.columns([1, 4, 1])

with img_col_izq:
    st.image("https://raw.githubusercontent.com/emipalma04/Actividad-integradora/main/Logo%20UACH.png", width=90)

with texto_col_centro:
    st.markdown(
        """
        <div style="text-align: center;">
            <h1 style="color: #0A2540; margin: 0; font-family: sans-serif; font-size: 28px;"><b>UNIVERSIDAD AUTÓNOMA DE CHIHUAHUA</b></h1>
            <h3 style="color: #D4AF37; margin: 5px 0 0 0; font-family: sans-serif; font-size: 20px;"><b>Facultad de Ciencias Químicas</b></h3>
        </div>
        """, 
        unsafe_allow_html=True
    )

with img_col_der:
    st.image("https://raw.githubusercontent.com/emipalma04/Actividad-integradora/main/FCQ.png", width=80)

st.markdown("<hr style='border: 1px solid #0A2540; margin-top: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)

# Datos del estudiante
st.markdown("**ACTIVIDAD INTEGRADORA:** Participación #4 (Unidad #3)")
st.markdown("**MATERIA:** Operaciones Unitarias II")
st.markdown("**PROYECTO:** Simulador de absorbedor de CO₂ en una torre empacada")
st.markdown("**DOCENTE:** Dr. Ildebrando Pérez Reyes")
st.markdown("**ALUMNO:** Gerardo Emiliano Palma Chávez")
st.markdown("---")

st.markdown("<h3 style='color: #0A2540;'>Instrucciones</h3>", unsafe_allow_html=True)
st.write("Modifica los parámetros según lo requieras y haz clic en el botón de abajo para actualizar de forma automática los resultados del modelo.")
st.info("Nota: Los valores numéricos precargados en el formulario corresponden por defecto a los datos de diseño del ejercicio U3-P4.")

# Formulario para las entradas del usuario
with st.form("simulador_form"):
    st.markdown("<h3 style='color: #0A2540;'>1. Entradas de diseño</h3>", unsafe_allow_html=True)
    
    C_MEA = st.number_input("Concentración de la solución de MEA (% en peso)", min_value=0.0, max_value=100.0, value=30.0, step=1.0, format="%.4f")
    
    st.markdown("<h4 style='color: #0A2540;'>Composición del gas de entrada (Fondo) - G1</h4>", unsafe_allow_html=True)
    y1_CO2_pct = st.number_input("Porcentaje de CO₂ (% en volumen)", min_value=0.0, max_value=100.0, value=15.0, format="%.4f")
    y1_O2_pct  = st.number_input("Porcentaje de O₂  (% en volumen)", min_value=0.0, max_value=100.0, value=6.0, format="%.4f")
    y1_N2_pct  = st.number_input("Porcentaje de N₂  (% en volumen)", min_value=0.0, max_value=100.0, value=79.0, format="%.4f")
    
    st.markdown("<h4 style='color: #0A2540;'>Condiciones operativas del sistema</h4>", unsafe_allow_html=True)
    x2_input = st.number_input("Concentración del líquido en el domo (mol CO₂/mol sol)", min_value=0.0, max_value=1.0, value=0.0580, format="%.4f")
    factor_min = st.number_input("Multiplicador de la relación Ls-min/Gs (Exceso)", min_value=1.0, max_value=5.0, value=1.2000, step=0.1, format="%.4f")
    y2_CO2_pct = st.number_input("Concentración de CO₂ deseada en el gas de salida (%)", min_value=0.0, max_value=100.0, value=2.0, format="%.4f")
    
    submit_button = st.form_submit_button(label="Correr simulación")

# ==============================================================================
# PROCESAMIENTO MATEMÁTICO REAL
# ==============================================================================
if submit_button:
    y1_CO2 = y1_CO2_pct / 100.0
    y2_CO2 = y2_CO2_pct / 100.0

    T_K = 25.0 + 273.15          
    R = 0.0820574614             

    PM_CO2 = 44.009
    PM_MEA = 61.080
    PM_O2  = 31.999
    PM_N2  = 28.013
    PM_H2O = 18.015

    x_table = np.array([0.058, 0.060, 0.062, 0.064, 0.066, 0.068, 0.070])
    P_table = np.array([5.6, 12.8, 29.0, 56.0, 98.7, 155.0, 232.0])

    Y1 = y1_CO2 / (1.0 - y1_CO2)
    Y2 = y2_CO2 / (1.0 - y2_CO2)
    X2 = x2_input

    PT_mmHg = 1.2 * 760.0025
    P_CO2_fondo = y1_CO2 * PT_mmHg

    X1_star = float(np.interp(P_CO2_fondo, P_table, x_table))

    LsGs_min = (Y1 - Y2) / (X1_star - X2)
    LsGs_real = LsGs_min * factor_min

    n_total_m3_real = (1.2 * 1000.0) / (R * T_K)
    Gs_real = n_total_m3_real * (1.0 - y1_CO2)
    Ls_real = Gs_real * LsGs_real

    n_total_m3_1atm = (1.0 * 1000.0) / (R * T_K)
    Gs_1atm = n_total_m3_1atm * (1.0 - y1_CO2)

    w_MEA = C_MEA / 100.0
    w_H2O = 1.0 - w_MEA
    moles_por_gramo = (w_MEA / PM_MEA) + (w_H2O / PM_H2O)
    PM_sol_g_mol = 1.0 / moles_por_gramo
    PM_sol_kg_mol = PM_sol_g_mol / 1000.0

    kg_solucion_m3 = Ls_real * PM_sol_kg_mol
    moles_CO2_L2 = Ls_real * X2

    PM_sol_visual = (w_MEA * PM_MEA) + (w_H2O * PM_H2O)

    g1_co2_visual = y1_CO2 / (1.0 - y1_CO2)
    g1_n2_visual = (y1_N2_pct / 100.0) / ((y1_N2_pct / 100.0) + 1.0)
    g1_o2_visual = (y1_O2_pct / y1_N2_pct) * 7.9

    g2_co2_visual = y2_CO2
    g2_n2_visual = 1.0 - y2_CO2
    g2_o2_visual = 1.0 - y2_CO2

    # ==========================================================================
    # INTERFAZ GRÁFICA DE RESPUESTAS (ESTILOS CSS OPTIMIZADOS Y DESCRIPTIVOS)
    # ==========================================================================
    st.markdown(
        """
        <style>
            .tabla-resultados { width: 100%; border-collapse: collapse; font-family: 'Segoe UI', sans-serif; }
            .tabla-resultados td { padding: 6px 4px; border-bottom: 1px solid rgba(0,0,0,0.05); font-size: 13.5px; }
            .tabla-resultados tr:last-child td { border-bottom: none; }
            .lbl { font-weight: 600; color: #2D3748; text-align: left; }
            .val { text-align: right; font-family: 'Courier New', monospace; font-weight: bold; color: #1A202C; }
            
            /* Estilos nuevos para las tarjetas de resultados finales */
            .contenedor-final {
                background-color: #F8FAFC;
                padding: 25px;
                border-radius: 12px;
                border: 1px solid #E2E8F0;
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
                font-family: 'Segoe UI', sans-serif;
            }
            .tarjeta-resultado {
                background-color: #FFFFFF;
                padding: 15px;
                margin-bottom: 12px;
                border-radius: 8px;
                border-left: 5px solid #0A2540;
                box-shadow: 0 2px 4px rgba(0,0,0,0.02);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .tarjeta-resultado-acento {
                background-color: #FFFDF5;
                padding: 15px;
                margin-bottom: 12px;
                border-radius: 8px;
                border-left: 5px solid #D4AF37;
                box-shadow: 0 2px 4px rgba(0,0,0,0.02);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .texto-inciso {
                color: #4A5568;
                font-size: 14.5px;
                font-weight: 500;
            }
            .valor-final {
                font-family: 'Courier New', monospace;
                font-weight: bold;
                font-size: 16px;
                color: #0A2540;
                background-color: #F1F5F9;
                padding: 4px 10px;
                border-radius: 4px;
                white-space: nowrap;
            }
            .valor-final-acento {
                font-family: 'Courier New', monospace;
                font-weight: bold;
                font-size: 16px;
                color: #8A6D1C;
                background-color: #FEF3C7;
                padding: 4px 10px;
                border-radius: 4px;
                white-space: nowrap;
            }
        </style>
        """, 
        unsafe_allow_html=True
    )

    st.markdown("---")
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        st.markdown(
            f"""
            <div style="background-color: #E6F0FA; padding: 20px; border-radius: 8px; border-left: 5px solid #0A2540; min-height: 550px;">
                <h3 style="color: #0A2540; margin-top: 0; margin-bottom: 18px; font-family: sans-serif;"><b>Datos de los componentes</b></h3>
                <table class="tabla-resultados">
                    <tr><td class="lbl">Peso molecular de CO₂ (g/mol)</td><td class="val">{PM_CO2:.4f}</td></tr>
                    <tr><td class="lbl">Peso molecular de MEA (g/mol)</td><td class="val">{PM_MEA:.4f}</td></tr>
                    <tr><td class="lbl">Peso molecular de O₂ (g/mol)</td><td class="val">{PM_O2:.4f}</td></tr>
                    <tr><td class="lbl">Peso molecular de N₂ (g/mol)</td><td class="val">{PM_N2:.4f}</td></tr>
                    <tr><td class="lbl">Peso molecular del H₂O (g/mol)</td><td class="val">{PM_H2O:.4f}</td></tr>
                    <tr><td class="lbl">Peso molecular promedio de la solución (g/mol)</td><td class="val">{PM_sol_visual:.4f}</td></tr>
                    <tr><td class="lbl">Presión total del sistema (atm)</td><td class="val">1.2000</td></tr>
                    <tr><td class="lbl">Presión total del sistema (mmHg)</td><td class="val">{PT_mmHg:.4f}</td></tr>
                    <tr><td class="lbl">Presión parcial de CO₂ en el fondo (mmHg)</td><td class="val">{P_CO2_fondo:.4f}</td></tr>
                    <tr><td class="lbl">Relación molar de entrada G1 (CO₂)</td><td class="val">{g1_co2_visual:.4f}</td></tr>
                    <tr><td class="lbl">Relación molar de entrada G1 (N₂)</td><td class="val">{g1_n2_visual:.4f}</td></tr>
                    <tr><td class="lbl">Relación molar de entrada G1 (O₂)</td><td class="val">{g1_o2_visual:.4f}</td></tr>
                    <tr><td class="lbl">Fracción molar de salida G2 (CO₂)</td><td class="val">{g2_co2_visual:.4f}</td></tr>
                    <tr><td class="lbl">Fracción molar de salida G2 (N₂)</td><td class="val">{g2_n2_visual:.4f}</td></tr>
                    <tr><td class="lbl">Fracción molar de salida G2 (O₂)</td><td class="val">{g2_o2_visual:.4f}</td></tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col_der:
        st.markdown(
            f"""
            <div style="background-color: #FFF9E6; padding: 20px; border-radius: 8px; border-left: 5px solid #D4AF37; min-height: 550px;">
                <h3 style="color: #8A6D1C; margin-top: 0; margin-bottom: 18px; font-family: sans-serif;"><b>Cálculos intermedios</b></h3>
                <table class="tabla-resultados">
                    <tr><td class="lbl">Composición de equilibrio (X₁*)</td><td class="val">{X1_star:.4f}</td></tr>
                    <tr><td class="lbl">Composición del líquido en el domo (X₂)</td><td class="val">{X2:.4f}</td></tr>
                    <tr><td class="lbl">Relación molar en el fondo (Y₁)</td><td class="val">{Y1:.4f}</td></tr>
                    <tr><td class="lbl">Relación molar en el domo (Y₂)</td><td class="val">{Y2:.4f}</td></tr>
                    <tr><td class="lbl">Relación líquido/gas mínima (Ls/Gs)_min</td><td class="val">{LsGs_min:.4f}</td></tr>
                    <tr><td class="lbl">Relación líquido/gas de operación (Ls/Gs)_real</td><td class="val">{LsGs_real:.4f}</td></tr>
                    <tr><td class="lbl">Moles totales a 1.0 atm (mol)</td><td class="val">{n_total_m3_1atm:.4f}</td></tr>
                    <tr><td class="lbl">Gas inerte estándar Gs a 1.0 atm (mol/m³)</td><td class="val">{Gs_1atm:.4f}</td></tr>
                    <tr><td class="lbl">Moles totales en operación a 1.2 atm (mol)</td><td class="val">{n_total_m3_real:.4f}</td></tr>
                    <tr><td class="lbl">Gas inerte real Gs a 1.2 atm (mol/m³)</td><td class="val">{Gs_real:.4f}</td></tr>
                    <tr><td class="lbl">Flujo molar de líquido inerte Ls (mol)</td><td class="val">{Ls_real:.4f}</td></tr>
                    <tr><td class="lbl">Masa total de solución absorbente (kg)</td><td class="val">{kg_solucion_m3:.4f}</td></tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    # ==========================================================================
    # SECCIÓN DE RESULTADOS FINALES (CUADROS INDEPENDIENTES EN MORADO CLARO)
    # ==========================================================================
    
    st.markdown("---")
    st.markdown("<h3 style='color: #0A2540; font-family: sans-serif;'><b>Resultados finales</b></h3>", unsafe_allow_html=True)
    
    st.markdown("*Todos los resultados se presentan en notación decimal estándar para su lectura:*")
    st.markdown("") # Espacio

    # 1. Declaramos el estilo CSS puro (Sin la 'f' para evitar errores de código en pantalla)
    st.markdown(
        """
        <style>
            .tarjeta-morada-individual {
                background-color: #F3E8FF; 
                padding: 14px 18px; 
                border-radius: 8px; 
                margin-bottom: 15px;
                font-family: sans-serif;
                color: #2D3748;
                box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            }
        </style>
        """, 
        unsafe_allow_html=True
    )

    # 2. Imprimimos cada cuadro de forma separada inyectando los datos con formato de 4 decimales
    st.markdown(f'<div class="tarjeta-morada-individual"><b>A)</b> Relación líquido/gas mínima (Ls/Gs)_min: {LsGs_min:.4f} mol/mol</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="tarjeta-morada-individual"><b>B)</b> Relación molar del gas en el domo de la torre (Y₂): {Y2:.4f} mol CO₂/mol inerte</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="tarjeta-morada-individual"><b>C)</b> Relación molar del líquido a la entrada de la torre (X₂): {X2:.4f} mol CO₂/mol sol</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="tarjeta-morada-individual"><b>D)</b> Relación molar del gas en el fondo de la torre (Y₁): {Y1:.4f} mol CO₂/mol inerte</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="tarjeta-morada-individual"><b>E)</b> Relación molar de equilibrio en el fondo (X₁*): {X1_star:.4f} mol CO₂/mol sol</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="tarjeta-morada-individual"><b>F)</b> Flujo de gas inerte Gs (para 1 m³ de G₁): {Gs_real:.4f} mol/m³</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="tarjeta-morada-individual"><b>G)</b> Masa de solución por m³ (a {factor_min:.4f} veces): {kg_solucion_m3:.4f} kg/m³</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="tarjeta-morada-individual"><b>H)</b> Moles de CO₂ transportados en la corriente L₂: {moles_CO2_L2:.4f} mol/m³</div>', unsafe_allow_html=True)
