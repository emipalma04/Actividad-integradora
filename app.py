import streamlit as st
import numpy as np

# Configuración de la página web
st.set_page_config(page_title="ACTIVIDAD INTEGRADORA", layout="centered")

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

# Datos del estudiante (Tus correcciones de formato exactas)
st.markdown("**MATERIA:** Operaciones Unitarias II")
st.markdown("**ACTIVIDAD:** Participación #4 (Unidad #3)")
st.markdown("**PROYECTO:** Simulador de Absorbedor de CO₂ en una Torre Empacada")
st.markdown("**CATEDRÁTICO:** Dr. Ildebrando Pérez Reyes")
st.markdown("**ALUMNO:** Gerardo Emiliano Palma Chávez")
st.markdown("---")

st.markdown("<h3 style='color: #0A2540;'>INSTRUCCIONES</h3>", unsafe_allow_html=True)
st.write("Modifica los parámetros según lo requieras y haz clic en el botón de abajo para actualizar de forma automática los resultados del modelo.")

# Formulario para las entradas del usuario
with st.form("simulador_form"):
    st.markdown("<h3 style='color: #0A2540;'>1. Entradas de Diseño</h3>", unsafe_allow_html=True)
    
    C_MEA = st.number_input("Concentración de la solución de MEA (% en peso) [Sugerido: 30]", min_value=0.0, max_value=100.0, value=30.0, step=1.0)
    
    st.markdown("<h4 style='color: #0A2540;'>Composición del Gas de Entrada (Fondo) - G1</h4>", unsafe_allow_html=True)
    y1_CO2_pct = st.number_input("Porcentaje de CO₂ (% en volumen) [Sugerido: 15]", min_value=0.0, max_value=100.0, value=15.0, format="%.2f")
    y1_O2_pct  = st.number_input("Porcentaje de O₂  (% en volumen) [Sugerido: 6]", min_value=0.0, max_value=100.0, value=6.0, format="%.2f")
    y1_N2_pct  = st.number_input("Porcentaje de N₂  (% en volumen) [Sugerido: 79]", min_value=0.0, max_value=100.0, value=79.0, format="%.2f")
    
    st.markdown("<h4 style='color: #0A2540;'>Condiciones Operativas del Sistema</h4>", unsafe_allow_html=True)
    x2_input = st.number_input("Concentración del líquido en el domo (mol CO2/mol sol) [Sugerido: 0.058]", min_value=0.0, max_value=1.0, value=0.058, format="%.3f")
    factor_min = st.number_input("Multiplicador de la relación Ls-min/Gs (Exceso) [Sugerido: 1.2]", min_value=1.0, max_value=5.0, value=1.2, step=0.1)
    y2_CO2_pct = st.number_input("Concentración de CO₂ deseada en el gas de salida (%) [Sugerido: 2]", min_value=0.0, max_value=100.0, value=2.0, format="%.2f")
    
    submit_button = st.form_submit_button(label="Correr Simulación")

