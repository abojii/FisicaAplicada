import pandas as pd
import streamlit as st

from prefijos import convertir_prefijo
from circuitos import (
    resolver_resistores_serie,
    resolver_resistores_paralelo,
    resolver_capacitores_serie,
    resolver_capacitores_paralelo
)
from dibujo_circuitos import crear_dibujo_circuito


def mostrar_pagina_circuitos():
    st.header("🔌 Circuitos simples: resistores y capacitores")

    st.markdown("""
    <div class="info-box">
    Esta sección permite resolver circuitos simples formados por una batería y un conjunto de resistores o capacitores
    conectados en serie o en paralelo. El programa calcula valores equivalentes, corrientes, voltajes y cargas según el caso.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.subheader("Datos del circuito")

        tipo = st.radio(
            "Tipo de componente",
            ["Resistores", "Capacitores"],
            horizontal=True
        )

        conexion = st.radio(
            "Tipo de conexión",
            ["Serie", "Paralelo"],
            horizontal=True
        )

        fuente_txt = st.text_input("Voltaje de la batería", value="12V")

        n = st.number_input(
            "Cantidad de elementos",
            min_value=1,
            max_value=10,
            value=3,
            step=1
        )

        ejemplo = "3K" if tipo == "Resistores" else "220nF"

        letra = "R" if tipo == "Resistores" else "C"

        datos = pd.DataFrame({
            "Elemento": [f"{letra}{i+1}" for i in range(int(n))],
            "Valor": [ejemplo for _ in range(int(n))]
        })

        st.write("Ingresa los valores directamente en la tabla:")
        tabla = st.data_editor(datos, use_container_width=True, hide_index=True)

        st.info("Prefijos válidos: p, n, u, µ, m, K, M, G. Ejemplo: 53mV, 10K, 3553pF, 2.2uF")

        calcular = st.button("Resolver circuito", use_container_width=True)

    with col2:
        if calcular:
            try:
                voltaje = convertir_prefijo(fuente_txt)
                valores = [convertir_prefijo(v) for v in tabla["Valor"]]

                if any(v <= 0 for v in valores):
                    raise ValueError("Todos los valores deben ser mayores que cero.")

                # ============================
                # CÁLCULOS
                # ============================
                if tipo == "Resistores" and conexion == "Serie":
                    equivalente, principal, registros = resolver_resistores_serie(voltaje, valores)
                    nombre_equivalente = "Resistencia equivalente"
                    nombre_principal = "Corriente de la batería"
                    unidad_equivalente = "Ω"
                    unidad_principal = "A"

                elif tipo == "Resistores" and conexion == "Paralelo":
                    equivalente, principal, registros = resolver_resistores_paralelo(voltaje, valores)
                    nombre_equivalente = "Resistencia equivalente"
                    nombre_principal = "Corriente de la batería"
                    unidad_equivalente = "Ω"
                    unidad_principal = "A"

                elif tipo == "Capacitores" and conexion == "Serie":
                    equivalente, principal, registros = resolver_capacitores_serie(voltaje, valores)
                    nombre_equivalente = "Capacitancia equivalente"
                    nombre_principal = "Carga en cada capacitor"
                    unidad_equivalente = "F"
                    unidad_principal = "C"

                else:
                    equivalente, principal, registros = resolver_capacitores_paralelo(voltaje, valores)
                    nombre_equivalente = "Capacitancia equivalente"
                    nombre_principal = "Carga total"
                    unidad_equivalente = "F"
                    unidad_principal = "C"

                # ============================
                # RESULTADOS
                # ============================
                st.subheader("Resultados principales")
                m1, m2 = st.columns(2)
                m1.metric(nombre_equivalente, f"{equivalente:.4e} {unidad_equivalente}")
                m2.metric(nombre_principal, f"{principal:.4e} {unidad_principal}")

                st.subheader("Resumen por elemento")
                df = pd.DataFrame(registros)
                for col in df.columns:
                    if col != "Elemento":
                        df[col] = df[col].map(lambda x: f"{x:.4e}" if isinstance(x, float) else x)
                st.dataframe(df, use_container_width=True, hide_index=True)

                # ============================
                # DIBUJO
                # ============================
                st.subheader("Dibujo del circuito")
                fig = crear_dibujo_circuito(tipo, conexion, valores)
                st.plotly_chart(fig, use_container_width=True)

                # ============================
                # PROCEDIMIENTO
                # ============================
                st.subheader("📘 Procedimiento paso a paso")

                # RESISTORES EN SERIE
                if tipo == "Resistores" and conexion == "Serie":
                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 1: Identificar el tipo de circuito</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.write("El circuito contiene resistores conectados en serie. En serie, la corriente es la misma en todos los resistores.")

                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 2: Calcular la resistencia equivalente</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.latex(r"R_{eq} = R_1 + R_2 + ... + R_n")
                    texto = " + ".join([f"{r:.4e}" for r in valores])
                    st.latex(rf"R_{{eq}} = {texto} = {equivalente:.4e}\,\Omega")

                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 3: Calcular la corriente de la batería</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.write("Se aplica la Ley de Ohm:")
                    st.latex(r"I = \frac{V}{R_{eq}}")
                    st.latex(rf"I = \frac{{{voltaje:.4e}}}{{{equivalente:.4e}}} = {principal:.4e}\,A")

                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 4: Calcular el voltaje en cada resistor</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.write("Como la corriente es la misma, el voltaje de cada resistor se calcula con:")
                    st.latex(r"V_i = I R_i")

                    for i, r in enumerate(valores, start=1):
                        v_i = principal * r
                        st.latex(rf"V_{i} = ({principal:.4e})({r:.4e}) = {v_i:.4e}\,V")

                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 5: Verificación</div>
                    </div>
                    """, unsafe_allow_html=True)

                    suma_voltajes = sum(principal * r for r in valores)
                    st.write("En serie, la suma de los voltajes debe ser igual al voltaje de la batería:")
                    st.latex(rf"V_{{total}} = {suma_voltajes:.4e}\,V \approx {voltaje:.4e}\,V")

                # RESISTORES EN PARALELO
                elif tipo == "Resistores" and conexion == "Paralelo":
                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 1: Identificar el tipo de circuito</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.write("El circuito contiene resistores conectados en paralelo. En paralelo, todos los resistores tienen el mismo voltaje de la batería.")

                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 2: Calcular la resistencia equivalente</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.latex(r"\frac{1}{R_{eq}} = \frac{1}{R_1} + \frac{1}{R_2} + ... + \frac{1}{R_n}")
                    suma_inversos = sum(1 / r for r in valores)
                    st.latex(rf"R_{{eq}} = \frac{{1}}{{{suma_inversos:.4e}}} = {equivalente:.4e}\,\Omega")

                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 3: Calcular la corriente total de la batería</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.latex(r"I = \frac{V}{R_{eq}}")
                    st.latex(rf"I = \frac{{{voltaje:.4e}}}{{{equivalente:.4e}}} = {principal:.4e}\,A")

                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 4: Calcular la corriente en cada resistor</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.write("Como todos tienen el mismo voltaje, la corriente en cada resistor es:")
                    st.latex(r"I_i = \frac{V}{R_i}")

                    for i, r in enumerate(valores, start=1):
                        i_i = voltaje / r
                        st.latex(rf"I_{i} = \frac{{{voltaje:.4e}}}{{{r:.4e}}} = {i_i:.4e}\,A")

                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 5: Verificación</div>
                    </div>
                    """, unsafe_allow_html=True)

                    suma_corrientes = sum(voltaje / r for r in valores)
                    st.write("En paralelo, la suma de las corrientes individuales debe ser igual a la corriente total:")
                    st.latex(rf"I_{{total}} = {suma_corrientes:.4e}\,A \approx {principal:.4e}\,A")

                # CAPACITORES EN SERIE
                elif tipo == "Capacitores" and conexion == "Serie":
                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 1: Identificar el tipo de circuito</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.write("El circuito contiene capacitores conectados en serie. En este tipo de conexión, la carga almacenada en cada capacitor es la misma.")
                    st.latex(r"Q_1 = Q_2 = ... = Q_n")

                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 2: Calcular la capacitancia equivalente</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.write("Para capacitores en serie se suman los inversos de las capacitancias:")
                    st.latex(r"\frac{1}{C_{eq}} = \sum \frac{1}{C_i}")

                    suma_inversos = sum(1 / c for c in valores)
                    st.latex(rf"C_{{eq}} = \frac{{1}}{{{suma_inversos:.4e}}} = {equivalente:.4e}\,F")

                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 3: Calcular la carga en cada capacitor</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.write("Como están en serie, la carga es igual para todos los capacitores:")
                    st.latex(r"Q = C_{eq}V")
                    st.latex(rf"Q = ({equivalente:.4e})({voltaje:.4e}) = {principal:.4e}\,C")

                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 4: Calcular el voltaje en cada capacitor</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.write("El voltaje de cada capacitor se obtiene despejando la fórmula de capacitancia:")
                    st.latex(r"V_i = \frac{Q}{C_i}")

                    for i, c in enumerate(valores, start=1):
                        v_i = principal / c
                        st.latex(rf"V_{i} = \frac{{{principal:.4e}}}{{{c:.4e}}} = {v_i:.4e}\,V")

                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 5: Verificación</div>
                    </div>
                    """, unsafe_allow_html=True)

                    suma_voltajes = sum(principal / c for c in valores)
                    st.write("La suma de los voltajes individuales debe ser aproximadamente igual al voltaje de la batería:")
                    st.latex(rf"V_{{total}} = {suma_voltajes:.4e}\,V \approx {voltaje:.4e}\,V")

                # CAPACITORES EN PARALELO
                else:
                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 1: Identificar el tipo de circuito</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.write("El circuito contiene capacitores conectados en paralelo. En paralelo, todos los capacitores tienen el mismo voltaje de la batería.")

                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 2: Calcular la capacitancia equivalente</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.latex(r"C_{eq} = C_1 + C_2 + ... + C_n")
                    texto = " + ".join([f"{c:.4e}" for c in valores])
                    st.latex(rf"C_{{eq}} = {texto} = {equivalente:.4e}\,F")

                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 3: Calcular la carga en cada capacitor</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.write("Como todos tienen el mismo voltaje, la carga en cada capacitor se calcula con:")
                    st.latex(r"Q_i = C_iV")

                    cargas_individuales = []
                    for i, c in enumerate(valores, start=1):
                        q_i = c * voltaje
                        cargas_individuales.append(q_i)
                        st.latex(rf"Q_{i} = ({c:.4e})({voltaje:.4e}) = {q_i:.4e}\,C")

                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 4: Calcular la carga total</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.write("La carga total se obtiene sumando las cargas individuales o usando la capacitancia equivalente:")
                    st.latex(r"Q_{total} = C_{eq}V")
                    st.latex(rf"Q_{{total}} = ({equivalente:.4e})({voltaje:.4e}) = {principal:.4e}\,C")

                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 5: Verificación</div>
                    </div>
                    """, unsafe_allow_html=True)

                    suma_cargas = sum(cargas_individuales)
                    st.latex(rf"Q_{{total}} = {suma_cargas:.4e}\,C \approx {principal:.4e}\,C")

            except Exception as e:
                st.error(f"Error: {e}")

        else:
            st.markdown("""
            <div class="bloque">
            <h3>Guía de uso</h3>
            <p>
            Selecciona si quieres resolver un circuito de resistores o capacitores.
            Luego elige si están conectados en serie o en paralelo, ingresa el voltaje
            de la batería y escribe los valores en la tabla.
            </p>
            </div>
            """, unsafe_allow_html=True)