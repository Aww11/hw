import numpy as np
import matplotlib.pyplot as plt

def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n += 1
    return n

def create_mandelbrot(width, height, x_min, x_max, y_min, y_max, max_iter):
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    img = np.zeros((height, width))
    
    for i in range(width):
        for j in range(height):
            img[j, i] = mandelbrot(x[i] + 1j*y[j], max_iter)
    
    return img

# Параметры для множества Мандельброта
width, height = 800, 800
x_min, x_max = -2.0, 1.0
y_min, y_max = -1.5, 1.5
max_iter = 100

# Создаем множество Мандельброта
mandelbrot_img = create_mandelbrot(width, height, x_min, x_max, y_min, y_max, max_iter)

# Отображаем результат
plt.imshow(mandelbrot_img, extent=(x_min, x_max, y_min, y_max), cmap='hot')
plt.colorbar()
plt.title('Mandelbrot Set')
plt.xlabel('Re')
plt.ylabel('Im')
plt.show()