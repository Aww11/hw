import turtle

def koch_curve(turtle, iterations, length, shortening_factor, angle):
    if iterations == 0:
        turtle.forward(length)
    else:
        iterations -= 1
        length /= shortening_factor
        koch_curve(turtle, iterations, length, shortening_factor, angle)
        turtle.left(angle)
        koch_curve(turtle, iterations, length, shortening_factor, angle)
        turtle.right(angle * 2)
        koch_curve(turtle, iterations, length, shortening_factor, angle)
        turtle.left(angle)
        koch_curve(turtle, iterations, length, shortening_factor, angle)

window = turtle.Screen()
window.bgcolor("white")

my_turtle = turtle.Turtle()
my_turtle.speed(0)

iterations = 4
length = 400
shortening_factor = 3
angle = 60

koch_curve(my_turtle, iterations, length, shortening_factor, angle)

window.mainloop()