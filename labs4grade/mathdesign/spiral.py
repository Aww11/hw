import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Параметры спиралей
a_archimedean = 0  # Начальное смещение для спирали Архимеда
b_archimedean = 0.2
a_bernoulli = 1  # Начальный радиус для спирали Бернулли
b_bernoulli = 0.2

# Углы для трех различных спиралей
angles = [0, np.pi/4, np.pi/2]

# Создание данных для спиралей
theta = np.linspace(0, 10 * np.pi, 1000)

# Создание фигуры и осей
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xlim(-8, 8)
ax.set_ylim(-8, 8)
ax.grid(True)

# Списки для хранения линий
lines_archimedean = []
lines_bernoulli = []

# Цвета для спиралей Архимеда (зеленые оттенки)
colors_archimedean = ['#006400', '#228B22', '#32CD32']

# Цвета для спиралей Бернулли (оранжевые оттенки)
colors_bernoulli = ['#FFA500', '#FF8C00', '#FF7F50']

# Создание линий для каждого угла для спирали Архимеда
for i, angle in enumerate(angles):
    r_archimedean = a_archimedean + b_archimedean * (theta + angle)
    x_archimedean = r_archimedean * np.cos(theta)
    y_archimedean = r_archimedean * np.sin(theta)
    line, = ax.plot([], [], lw=1, color=colors_archimedean[i])
    lines_archimedean.append(line)

# Создание линий для каждого угла для спирали Бернулли
for i, angle in enumerate(angles):
    r_bernoulli = a_bernoulli * np.exp(b_bernoulli * (theta + angle))
    x_bernoulli = r_bernoulli * np.cos(theta)
    y_bernoulli = r_bernoulli * np.sin(theta)
    line, = ax.plot([], [], lw=1, color=colors_bernoulli[i])
    lines_bernoulli.append(line)

# Функция инициализации анимации
def init():
    for line in lines_archimedean + lines_bernoulli:
        line.set_data([], [])
    return lines_archimedean + lines_bernoulli

# Функция анимации
def animate(i):
    for j, line in enumerate(lines_archimedean):
        angle = angles[j]
        r_archimedean = a_archimedean + b_archimedean * (theta[:i] + angle)
        x_archimedean = r_archimedean * np.cos(theta[:i])
        y_archimedean = r_archimedean * np.sin(theta[:i])
        line.set_data(x_archimedean, y_archimedean)

    for j, line in enumerate(lines_bernoulli):
        angle = angles[j]
        r_bernoulli = a_bernoulli * np.exp(b_bernoulli * (theta[:i] + angle))
        x_bernoulli = r_bernoulli * np.cos(theta[:i])
        y_bernoulli = r_bernoulli * np.sin(theta[:i])
        line.set_data(x_bernoulli, y_bernoulli)

    return lines_archimedean + lines_bernoulli

# Создание анимации
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(theta), interval=20, blit=True)

# Отображение анимации
plt.show()