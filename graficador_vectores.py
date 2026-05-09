import plotly.graph_objects as go


def agregar_vector(fig, vector, nombre, color):
    x, y, z = vector

    fig.add_trace(go.Scatter3d(
        x=[0, x],
        y=[0, y],
        z=[0, z],
        mode="lines+markers+text",
        line=dict(color=color, width=7),
        marker=dict(size=4, color=color),
        text=["", nombre],
        textposition="top center",
        name=nombre
    ))


def crear_grafica_vectores(vector_a, vector_b, vector_resultado):
    fig = go.Figure()

    agregar_vector(fig, vector_a, "Vector A", "#38bdf8")
    agregar_vector(fig, vector_b, "Vector B", "#22c55e")
    agregar_vector(fig, vector_resultado, "A × B", "#ef4444")

    fig.update_layout(
        template="plotly_dark",
        height=560,
        title="Visualización 3D del producto vectorial",
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
            bgcolor="#0b1220"
        ),
        paper_bgcolor="#0b1220",
        plot_bgcolor="#0b1220",
        legend=dict(
            font=dict(color="white")
        )
    )

    return fig


def crear_grafica_fuerza(vector_l, campo_b, fuerza):
    fig = go.Figure()

    agregar_vector(fig, vector_l, "Vector L", "#38bdf8")
    agregar_vector(fig, campo_b, "Campo B", "#22c55e")
    agregar_vector(fig, fuerza, "Fuerza magnética", "#ef4444")

    fig.update_layout(
        template="plotly_dark",
        height=560,
        title="Fuerza magnética: F = I(L × B)",
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
            bgcolor="#0b1220"
        ),
        paper_bgcolor="#0b1220",
        plot_bgcolor="#0b1220",
        legend=dict(
            font=dict(color="white")
        )
    )

    return fig