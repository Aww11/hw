import numpy as np
import matplotlib.pyplot as plt

def julia_set(c, width, height, zoom=1, max_iter=256):
    # Создаем массив для хранения значений итераций
    img = np.zeros((width, height))
    
    # Центр изображения
    x_center = 0
    y_center = 0
    
    # Диапазон значений x и y
    x_range = 1.5 / zoom
    y_range = 1.5 / zoom
    
    # Шаг сетки
    x_step = 2 * x_range / width
    y_step = 2 * y_range / height
    
    # Заполняем массив значениями итераций
    for x in range(width):
        for y in range(height):
            zx = x * x_step - x_range + x_center
            zy = y * y_step - y_range + y_center
            z = complex(zx, zy)
            i = max_iter
            while abs(z) < 2 and i > 0:
                z = z * z + c
                i -= 1
            img[y, x] = i
    
    return img

# Параметры множества Жюлиа
c = complex(-0.7, 0.27015)  # Константа c
width, height = 800, 800  # Размер изображения
zoom = 1  # Уровень масштабирования
max_iter = 256  # Максимальное количество итераций

# Генерируем множество Жюлиа
julia = julia_set(c, width, height, zoom, max_iter)

# Визуализация
plt.figure(figsize=(8, 8))
plt.imshow(julia, cmap='hot', extent=(-1.5, 1.5, -1.5, 1.5))
plt.title(f"Julia Set for c = {c}")
plt.xlabel("Re(z)")
plt.ylabel("Im(z)")
plt.show()