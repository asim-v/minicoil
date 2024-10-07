import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Usar el backend de TkAgg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.io import savemat
import tkinter as tk
from tkinter import ttk

# Configuración inicial de los parámetros
initial_num_springs = 4
initial_r_inicial = 2
initial_distance_between_springs = 2  # Nueva variable
initial_length_spiral = 40 * np.pi
initial_points_per_spiral = 400
initial_z_limit = 10
initial_a = 0.02  # Altura inicial del resorte

# Variable global para almacenar los puntos
last_points = {}
spring_colors = []  # Lista para almacenar los colores de los resortes

def update(*args):
    ax.clear()
    try:
        num_springs = int(num_resortes_var.get())
        r_inicial = float(r_inicial_var.get())
        distancia_entre_resortes = float(distancia_resortes_var.get())
        length_spiral = float(longitud_espiral_var.get())
        points_per_spiral = int(puntos_por_espiral_var.get())
        z_limit = float(limite_z_var.get())
        a = float(a_var.get())
    except ValueError:
        return  # Si hay un valor no válido, no actualiza

    total_coil = np.empty((0, 3))  # Inicializar array para la línea continua

    # Limpiar la lista de resortes y colores
    springs_list.delete(0, tk.END)
    spring_colors.clear()

    colors = plt.cm.viridis(np.linspace(0, 1, num_springs))

    for i in range(num_springs):
        if num_springs > 1:
            current_radius = r_inicial + i * distancia_entre_resortes
        else:
            current_radius = r_inicial  # Usa r_inicial si hay solo un resorte

        t = np.linspace(0, length_spiral, points_per_spiral)
        x = current_radius * np.cos(t)
        y = current_radius * np.sin(t)
        z = a * t % z_limit

        # Convertir a centímetros
        coil = np.column_stack((x * 10, y * 10, z * 10))

        if i > 0:
            # Conectar el final del coil anterior con el inicio del actual
            prev_end = total_coil[-1]
            current_start = coil[0]
            connection = np.linspace(prev_end, current_start, num=10)
            total_coil = np.vstack((total_coil, connection))

        total_coil = np.vstack((total_coil, coil))
        color = colors[i]
        ax.plot(coil[:, 0]/10, coil[:, 1]/10, coil[:, 2]/10, color=color)

        # Añadir el resorte a la lista con su color
        springs_list.insert(tk.END, f'Resorte {i+1}')
        # Convertir color RGBA a hexadecimal
        color_hex = '#%02x%02x%02x' % (int(color[0]*255), int(color[1]*255), int(color[2]*255))
        spring_colors.append(color_hex)
        # Aplicar color de fondo al elemento de la lista
        springs_list.itemconfig(i, {'bg': color_hex})

    ax.set_zlim(0, z_limit)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    canvas.draw()

    global last_points
    last_points = {'coils': total_coil}  # Guardar la línea continua

def save_mat():
    # Guardar la línea continua en el formato compatible con MATLAB
    savemat("espirales.mat", {'coils': last_points['coils']})

def on_limite_z_slider(val):
    limite_z_var.set(f"{float(val):.2f}")
    update()

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Generador de Resortes")

# Crear el marco principal para los controles y centrarlo verticalmente
controls_frame = tk.Frame(root)
controls_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)

# Usar un marco interior para centrar verticalmente
inner_frame = tk.Frame(controls_frame)
inner_frame.pack(expand=True)

# Variables de control
num_resortes_var = tk.StringVar(value=str(initial_num_springs))
r_inicial_var = tk.StringVar(value=str(initial_r_inicial))
distancia_resortes_var = tk.StringVar(value=str(initial_distance_between_springs))
longitud_espiral_var = tk.StringVar(value=str(initial_length_spiral))
puntos_por_espiral_var = tk.StringVar(value=str(initial_points_per_spiral))
limite_z_var = tk.StringVar(value=str(initial_z_limit))
a_var = tk.StringVar(value=str(initial_a))

# Etiquetas y campos de entrada
params = [
    ("Número de Resortes", num_resortes_var),
    ("Radio Inicial", r_inicial_var),
    ("Distancia entre Resortes", distancia_resortes_var),
    ("Longitud de la Espiral", longitud_espiral_var),
    ("Puntos por Espiral", puntos_por_espiral_var),
    ("Altura del Resorte", a_var),
]

for i, (label_text, var) in enumerate(params):
    label = tk.Label(inner_frame, text=label_text)
    label.grid(row=i, column=0, sticky='e', pady=2)
    entry = tk.Entry(inner_frame, textvariable=var)
    entry.grid(row=i, column=1, pady=2)
    var.trace_add('write', update)  # Actualizar cuando cambia el valor

# Slider para Límite de Z
limite_z_label = tk.Label(inner_frame, text="Límite de Z")
limite_z_label.grid(row=len(params), column=0, sticky='e', pady=10)
limite_z_slider = ttk.Scale(inner_frame, from_=1, to=50, orient='horizontal', command=on_limite_z_slider)
limite_z_slider.set(initial_z_limit)
limite_z_slider.grid(row=len(params), column=1, pady=10)
limite_z_var.trace_add('write', update)

# Campo de entrada para Límite de Z (sin etiqueta)
limite_z_entry = tk.Entry(inner_frame, textvariable=limite_z_var)
limite_z_entry.grid(row=len(params)+1, column=1)
limite_z_var.trace_add('write', lambda *args: limite_z_slider.set(float(limite_z_var.get()) if limite_z_var.get() else 1))

# Botón para guardar
save_button = tk.Button(inner_frame, text="Guardar .mat", command=save_mat)
save_button.grid(row=len(params)+2, column=0, columnspan=2, pady=10)

# Lista scrollable de resortes con colores
springs_list_label = tk.Label(inner_frame, text="Resortes")
springs_list_label.grid(row=0, column=2, padx=10, pady=2)

springs_list_frame = tk.Frame(inner_frame)
springs_list_frame.grid(row=1, column=2, rowspan=len(params)+3, padx=10, sticky='ns')

springs_list = tk.Listbox(springs_list_frame, height=10, width=20)
springs_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

springs_scrollbar = ttk.Scrollbar(springs_list_frame, orient="vertical", command=springs_list.yview)
springs_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
springs_list.configure(yscrollcommand=springs_scrollbar.set)

# Crear el marco para el gráfico
figure_frame = tk.Frame(root)
figure_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Crear la figura de Matplotlib
fig = Figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection='3d')

canvas = FigureCanvasTkAgg(fig, master=figure_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

update()  # Dibujar inicialmente

root.mainloop()
