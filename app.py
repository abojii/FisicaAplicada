import pandas as pd
import streamlit as st

from conversiones import convertir_notacion, parsear_coordenada
from calculos import calcular_fuerza_total, calcular_fuerza_individual
from graficador import crear_grafica


st.set_page_config(
    page_title="Ley de Coulomb",
    page_icon="⚡",
    layout="wide"
)

# ---------------------------------------------------
# ESTILOS
# ---------------------------------------------------
st.markdown("""
<style>
/* Fondo general */
.stApp {
    background: linear-gradient(180deg, #081224 0%, #0f172a 100%);
    color: white;
}

/* Títulos */
h1, h2, h3 {
    color: #38bdf8 !important;
}

/* Texto general */
html, body, p, li, span, div {
    color: white;
}

/* Bloques principales */
.bloque {
    background: rgba(17, 24, 39, 0.95);
    border: 1px solid rgba(56, 189, 248, 0.18);
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.22);
}

.info-box {
    background: rgba(15, 23, 42, 0.95);
    border-left: 4px solid #22c55e;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 16px;
    color: white !important;
}

.formula-box {
    background: rgba(2, 6, 23, 0.95);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 14px;
    color: white !important;
}

/* Tarjetas de pasos */
.paso-box {
    background: rgba(2, 6, 23, 0.90);
    border-left: 4px solid #22c55e;
    border-radius: 12px;
    padding: 14px 16px;
    margin-top: 12px;
    margin-bottom: 12px;
}

.paso-title {
    color: #22c55e !important;
    font-weight: 700;
    font-size: 16px;
    margin-bottom: 4px;
}

/* Labels */
label,
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] * {
    color: white !important;
    font-weight: 600 !important;
    opacity: 1 !important;
}

/* Inputs */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background-color: #0b1220 !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}

/* Botones + y - del number input */
[data-testid="stNumberInput"] button {
    color: white !important;
}

/* Métricas */
[data-testid="stMetricValue"] {
    color: white !important;
    font-weight: 700 !important;
}

[data-testid="stMetricLabel"] {
    color: #e2e8f0 !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}

div[data-testid="stMetric"] {
    background: rgba(17, 24, 39, 0.95);
    border: 1px solid rgba(56, 189, 248, 0.18);
    border-radius: 16px;
    padding: 14px;
}

/* Botón principal */
.stButton > button {
    background: linear-gradient(90deg, #16a34a, #22c55e) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.75rem 1rem !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    box-shadow: 0 8px 20px rgba(34,197,94,0.25) !important;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #15803d, #16a34a) !important;
    color: white !important;
}

/* Expander */
details {
    background: rgba(17, 24, 39, 0.92) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    padding: 6px 10px !important;
    margin-bottom: 12px !important;
}

summary {
    color: white !important;
    font-weight: 700 !important;
}

summary * {
    color: white !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * {
    color: white !important;
    opacity: 1 !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 16px !important;
    overflow: hidden !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TÍTULO
# ---------------------------------------------------
st.title("⚡ Principio de Superposición - Ley de Coulomb")
st.caption("Aplicación web para calcular, visualizar y explicar la fuerza eléctrica neta sobre una carga objetivo.")

# ---------------------------------------------------
# LAYOUT
# ---------------------------------------------------
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown('<div class="bloque">', unsafe_allow_html=True)
    st.subheader("Datos de entrada")

    st.markdown("""
    <div class="info-box">
    <b>¿Qué hace esta aplicación?</b><br><br>
    Esta herramienta permite ingresar una <b>carga objetivo</b> y varias <b>cargas puntuales</b> ubicadas en el plano cartesiano.
    Luego aplica la <b>Ley de Coulomb</b> y el <b>Principio de Superposición</b> para calcular:
    <ul>
        <li>La fuerza individual que ejerce cada carga sobre la carga objetivo</li>
        <li>Las componentes de la fuerza en <b>X</b> y <b>Y</b></li>
        <li>La fuerza neta total en forma vectorial</li>
        <li>La magnitud de la fuerza resultante</li>
        <li>La representación gráfica del sistema con su vector neto</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="formula-box">
    <b>Concepto:</b><br><br>
    La Ley de Coulomb establece que la fuerza eléctrica entre dos cargas puntuales es directamente proporcional al producto de sus cargas
    e inversamente proporcional al cuadrado de la distancia que las separa. Como la fuerza es un vector, en esta aplicación se
    descompone en sus componentes horizontal y vertical para luego sumarlas mediante el Principio de Superposición.
    </div>
    """, unsafe_allow_html=True)

    q_obj_texto = st.text_input("Magnitud de la carga objetivo q₀ (C)", value="2x10^-6")
    pos_obj_texto = st.text_input("Posición de la carga objetivo (x,y)", value="(0,0)")

    st.info("Formatos válidos: 2x10^-6, 2e-6, -3x10^-6, (1,0), (-2,3.5)")

    st.subheader("Cargas puntuales")
    n = st.number_input("Cantidad de cargas", min_value=1, max_value=10, value=2, step=1)

    cargas_texto = []
    posiciones_texto = []

    for i in range(int(n)):
        st.markdown(f"**Carga {i+1}**")
        q_txt = st.text_input(f"q{i+1} (C)", value="1x10^-6", key=f"q_{i}")
        pos_txt = st.text_input(f"Posición q{i+1} (x,y)", value=f"({i+1},0)", key=f"p_{i}")
        cargas_texto.append(q_txt)
        posiciones_texto.append(pos_txt)

    calcular = st.button("Calcular fuerza neta", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if calcular:
        try:
            q_obj = convertir_notacion(q_obj_texto)
            x_obj, y_obj = parsear_coordenada(pos_obj_texto)

            cargas = []
            for q_txt, pos_txt in zip(cargas_texto, posiciones_texto):
                q = convertir_notacion(q_txt)
                x, y = parsear_coordenada(pos_txt)
                cargas.append({"q": q, "x": x, "y": y})

            fx_total, fy_total, magnitud, registros = calcular_fuerza_total(
                q_obj, x_obj, y_obj, cargas
            )

            # RESULTADOS PRINCIPALES
            st.subheader("Resultados principales")
            m1, m2, m3 = st.columns(3)
            m1.metric("Fx neta", f"{fx_total:.4e} N")
            m2.metric("Fy neta", f"{fy_total:.4e} N")
            m3.metric("Magnitud", f"{magnitud:.4e} N")

            st.markdown("### Vector fuerza neta")
            st.code(f"<{fx_total:.4e}, {fy_total:.4e}> N")

            # TABLA
            st.markdown("### Resumen por carga")
            df = pd.DataFrame(registros)
            columnas_numericas = ["q (C)", "r (m)", "Fx (N)", "Fy (N)"]
            for col in columnas_numericas:
                df[col] = df[col].map(lambda x: f"{x:.4e}")
            st.dataframe(df, use_container_width=True, hide_index=True)

            # GRÁFICA
            st.markdown("### Gráfica del sistema")
            fig = crear_grafica(x_obj, y_obj, q_obj, cargas, fx_total, fy_total)
            st.plotly_chart(fig, use_container_width=True)

            # PROCEDIMIENTO
            st.markdown("### Procedimiento de cálculo")

            st.markdown("""
            <div class="bloque">
            <b>1. Fórmulas utilizadas</b>
            </div>
            """, unsafe_allow_html=True)

            st.write("Para resolver el problema, se emplea la forma vectorial de la Ley de Coulomb:")
            st.latex(r"F_x = k \frac{q_0 q_i \, dx}{r^3}")
            st.latex(r"F_y = k \frac{q_0 q_i \, dy}{r^3}")
            st.latex(r"r = \sqrt{dx^2 + dy^2}")
            st.latex(r"|F| = \sqrt{F_x^2 + F_y^2}")

            st.markdown("""
            <div class="bloque">
            <b>2. Sustitución y desarrollo por cada carga</b>
            </div>
            """, unsafe_allow_html=True)

            for i, carga in enumerate(cargas, start=1):
                q = carga["q"]
                x = carga["x"]
                y = carga["y"]

                fx, fy, r = calcular_fuerza_individual(q_obj, x_obj, y_obj, q, x, y)

                dx = x_obj - x
                dy = y_obj - y

                with st.expander(f"Desarrollo de la carga {i}", expanded=(i == 1)):
                    st.markdown(f"### Carga {i}")

                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 1: Identificar los datos</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.write(f"- Carga objetivo: q₀ = {q_obj:.4e} C en ({x_obj}, {y_obj})")
                    st.write(f"- Carga analizada: q{i} = {q:.4e} C en ({x}, {y})")

                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 2: Calcular las diferencias de posición</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.write("Estas diferencias muestran cuánto separada está la carga objetivo de la carga analizada en cada eje.")
                    st.write(f"- dx = x₀ - x{i} = {x_obj} - {x} = {dx}")
                    st.write(f"- dy = y₀ - y{i} = {y_obj} - {y} = {dy}")

                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 3: Calcular la distancia entre ambas cargas</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.write("Se usa la fórmula de distancia entre dos puntos en el plano cartesiano:")
                    st.latex(r"r = \sqrt{dx^2 + dy^2}")
                    st.write(f"Entonces, la distancia entre las dos cargas es: r = {r:.4e} m")

                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 4: Sustituir en la Ley de Coulomb</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.write("Con la distancia y las diferencias de posición ya calculadas, se sustituyen los valores en las fórmulas de las componentes de la fuerza:")

                    st.latex(r"F_x = k \frac{q_0 q_i \, dx}{r^3}")
                    st.latex(r"F_y = k \frac{q_0 q_i \, dy}{r^3}")

                    st.write("Sustitución en la componente horizontal:")
                    st.latex(
                        rf"F_x = 9\times10^9 \cdot \frac{{({q_obj:.4e})({q:.4e})({dx:.4e})}}{{({r:.4e})^3}} = {fx:.4e}\,N"
                    )

                    st.write("Sustitución en la componente vertical:")
                    st.latex(
                        rf"F_y = 9\times10^9 \cdot \frac{{({q_obj:.4e})({q:.4e})({dy:.4e})}}{{({r:.4e})^3}} = {fy:.4e}\,N"
                    )

                    st.markdown("""
                    <div class="paso-box">
                    <div class="paso-title">Paso 5: Interpretar el resultado de esta carga</div>
                    </div>
                    """, unsafe_allow_html=True)

                    if fx > 0:
                        st.write("- La componente en X es positiva, por lo tanto esta carga aporta hacia la derecha.")
                    elif fx < 0:
                        st.write("- La componente en X es negativa, por lo tanto esta carga aporta hacia la izquierda.")
                    else:
                        st.write("- La componente en X es cero, así que no hay aporte horizontal.")

                    if fy > 0:
                        st.write("- La componente en Y es positiva, por lo tanto esta carga aporta hacia arriba.")
                    elif fy < 0:
                        st.write("- La componente en Y es negativa, por lo tanto esta carga aporta hacia abajo.")
                    else:
                        st.write("- La componente en Y es cero, así que no hay aporte vertical.")

            st.markdown("""
            <div class="bloque">
            <b>3. Aplicar el Principio de Superposición</b>
            </div>
            """, unsafe_allow_html=True)

            st.write("Después de calcular la fuerza que ejerce cada carga por separado, se suman todas las componentes horizontales y todas las componentes verticales.")
            st.write("Esto se hace porque la fuerza eléctrica neta es una suma vectorial de todas las fuerzas individuales.")

            st.latex(r"F_{x,\text{neta}} = \sum F_{x_i}")
            st.latex(r"F_{y,\text{neta}} = \sum F_{y_i}")

            st.write(f"- Componente neta en X: {fx_total:.4e} N")
            st.write(f"- Componente neta en Y: {fy_total:.4e} N")

            st.markdown("""
            <div class="bloque">
            <b>4. Calcular la magnitud de la fuerza neta</b>
            </div>
            """, unsafe_allow_html=True)

            st.write("Una vez obtenidas las componentes netas en X y Y, se calcula la magnitud del vector resultante usando el teorema de Pitágoras:")
            st.latex(r"|F| = \sqrt{F_x^2 + F_y^2}")

            st.write("Sustituyendo los valores finales:")
            st.latex(
                rf"|F| = \sqrt{{({fx_total:.4e})^2 + ({fy_total:.4e})^2}} = {magnitud:.4e}\,N"
            )

            st.write("Este valor representa la intensidad total de la fuerza eléctrica neta que actúa sobre la carga objetivo.")

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.markdown("""
        <div class="bloque">
        <h3>Guía rápida de uso</h3>
        <p>
        Esta aplicación resuelve ejercicios de electrostática con cargas puntuales.
        Ingresa la magnitud y la posición de la carga objetivo, luego añade las cargas del sistema.
        Al presionar <b>Calcular fuerza neta</b>, la app mostrará:
        </p>
        <ul>
            <li>Las componentes netas en X y Y</li>
            <li>La magnitud total de la fuerza</li>
            <li>Una tabla con cada contribución individual</li>
            <li>La gráfica del plano cartesiano con la flecha del vector resultante</li>
            <li>El procedimiento matemático paso a paso</li>
        </ul>
        <p>
        Esto permite no solo obtener el resultado, sino también comprender cómo se llegó a él.
        </p>
        </div>
        """, unsafe_allow_html=True)