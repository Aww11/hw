import turtle
import random

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

def draw_koch_snowflake(turtle, iterations, length, shortening_factor, angle, num_rays):
    for _ in range(num_rays):
        koch_curve(turtle, iterations, length, shortening_factor, angle)
        turtle.right(360 / num_rays)

def animate_koch_snowflake(turtle, iterations, length, shortening_factor, angle, num_rays, frames):
    for i in range(frames):
        turtle.clear()
        draw_koch_snowflake(turtle, iterations, length, shortening_factor, angle, num_rays)
        turtle.right(1)
        turtle.update()

def main():
    window = turtle.Screen()
    window.bgcolor("white")

    my_turtle = turtle.Turtle()
    my_turtle.speed(0)

    num_rays = random.randint(3, 12)  # Random number of rays
    color = random.choice(["blue", "red", "green", "yellow", "purple"])  # Random color
    my_turtle.color(color)

    iterations = 4
    length = 100
    shortening_factor = 3
    angle = 60

    animate_koch_snowflake(my_turtle, iterations, length, shortening_factor, angle, num_rays, 360)

    window.mainloop()

if __name__ == "__main__":
    main()