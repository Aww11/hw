import numpy as np
import matplotlib.pyplot as plt

# Определение функций
def f1(x):
    return np.exp(x/2)

def f2(x):
    return np.sin(3 * x)

def f3(x):
    return np.cos(5 * x)**2

def f4(x, n_terms=10):
    result = np.zeros_like(x)
    for n in range(n_terms):
        result += x**(2*n) / np.math.factorial(2*n)
    return result

# Отрезки
intervals = [(0, np.pi/2), (2, 10), (-3, 3)]

# Шаги сетки
steps = [0.01, 0.005, 0.001]

# Функция для генерации сеточной функции
def generate_grid_function(func, interval, step):
    a, b = interval
    x = np.arange(a, b + step, step)
    y = func(x)
    return x, y

# Построение графиков
def plot_functions(func, interval, steps, func_name):
    plt.figure(figsize=(10, 6))
    plt.title(f"График функции {func_name} на отрезке {interval}")
    plt.xlabel("x")
    plt.ylabel("y")
    
    # График исходной функции
    x_exact = np.linspace(interval[0], interval[1], 1000)
    y_exact = func(x_exact)
    plt.plot(x_exact, y_exact, label="Исходная функция", linewidth=2)
    
    # Графики сеточных функций
    for step in steps:
        x, y = generate_grid_function(func, interval, step)
        plt.plot(x, y, label=f"Сетка с шагом h = {step}", linestyle='--')
    
    plt.legend()
    plt.grid(True)
    plt.show()

# Построение графиков для каждой функции и каждого отрезка
functions = [(f1, "e^(x/2)"), (f2, "sin(3x)"), (f3, "cos^2(5x)"), (lambda x: f4(x, n_terms=10), "Степенной ряд")]

for func, func_name in functions:
    for interval in intervals:
        plot_functions(func, interval, steps, func_name)