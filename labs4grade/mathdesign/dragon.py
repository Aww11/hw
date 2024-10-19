import turtle

def dragon_curve(turtle, iterations, length, angle):
    if iterations == 0:
        turtle.forward(length)
    else:
        iterations -= 1
        dragon_curve(turtle, iterations, length, -angle)
        turtle.right(angle)
        dragon_curve(turtle, iterations, length, angle)
        turtle.left(angle)

window = turtle.Screen()
window.bgcolor("white")

my_turtle = turtle.Turtle()
my_turtle.speed(0)

iterations = 10
length = 5
angle = 45

dragon_curve(my_turtle, iterations, length, angle)

window.mainloop()