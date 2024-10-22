import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import derivative

# Определение функций
def f1(x):
    return np.exp((x**2)/2)

def f2(x):
    return np.sin(3*x**4/5)**3

def f3(x):
    return np.cos((x + 1e-9) / (x + 1 + 1e-9))**2  # Добавляем небольшое смещение

def f4(x):
    return np.log(x + np.sqrt(4 + x**2))

def f5(x):
    return x * np.arctan(2*x) / (x**2 + 4)

# Определение аналитических производных
def df1(x):
    return x * np.exp((x**2)/2)

def df2(x):
    return 3 * np.sin(3*x**4/5)**2 * np.cos(3*x**4/5) * 12*x**3/5

def df3(x):
    return -2 * np.cos((x + 1e-9) / (x + 1 + 1e-9)) * np.sin((x + 1e-9) / (x + 1 + 1e-9)) / (x + 1 + 1e-9)**2

def df4(x):
    return 1 / (np.sqrt(4 + x**2))

def df5(x):
    return (2*x**2 / (x**2 + 4) + np.arctan(2*x)) / (x**2 + 4)

# Функция для построения графиков
def plot_derivatives(f, df, intervals, h_values, fig_num):
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle(f'Функция {fig_num}')
    
    for i, (interval, h) in enumerate(zip(intervals, h_values)):
        a, b = interval
        x = np.arange(a, b, h)
        y_num = np.array([derivative(f, xi, dx=h) for xi in x])
        y_anal = df(x)
        
        axs[i].plot(x, y_num, label=f'Численная производная (h={h})')
        axs[i].plot(x, y_anal, label='Аналитическая производная', linestyle='--')
        axs[i].set_title(f'Интервал [{a}, {b}]')
        axs[i].legend()
        axs[i].grid(True)
    
    plt.tight_layout()
    plt.show()

# Интервалы и шаги
intervals = [
    [0, 1],
    [2, 15]
]

h_values = [0.01, 0.005]

# Построение графиков для каждой функции
plot_derivatives(f1, df1, intervals, h_values, 1)
plot_derivatives(f2, df2, intervals, h_values, 2)
plot_derivatives(f3, df3, intervals, h_values, 3)
plot_derivatives(f4, df4, intervals, h_values, 4)
plot_derivatives(f5, df5, intervals, h_values, 5)