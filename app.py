# ==========================================================================
    # SECCIÓN DE ESTILOS GLOBALES (FUENTES BONITAS Y ALINEACIÓN DE TABLAS)
    # ==========================================================================
    st.markdown(
        """
        <style>
            /* Fuente global más moderna y limpia para toda la app */
            html, body, [data-testid="stMarkdownContainer"] {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            }
            
            /* Estilo unificado para las tablas superiores */
            .tabla-estilizada { 
                width: 100%; 
                border-collapse: collapse; 
            }
            .tabla-estilizada td { 
                padding: 8px 10px; 
                border-bottom: 1px solid rgba(0,0,0,0.06); 
                font-size: 14px; 
                vertical-align: middle;
            }
            .tabla-estilizada tr:last-child td { 
                border-bottom: none; 
            }
            .lbl-tabla { 
                font-weight: 500; 
                color: #2D3748; 
                text-align: left; 
            }
            /* Formato limpio, recto y alineado para los números de las tablas */
            .val-tabla { 
                text-align: right; 
                font-family: "Courier New", Courier, monospace; 
                font-weight: 600; 
                color: #1A202C; 
                background-color: rgba(0, 0, 0, 0.02);
                padding: 4px 8px !important;
                border-radius: 4px;
                white-space: nowrap;
            }
            
            /* Estilo para las tarjetas moradas individuales de abajo */
            .tarjeta-morada-individual {
                background-color: #F3E8FF; 
                padding: 14px 18px; 
                border-radius: 8px; 
                margin-bottom: 12px;
                color: #2D3748;
                font-size: 15px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }
            /* Número normal, recto, sin negrita pero destacado con tipografía limpia */
            .numero-resultado {
                font-family: "Courier New", Courier, monospace;
                font-weight: 600;
                font-size: 16px;
                color: #1A202C;
            }
        </style>
        """, 
        unsafe_allow_html=True
    )

    # ==========================================================================
    # RENDERIZADO DE LAS DOS TABLAS SUPERIORES RE-ESTILIZADAS
    # ==========================================================================
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        st.markdown(
            f"""
            <div style="background-color: #E6F0FA; padding: 20px; border-radius: 12px; border-left: 6px solid #0A2540; min-height: 580px;">
                <h3 style="color: #0A2540; margin-top: 0; margin-bottom: 18px;"><b>Datos de los componentes</b></h3>
                <table class="tabla-estilizada">
                    <tr><td class="lbl-tabla">Peso molecular de CO₂ (g/mol)</td><td class="val-tabla">{PM_CO2:.4f}</td></tr>
                    <tr><td class="lbl-tabla">Peso molecular de MEA (g/mol)</td><td class="val-tabla">{PM_MEA:.4f}</td></tr>
                    <tr><td class="lbl-tabla">Peso molecular de O₂ (g/mol)</td><td class="val-tabla">{PM_O2:.4f}</td></tr>
                    <tr><td class="lbl-tabla">Peso molecular de N₂ (g/mol)</td><td class="val-tabla">{PM_N2:.4f}</td></tr>
                    <tr><td class="lbl-tabla">Peso molecular del H₂O (g/mol)</td><td class="val-tabla">{PM_H2O:.4f}</td></tr>
                    <tr><td class="lbl-tabla">Peso molecular promedio de la solución (g/mol)</td><td class="val-tabla">{PM_sol_visual:.4f}</td></tr>
                    <tr><td class="lbl-tabla">Presión total del sistema (atm)</td><td class="val-tabla">1.2000</td></tr>
                    <tr><td class="lbl-tabla">Presión total del sistema (mmHg)</td><td class="val-tabla">{PT_mmHg:.4f}</td></tr>
                    <tr><td class="lbl-tabla">Presión parcial de CO₂ en el fondo (mmHg)</td><td class="val-tabla">{P_CO2_fondo:.4f}</td></tr>
                    <tr><td class="lbl-tabla">Relación molar de entrada G1 (CO₂)</td><td class="val-tabla">{g1_co2_visual:.4f}</td></tr>
                    <tr><td class="lbl-tabla">Relación molar de entrada G1 (N₂)</td><td class="val-tabla">{g1_n2_visual:.4f}</td></tr>
                    <tr><td class="lbl-tabla">Relación molar de entrada G1 (O₂)</td><td class="val-tabla">{g1_o2_visual:.4f}</td></tr>
                    <tr><td class="lbl-tabla">Fracción molar de salida G2 (CO₂)</td><td class="val-tabla">{g2_co2_visual:.4f}</td></tr>
                    <tr><td class="lbl-tabla">Fracción molar de salida G2 (N₂)</td><td class="val-tabla">{g2_n2_visual:.4f}</td></tr>
                    <tr><td class="lbl-tabla">Fracción molar de salida G2 (O₂)</td><td class="val-tabla">{g2_o2_visual:.4f}</td></tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col_der:
        st.markdown(
            f"""
            <div style="background-color: #FFF9E6; padding: 20px; border-radius: 12px; border-left: 6px solid #D4AF37; min-height: 580px;">
                <h3 style="color: #8A6D1C; margin-top: 0; margin-bottom: 18px;"><b>Cálculos intermedios</b></h3>
                <table class="tabla-estilizada">
                    <tr><td class="lbl-tabla">Composición de equilibrio (X₁*)</td><td class="val-tabla">{X1_star:.4f}</td></tr>
                    <tr><td class="lbl-tabla">Composición del líquido en el domo (X₂)</td><td class="val-tabla">{X2:.4f}</td></tr>
                    <tr><td class="lbl-tabla">Relación molar en el fondo (Y₁)</td><td class="val-tabla">{Y1:.4f}</td></tr>
                    <tr><td class="lbl-tabla">Relación molar en el domo (Y₂)</td><td class="val-tabla">{Y2:.4f}</td></tr>
                    <tr><td class="lbl-tabla">Relación líquido/gas mínima (Ls/Gs)_min</td><td class="val-tabla">{LsGs_min:.4f}</td></tr>
                    <tr><td class="lbl-tabla">Relación líquido/gas de operación (Ls/Gs)_real</td><td class="val-tabla">{LsGs_real:.4f}</td></tr>
                    <tr><td class="lbl-tabla">Moles totales a 1.0 atm (mol)</td><td class="val-tabla">{n_total_m3_1atm:.4f}</td></tr>
                    <tr><td class="lbl-tabla">Gas inerte estándar Gs a 1.0 atm (mol/m³)</td><td class="val-tabla">{Gs_1atm:.4f}</td></tr>
                    <tr><td class="lbl-tabla">Moles totales en operación a 1.2 atm (mol)</td><td class="val-tabla">{n_total_m3_real:.4f}</td></tr>
                    <tr><td class="lbl-tabla">Gas inerte real Gs a 1.2 atm (mol/m³)</td><td class="val-tabla">{Gs_real:.4f}</td></tr>
                    <tr><td class="lbl-tabla">Flujo molar de líquido inerte Ls (mol)</td><td class="val-tabla">{Ls_real:.4f}</td></tr>
                    <tr><td class="lbl-tabla">Masa total de solución absorbente (kg)</td><td class="val-tabla">{kg_solucion_m3:.4f}</td></tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ==========================================================================
    # SECCIÓN DE RESULTADOS FINALES POR INCISOS
    # ==========================================================================
    st.markdown("---")
    st.markdown("<h3 style='color: #0A2540;'><b>Resultados finales</b></h3>", unsafe_allow_html=True)
    
    st.markdown("<p style='color: #4A5568;'><i>Todos los resultados se presentan en notación decimal estándar para su lectura:</i></p>", unsafe_allow_html=True)
    st.markdown("")

    st.markdown(f'<div class="tarjeta-morada-individual"><b>A)</b> Relación líquido/gas mínima (Ls/Gs)_min: <span class="numero-resultado">{LsGs_min:.4f}</span> mol/mol</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="tarjeta-morada-individual"><b>B)</b> Relación molar del gas en el domo de la torre (Y₂): <span class="numero-resultado">{Y2:.4f}</span> mol CO₂/mol inerte</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="tarjeta-morada-individual"><b>C)</b> Relación molar del líquido a la entrada de la torre (X₂): <span class="numero-resultado">{X2:.4f}</span> mol CO₂/mol sol</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="tarjeta-morada-individual"><b>D)</b> Relación molar del gas en el fondo de la torre (Y₁): <span class="numero-resultado">{Y1:.4f}</span> mol CO₂/mol inerte</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="tarjeta-morada-individual"><b>E)</b> Relación molar de equilibrio en el fondo (X₁*): <span class="numero-resultado">{X1_star:.4f}</span> mol CO₂/mol sol</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="tarjeta-morada-individual"><b>F)</b> Flujo de gas inerte Gs (para 1 m³ de G₁): <span class="numero-resultado">{Gs_real:.4f}</span> mol/m³</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="tarjeta-morada-individual"><b>G)</b> Masa de solución por m³ (a {factor_min:.4f} veces): <span class="numero-resultado">{kg_solucion_m3:.4f}</span> kg/m³</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="tarjeta-morada-individual"><b>H)</b> Moles de CO₂ transportados en la corriente L₂: <span class="numero-resultado">{moles_CO2_L2:.4f}</span> mol/m³</div>', unsafe_allow_html=True)
