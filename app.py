import streamlit as st
import numpy as np

# Configuración de la página web
st.set_page_config(page_title="Simulador UACh", layout="centered")

# Encabezado institucional
st.title("UNIVERSIDAD AUTÓNOMA DE CHIHUAHUA")
st.subheader("Facultad de Ciencias Químicas")
st.markdown("**MATERIA:** Operaciones Unitarias II")
st.markdown("**PROYECTO:** Simulador de Absorbedor de CO₂ en una Torre Empacada")
st.markdown("**CATEDRÁTICO:** Dr. Ildebrando Pérez Reyes")
st.markdown("**ALUMNO:** Gerardo Emiliano Palma Chávez")
st.divider()

st.header("1. Entradas de Diseño")

# Cajas de entrada numéricas interactivas
C_MEA = st.number_input("Concentración de la solución de MEA (% en peso)", value=30.0)

st.subheader("Composición del gas de entrada (%)")
y1_CO2_pct = st.number_input("Porcentaje de CO₂ (% vol)", value=15.0)
y1_O2_pct = st.number_input("Porcentaje de O₂ (% vol)", value=6.0)
y1_N2_pct = st.number_input("Porcentaje de N₂ (% vol)", value=79.0)

st.subheader("Parámetros operativos")
x2_input = st.number_input("Composición de la solución de entrada (X₂ - mol CO2/mol sol)", value=0.058, format="%.3f")
factor_min = st.number_input("Multiplicador de la relación Ls-min/Gs (Exceso)", value=1.2)
y2_CO2_pct = st.number_input("Composición del CO₂ en el gas de salida (%)", value=2.0)

# --- CÁLCULOS MATEMÁTICOS ---
y1_CO2 = y1_CO2_pct / 100.0
y2_CO2 = y2_CO2_pct / 100.0

T_K = 25.0 + 273.15          
R = 0.0820574614             

PM_CO2, PM_MEA, PM_O2, PM_N2, PM_H2O = 44.009, 61.080, 31.999, 28.013, 18.015

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
PM_sol_kg_mol = (1.0 / moles_por_gramo) / 1000.0

kg_solucion_m3 = Ls_real * PM_sol_kg_mol
moles_CO2_L2 = Ls_real * X2

PM_sol_visual = (w_MEA * PM_MEA) + (w_H2O * PM_H2O)
g1_co2_visual = y1_CO2 / (1.0 - y1_CO2)

# --- DESPLIEGUE DE RESULTADOS EN LA WEB ---
if st.button("Correr Simulación"):
    st.divider()
    st.header("Resultados de la Simulación")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Datos del Sistema")
        st.write(f"**PM sol:** {PM_sol_visual:.3f} g/mol")
        st.write(f"**PT:** {PT_mmHg:.3f} mmHg")
        st.write(f"**PCO₂ fondo:** {P_CO2_fondo:.3f} mmHg")
        st.write(f"**G₁ CO₂:** {g1_co2_visual:.6f}")
        
    with col2:
        st.subheader("Cálculos Operativos")
        st.write(f"**X₁\* (Equilibrio):** {X1_star:.6f}")
        st.write(f"**Relación (Ls/Gs) mín:** {LsGs_min:.6f}")
        st.write(f"**Relación (Ls/Gs) real:** {LsGs_real:.6f}")
        st.write(f"**Gs (1.2 atm):** {Gs_real:.6f} mol/m³")
        st.write(f"**Ls (Líquido inerte):** {Ls_real:.6f} mol/m³")
    
    st.success("Respuestas oficiales para el cuestionario:")
    st.info(f"**A) (Ls/Gs)_min:** {LsGs_min:.6f} mol/mol")
    st.info(f"**B) Y₂ (Domo):** {Y2:.6f} mol CO2/mol inert")
    st.info(f"**C) X₂ (Domo):** {X2:.6f} mol CO2/mol sol")
    st.info(f"**D) Y₁ (Fondo):** {Y1:.6f} mol CO2/mol inert")
    st.info(f"**E) X₁\* (Equilibrio):** {X1_star:.6f} mol CO2/mol sol")
    st.info(f"**F) Gs (mol/m³):** {Gs_real:.6f} mol/m³")
    st.info(f"**G) Masa de solución:** {kg_solucion_m3:.6f} kg/m³")
    st.info(f"**H) Moles CO₂ en L₂:** {moles_CO2_L2:.6f} mol/m³")
