import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from scipy.io import savemat

# Configuración inicial de los parámetros
initial_num_springs = 4
initial_r_inicial = 2
initial_r_final = 10
initial_length_spiral = 40 * np.pi
initial_points_per_spiral = 400
initial_z_limit = 10
initial_a = 0.02  # Altura inicial del resorte

# Configuración de la figura y los ejes
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
plt.subplots_adjust(left=0.25, bottom=0.35)

# Variable global para almacenar los puntos
last_points = {}

def update(val):
    ax.clear()
    num_springs = int(s_num_resortes.val)
    r_inicial = s_r_inicial.val
    r_final = s_r_final.val
    length_spiral = s_longitud_espiral.val
    points_per_spiral = int(s_puntos_por_espiral.val)
    z_limit = s_limite_z.val
    a = s_a.val

    total_coil = np.empty((0, 3))  # Inicializar array para la línea continua

    for i in range(num_springs):
        if num_springs > 1:
            current_radius = r_inicial + i * (r_final - r_inicial) / (num_springs - 1)
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
        ax.plot(coil[:, 0]/10, coil[:, 1]/10, coil[:, 2]/10, label=f'Spiral {i+1}')

    ax.legend()
    ax.set_zlim(0, z_limit)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    fig.canvas.draw_idle()

    global last_points
    last_points = {'coils': total_coil}  # Guardar la línea continua

def save_mat(event):
    # Guardar la línea continua en el formato compatible con MATLAB
    savemat("espirales.mat", {'coils': last_points['coils']})

# Creación de sliders y botón
axcolor = 'lightgoldenrodyellow'
ax_num_resortes = plt.axes([0.25, 0.25, 0.65, 0.03], facecolor=axcolor)
ax_r_inicial = plt.axes([0.25, 0.20, 0.65, 0.03], facecolor=axcolor)
ax_r_final = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_longitud_espiral = plt.axes([0.25, 0.10, 0.65, 0.03], facecolor=axcolor)
ax_puntos_por_espiral = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
ax_limite_z = plt.axes([0.25, 0.00, 0.65, 0.03], facecolor=axcolor)
ax_a = plt.axes([0.25, 0.30, 0.65, 0.03], facecolor=axcolor)

s_num_resortes = Slider(ax_num_resortes, 'Número de Resortes', 1, 10, valinit=initial_num_springs, valfmt='%0.0f')
s_r_inicial = Slider(ax_r_inicial, 'Radio Inicial', 0.1, 10, valinit=initial_r_inicial)
s_r_final = Slider(ax_r_final, 'Radio Final', 0.1, 10, valinit=initial_r_final)
s_longitud_espiral = Slider(ax_longitud_espiral, 'Longitud de la Espiral', 2*np.pi, 100*np.pi, valinit=initial_length_spiral)
s_puntos_por_espiral = Slider(ax_puntos_por_espiral, 'Puntos por Espiral', 100, 1000, valinit=initial_points_per_spiral)
s_limite_z = Slider(ax_limite_z, 'Límite de Z', 1, 50, valinit=initial_z_limit)
s_a = Slider(ax_a, 'Altura del Resorte', 0.01, 0.1, valinit=initial_a)

s_num_resortes.on_changed(update)
s_r_inicial.on_changed(update)
s_r_final.on_changed(update)
s_longitud_espiral.on_changed(update)
s_puntos_por_espiral.on_changed(update)
s_limite_z.on_changed(update)
s_a.on_changed(update)

# Botón para guardar los datos
ax_button = plt.axes([0.05, 0.025, 0.1, 0.04])
button = Button(ax_button, 'Guardar .mat', color=axcolor, hovercolor='0.975')
button.on_clicked(save_mat)

update(None)
plt.show()
