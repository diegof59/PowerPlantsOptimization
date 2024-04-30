import tkinter as tk
from tkinter import ttk, Entry, Scrollbar, RIDGE, Label, Button, END, Toplevel
from tkinter.font import Font
from utils import *

# Global variables
num_days = 0
num_clients = 0
centrales = ["Nuclear", "Hidroeléctrica", "Térmica"]
g = 0
pago = []
capacidad = []
costo = []
demanda = []

# Methods

def set_container_color(container, color):
    container.configure(bg=color)

def init_tb_payments(num_clients: int):
    columnas = []
    # cleanup container4
    container4.delete("all")
    lb_clients_c4 = Label(
        container4, text="Clientes", font=('Arial', 12), bg="lightgray")
    lb_pago_c4 = Label(container4, text="Pago",
                       font=('Arial', 12), bg="lightgray")
    container4.create_window(
        (50, 30), window=lb_clients_c4, anchor="nw")
    container4.create_window(
        (200, 30), window=lb_pago_c4, anchor="nw")

    for i in range(2):
        filas = []
        for j in range(num_clients):
            data = f'Cliente {j+1}' if i == 0 else ""
            e = Entry(container4, relief=RIDGE)
            e.insert(END, data)
            e.configure(validate="key", validatecommand=(
                e.register(validate_float_input), "%P")
            )
            container4.create_window(
                (4+i*160, 50+j*20), window=e, anchor="nw")
            filas.append(e)
        columnas.append(filas)
    pago.append(columnas)

def init_tb_demanda(num_clients: int, num_days: int):
    columnas = []
    # cleanup container4
    container6.delete("all")
    lb_clients_c6 = Label(
        container6, text="Clientes", font=('Arial', 12), bg="lightgray")
    container6.create_window(
        (50, 50), window=lb_clients_c6, anchor="nw")

    for i in range(num_days + 1):
        filas = []
        data = f'Día {i}' if i >= 1 else ""
        lb_days_c6 = Label(
            container6, text=data, font=('Arial', 12), bg="lightgray")
        container6.create_window(
            (160*i, 50), window=lb_days_c6, anchor="nw")
        for j in range(num_clients):
            data = f'Cliente {j+1}' if i == 0 else ""
            e = Entry(container6, relief=RIDGE)
            e.insert(END, data)
            container6.create_window(
                (4+i*160, 70+j*20), window=e, anchor="nw")
            filas.append(e)
        columnas.append(filas)
    demanda.append(columnas)

def init_tb_capacidad():
    columnas = []
    container5.delete("all")
    lb_centrales_c5 = Label(
        container5, text="Centrales", font=('Arial', 16), bg="lightgray")
    container5.create_window(
        (50, 0), window=lb_centrales_c5, anchor="nw")
    lb_capacidad_c5 = Label(
        container5, text="Capacidad", font=('Arial', 16), bg="lightgray")
    container5.create_window(
        (200, 0), window=lb_capacidad_c5, anchor="nw")
    lb_costo_c5 = Label(
        container5, text="Costo", font=('Arial', 16), bg="lightgray")
    container5.create_window(
        (350, 0), window=lb_costo_c5, anchor="nw")

    for i in range(len(centrales)):
        filas = []
        lb_central_c5 = Label(
            container5, text=centrales[i], font=('Arial', 12), bg="lightgray")
        container5.create_window(
            (50, 35 + i * 30), window=lb_central_c5, anchor="nw")

        e_capacidad = Entry(container5, relief=RIDGE)
        e_capacidad.insert(END, "")
        container5.create_window(
            (200, 30 + i * 30), window=e_capacidad, anchor="nw")
        filas.append(e_capacidad)

        e_costo = Entry(container5, relief=RIDGE)
        e_costo.insert(END, "")
        container5.create_window(
            (350, 30 + i * 30), window=e_costo, anchor="nw")
        filas.append(e_costo)

        columnas.append(filas)
    capacidad.append(columnas)

def disable_button():
    if num_days > 0 or num_clients > 0:
        boton_solve.config(state="normal")
    else:
        boton_solve.config(state="disabled")

