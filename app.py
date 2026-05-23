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

# Título del Proyecto Integrador y Datos del Estudiante (Conforme a la Portada Oficial)

st.markdown("<h2 style='color: #0A2540; font-family: sans-serif; font-size: 24px; margin-bottom: 15px;'><b> AUTOMATIZACIÓN Y ANÁLISIS DEL PROCESO DE ABSORCIÓN DE CO₂ USANDO SOLUCIONES ACUOSAS DE MONOETANOLAMINA (MEA)</b></h2>", unsafe_allow_html=True)

# ==============================================================================
# GUÍA DE USO Y DIAGRAMA DE FLUJO DE APOYO
# ==============================================================================
st.markdown("<h3 style='color: #0A2540;'>Instrucciones de operación</h3>", unsafe_allow_html=True)
st.write(
    "Este simulador automatiza el cálculo de las condiciones operacionales y relaciones de equilibrio para una columna de absorción empacada. "
    "El programa permite evaluar la sensibilidad del proceso modificando dinámicamente la concentración del solvente, "
    "las mezclas de gas alimentadas y las condiciones reales de exceso en la relación líquido/gas."
)

st.info(
    "💡 **Nota sobre los datos:** Todos los valores que requieran porcentaje (%) deben introducirse en una escala de 0 a 100. "
    "Por ejemplo, si desea ingresar un 25%, introduzca **25.0** (no escriba 0.25)."
)

# DIAGRAMA DE FLUJO EN INGLÉS (Requerido para soporte visual)
st.markdown("---")
st.markdown(
    "<h4 style='color: #0A2540; text-align: center;'>"
    "Esquema del sistema "
    "</h4>",
    unsafe_allow_html=True
)
st.write(
    "Como apoyo para la interpretación de los resultados y balances, el siguiente diagrama ilustra "
    "el flujo a contracorriente de la torre, donde el gas alimentado asciende desde la parte inferior "
    "y se encuentra con el líquido absorbente que desciende desde la parte superior."
)

# Insertamos la imagen del diagrama de flujo como soporte conceptual
st.image("https://raw.githubusercontent.com/emipalma04/Actividad-integradora/main/Diagrama.png", caption="Figura 1: Absorption of CO₂ in a Packed Absorber / Absorción de CO₂ en una Torre Empacada.", use_container_width=True)
st.markdown("---")


# ==============================================================================
# FORMULARIO DE ENTRADAS DE DISEÑO
# ==============================================================================
with st.form("simulador_form"):
    st.write("#### :blue[Variables de entrada del proceso]")
    
    C_MEA = st.number_input("Concentración inicial de la solución de MEA (% en peso)", min_value=0.0, max_value=100.0, value=30.0, step=1.0, format="%.4f")
    
    st.write("#### :blue[Composición del Gas de Entrada (Parte Inferior - Corriente G₁)]")
    
    # Inputs numéricos (Se quedan igual)
    y1_CO2_pct = st.number_input("Porcentaje volumétrico de CO₂ (% vol)", min_value=0.0, max_value=100.0, value=15.0, format="%.4f")
    y1_O2_pct  = st.number_input("Porcentaje volumétrico de O₂ (% vol)", min_value=0.0, max_value=100.0, value=6.0, format="%.4f")
    y1_N2_pct  = st.number_input("Porcentaje volumétrico de N₂ (% vol)", min_value=0.0, max_value=100.0, value=79.0, format="%.4f")

    # Inicializamos las variables en el session_state para evitar pérdidas de estado
    if "datos_gas_validos" not in st.session_state:
        st.session_state.datos_gas_validos = False
    if "mensaje_balance" not in st.session_state:
        st.session_state.mensaje_balance = None
    if "tipo_mensaje" not in st.session_state: 
        st.session_state.tipo_mensaje = None

    # CORRECCIÓN CLAVE: Ambos deben ser botones nativos del formulario para procesar los datos
    btn_verificar = st.form_submit_button("Verificar Balance")

    if btn_verificar:
        suma_total_gas = y1_CO2_pct + y1_O2_pct + y1_N2_pct
        
        if abs(suma_total_gas - 100.0) <= 0.0001:
            st.session_state.mensaje_balance = f"✅ Mezcla balanceada correctamente: Suma total = {suma_total_gas:.4f}%"
            st.session_state.tipo_mensaje = "success"
            st.session_state.datos_gas_validos = True
        elif suma_total_gas > 100.0:
            excaso = suma_total_gas - 100.0
            st.session_state.mensaje_balance = f"❌ **¡Error en la composición!** La suma total es mayor a 100.00% (Actual: {suma_total_gas:.4f}%). Por favor, reajuste los valores."
            st.session_state.tipo_mensaje = "error"
            st.session_state.datos_gas_validos = False
        else:
            faltante = 100.0 - suma_total_gas
            st.session_state.mensaje_balance = f"⚠️ **Composición incompleta:** La suma total es de **{suma_total_gas:.4f}%**. Falta un **{faltante:.4f}%** para alcanzar el 100.00% de la mezcla."
            st.session_state.tipo_mensaje = "warning"
            st.session_state.datos_gas_validos = False

    # Renderizar el cuadro de diálogo correspondiente bajo el botón
    if st.session_state.mensaje_balance:
        if st.session_state.tipo_mensaje == "success":
            st.success(st.session_state.mensaje_balance)
        elif st.session_state.tipo_mensaje == "error":
            st.error(st.session_state.mensaje_balance)
        elif st.session_state.tipo_mensaje == "warning":
            st.warning(st.session_state.mensaje_balance)
    
    st.write("#### :blue[Condiciones de operación y especificaciones de salida]")
    x2_input = st.number_input("Concentración de $CO_2$ en el líquido de entrada en la Parte Superior ($x_2$, mol CO₂/mol sol)", min_value=0.0, max_value=1.0, value=0.0580, format="%.4f")
    factor_min = st.number_input("Multiplicador de exceso para la relación real (Factor respecto a $L_{s-min}/G_s$)", min_value=1.0, max_value=5.0, value=1.2000, step=0.1, format="%.4f")
    y2_CO2_pct = st.number_input("Concentración residual de $CO_2$ deseada en el gas de salida por la Parte Superior (% vol)", min_value=0.0, max_value=100.0, value=2.0, format="%.4f")
    
    st.info(
    "📌 **Nota:** De acuerdo con los requerimientos fijos del modelo simplificado, las condiciones térmicas y de presión se establecen en 25 °C y 1.2 atm."
 )

    st.warning(
        "⚠️ **Aviso:** Dependiendo de la configuración regional del sistema, los números decimales "
        "pueden visualizarse con coma (,) o punto (.) como separador decimal. "
        "Esto no afecta los cálculos realizados ni los resultados generados por el modelo."
    )

    submit_button = st.form_submit_button(
        label="Correr simulación"
    )

