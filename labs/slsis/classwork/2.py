import numpy as np
import matplotlib.pyplot as plt

# Параметры задачи
T = 10
Q = 0.01
h_values = [0.01, 0.005]
x_min, x_max = 0, 20

def solve_cauchy_problem(u_old, Q, h):
    N = len(u_old)
    u = np.zeros(N)
    
    for j in range(1, N-1):
        u[j] = u_old[j] - Q / h * (u_old[j] - u_old[j-1])
    
    u[0] = -u[1]
    u[N-1] = -u[N-2]
    
    return u

def plot_solution(x, u, t):
    plt.clf()
    plt.plot(x, u, label=f't = {t:.3f}')
    plt.xlabel('x')
    plt.ylabel('u(x, t)')
    plt.title(f'Решение при t = {t:.3f}, Method: backward')
    plt.legend()
    plt.grid(True)
    plt.pause(0.001)

for h in h_values:
    N = int((x_max - x_min) / h)
    x = np.linspace(x_min, x_max, N)
    u_old = np.exp(-3 * (x - 4)**2)
    
    print(f"Solving with h = {h}, method = backward...")
    t = 0
    while t < T:
        u = solve_cauchy_problem(u_old, Q, h)
        t += Q
        u_old = np.copy(u)
        plot_solution(x, u, t)

plt.show()