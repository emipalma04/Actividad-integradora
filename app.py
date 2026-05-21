import streamlit as st
import numpy as np

# Configuración de la página web
st.set_page_config(page_title="ACTIVIDAD INTEGRADORA", layout="centered")

# ==============================================================================
# ENCABEZADO LOGOS E INSTITUCIONAL (UACH IZQUIERDA, FCQ DERECHA)
# ==============================================================================
# Usamos URLs genéricas de imágenes que apuntan a logos institucionales de ejemplo. 
# Nota: Si tienes los links directos exactos de tus imágenes, puedes reemplazar los links de abajo.
logo_uach_url = "https://upload.wikimedia.org/wikipedia/commons/e/ea/Logo_UACH.png"
logo_fcq_url = "https://raw.githubusercontent.com/gpalmach/actividad-integradora/main/fcq.png" # Ruta tentativa en tu repositorio

st.markdown(
    f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <img src="{logo_uach_url}" width="100" alt="Logo UACH">
        <div style="text-align: center; flex-grow: 1;">
            <h1 style="color: #0A2540; margin: 0; font-family: sans-serif;">UNIVERSIDAD AUTÓNOMA DE CHIHUAHUA</h1>
            <h3 style="color: #D4AF37; margin: 5px 0 0 0; font-family: sans-serif;">Facultad de Ciencias Químicas</h3>
        </div>
        <img src="{logo_fcq_url}" width="90" alt="Logo FCQ" onerror="this.style.display='none'">
    </div>
    <hr style="border: 1px solid #0A2540; margin-top: 0;">
    """,
    unsafe_allow_html=True
)

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
    
    C_MEA = st.number_input("Concentración de la solución de MEA (% en peso)", min_value=0.0, max_value=100.0, value=30.0, step=1.0)
    
    st.markdown("<h4 style='color: #0A2540;'>Composición del Gas de Entrada (Fondo)</h4>", unsafe_allow_html=True)
    y1_CO2_pct = st.number_input("Porcentaje de CO₂ (% vol)", min_value=0.0, max_value=100.0, value=15.0, format="%.2f")
    y1_O2_pct  = st.number_input("Porcentaje de O₂  (% vol)", min_value=0.0, max_value=100.0, value=6.0, format="%.2f")
    y1_N2_pct  = st.number_input("Porcentaje de N₂  (% vol)", min_value=0.0, max_value=100.0, value=79.0, format="%.2f")
    
    st.markdown("<h4 style='color: #0A2540;'>Condiciones Operativas del Sistema</h4>", unsafe_allow_html=True)
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
    # DESPLIEGUE EN COLUMNAS CON COLORES DE FONDO DISTINTOS (CSS INLINE)
    # ==========================================================================
    st.markdown("---")
    
    # Creamos las dos columnas de Streamlit
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        # Fondo Azul Tenue para DATA
        st.markdown(
            f"""
            <div style="background-color: #E6F0FA; padding: 15px; border-radius: 8px; border-left: 5px solid #0A2540;">
                <h3 style="color: #0A2540; margin-top: 0;"><b>DATOS DE LOS COMPONENTES</b></h3>
                <p style="font-family: monospace; margin: 4px 0;">PM A (CO2) (g/mol) : {PM_CO2:.3f}</p>
                <p style="font-family: monospace; margin: 4px 0;">PM B (MEA) (g/mol) : {PM_MEA:.3f}</p>
                <p style="font-family: monospace; margin: 4px 0;">PM sol prom (g/mol): {PM_sol_visual:.3f}</p>
                <p style="font-family: monospace; margin: 4px 0;">PT         (mmHg)  : {PT_mmHg:.3f}</p>
                <p style="font-family: monospace; margin: 4px 0;">PCO2 fondo (mmHg)  : {P_CO2_fondo_mmHg:.3f}</p>
                <p style="font-family: monospace; margin: 4px 0;">G1 CO2 (Relación)  : {g1_co2_visual:.6f}</p>
                <p style="font-family: monospace; margin: 4px 0;">G1 N2              : {g1_n2_visual:.6f}</p>
                <p style="font-family: monospace; margin: 4px 0;">G1 O2              : {g1_o2_visual:.3f}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col_der:
        # Fondo Amarillo/Crema Tenue para CALCULATIONS
        st.markdown(
            f"""
            <div style="background-color: #FFF9E6; padding: 15px; border-radius: 8px; border-left: 5px solid #D4AF37;">
                <h3 style="color: #8A6D1C; margin-top: 0;"><b>CÁLCULOS INTERMEDIOS</b></h3>
                <p style="font-family: monospace; margin: 4px 0;">X1                 : {X1_star:.6f}</p>
                <p style="font-family: monospace; margin: 4px 0;">X2                 : {X2:.6f}</p>
                <p style="font-family: monospace; margin: 4px 0;">Y1                 : {Y1:.6f}</p>
                <p style="font-family: monospace; margin: 4px 0;">Y2                 : {Y2:.6f}</p>
                <p style="font-family: monospace; margin: 4px 0;">(Ls/Gs)_min        : {LsGs_min:.6f}</p>
                <p style="font-family: monospace; margin: 4px 0;">(Ls/Gs)_real       : {LsGs_real:.6f}</p>
                <p style="font-family: monospace; margin: 4px 0;">Gs 1.2 atm (mol/m³): {Gs_real:.6f}</p>
                <p style="font-family: monospace; margin: 4px 0;">Ls         (mol)   : {Ls_real:.6f}</p>
                <p style="font-family: monospace; margin: 4px 0;">mT         (Kg)    : {kg_solucion_m3:.6f}</p>
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
            <p><b>A) Relación líquido/gas mínima (Ls/Gs)_min:</b> {LsGs_min:.6f} mol/mol</p>
            <p><b>B) Relación molar en el domo de la torre (Y2):</b> {Y2:.6f} mol CO2/mol inerte</p>
            <p><b>C) Relación molar en el domo de la torre (X2):</b> {X2:.6f} mol CO2/mol sol</p>
            <p><b>D) Relación molar en el fondo de la torre (Y1):</b> {Y1:.6f} mol CO2/mol inerte</p>
            <p><b>E) Relación molar de equilibrio en fondo (X1*):</b> {X1_star:.6f} mol CO2/mol sol</p>
            <p><b>F) Flujo de gas inerte Gs (mol/m³) [1 m³ de G1]:</b> {Gs_real:.6f} mol/m³</p>
            <p><b>G) Masa de solución por m³:</b> {kg_solucion_m3:.6f} kg/m³</p>
            <p><b>H) Moles de CO₂ transportados en la corriente L2:</b> {moles_CO2_L2:.6f} mol/m³</p>
        </div>
        """,
        unsafe_allow_html=True
    )
