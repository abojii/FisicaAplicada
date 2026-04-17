import math
import plotly.graph_objects as go


def crear_grafica(x_obj, y_obj, q_obj, cargas, fx_total, fy_total):
    """
    Crea una gráfica interactiva del sistema de cargas y del vector
    de fuerza neta sobre la carga objetivo.
    """

    fig = go.Figure()

    # -----------------------------
    # Cargas puntuales
    # -----------------------------
    for i, carga in enumerate(cargas, start=1):
        color = "#ff4d4f" if carga["q"] > 0 else "#4da6ff"

        fig.add_trace(go.Scatter(
            x=[carga["x"]],
            y=[carga["y"]],
            mode="markers+text",
            marker=dict(size=14, color=color, line=dict(color="white", width=1)),
            text=[f"q{i}"],
            textposition="top center",
            name=f"q{i} = {carga['q']:.2e} C"
        ))

    # -----------------------------
    # Carga objetivo
    # -----------------------------
    fig.add_trace(go.Scatter(
        x=[x_obj],
        y=[y_obj],
        mode="markers+text",
        marker=dict(size=20, color="gold", symbol="star", line=dict(color="white", width=1)),
        text=["Objetivo"],
        textposition="top center",
        name=f"Objetivo ({q_obj:.2e} C)"
    ))

    # -----------------------------
    # Escala inteligente para que la flecha sí se vea
    # -----------------------------
    magnitud = math.sqrt(fx_total**2 + fy_total**2)

    xs_cargas = [x_obj] + [c["x"] for c in cargas]
    ys_cargas = [y_obj] + [c["y"] for c in cargas]

    ancho_base = max(xs_cargas) - min(xs_cargas) if len(xs_cargas) > 1 else 2
    alto_base = max(ys_cargas) - min(ys_cargas) if len(ys_cargas) > 1 else 2
    escala_base = max(ancho_base, alto_base, 2)

    # Si la fuerza es muy pequeña, la flecha sigue siendo visible.
    if magnitud != 0:
        largo_flecha = escala_base * 0.35
        ux = fx_total / magnitud
        uy = fy_total / magnitud
        x_final = x_obj + ux * largo_flecha
        y_final = y_obj + uy * largo_flecha
    else:
        x_final = x_obj
        y_final = y_obj

    # -----------------------------
    # Flecha de fuerza neta
    # -----------------------------
    if magnitud != 0:
        fig.add_annotation(
            x=x_final,
            y=y_final,
            ax=x_obj,
            ay=y_obj,
            xref="x",
            yref="y",
            axref="x",
            ayref="y",
            showarrow=True,
            arrowhead=4,
            arrowsize=1.8,
            arrowwidth=4,
            arrowcolor="#22c55e"
        )

        fig.add_trace(go.Scatter(
            x=[(x_obj + x_final) / 2],
            y=[(y_obj + y_final) / 2],
            mode="text",
            text=["Fuerza neta"],
            textfont=dict(color="#22c55e", size=14),
            showlegend=False
        ))
    else:
        fig.add_trace(go.Scatter(
            x=[x_obj],
            y=[y_obj],
            mode="text",
            text=["Fuerza neta = 0"],
            textfont=dict(color="#22c55e", size=14),
            showlegend=False
        ))

    # -----------------------------
    # Límites del plano
    # -----------------------------
    xs = xs_cargas + [x_final]
    ys = ys_cargas + [y_final]

    margen = 1
    xmin, xmax = min(xs) - margen, max(xs) + margen
    ymin, ymax = min(ys) - margen, max(ys) + margen

    # -----------------------------
    # Diseño estilo académico / GeoGebra oscuro
    # -----------------------------
    fig.update_layout(
        title=dict(
            text="Plano cartesiano de cargas y vector de fuerza neta",
            font=dict(size=20, color="white")
        ),
        template="plotly_dark",
        height=620,
        xaxis=dict(
            title="Eje X (m)",
            range=[xmin, xmax],
            showgrid=True,
            gridcolor="rgba(255,255,255,0.12)",
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor="white",
            tickfont=dict(color="white"),
            title_font=dict(color="white"),
            scaleanchor="y",
            scaleratio=1
        ),
        yaxis=dict(
            title="Eje Y (m)",
            range=[ymin, ymax],
            showgrid=True,
            gridcolor="rgba(255,255,255,0.12)",
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor="white",
            tickfont=dict(color="white"),
            title_font=dict(color="white")
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(color="white")
        ),
        paper_bgcolor="#0b1220",
        plot_bgcolor="#0b1220"
    )

    return fig