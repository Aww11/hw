import turtle

def sierpinski_triangle(turtle, iterations, length):
    if iterations == 0:
        for _ in range(3):
            turtle.forward(length)
            turtle.right(120)
    else:
        iterations -= 1
        length /= 2
        sierpinski_triangle(turtle, iterations, length)
        turtle.forward(length)
        sierpinski_triangle(turtle, iterations, length)
        turtle.backward(length)
        turtle.left(60)
        turtle.forward(length)
        turtle.right(60)
        sierpinski_triangle(turtle, iterations, length)
        turtle.left(60)
        turtle.backward(length)
        turtle.right(60)

window = turtle.Screen()
window.bgcolor("white")

my_turtle = turtle.Turtle()
my_turtle.speed(0)

iterations = 4
length = 200

sierpinski_triangle(my_turtle, iterations, length)

window.mainloop()