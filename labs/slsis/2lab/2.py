import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve

# Параметры задачи
a = 0.5  # Левая граница
b = 1.0  # Правая граница
N = 100  # Количество узлов сетки
h = (b - a) / N  # Шаг сетки

# Сетка
x = np.linspace(a, b, N+1)

# Инициализация матрицы и вектора правой части
A = np.zeros((N+1, N+1))
B = np.zeros(N+1)

# Заполнение матрицы и вектора правой части
for i in range(1, N):
    A[i, i-1] = 1 - x[i]**2 * h / 2
    A[i, i] = -2 + 2 / x[i]**2 * h**2
    A[i, i+1] = 1 + x[i]**2 * h / 2
    B[i] = 1 + 4 / x[i]**2 * h**2

# Граничные условия
A[0, 0] = 2
A[0, 1] = -1
B[0] = 6

A[N, N-1] = -3
A[N, N] = 1
B[N] = -1

# Решение системы линейных уравнений
y = solve(A, B)

# График решения
plt.figure(figsize=(8, 6))
plt.plot(x, y, label="Решение y(x)")
plt.title("График решения краевой задачи")
plt.xlabel("x")
plt.ylabel("y(x)")
plt.legend()
plt.grid(True)
plt.show()

# Вывод значений табличной функции в терминале
print("x\t\ty(x)")
for i in range(N+1):
    print(f"{x[i]:.4f}\t{y[i]:.4f}")