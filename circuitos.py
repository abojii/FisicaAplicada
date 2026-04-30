def resolver_resistores_serie(voltaje, resistencias):
    req = sum(resistencias)
    corriente = voltaje / req

    registros = []
    for i, r in enumerate(resistencias, start=1):
        v_i = corriente * r
        registros.append({
            "Elemento": f"R{i}",
            "Valor": r,
            "Voltaje (V)": v_i,
            "Corriente (A)": corriente
        })

    return req, corriente, registros


def resolver_resistores_paralelo(voltaje, resistencias):
    req = 1 / sum(1 / r for r in resistencias)
    corriente_total = voltaje / req

    registros = []
    for i, r in enumerate(resistencias, start=1):
        i_i = voltaje / r
        registros.append({
            "Elemento": f"R{i}",
            "Valor": r,
            "Voltaje (V)": voltaje,
            "Corriente (A)": i_i
        })

    return req, corriente_total, registros


def resolver_capacitores_serie(voltaje, capacitancias):
    ceq = 1 / sum(1 / c for c in capacitancias)
    carga = ceq * voltaje

    registros = []
    for i, c in enumerate(capacitancias, start=1):
        v_i = carga / c
        registros.append({
            "Elemento": f"C{i}",
            "Valor": c,
            "Carga (C)": carga,
            "Voltaje (V)": v_i
        })

    return ceq, carga, registros


def resolver_capacitores_paralelo(voltaje, capacitancias):
    ceq = sum(capacitancias)
    carga_total = ceq * voltaje

    registros = []
    for i, c in enumerate(capacitancias, start=1):
        q_i = c * voltaje
        registros.append({
            "Elemento": f"C{i}",
            "Valor": c,
            "Carga (C)": q_i,
            "Voltaje (V)": voltaje
        })

    return ceq, carga_total, registros