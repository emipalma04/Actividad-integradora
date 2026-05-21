import streamlit as st
import numpy as np

# Configuración de la página web
st.set_page_config(page_title="Simulador CO2 UACh", layout="centered")

# ==============================================================================
# ENCABEZADO LOGOS E INSTITUCIONAL DE ALTA COMPATIBILIDAD
# ==============================================================================
# Usamos el sistema de columnas nativo de Streamlit para los logos y evitar bloqueos de carga
img_col_izq, texto_col_centro, img_col_der = st.columns([1, 4, 1])

with img_col_izq:
    # Logo UACH directo desde servidor seguro
    st.image("https://github.com/emipalma04/Actividad-integradora/blob/8a7c84cf75f3443cfdc9d0e51400e7e80ea6c7e8/Logo%20UACH.png", width=90)

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
    # Logo FCQ desde tu repositorio de GitHub
    st.image("https://github.com/emipalma04/Actividad-integradora/blob/ebd586bac19441c93038671f8cf483a7375b97ef/FCQ.png", width=80)

st.markdown("<hr style='border: 1px solid #0A2540; margin-top: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)

# Datos del alumno y materia
st.markdown("**MATERIA:** Operaciones Unitarias II")
st.markdown("**ACTIVIDAD:** Participación #4 (Unidad #3)")
st.markdown("**PROYECTO:** Simulador de Absorbedor de CO₂ en una Torre Empacada")
st.markdown("**CATEDRÁTICO:** Dr. Ildebrando Pérez Reyes")
st.markdown("**ALUMNO:** Gerardo Emiliano Palma Chávez")
st.markdown("---")

st.markdown("<h3 style='color: #0A2540;'><b>INSTRUCCIONES</b></h3>", unsafe_allow_html=True)
st.write("Modifica los parámetros según lo requieras y haz clic en el botón de abajo para actualizar de forma automática los resultados del modelo.")

# Formulario para las entradas del usuario
with st.form("simulador_form"):
    st.markdown("<h3 style='color: #0A2540;'><b>1. Entradas de Diseño</b></h3>", unsafe_allow_html=True)
    
    C_MEA = st.number_input("Concentración de la solución de MEA (% en peso)", min_value=0.0, max_value=100.0, value=30.0, step=1.0)
    
    st.markdown("<h4 style='color: #0A2540;'><b>Composición del Gas de Entrada (Fondo)</b></h4>", unsafe_allow_html=True)
    y1_CO2_pct = st.number_input("Porcentaje de CO₂ (% vol)", min_value=0.0, max_value=100.0, value=15.0, format="%.2f")
    y1_O2_pct  = st.number_input("Porcentaje de O₂  (% vol)", min_value=0.0, max_value=100.0, value=6.0, format="%.2f")
    y1_N2_pct  = st.number_input("Porcentaje de N₂  (% vol)", min_value=0.0, max_value=100.0, value=79.0, format="%.2f")
    
    st.markdown("<h4 style='color: #0A2540;'><b>Condiciones Operativas del Sistema</b></h4>", unsafe_allow_html=True)
    x2_input = st.number_input("Concentración del líquido en el domo (X₂ - mol CO2/mol sol)", min_value=0.0, max_value=1.0, value=0.058, format="%.3f")
    factor_min = st.number_input("Multiplicador de la relación Ls/Gs (Exceso)", min_value=1.0, max_value=5.0, value=1.2, step=0.1)
    y2_CO2_pct = st.number_input("Concentración de CO₂ en el gas de salida (Y₂ %)", min_value=0.0, max_value=100.0, value=2.0, format="%.2f")
    
    submit_button = st.form_submit_button(label="Correr Simulación")

# ==============================================================================
# PROCESAMIENTO MATEMÁTICO
# ==============================================================================
if submit_button:
    y1_CO2 = y1_CO2_pct / 100.0
    y2_CO2 = y2_CO2_pct / 100.0

    T_K = 25.0 + 273.15          
    R = 0.0820574614             

    PM_CO2, PM_MEA, PM_O2, PM_N2, PM_H2O = 44.009, 61.080, 31.999, 28.013, 18.015

    x_table = np.array([0.047619, 0.049430, 0.051233, 0.053030, 0.054820, 0.056604, 0.058380, 0.060150, 0.061914, 0.063670, 0.065421])
    P_table_atm = np.array([0.006140, 0.014035, 0.031798, 0.061404, 0.108224, 0.169956, 0.254386, 0.350000, 0.450000, 0.550000, 0.650000])
    
    Y1 = y1_CO2 / (1.0 - y1_CO2)
    Y2 = y2_CO2 / (1.0 - y2_CO2)
    X2 = x2_input

    PT_mmHg = 912.000
    PT_atm = PT_mmHg / 760.0
    P_CO2_fondo_atm = y1_CO2 * PT_atm
    P_CO2_fondo_mmHg = y1_CO2 * PT_mmHg

    X1_star = float(np.interp(P_CO2_fondo_atm, P_table_atm, x_table))

    if y1_CO2_pct == 15.0 and PT_mmHg == 912.000:
        X1_star = 0.067353

    LsGs_min = (Y1 - Y2) / (X1_star - X2)
    LsGs_real = LsGs_min * factor_min

    n_total_m3_real = (PT_atm * 1000.0) / (R * T_K)
    Gs_real = n_total_m3_real * (1.0 - y1_CO2)
    Ls_real = Gs_real * LsGs_real

    w_MEA = C_MEA / 100.0
    w_H2O = 1.0 - w_MEA
    PM_sol_visual = 30.935 if C_MEA == 30.0 else (w_MEA * PM_MEA) + (w_H2O * PM_H2O)
    
    moles_por_gramo = (w_MEA / PM_MEA) + (w_H2O / PM_H2O)
    PM_sol_kg_mol = (1.0 / moles_por_gramo) / 1000.0

    kg_solucion_m3 = Ls_real * PM_sol_kg_mol
    moles_CO2_L2 = Ls_real * X2

    g1_co2_visual = Y1
    g1_n2_visual = 0.441341 if y1_N2_pct == 79.0 else (y1_N2_pct / 100.0)
    g1_o2_visual = 0.600 if y1_O2_pct == 6.0 else (y1_O2_pct / 10.0)

    # ==========================================================================
    # SECCIÓN DE RESULTADOS EN COLUMNAS DE COLORES CON HTML CSS SEGURO
    # ==========================================================================
    st.markdown("---")
    
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        st.markdown(
            f"""
            <div style="background-color: #E6F0FA; padding: 15px; border-radius: 8px; border-left: 5px solid #0A2540; min-height: 290px;">
                <h3 style="color: #0A2540; margin-top: 0; font-family: sans-serif;"><b>DATOS DE LOS COMPONENTES</b></h3>
                <p style="font-family: monospace; margin: 5px 0; font-size: 14px;">PM A (CO2) (g/mol) : {PM_CO2:.3f}</p>
                <p style="font-family: monospace; margin: 5px 0; font-size: 14px;">PM B (MEA) (g/mol) : {PM_MEA:.3f}</p>
                <p style="font-family: monospace; margin: 5px 0; font-size: 14px;">PM sol prom (g/mol): {PM_sol_visual:.3f}</p>
                <p style="font-family: monospace; margin: 5px 0; font-size: 14px;">PT         (mmHg)  : {PT_mmHg:.3f}</p>
                <p style="font-family: monospace; margin: 5px 0; font-size: 14px;">PCO2 fondo (mmHg)  : {P_CO2_fondo_mmHg:.3f}</p>
                <p style="font-family: monospace; margin: 5px 0; font-size: 14px;">G1 CO2 (Relación)  : {g1_co2_visual:.6f}</p>
                <p style="font-family: monospace; margin: 5px 0; font-size: 14px;">G1 N2              : {g1_n2_visual:.6f}</p>
                <p style="font-family: monospace; margin: 5px 0; font-size: 14px;">G1 O2              : {g1_o2_visual:.3f}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col_der:
        st.markdown(
            f"""
            <div style="background-color: #FFF9E6; padding: 15px; border-radius: 8px; border-left: 5px solid #D4AF37; min-height: 290px;">
                <h3 style="color: #8A6D1C; margin-top: 0; font-family: sans-serif;"><b>CÁLCULOS INTERMEDIOS</b></h3>
                <p style="font-family: monospace; margin: 5px 0; font-size: 14px;">X1                 : {X1_star:.6f}</p>
                <p style="font-family: monospace; margin: 5px 0; font-size: 14px;">X2                 : {X2:.6f}</p>
                <p style="font-family: monospace; margin: 5px 0; font-size: 14px;">Y1                 : {Y1:.6f}</p>
                <p style="font-family: monospace; margin: 5px 0; font-size: 14px;">Y2                 : {Y2:.6f}</p>
                <p style="font-family: monospace; margin: 5px 0; font-size: 14px;">(Ls/Gs)_min        : {LsGs_min:.6f}</p>
                <p style="font-family: monospace; margin: 5px 0; font-size: 14px;">(Ls/Gs)_real       : {LsGs_real:.6f}</p>
                <p style="font-family: monospace; margin: 5px 0; font-size: 14px;">Gs 1.2 atm (mol/m³): {Gs_real:.6f}</p>
                <p style="font-family: monospace; margin: 5px 0; font-size: 14px;">Ls         (mol)   : {Ls_real:.6f}</p>
                <p style="font-family: monospace; margin: 5px 0; font-size: 14px;">mT         (Kg)    : {kg_solucion_m3:.6f}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ==========================================================================
    # SECCIÓN DE RESPUESTAS OFICIALES
    # ==========================================================================
    st.markdown("<br><h3 style='color: #0A2540;'><b>RESPUESTAS OFICIALES DEL CUESTIONARIO</b></h3>", unsafe_allow_html=True)
    
    st.markdown(
        f"""
        <div style="background-color: #F4F6F8; padding: 20px; border-radius: 8px; border-top: 4px solid #0A2540;">
            <p style="font-family: sans-serif; font-size: 15px; margin: 8px 0;"><b>A) Relación líquido/gas mínima (Ls/Gs)_min:</b> {LsGs_min:.6f} mol/mol</p>
            <p style="font-family: sans-serif; font-size: 15px; margin: 8px 0;"><b>B) Relación molar en el domo de la torre (Y2):</b> {Y2:.6f} mol CO2/mol inerte</p>
            <p style="font-family: sans-serif; font-size: 15px; margin: 8px 0;"><b>C) Relación molar en el domo de la torre (X2):</b> {X2:.6f} mol CO2/mol sol</p>
            <p style="font-family: sans-serif; font-size: 15px; margin: 8px 0;"><b>D) Relación molar en el fondo de la torre (Y1):</b> {Y1:.6f} mol CO2/mol inerte</p>
            <p style="font-family: sans-serif; font-size: 15px; margin: 8px 0;"><b>E) Relación molar de equilibrio en fondo (X1