# ==============================================================================
# ALGORITMO MATEMÁTICO Y BALANCES DE MATERIA
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

    # Tabla de presiones parciales de equilibrio experimental para el sistema de MEA
    x_table = np.array([0.058, 0.060, 0.062, 0.064, 0.066, 0.068, 0.070])
    P_table = np.array([5.6, 12.8, 29.0, 56.0, 98.7, 155.0, 232.0])

    # Conversión de fracciones a relaciones molares (X, Y)
    Y1 = y1_CO2 / (1.0 - y1_CO2)
    Y2 = y2_CO2 / (1.0 - y2_CO2)
    X2 = x2_input

    PT_mmHg = 1.2 * 760.0025
    P_CO2_fondo = y1_CO2 * PT_mmHg

    # Interpolación para hallar la concentración límite teórica en la fase líquida
    X1_star = float(np.interp(P_CO2_fondo, P_table, x_table))

    # Relaciones operativas mínimas y reales
    LsGs_min = (Y1 - Y2) / (X1_star - X2)
    LsGs_real = LsGs_min * factor_min

    # Flujos molares referenciados a 1 m3 de mezcla gaseosa alimentada
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
    # INTERFAZ GRÁFICA DE PRESENTACIÓN DE RESULTADOS
    # ==========================================================================
    st.markdown(
        """
        <style>
            .tabla-resultados { width: 100%; border-collapse: collapse; font-family: 'Segoe UI', sans-serif; }
            .tabla-resultados td { padding: 6px 4px; border-bottom: 1px solid rgba(0,0,0,0.05); font-size: 13.5px; }
            .tabla-resultados tr:last-child td { border-bottom: none; }
            .lbl { font-weight: 600; color: #2D3748; text-align: left; }
            .val { text-align: right; font-family: 'Courier New', monospace; font-weight: bold; color: #1A202C; }
            
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

    st.markdown("---")
  
    # Dividimos la sección en 2 columnas iguales
    
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        st.markdown(
            f"""
            <div style="background-color: #E6F0FA; padding: 20px; border-radius: 8px; border-left: 5px solid #0A2540; min-height: 530px;">
                <h3 style="color: #0A2540; margin-top: 0; margin-bottom: 18px; font-family: sans-serif;"><b>Datos de los componentes</b></h3>
                <table class="tabla-resultados">
                    <tr><td class="lbl">Peso molecular del CO₂ (g/mol)</td><td class="val">{PM_CO2:.4f}</td></tr>
                    <tr><td class="lbl">Peso molecular del monoetanolamina (MEA) (g/mol)</td><td class="val">{PM_MEA:.4f}</td></tr>
                    <tr><td class="lbl">Peso molecular del O₂ (g/mol)</td><td class="val">{PM_O2:.4f}</td></tr>
                    <tr><td class="lbl">Peso molecular del N₂ (g/mol)</td><td class="val">{PM_N2:.4f}</td></tr>
                    <tr><td class="lbl">Peso molecular del H₂O (g/mol)</td><td class="val">{PM_H2O:.4f}</td></tr>
                    <tr><td class="lbl">Peso molecular promedio de la solución (g/mol)</td><td class="val">{PM_sol_visual:.4f}</td></tr>
                    <tr><td class="lbl">Presión total del sistema (atm)</td><td class="val">1.2000</td></tr>
                    <tr><td class="lbl">Presión total del sistema (mmHg)</td><td class="val">{PT_mmHg:.4f}</td></tr>
                    <tr><td class="lbl">Presión parcial de CO₂ en la parte inferior (mmHg)</td><td class="val">{P_CO2_fondo:.4f}</td></tr>
                    <tr><td class="lbl">Relación molar de entrada G1 (CO₂)</td><td class="val">{g1_co2_visual:.4f}</td></tr>
                    <tr><td class="lbl">Fracción molar de salida G2 (CO₂)</td><td class="val">{g2_co2_visual:.4f}</td></tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col_der:
        st.markdown(
            f"""
            <div style="background-color: #FFF9E6; padding: 20px; border-radius: 8px; border-left: 5px solid #D4AF37; min-height: 530px;">
                <h3 style="color: #8A6D1C; margin-top: 0; margin-bottom: 18px; font-family: sans-serif;"><b>Cálculos intermedios</b></h3>
                <table class="tabla-resultados">
                    <tr><td class="lbl">Composición de equilibrio (X₁*)</td><td class="val">{X1_star:.4f}</td></tr>
                    <tr><td class="lbl">Relación molar en la parte superior (X₂)</td><td class="val">{X2:.4f}</td></tr>
                    <tr><td class="lbl">Relación molar en la parte inferior (Y₁)</td><td class="val">{Y1:.4f}</td></tr>
                    <tr><td class="lbl">Relación molar en la parte superior (Y₂)</td><td class="val">{Y2:.4f}</td></tr>
                    <tr><td class="lbl">Relación Líquido/Gas mínima (Ls/Gs)<sub>min</sub></td><td class="val">{LsGs_min:.4f}</td></tr>
                    <tr><td class="lbl">Relación Líquido/Gas operacional (Ls/Gs)<sub>real</sub></td><td class="val">{LsGs_real:.4f}</td></tr>
                    <tr><td class="lbl">Gas inerte estándar Gs a 1.0 atm (mol/m³)</td><td class="val">{Gs_1atm:.4f}</td></tr>
                    <tr><td class="lbl">Gas inerte de operación Gs a 1.2 atm (mol/m³)</td><td class="val">{Gs_real:.4f}</td></tr>
                    <tr><td class="lbl">Flujo molar del solvente inerte Ls (mol)</td><td class="val">{Ls_real:.4f}</td></tr>
                    <tr><td class="lbl">Masa total de la solución absorbente (kg)</td><td class="val">{kg_solucion_m3:.4f}</td></tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    # ==========================================================================
    # TABLA RESUMEN DE RESPUESTAS (DISEÑO TOTALMENTE PINTADO EN MORADO PASTEL)
    # ==========================================================================
    st.markdown("<h3 style='color: #0A2540;'> </h3>", unsafe_allow_html=True)
    
    st.markdown(
        f"""
        <div style="background-color: #F4EFFF; padding: 20px; border-radius: 8px; border-left: 5px solid #9061F9; min-height: 430px;">
            <h3 style="color: #4C1D95; margin-top: 0; margin-bottom: 18px; font-family: sans-serif;"><b>Resultados obtenidos</b></h3>
            <table class="tabla-resultados" style="width: 100%; border-collapse: collapse; background-color: transparent;">
                <tr><td class="lbl">Relación líquido/gas mínima (Ls-min/Gs)</td><td class="val">{LsGs_min:.4f} mol/mol</td></tr>
                <tr><td class="lbl">Relación molar del gas de salida en la parte superior de la torre (Y₂)</td><td class="val">{Y2:.4f} mol CO₂/mol inerte</td></tr>
                <tr><td class="lbl">Relación molar del líquido de entrada en la parte superior de la torre (X₂)</td><td class="val">{X2:.4f} mol CO₂/mol sol</td></tr>
                <tr><td class="lbl">Relación molar del gas de entrada en la parte inferior de la torre (Y₁)</td><td class="val">{Y1:.4f} mol CO₂/mol inerte</td></tr>
                <tr><td class="lbl">Relación molar de equilibrio teórico en la parte inferior (X₁*)</td><td class="val">{X1_star:.4f} mol CO₂/mol sol</td></tr>
                <tr><td class="lbl">Flujo molar de gas inerte real Gs por unidad de volumen</td><td class="val">{Gs_real:.4f} mol/m³</td></tr>
                <tr><td class="lbl">Masa total requerida de solución absorbente por unidad de volumen (al exceso seleccionado)</td><td class="val">{kg_solucion_m3:.4f} kg/m³</td></tr>
                <tr><td class="lbl">Moles de CO₂ transportados en la corriente de líquido alimentada por la parte superior L₂</td><td class="val">{moles_CO2_L2:.4f} mol/m³</td></tr>
            </table>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<h3 style='color: #0A2540;'> </h3>", unsafe_allow_html=True)
    
    st.info(
    "📌 **Nota:** Si desea modificar los parámetros o condiciones de entrada, "
    "desplácese hacia la parte superior del formulario y ajuste los valores según corresponda. "
    "Los resultados se actualizarán automáticamente con los nuevos datos ingresados."
)