# ==============================================================================
# ALGORITMO MATEMÁTICO REAL EXTRAÍDO DE TU SCRIPT
# ==============================================================================
if submit_button:
    # Conversión de porcentajes a fracciones molares (y)
    y1_CO2 = y1_CO2_pct / 100.0
    y2_CO2 = y2_CO2_pct / 100.0

    # Constantes físicas exactas
    T_K = 25.0 + 273.15          
    R = 0.0820574614             

    PM_CO2 = 44.009
    PM_MEA = 61.080
    PM_O2  = 31.999
    PM_N2  = 28.013
    PM_H2O = 18.015

    # Tabla de equilibrio (25°C, MEA 30%)
    x_table = np.array([0.058, 0.060, 0.062, 0.064, 0.066, 0.068, 0.070])
    P_table = np.array([5.6, 12.8, 29.0, 56.0, 98.7, 155.0, 232.0])

    # Relaciones molares de operación
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

    # Variables auxiliares de la interfaz de Excel
    PM_sol_visual = (w_MEA * PM_MEA) + (w_H2O * PM_H2O)

    g1_co2_visual = y1_CO2 / (1.0 - y1_CO2)
    g1_n2_visual = (y1_N2_pct / 100.0) / ((y1_N2_pct / 100.0) + 1.0)
    g1_o2_visual = (y1_O2_pct / y1_N2_pct) * 7.9

    g2_co2_visual = y2_CO2
    g2_n2_visual = 1.0 - y2_CO2
    g2_o2_visual = 1.0 - y2_CO2

    # ==========================================================================
    # INYECCIÓN DE CSS AISLADA
    # ==========================================================================
    st.markdown(
        """
        <style>
            .tabla-resultados { width: 100%; border-collapse: collapse; font-family: 'Segoe UI', sans-serif; }
            .tabla-resultados td { padding: 4.5px 0; border-bottom: 1px solid rgba(0,0,0,0.04); font-size: 13px; }
            .tabla-resultados tr:last-child td { border-bottom: none; }
            .lbl { font-weight: 600; color: #4A5568; }
            .val { text-align: right; font-family: monospace; font-weight: bold; color: #1A202C; }
        </style>
        """, 
        unsafe_allow_html=True
    )

    st.markdown("---")
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        # Bloque de Datos de los Componentes (ORDEN Y CONTENIDO EXACTO DE TU SCRIPT)
        st.markdown(
            f"""
            <div style="background-color: #E6F0FA; padding: 18px; border-radius: 8px; border-left: 5px solid #0A2540; min-height: 520px;">
                <h3 style="color: #0A2540; margin-top: 0; margin-bottom: 15px; font-family: sans-serif;"><b>DATOS DE LOS COMPONENTES</b></h3>
                <table class="tabla-resultados">
                    <tr><td class="lbl">PM A (CO2) (g/mol)</td><td class="val">{PM_CO2:.3f}</td></tr>
                    <tr><td class="lbl">PM B (MEA) (g/mol)</td><td class="val">{PM_MEA:.3f}</td></tr>
                    <tr><td class="lbl">PM C (O2) (g/mol)</td><td class="val">{PM_O2:.3f}</td></tr>
                    <tr><td class="lbl">PM D (N2) (g/mol)</td><td class="val">{PM_N2:.3f}</td></tr>
                    <tr><td class="lbl">PM H2O (g/mol)</td><td class="val">{PM_H2O:.3f}</td></tr>
                    <tr><td class="lbl">PM sol (g/mol)</td><td class="val">{PM_sol_visual:.3f}</td></tr>
                    <tr><td class="lbl">PT (atm)</td><td class="val">1.200</td></tr>
                    <tr><td class="lbl">PT (mmHg)</td><td class="val">{PT_mmHg:.3f}</td></tr>
                    <tr><td class="lbl">PCO2 (mmHg)</td><td class="val">{P_CO2_fondo:.3f}</td></tr>
                    <tr><td class="lbl">G1 CO2</td><td class="val">{g1_co2_visual:.6f}</td></tr>
                    <tr><td class="lbl">G1 N2</td><td class="val">{g1_n2_visual:.6f}</td></tr>
                    <tr><td class="lbl">G1 O2</td><td class="val">{g1_o2_visual:.3f}</td></tr>
                    <tr><td class="lbl">G2 CO2</td><td class="val">{g2_co2_visual:.3f}</td></tr>
                    <tr><td class="lbl">G2 N2</td><td class="val">{g2_n2_visual:.3f}</td></tr>
                    <tr><td class="lbl">G2 O2</td><td class="val">{g2_o2_visual:.3f}</td></tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col_der:
        # Bloque de Cálculos Intermedios (ORDEN Y CONTENIDO EXACTO DE TU SCRIPT)
        st.markdown(
            f"""
            <div style="background-color: #FFF9E6; padding: 18px; border-radius: 8px; border-left: 5px solid #D4AF37; min-height: 520px;">
                <h3 style="color: #8A6D1C; margin-top: 0; margin-bottom: 15px; font-family: sans-serif;"><b>CÁLCULOS INTERMEDIOS</b></h3>
                <table class="tabla-resultados">
                    <tr><td class="lbl">X1</td><td class="val">{X1_star:.6f}</td></tr>
                    <tr><td class="lbl">X2</td><td class="val">{X2:.6f}</td></tr>
                    <tr><td class="lbl">Y1</td><td class="val">{Y1:.6f}</td></tr>
                    <tr><td class="lbl">Y2</td><td class="val">{Y2:.6f}</td></tr>
                    <tr><td class="lbl">(Ls/Gs)_min</td><td class="val">{LsGs_min:.6f}</td></tr>
                    <tr><td class="lbl">(Ls/Gs)_real</td><td class="val">{LsGs_real:.6f}</td></tr>
                    <tr><td class="lbl">nT 1.0 atm (mol)</td><td class="val">{n_total_m3_1atm:.6f}</td></tr>
                    <tr><td class="lbl">Gs 1.0 atm (mol/m³)</td><td class="val">{Gs_1atm:.6f}</td></tr>
                    <tr><td class="lbl">nT 1.2 atm (mol)</td><td class="val">{n_total_m3_real:.6f}</td></tr>
                    <tr><td class="lbl">Gs 1.2 atm (mol/m³)</td><td class="val">{Gs_real:.6f}</td></tr>
                    <tr><td class="lbl">Ls (mol)</td><td class="val">{Ls_real:.6f}</td></tr>
                    <tr><td class="lbl">mT (Kg)</td><td class="val">{kg_solucion_m3:.6f}</td></tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ==========================================================================
    # SECCIÓN DE RESULTADOS FINALES (FORMATO EXACTO DE TU PRINT FINAL)
    # ==========================================================================
    st.markdown("<br><h3 style='color: #0A2540; text-align: center;'><b>RESULTADOS FINALES</b></h3>", unsafe_allow_html=True)
    
    st.markdown(
        f"""
        <div style="background-color: #F4F6F8; padding: 20px; border-radius: 8px; border-top: 4px solid #0A2540; font-family: sans-serif;">
            <p style="font-size: 14.5px; color: #4A5568;">Todos los resultados se presentan en notación decimal estándar para su lectura:</p>
            <p style="margin: 6px 0;"><b>A) Relación líquido/gas mínima (Ls/Gs)_min:</b> <span style="font-family: monospace; font-weight: bold;">{LsGs_min:.6f}</span> mol/mol</p>
            <p style="margin: 6px 0;"><b>B) Relación molar en el domo de la torre (Y₂):</b> <span style="font-family: monospace; font-weight: bold;">{Y2:.6f}</span> mol CO2/mol inerte</p>
            <p style="margin: 6px 0;"><b>C) Relación molar en el domo de la torre (X₂):</b> <span style="font-family: monospace; font-weight: bold;">{X2:.6f}</span> mol CO2/mol sol</p>
            <p style="margin: 6px 0;"><b>D) Relación molar en el fondo de la torre (Y₁):</b> <span style="font-family: monospace; font-weight: bold;">{Y1:.6f}</span> mol CO2/mol inerte</p>
            <p style="margin: 6px 0;"><b>E) Relación molar de equilibrio en fondo (X₁*):</b> <span style="font-family: monospace; font-weight: bold;">{X1_star:.6f}</span> mol CO2/mol sol</p>
            <p style="margin: 6px 0;"><b>F) Flujo de gas inerte Gs (mol/m³) [1 m³ de G₁]:</b> <span style="font-family: monospace; font-weight: bold;">{Gs_real:.6f}</span> mol/m³</p>
            <p style="margin: 6px 0;"><b>G) Masa de solución por m³ (a {factor_min:.1f} veces):</b> <span style="font-family: monospace; font-weight: bold;">{kg_solucion_m3:.6f}</span> kg/m³</p>
            <p style="margin: 6px 0;"><b>H) Moles de CO₂ transportados en la corriente L₂:</b> <span style="font-family: monospace; font-weight: bold;">{moles_CO2_L2:.6f}</span> mol/m³</p>
        </div>
        """,
        unsafe_allow_html=True
    )
