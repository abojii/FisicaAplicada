import plotly.graph_objects as go


def crear_dibujo_circuito(tipo, conexion, valores):
    fig = go.Figure()

    fig.update_layout(
        template="plotly_dark",
        height=430,
        title=f"Circuito de {tipo} en {conexion}",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor="#0b1220",
        paper_bgcolor="#0b1220",
        margin=dict(l=20, r=20, t=50, b=20)
    )

    cantidad = len(valores)

    # Línea base del circuito
    y_top = 3
    y_bottom = 0
    x_left = 0
    x_right = max(5, cantidad * 2)

    # Batería izquierda
    fig.add_shape(type="line", x0=x_left, y0=y_bottom, x1=x_left, y1=1.2, line=dict(color="white", width=3))
    fig.add_shape(type="line", x0=x_left, y0=1.8, x1=x_left, y1=y_top, line=dict(color="white", width=3))

    fig.add_shape(type="line", x0=-0.25, y0=1.2, x1=0.25, y1=1.2, line=dict(color="#22c55e", width=2))
    fig.add_shape(type="line", x0=-0.35, y0=1.8, x1=0.35, y1=1.8, line=dict(color="#22c55e", width=4))

    fig.add_annotation(x=-0.6, y=1.5, text="Batería", showarrow=False, font=dict(color="white"))
    fig.add_annotation(x=-0.45, y=1.95, text="+", showarrow=False, font=dict(color="white", size=16))
    fig.add_annotation(x=-0.45, y=1.05, text="-", showarrow=False, font=dict(color="white", size=16))

    if conexion == "Serie":
        # Cables laterales y abajo
        fig.add_shape(type="line", x0=x_left, y0=y_top, x1=1, y1=y_top, line=dict(color="white", width=3))
        fig.add_shape(type="line", x0=x_right, y0=y_top, x1=x_right, y1=y_bottom, line=dict(color="white", width=3))
        fig.add_shape(type="line", x0=x_right, y0=y_bottom, x1=x_left, y1=y_bottom, line=dict(color="white", width=3))

        espacio = (x_right - 2) / cantidad
        x_actual = 1

        for i, valor in enumerate(valores, start=1):
            x1 = x_actual
            x2 = x_actual + espacio * 0.55
            centro = (x1 + x2) / 2

            # cable antes
            fig.add_shape(type="line", x0=x_actual, y0=y_top, x1=x1, y1=y_top, line=dict(color="white", width=3))

            if tipo == "Resistores":
                fig.add_shape(
                    type="rect",
                    x0=x1, y0=y_top - 0.25,
                    x1=x2, y1=y_top + 0.25,
                    line=dict(color="#38bdf8", width=2),
                    fillcolor="#111827"
                )
            else:
                # Capacitor: dos placas
                fig.add_shape(type="line", x0=centro - 0.12, y0=y_top - 0.35, x1=centro - 0.12, y1=y_top + 0.35,
                              line=dict(color="#38bdf8", width=4))
                fig.add_shape(type="line", x0=centro + 0.12, y0=y_top - 0.35, x1=centro + 0.12, y1=y_top + 0.35,
                              line=dict(color="#38bdf8", width=4))

            letra = "R" if tipo == "Resistores" else "C"

            fig.add_annotation(
                x=centro,
                y=y_top + 0.6,
                text=f"{letra}{i}<br>{valor:.2e}",
                showarrow=False,
                font=dict(color="white")
            )

            # cable después
            x_actual = x_actual + espacio
            fig.add_shape(type="line", x0=x2, y0=y_top, x1=x_actual, y1=y_top, line=dict(color="white", width=3))

        fig.add_shape(type="line", x0=x_actual, y0=y_top, x1=x_right, y1=y_top, line=dict(color="white", width=3))

    else:
        # Paralelo: dos rieles
        fig.add_shape(type="line", x0=x_left, y0=1.5, x1=1, y1=1.5, line=dict(color="white", width=3))
        fig.add_shape(type="line", x0=1, y0=3.3, x1=1, y1=-0.3, line=dict(color="white", width=3))
        fig.add_shape(type="line", x0=x_right, y0=3.3, x1=x_right, y1=-0.3, line=dict(color="white", width=3))

        espacio = 3 / max(cantidad - 1, 1)

        for i, valor in enumerate(valores, start=1):
            y = 3 - (i - 1) * espacio

            fig.add_shape(type="line", x0=1, y0=y, x1=2.1, y1=y, line=dict(color="white", width=3))

            if tipo == "Resistores":
                fig.add_shape(
                    type="rect",
                    x0=2.1, y0=y - 0.22,
                    x1=3.4, y1=y + 0.22,
                    line=dict(color="#38bdf8", width=2),
                    fillcolor="#111827"
                )
            else:
                # Capacitor en paralelo
                fig.add_shape(type="line", x0=2.65, y0=y - 0.35, x1=2.65, y1=y + 0.35,
                              line=dict(color="#38bdf8", width=4))
                fig.add_shape(type="line", x0=2.95, y0=y - 0.35, x1=2.95, y1=y + 0.35,
                              line=dict(color="#38bdf8", width=4))

            letra = "R" if tipo == "Resistores" else "C"

            fig.add_annotation(
                x=2.75,
                y=y + 0.55,
                text=f"{letra}{i}<br>{valor:.2e}",
                showarrow=False,
                font=dict(color="white")
            )

            fig.add_shape(type="line", x0=3.4, y0=y, x1=x_right, y1=y, line=dict(color="white", width=3))

        fig.add_shape(type="line", x0=x_right, y0=1.5, x1=x_right + 0.7, y1=1.5, line=dict(color="white", width=3))
        fig.add_shape(type="line", x0=x_right + 0.7, y0=1.5, x1=x_right + 0.7, y1=0, line=dict(color="white", width=3))
        fig.add_shape(type="line", x0=x_right + 0.7, y0=0, x1=x_left, y1=0, line=dict(color="white", width=3))

    return fig