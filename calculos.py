import math

K = 9e9  # Constante de Coulomb


def calcular_fuerza_individual(q_obj, x_obj, y_obj, q, x, y):
    """
    Calcula la fuerza que una carga puntual ejerce sobre la carga objetivo.
    Retorna Fx, Fy y la distancia r.
    """
    dx = x_obj - x
    dy = y_obj - y
    r = math.sqrt(dx**2 + dy**2)

    if r == 0:
        raise ValueError("Dos cargas no pueden estar en la misma posición.")

    fx = K * q_obj * q * dx / (r**3)
    fy = K * q_obj * q * dy / (r**3)

    return fx, fy, r


def calcular_fuerza_total(q_obj, x_obj, y_obj, cargas):
    """
    Calcula la fuerza neta sobre la carga objetivo.
    """
    fx_total = 0.0
    fy_total = 0.0
    registros = []

#Utilizamos un ciclo for porque la carga objetivo puede estar influenciada por varias cargas puntuales, 
# y necesitamos calcular la contribución de cada una para obtener la fuerza neta total.    

    for i, carga in enumerate(cargas, start=1):

        #Cada carga se guarda como un diccionario con sus datos.
        q = carga["q"]
        x = carga["x"]
        y = carga["y"]

        fx, fy, r = calcular_fuerza_individual(q_obj, x_obj, y_obj, q, x, y)

        fx_total += fx
        fy_total += fy

        registros.append({
            "Carga": i,
            "q (C)": q,
            "Posición": f"({x}, {y})",
            "r (m)": r,
            "Fx (N)": fx,
            "Fy (N)": fy
        })

    magnitud = math.sqrt(fx_total**2 + fy_total**2)

    return fx_total, fy_total, magnitud, registros