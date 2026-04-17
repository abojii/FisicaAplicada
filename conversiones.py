def convertir_notacion(texto):
    """
    Convierte entradas como:
    2x10^-6, 2*10^-6, 2e-6, 0.000002
    a float.
    """
    texto = str(texto).lower().replace(" ", "")

    if "x10^" in texto:
        base, exponente = texto.split("x10^")
        return float(base) * (10 ** float(exponente))
    elif "*10^" in texto:
        base, exponente = texto.split("*10^")
        return float(base) * (10 ** float(exponente))
    else:
        return float(texto)


def parsear_coordenada(texto):
    """
    Convierte una coordenada tipo (x,y) a dos valores float.
    """
    texto = str(texto).replace(" ", "").replace("(", "").replace(")", "")
    partes = texto.split(",")

    if len(partes) != 2:
        raise ValueError("La coordenada debe tener formato (x,y).")

    x = convertir_notacion(partes[0])
    y = convertir_notacion(partes[1])
    return x, y