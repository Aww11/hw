import turtle

def tree_fractal(turtle, iterations, length, angle):
    if iterations == 0:
        turtle.forward(length)
    else:
        iterations -= 1
        length *= 0.7
        turtle.forward(length)
        turtle.right(angle)
        tree_fractal(turtle, iterations, length, angle)
        turtle.left(angle * 2)
        tree_fractal(turtle, iterations, length, angle)
        turtle.right(angle)
        turtle.backward(length)

window = turtle.Screen()
window.bgcolor("white")

my_turtle = turtle.Turtle()
my_turtle.speed(0)

iterations = 10
length = 100
angle = 30

tree_fractal(my_turtle, iterations, length, angle)

window.mainloop()