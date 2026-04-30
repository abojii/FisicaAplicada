import re

PREFIJOS = {
    "p": 1e-12,
    "n": 1e-9,
    "u": 1e-6,
    "µ": 1e-6,
    "m": 1e-3,
    "k": 1e3,
    "K": 1e3,
    "M": 1e6,
    "G": 1e9
}


def convertir_prefijo(texto):
    """
    Convierte valores como:
    53mV, 10K, 3553pF, 2.2uF, 1M
    a su valor base numérico.
    """
    texto = str(texto).strip().replace(" ", "")

    patron = r"^([-+]?\d*\.?\d+)([pnuµmKkMG]?)[a-zA-ZΩ]*$"
    match = re.match(patron, texto)

    if not match:
        raise ValueError(f"Valor inválido: {texto}")

    numero = float(match.group(1))
    prefijo = match.group(2)

    factor = PREFIJOS.get(prefijo, 1)

    return numero * factor