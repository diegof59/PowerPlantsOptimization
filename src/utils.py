import os
# Rutas a los archivos del modelo y datos
model_path = './PlantaEnergia.mzn'
data_path = './Datos.dzn'

def validate_int_input(P):
    if P == "":
        return True
    try:
        int(P)
        return True
    except ValueError:
        return False


def validate_float_input(P):
    if P == "":
        return True
    try:
        float(P)
        return True
    except ValueError:
        return False


def write_data(G, num_clientes, num_dias, costo, capacidad, pago, nueva_demanda, file_name=data_path):
    with open(file_name, 'w') as file:
        file.write(f"G = {G};\n")
        file.write(f"costo = {costo};\n")
        file.write(f"capacidad = {capacidad};\n")
        file.write(f"num_clientes = {num_clientes};\n")
        file.write(f"num_dias = {num_dias};\n")
        file.write(f"num_plantas = {3};\n")
        file.write(f"pago = {pago};\n")
        file.write("demanda = [")
        for fila in nueva_demanda:
            file.write("|")
            file.write(", ".join(map(str, fila)))
            file.write("\n")
        file.write("        |];\n")


def solve(G, num_clientes, num_dias, costo, capacidad, pago, nueva_demanda, file_name=data_path):
    write_data(G, num_clientes, num_dias, costo, capacidad,
               pago, nueva_demanda, file_name)
    result = os.popen(
        f'minizinc --solver HiGHS {model_path} {data_path}').read()

    if result != "UNSATISFIABLE\n":
        r = result.split('&')
        ganancia = r[0]
        index = r[1].index(']')
        production_str = r[1][1:index].split(', ')
        production_str = [valor.rstrip(',') for valor in production_str]
        production = [float(valor) for valor in production_str]
    return [ganancia, production]
