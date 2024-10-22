import numpy as np
import matplotlib.pyplot as plt

# Функция для метода Эйлера
def euler_method(f, y0, t_span, h):
    t = np.arange(t_span[0], t_span[1] + h, h)
    y = np.zeros((len(t), len(y0)))
    y[0] = y0
    for i in range(len(t) - 1):
        y[i + 1] = y[i] + h * f(t[i], y[i])
    return t, y

# Задача а) y' = 1/2 * y, y(0) = 1
def f_a(t, y):
    return 0.5 * y

t_a, y_a = euler_method(f_a, [1], [0, 10], 0.025)

plt.figure(figsize=(8, 4))
plt.plot(t_a, y_a, label="y(t)")
plt.title("Задача а) y' = 1/2 * y, y(0) = 1")
plt.xlabel("t")
plt.ylabel("y(t)")
plt.legend()
plt.grid(True)
plt.show()

# Задача b) y' = 2*x + 3*y, y(0) = -2
def f_b(t, y):
    return 2 * t + 3 * y

t_b, y_b = euler_method(f_b, [-2], [0, 10], 0.025)

plt.figure(figsize=(8, 4))
plt.plot(t_b, y_b, label="y(t)")
plt.title("Задача b) y' = 2*x + 3*y, y(0) = -2")
plt.xlabel("t")
plt.ylabel("y(t)")
plt.legend()
plt.grid(True)
plt.show()

# Задача c) система x1' = x2, x2' = -x1, x1(0) = 1, x2(0) = 0
def f_c(t, x):
    return np.array([x[1], -x[0]])

t_c, x_c = euler_method(f_c, [1, 0], [0, 10], 0.025)

plt.figure(figsize=(8, 4))
plt.plot(t_c, x_c[:, 0], label="x1(t)")
plt.plot(t_c, x_c[:, 1], label="x2(t)")
plt.title("Задача c) x1' = x2, x2' = -x1, x1(0) = 1, x2(0) = 0")
plt.xlabel("t")
plt.ylabel("x(t)")
plt.legend()
plt.grid(True)
plt.show()

# Задача d) система x1' = x2, x2' = 4*x1, x1(0) = 1, x2(0) = 1
def f_d(t, x):
    return np.array([x[1], 4 * x[0]])

t_d, x_d = euler_method(f_d, [1, 1], [0, 10], 0.025)

plt.figure(figsize=(8, 4))
plt.plot(t_d, x_d[:, 0], label="x1(t)")
plt.plot(t_d, x_d[:, 1], label="x2(t)")
plt.title("Задача d) x1' = x2, x2' = 4*x1, x1(0) = 1, x2(0) = 1")
plt.xlabel("t")
plt.ylabel("x(t)")
plt.legend()
plt.grid(True)
plt.show()