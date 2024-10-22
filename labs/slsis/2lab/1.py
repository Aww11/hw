import numpy as np
import matplotlib.pyplot as plt

# Параметры системы
k = 1.0  # жесткость пружины
m = 1.0  # масса груза
h_coeff = 0.5  # коэффициент сопротивления
u0 = 1.0  # начальная скорость

# Временной интервал и шаг
t_span = (0, 20)
h = 0.025
t = np.arange(t_span[0], t_span[1] + h, h)

# Функция для метода Эйлера
def euler_method(f, y0, t_span, h):
    t = np.arange(t_span[0], t_span[1] + h, h)
    y = np.zeros((len(t), len(y0)))
    y[0] = y0
    for i in range(len(t) - 1):
        y[i + 1] = y[i] + h * np.array(f(t[i], y[i]))
    return t, y

# Система дифференциальных уравнений
def system(y, t, f):
    x, u = y
    dxdt = u
    dudt = (f(t) - h_coeff * u - k * x) / m
    return np.array([dxdt, dudt])

# Аналитическое решение для случая h^2 < 4*k*m
def analytical_solution_underdamped(t, f):
    w0 = np.sqrt(k / m)
    w = np.sqrt(w0**2 - (h_coeff / (2 * m))**2)
    A = u0 / w
    B = -u0 * h_coeff / (2 * m * w)
    x = A * np.exp(-h_coeff * t / (2 * m)) * np.sin(w * t) + B * np.exp(-h_coeff * t / (2 * m)) * np.cos(w * t)
    return x

# Аналитическое решение для случая h^2 > 4*k*m
def analytical_solution_overdamped(t, f):
    w0 = np.sqrt(k / m)
    w1 = np.sqrt((h_coeff / (2 * m))**2 - w0**2)
    A = u0 / w1
    B = -u0 * h_coeff / (2 * m * w1)
    x = A * np.exp(-h_coeff * t / (2 * m)) * np.sinh(w1 * t) + B * np.exp(-h_coeff * t / (2 * m)) * np.cosh(w1 * t)
    return x

# Случаи внешней силы
def f1(t):
    return 0

def f2(t):
    return t - 1

def f3(t):
    return np.exp(-t)

def f4(t):
    return 0.5 * np.sin(2 * t)

# Решение для каждого случая
cases = [(f1, "f = 0"), (f2, "f = t - 1"), (f3, "f = exp(-t)"), (f4, "f = 0.5 * sin(2t)")]

for i, (f, label) in enumerate(cases):
    plt.figure(figsize=(12, 6))

    # Численное решение
    t_num, y_num = euler_method(lambda t, y: system(y, t, f), [0, u0], t_span, h)
    plt.subplot(1, 2, 1)
    plt.plot(t_num, y_num[:, 0], label="Численное решение")
    plt.title(f"Численное решение: {label}")
    plt.xlabel("t")
    plt.ylabel("x(t)")
    plt.legend()
    plt.grid(True)

    # Аналитическое решение
    if h_coeff**2 < 4 * k * m:
        x_anal = analytical_solution_underdamped(t, f)
    else:
        x_anal = analytical_solution_overdamped(t, f)

    plt.subplot(1, 2, 2)
    plt.plot(t, x_anal, label="Аналитическое решение")
    plt.title(f"Аналитическое решение: {label}")
    plt.xlabel("t")
    plt.ylabel("x(t)")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()