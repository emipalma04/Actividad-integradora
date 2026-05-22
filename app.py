import streamlit as st
import numpy as np

# Configuración de la página web
st.set_page_config(page_title="Simulador de Absorción - Operaciones Unitarias II", layout="centered") 

# ==============================================================================
# ENCABEZADO INSTITUCIONAL
# ==============================================================================
img_col_izq, texto_col_centro, img_col_der = st.columns([1, 4, 1])

with img_col_izq:
    st.image("https://raw.githubusercontent.com/emipalma04/Actividad-integradora/main/Logo%20UACH.png", width=90)

with texto_col_centro:
    st.markdown(
        """
        <div style="text-align: center;">
            <h1 style="color: #0A2540; margin: 0; font-family: sans-serif; font-size: 26px;"><b>UNIVERSIDAD AUTÓNOMA DE CHIHUAHUA</b></h1>
            <h3 style="color: #D4AF37; margin: 5px 0 0 0; font-family: sans-serif; font-size: 18px;"><b>Facultad de Ciencias Químicas</b></h3>
        </div>
        """, 
        unsafe_allow_html=True
    )

with img_col_der:
    st.image("https://raw.githubusercontent.com/emipalma04/Actividad-integradora/main/FCQ.png", width=57)

st.markdown("<hr style='border: 1px solid #0A2540; margin-top: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)

# Título del Proyecto Integrador y Datos del Estudiante (Conforme a la Portada del PDF)
st.markdown("<h2 style='color: #0A2540; font-family: sans-serif; font-size: 24px; margin-bottom: 15px;'><b>Modelación Matemático-Computacional de Procesos de Separación</b></h2>", unsafe_allow_html=True)
st.markdown("**Unidad de Aprendizaje:** Operaciones Unitarias II")
st.markdown("**Proyecto Integrador:** Solución automatizada y análisis analítico del sistema de absorción de $CO_2$ mediante soluciones acuosas de Monoetanolamina (MEA)")
st.markdown("**Desarrollado por:** Gerardo Emiliano Palma Chávez")
st.markdown("---")

# ==============================================================================
# GUÍA DE USO Y DIAGRAMA DE FLUJO DE APOYO
# ==============================================================================
st.markdown("<h3 style='color: #0A2540;'>Instrucciones de Operación</h3>", unsafe_allow_html=True)
st.write(
    "Este simulador automatiza el cálculo de las condiciones operacionales y relaciones de equilibrio para una columna de absorción empacada. "
    "El programa permite evaluar la sensibilidad del proceso modificando dinámicamente la concentración del solvente, "
    "las mezclas de gas alimentadas y las condiciones reales de exceso en la relación líquido/gas."
)

st.info(
    "💡 **Nota sobre los datos:** Todos los valores que requieran porcentaje (%) deben introducirse en una escala de 0 a 100. "
    "Por ejemplo, si desea ingresar un treinta por ciento, introduzca **30.0** (no escriba 0.3)."
)

st.warning(
    "📌 **Nota de diseño:** Los valores numéricos precargados de forma predeterminada en el formulario "
    "corresponden exactamente a las especificaciones y datos base del ejercicio clásico U3-P4."
)

# DIAGRAMA DE FLUJO EN INGLÉS (Requerido para soporte visual)
st.markdown("---")
st.markdown("<h4 style='color: #0A2540; text-align: center;'>Absorption of $CO_2$ in a packed absorber</h4>", unsafe_allow_html=True)
st.write(
    "Como apoyo para la interpretación de los resultados y balances, el siguiente diagrama ilustra "
    "el flujo a contracorriente de la torre, donde el gas alimentado asciende desde la parte inferior "
    "y se encuentra con el líquido absorbente que desciende desde la parte superior."
)

# Insertamos la imagen del diagrama de flujo como soporte conceptual
st.image("https://raw.githubusercontent.com/emipalma04/Actividad-integradora/main/Diagrama%20Torre.png", caption="Figura 1: Absorption of CO2 in a packed absorber (Countercurrent flow).", use_container_width=True)
st.markdown("---")


# ==============================================================================
# FORMULARIO DE ENTRADAS DE DISEÑO
# ==============================================================================
with st.form("simulador_form"):
    st.markdown("<h3 style='color: #0A2540;'>Variables de Entrada del Proceso</h3>", unsafe_allow_html=True)
    
    C_MEA = st.number_input("Concentración inicial de la solución de MEA (% en peso, ej. 30.0 = 30%)", min_value=0.0, max_value=100.0, value=30.0, step=1.0, format="%.4f")
    
    st.markdown("<h4 style='color: #0A2540;'>Composición del Gas de Entrada (Parte Inferior - Corriente $G_1$)</h4>", unsafe_allow_html=True)
    y1_CO2_pct = st.number_input("Porcentaje volumétrico de $CO