def create_table(ganancia, producion, num_clients, num_days):

    window = Toplevel(root)
    window.title("resultados")

    columns = ["Clientes / Plantas"] + [f"Día {i+1}" for i in range(num_days)]
    columns.append("Producción Total (MW)")
    table = ttk.Treeview(window, columns=columns)

    for col in columns:
        table.heading(col, text=col)

    nuclear_totals = [0.0] * num_days
    hydro_totals = [0.0] * num_days
    thermal_totals = [0.0] * num_days

    for i in range(num_clients):
        start = i * num_days * 3
        end = start + num_days * 3

        if end <= len(producion):  # Verifica que haya suficientes elementos en data
            client_data = [producion[j:j+3] for j in range(start, end, 3)]
            client_num = i + 1

            # Formatear la lista de tuplas como cadenas
            formatted_data = [str(tuple) for tuple in client_data]

        # Calcular las sumas para las plantas
            for j in range(num_days):
                nuclear_totals[j] += client_data[j][0]
                hydro_totals[j] += client_data[j][1]
                thermal_totals[j] += client_data[j][2]

            table.insert("", "end", values=[
                f"Cliente {client_num}"] + formatted_data)
        else:
            print(
                f"No hay suficientes datos en 'data' para el cliente")

    nuclear_totals.append(sum(nuclear_totals))
    hydro_totals.append(sum(hydro_totals))
    thermal_totals.append(sum(thermal_totals))

    # Insertar filas para las sumas de plantas
    table.insert("", "end", values=["Nuclear"] +
                 [f"{total:.1f}" for total in nuclear_totals])
    table.insert("", "end", values=[
                 "Hidroeléctrica"] + [f"{total:.1f}" for total in hydro_totals])
    table.insert("", "end", values=["Térmica"] +
                 [f"{total:.1f}" for total in thermal_totals])

    # Insertar la fila de Ganancia Total
    table.insert("", "end", values=["Ganancia Total", ganancia])

    table.pack()

def clickStart():
    global num_clients, num_days, g
    try:
        num_clients = int(input_clients.get(), 10)
        num_days = int(input_days.get(), 10)
        g = float(input_g.get())
        # Agregar entradas a container4
        init_tb_payments(num_clients)
        init_tb_demanda(num_clients, num_days)
        init_tb_capacidad()
        disable_button()
    except IndexError:
        pass  # Manejo de excepción

def clickSolve():
    global num_clients, num_days, g

    num_clients = int(input_clients.get(), 10)
    num_days = int(input_days.get(), 10)
    g = float(input_g.get())
    capacidad_values = []
    costo_values = []
    demanda_values = []
    pago_values = []

    try:
        for i in range(1, len(demanda[0])):
            lista = demanda[0][i]
            temp = []
            for j in range(len(lista)):
                temp.append(float(lista[j].get()))
            demanda_values.append(temp)

        demanda_values = [list(x) for x in zip(*demanda_values)]

        for i in range(len(pago[0][1])):
            value = pago[0][1][i].get()
            pago_values.append(float(value))

        for i in range(len(capacidad[0])):
            value = capacidad[0][i][0].get()
            capacidad_values.append(float(value))
            value = capacidad[0][i][1].get()
            costo_values.append(float(value))

        data = solve(g, num_clients, num_days, costo_values,
                     capacidad_values, pago_values, demanda_values)
        ganancia = data[0]
        producion = data[1]

        create_table(ganancia, producion, num_clients, num_days)

    except ValueError:
        t = Toplevel(root)
        t.wm_title("Error")
        t.geometry("480x40")
        t.resizable(False, False)
        label_t = Label(t, text="ERROR: Complete o inserte datos validos", font=(
            'Arial', 20), fg="red")
        label_t.place(relx=0, y=0)

    # solve(g, num_clients, num_days, costo, capacidad,
    #       pago, demanda)

def on_horizontal_scroll(event):
    container = event.widget
    if event.delta > 0:
        container.xview_scroll(-1, "units")
    else:
        container.xview_scroll(1, "units")

