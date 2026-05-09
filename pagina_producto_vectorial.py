import streamlit as st
import pandas as pd

from producto_vectorial import (
    parsear_vector,
    producto_vectorial,
    magnitud_vector,
    vector_desde_puntos,
    fuerza_magnetica
)

from graficador_vectores import (
    crear_grafica_vectores,
    crear_grafica_fuerza
)


def mostrar_vector(nombre, vector):
    x, y, z = vector
    st.code(f"{nombre} = <{x:.4e}, {y:.4e}, {z:.4e}>")


def mostrar_pagina_producto_vectorial():
    st.header("🧲 Producto vectorial y fuerza magnética")

    st.markdown("""
    <div class="info-box">
    El producto vectorial permite obtener un nuevo vector perpendicular a dos vectores dados.
    En física, se utiliza para calcular fuerzas como la fuerza magnética sobre un conductor con corriente.
    </div>
    """, unsafe_allow_html=True)

    opcion = st.radio(
        "Selecciona el tipo de ejercicio",
        ["Producto vectorial", "Fuerza magnética"],
        horizontal=True
    )

    if opcion == "Producto vectorial":
        mostrar_producto_vectorial()

    else:
        mostrar_fuerza_magnetica()


def mostrar_producto_vectorial():
    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.subheader("Datos de entrada")

        vector_a_txt = st.text_input("Vector A (x,y,z)", value="(2,3,4)")
        vector_b_txt = st.text_input("Vector B (x,y,z)", value="(5,1,2)")

        calcular = st.button("Calcular producto vectorial", use_container_width=True)

    with col2:
        if calcular:
            try:
                a = parsear_vector(vector_a_txt)
                b = parsear_vector(vector_b_txt)

                resultado = producto_vectorial(a, b)
                magnitud = magnitud_vector(resultado)

                st.subheader("Resultados principales")

                m1, m2 = st.columns(2)
                m1.metric("Magnitud de A × B", f"{magnitud:.4e}")
                m2.metric("Tipo de resultado", "Vector")

                mostrar_vector("A", a)
                mostrar_vector("B", b)
                mostrar_vector("A × B", resultado)

                st.subheader("Resumen")
                df = pd.DataFrame([
                    {"Vector": "A", "x": a[0], "y": a[1], "z": a[2]},
                    {"Vector": "B", "x": b[0], "y": b[1], "z": b[2]},
                    {"Vector": "A × B", "x": resultado[0], "y": resultado[1], "z": resultado[2]},
                ])
                st.dataframe(df, use_container_width=True, hide_index=True)

                st.subheader("Gráfica 3D")
                fig = crear_grafica_vectores(a, b, resultado)
                st.plotly_chart(fig, use_container_width=True)

                mostrar_procedimiento_producto(a, b, resultado)

            except Exception as e:
                st.error(f"Error: {e}")


def mostrar_fuerza_magnetica():
    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.subheader("Datos de entrada")

        usar_escenario = st.checkbox("Usar escenario 2 del documento")

        if usar_escenario:
            p_txt = "(-7,4,5)"
            q_txt = "(8,0,-4)"
            corriente_txt = "20"
        else:
            p_txt = "(0,0,0)"
            q_txt = "(3,2,1)"
            corriente_txt = "10"

        p_texto = st.text_input("Punto P (x,y,z)", value=p_txt)
        q_texto = st.text_input("Punto Q (x,y,z)", value=q_txt)
        corriente = st.number_input("Corriente I (A)", value=float(corriente_txt))
        campo_b_texto = st.text_input("Campo magnético B (x,y,z)", value="(0,0,2)")

        calcular = st.button("Calcular fuerza magnética", use_container_width=True)

    with col2:
        if calcular:
            try:
                p = parsear_vector(p_texto)
                q = parsear_vector(q_texto)
                b = parsear_vector(campo_b_texto)

                l = vector_desde_puntos(p, q)
                producto = producto_vectorial(l, b)
                fuerza = fuerza_magnetica(corriente, l, b)
                magnitud = magnitud_vector(fuerza)

                st.subheader("Resultados principales")

                m1, m2 = st.columns(2)
                m1.metric("Magnitud de la fuerza", f"{magnitud:.4e} N")
                m2.metric("Corriente", f"{corriente:.4e} A")

                mostrar_vector("Vector L", l)
                mostrar_vector("Campo B", b)
                mostrar_vector("L × B", producto)
                mostrar_vector("F", fuerza)

                st.subheader("Resumen")
                df = pd.DataFrame([
                    {"Vector": "L", "x": l[0], "y": l[1], "z": l[2]},
                    {"Vector": "B", "x": b[0], "y": b[1], "z": b[2]},
                    {"Vector": "L × B", "x": producto[0], "y": producto[1], "z": producto[2]},
                    {"Vector": "F", "x": fuerza[0], "y": fuerza[1], "z": fuerza[2]},
                ])
                st.dataframe(df, use_container_width=True, hide_index=True)

                st.subheader("Gráfica 3D")
                fig = crear_grafica_fuerza(l, b, fuerza)
                st.plotly_chart(fig, use_container_width=True)

                mostrar_procedimiento_fuerza(p, q, l, b, corriente, producto, fuerza)

            except Exception as e:
                st.error(f"Error: {e}")


