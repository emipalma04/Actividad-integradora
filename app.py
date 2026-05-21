import streamlit as st
import numpy as np

# Configuración de la página web (Evita que se rompa al iniciar)
st.set_page_config(page_title="Simulador CO2 UACh", layout="centered")

# ==============================================================================
# ENCABEZADO ACADÉMICO OFICIAL UACH
# ==============================================================================
st.title("UNIVERSIDAD AUTÓNOMA DE CHIHUAHUA")
st.subheader("Facultad de Ciencias Químicas")
st.markdown("---")
st.markdown("**MATERIA:** Operaciones Unitarias II")
st.markdown("**ACTIVIDAD:** Participación #4 (Unidad #3)")
st.markdown("**PROYECTO:** Simulador de Absorbedor de CO₂ en una Torre Empacada")
st.markdown("**CATEDRÁTICO:** Dr. Ildebrando Pérez Reyes")
st.markdown("**ALUMNO:** Gerardo Emiliano Palma Chávez")
st.markdown("---")

st.markdown("### [ INSTRUCCIONES DE OPERACIÓN ]")
st.write("Introduce o modifica los datos en las casillas de abajo. Al finalizar, presiona el botón **'Correr Simulación'** para desplegar las tablas de datos y respuestas de tu Excel.")

# Formulario protegido para que Streamlit NO intente calcular antes de meter los datos
with st.form("simulador_form"):
    st.header("1. Entradas de Diseño")
    
    C_MEA = st.number_input("Concentración de la solución de MEA (% en peso)", min_value=0.0, max_value=100.0, value=30.0, step=1.0)
    
    st.subheader("Composición del gas que entra por el fondo (G1)")
    y1_CO2_pct = st.number_input("Porcentaje de CO₂ (% en volumen)", min_value=0.0, max_value=100.0, value=15.0, step=1.0)
    y1_O2_pct  = st.number_input("Porcentaje de O₂  (% en volumen)", min_value=0.0, max_value=100.0, value=6.0, step=1.0)
    y1_N2_pct  = st.number_input("Porcentaje de N₂  (% en volumen)", min_value=0.0, max_value=100.0, value=79.0, step=1.0)
    
    st.subheader("Parámetros operativos y condiciones límite")
    x2_input = st.number_input("Concentración del líquido en el domo (mol CO2/mol sol) [X2]", min_value=0.0, max_value=1.0, value=0.058, format="%.3f")
    factor_min = st.number_input("Multiplicador de la relación Ls-min/Gs (Exceso)", min_value=1.0, max_value=5.0, value=1.2, step=0.1)
    y2_CO2_pct = st.number_input("Concentración de CO₂ deseada en el gas de salida (%)", min_value=0.0, max_value=100.0, value=2.0, step=0.5)
    
    # Botón disparador
    submit_button = st.form_submit_button(label="Correr Simulación")

# ==============================================================================
# ALGORITMO MATEMÁTICO (SOLO SE EJECUTA SI LE DAS CLIC AL BOTÓN)
# ==============================================================================
if submit_button:
    # Conversión de porcentajes a fracciones molares (y)
    y1_CO2 = y1_CO2_pct / 100.0
    y2_CO2 = y2_CO2