root = tk.Tk()
root.title("Planta-de-Energı́a")

# Setup rows and columns for distribution
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=19)
root.grid_rowconfigure(2, weight=35)
root.grid_rowconfigure(3, weight=45)  # container6
root.grid_columnconfigure(0, weight=50)
root.grid_columnconfigure(1, weight=50)

# Create containers
container1 = tk.Frame(root)
container2 = tk.Frame(root)

container4 = tk.Canvas(root, bg="lightgray")
scrollbar4_y = Scrollbar(container4, orient="vertical")
container4.config(yscrollcommand=scrollbar4_y.set)
scrollbar4_y.config(command=container4.yview)
container4.bind("<MouseWheel>", on_horizontal_scroll)

container5 = tk.Canvas(root, bg="lightgray")
scrollbar5_y = Scrollbar(container5, orient="vertical")
scrollbar5_x = Scrollbar(container5, orient="horizontal")
container5.config(yscrollcommand=scrollbar5_y.set,
                  xscrollcommand=scrollbar5_x.set)
scrollbar5_y.config(command=container5.yview)
scrollbar5_x.config(command=container5.xview)

container6 = tk.Canvas(root, bg="lightgray")
scrollbar6_y = Scrollbar(container6, orient="vertical")
scrollbar6_x = Scrollbar(container6, orient="horizontal")
container6.config(yscrollcommand=scrollbar6_y.set,
                  xscrollcommand=scrollbar6_x.set)
scrollbar6_y.config(command=container6.yview)
scrollbar6_x.config(command=container6.xview)

container1.grid(row=0, column=0, columnspan=2, sticky="nsew")
container2.grid(row=1, column=0, sticky="nsew")

container4.grid(row=2, column=0, sticky="nsew")
scrollbar4_y.pack(side="right", fill="y")

container5.grid(row=2, column=1, sticky="nsew")
scrollbar5_y.pack(side="right", fill="y")
scrollbar5_x.pack(side="bottom", fill="x")

container6.grid(row=3, column=0, columnspan=2, sticky="nsew")
scrollbar6_y.pack(side="right", fill="y")
scrollbar6_x.pack(side="bottom", fill="x")

# Containers data

# container1
title_font = Font(family="Arial", size=20, weight="bold")
title_label = Label(container1, text="Plantas de Energía", font=title_font, bg="lightgray")
title_label.pack(fill="both", expand=True)

# container2
lb_clients = Label(container2, text="Ingrese el número de clientes =>", bg="lightgray")
lb_clients.place(x=20, y=10)

lb_days = Label(container2, text="Ingrese el número de días =>", bg="lightgray")
lb_days.place(x=20, y=30)

lb_clients = Label(container2, text="Porcentaje mínimo demanda =>", bg="lightgray")
lb_clients.place(x=20, y=50)

input_clients = Entry(container2, width=10)
input_clients.place(x=230, y=10)
input_clients.configure(validate="key", validatecommand=(
    input_clients.register(validate_int_input), "%P"))

input_days = Entry(container2, width=10)
input_days.place(x=230, y=30)
input_days.configure(validate="key", validatecommand=(
    input_days.register(validate_int_input), "%P"))

input_g = Entry(container2, width=10)
input_g.place(x=230, y=50)
input_g.configure(validate="key", validatecommand=(
    input_g.register(validate_float_input), "%P"))

boton_cargar = Button(
    container2, text="Iniciar carga de datos", command=clickStart, width=25)
boton_cargar.place(x=50, y=80)

boton_solve = Button(
    container2, text="Calcular", command=clickSolve, width=20, state="disabled")
boton_solve.place(x=400, y=30)

# Set scrollregion to update scrollbars
container4.update_idletasks()
container5.update_idletasks()
container6.update_idletasks()

container4.config(scrollregion=container4.bbox("all"))
container5.config(scrollregion=container5.bbox("all"))
container6.config(scrollregion=container6.bbox("all"))

# Start the application
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.mainloop()
