import math


def parsear_vector(texto):
    texto = str(texto).replace(" ", "").replace("(", "").replace(")", "")
    partes = texto.split(",")

    if len(partes) != 3:
        raise ValueError("El vector debe tener formato (x,y,z).")

    return tuple(float(p) for p in partes)


def producto_vectorial(a, b):
    ax, ay, az = a
    bx, by, bz = b

    cx = ay * bz - az * by
    cy = az * bx - ax * bz
    cz = ax * by - ay * bx

    return (cx, cy, cz)


def magnitud_vector(v):
    x, y, z = v
    return math.sqrt(x**2 + y**2 + z**2)


def vector_desde_puntos(p, q):
    px, py, pz = p
    qx, qy, qz = q

    return (
        qx - px,
        qy - py,
        qz - pz
    )


def fuerza_magnetica(corriente, vector_l, campo_b):
    producto = producto_vectorial(vector_l, campo_b)

    return (
        corriente * producto[0],
        corriente * producto[1],
        corriente * producto[2]
    )