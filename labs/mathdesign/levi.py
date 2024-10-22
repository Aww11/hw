import turtle

def levy_curve(t, order, size):
    if order == 0:
        t.forward(size)
    else:
        t.left(45)
        levy_curve(t, order-1, size/2**0.5)
        t.right(90)
        levy_curve(t, order-1, size/2**0.5)
        t.left(45)

def main():
    # Настройки экрана
    screen = turtle.Screen()
    screen.setup(800, 800)
    screen.title("Levy C Curve")
    
    # Настройки черепашки
    t = turtle.Turtle()
    t.speed(0)  # Максимальная скорость
    t.penup()
    t.goto(-200, 0)  # Начальная позиция
    t.pendown()
    
    # Рисуем кривую Леви
    order = 10  # Порядок фрактала
    size = 400  # Размер линии
    levy_curve(t, order, size)
    
    # Завершение работы
    turtle.done()

if __name__ == "__main__":
    main()