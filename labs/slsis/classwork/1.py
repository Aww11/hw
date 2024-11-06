'''
u1+u2=0; u(t=0) = exp^(-3*(x-4)^2)
написать скрипт решения приближенной задачи коши до T=10
Q = 0,001
h = 0,01; 0,005
ut = (uj^(n+1)-uj^n)/Q
ux = (u(j+1)^n-uj^n)/h
ux = (uj^n-u(j-1)^n)/h
ux = (u(j+1)^n-u(j-1)^n)/2
(uj^(n+1)-uj^n)/Q+(u(j+1)^n-uj^n)/h

u[j] = u_old[j]-Q/h(u_old[j+1]-u_old[j])
u_old = u; t = t+Q
'''

import numpy as np
import matplotlib.pyplot as plt

T = 10
Q = 0.001
h = 0.01
x_min, x_max = 0, 10

N = int((x_max - x_min) / h)

x = np.linspace(x_min, x_max, N)
u_old = np.exp(-3 * (x - 4)**2)

u = np.zeros(N)

t = 0

def plot_solution(x, u, t):
    plt.clf()
    plt.plot(x, u, label=f't = {t:.3f}')
    plt.xlabel('x')
    plt.ylabel('u(x, t)')
    plt.title(f'Решение при t = {t:.3f}')
    plt.legend()
    plt.grid(True)
    plt.pause(0.001)

while t < T:
    for j in range(1, N-1):
        u[j] = u_old[j] - Q / h * (u_old[j+1] - u_old[j])
    
    u[0] = -u[1]
    u[N-1] = -u[N-2]
    
    t += Q
    
    u_old = np.copy(u)
    
    plot_solution(x, u, t)

plt.show()