def mostrar_procedimiento_producto(a, b, resultado):
    ax, ay, az = a
    bx, by, bz = b
    cx, cy, cz = resultado

    st.subheader("📘 Procedimiento paso a paso")

    st.markdown("""
    <div class="paso-box">
    <div class="paso-title">Paso 1: Identificar los vectores</div>
    </div>
    """, unsafe_allow_html=True)

    st.latex(rf"\vec{{A}} = \langle {ax}, {ay}, {az} \rangle")
    st.latex(rf"\vec{{B}} = \langle {bx}, {by}, {bz} \rangle")

    st.markdown("""
    <div class="paso-box">
    <div class="paso-title">Paso 2: Usar la fórmula del producto vectorial</div>
    </div>
    """, unsafe_allow_html=True)

    st.latex(r"""
    \vec{A} \times \vec{B} =
    \begin{vmatrix}
    \hat{i} & \hat{j} & \hat{k} \\
    A_x & A_y & A_z \\
    B_x & B_y & B_z
    \end{vmatrix}
    """)

    st.markdown("""
    <div class="paso-box">
    <div class="paso-title">Paso 3: Sustituir valores</div>
    </div>
    """, unsafe_allow_html=True)

    st.latex(rf"""
    \vec{{A}} \times \vec{{B}} =
    \begin{{vmatrix}}
    \hat{{i}} & \hat{{j}} & \hat{{k}} \\
    {ax} & {ay} & {az} \\
    {bx} & {by} & {bz}
    \end{{vmatrix}}
    """)

    st.markdown("""
    <div class="paso-box">
    <div class="paso-title">Paso 4: Calcular componentes</div>
    </div>
    """, unsafe_allow_html=True)

    st.latex(rf"C_x = A_yB_z - A_zB_y = ({ay})({bz}) - ({az})({by}) = {cx}")
    st.latex(rf"C_y = A_zB_x - A_xB_z = ({az})({bx}) - ({ax})({bz}) = {cy}")
    st.latex(rf"C_z = A_xB_y - A_yB_x = ({ax})({by}) - ({ay})({bx}) = {cz}")

    st.markdown("""
    <div class="paso-box">
    <div class="paso-title">Paso 5: Resultado final</div>
    </div>
    """, unsafe_allow_html=True)

    st.latex(rf"\vec{{A}} \times \vec{{B}} = \langle {cx}, {cy}, {cz} \rangle")

    st.write("El resultado es un nuevo vector perpendicular a los dos vectores originales.")


def mostrar_procedimiento_fuerza(p, q, l, b, corriente, producto, fuerza):
    px, py, pz = p
    qx, qy, qz = q
    lx, ly, lz = l
    bx, by, bz = b
    pxv, pyv, pzv = producto
    fx, fy, fz = fuerza

    st.subheader("📘 Procedimiento paso a paso")

    st.markdown("""
    <div class="paso-box">
    <div class="paso-title">Paso 1: Identificar los datos</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("El conductor une los puntos P y Q, por lo que primero se obtiene el vector L.")
    st.latex(rf"P = ({px}, {py}, {pz})")
    st.latex(rf"Q = ({qx}, {qy}, {qz})")
    st.latex(rf"I = {corriente}\,A")
    st.latex(rf"\vec{{B}} = \langle {bx}, {by}, {bz} \rangle")

    st.markdown("""
    <div class="paso-box">
    <div class="paso-title">Paso 2: Calcular el vector del conductor</div>
    </div>
    """, unsafe_allow_html=True)

    st.latex(r"\vec{L} = Q - P")
    st.latex(rf"\vec{{L}} = \langle {qx} - ({px}), {qy} - ({py}), {qz} - ({pz}) \rangle")
    st.latex(rf"\vec{{L}} = \langle {lx}, {ly}, {lz} \rangle")

    st.markdown("""
    <div class="paso-box">
    <div class="paso-title">Paso 3: Aplicar producto vectorial</div>
    </div>
    """, unsafe_allow_html=True)

    st.latex(r"\vec{L} \times \vec{B}")
    st.latex(rf"""
    \vec{{L}} \times \vec{{B}} =
    \begin{{vmatrix}}
    \hat{{i}} & \hat{{j}} & \hat{{k}} \\
    {lx} & {ly} & {lz} \\
    {bx} & {by} & {bz}
    \end{{vmatrix}}
    """)

    st.latex(rf"\vec{{L}} \times \vec{{B}} = \langle {pxv}, {pyv}, {pzv} \rangle")

    st.markdown("""
    <div class="paso-box">
    <div class="paso-title">Paso 4: Calcular la fuerza magnética</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("La fuerza magnética sobre un conductor con corriente se calcula con:")
    st.latex(r"\vec{F} = I(\vec{L} \times \vec{B})")

    st.latex(rf"\vec{{F}} = {corriente}\langle {pxv}, {pyv}, {pzv} \rangle")
    st.latex(rf"\vec{{F}} = \langle {fx}, {fy}, {fz} \rangle\,N")

    st.markdown("""
    <div class="paso-box">
    <div class="paso-title">Paso 5: Interpretación</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("La fuerza resultante es perpendicular tanto al vector del conductor como al campo magnético.")