import turtle
import winsound
import time
import importlib

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.setup(width=700, height=700)

# Add shapes
screen.addshape('cat2.gif')
screen.addshape('grass.gif')
screen.addshape('cat.gif')
screen.addshape('cookie.gif')

kitty = turtle.Turtle()
grass = turtle.Turtle()
cat = turtle.Turtle()
cookie = turtle.Turtle()

# Create a turtle object for drawing
t = turtle.Turtle()
t.hideturtle()

# Function to display the title welcome screen
def show_title_screen():
    winsound.PlaySound('game_open.wav', winsound.SND_ASYNC)

    t.penup()
    t.goto(0, 250)
    t.color("white")
    t.write("Maze-O-Cat", align="center", font=("Arial", 30, "bold"))
    t.goto(0, 175)
    t.write("Welcome to the Game!", align="center", font=("Arial", 20, "bold"))
    t.goto(0, 100)
    t.write("Come help Kitty, to reach her cookies...", align="center", font=("Arial", 16, "bold"))
    t.goto(0, 50)
    t.write("without getting caught!!", align="center", font=("Arial", 16, "bold"))
    t.goto(0, 0)
    t.write("Can you help Kitty?", align="center", font=("Arial", 16))

    draw_button("Play game", -200, -150)

    kitty.penup()
    kitty.goto(100, -200)
    kitty.shape('cat2.gif')
    screen.update()

    # Wait for a click on the button to move to level selection
    screen.onscreenclick(show_levels_screen)

# Function to draw any button
def draw_button(label, x, y):
    t.goto(x, y)
    t.pendown()
    t.begin_fill()
    t.color("white")
    for _ in range(2):
        t.forward(100)
        t.right(90)
        t.forward(40)
        t.right(90)
    t.end_fill()
    t.penup()
    t.color("black")
    t.goto(x + 50, y - 30)
    t.write(label, align="center", font=("Arial", 16, "normal"))

# Function to clear the screen
def clear_screen():
    t.clear()
    for obj in [kitty, grass, cat, cookie]:
        obj.hideturtle()

# Function to show the level selection screen
def show_levels_screen(x, y):
    winsound.PlaySound('game_levels.wav', winsound.SND_ASYNC)
    clear_screen()

    # Adding grass
    grass.penup()
    grass.goto(0, -100)
    grass.shape('grass.gif')
    grass.showturtle()

    # Adding cat
    cat.penup()
    cat.goto(200, -200)
    cat.shape('cat.gif')
    cat.showturtle()

    # Adding cookie
    cookie.penup()
    cookie.goto(100, -100)
    cookie.shape('cookie.gif')
    cookie.showturtle()

    # Adding effect
    t.goto(0, 200)
    t.color("lightblue")
    t.write("Choose the level:", align="center", font=("Arial", 30, "bold"))

    draw_button("Easy", -200, 100)
    draw_button("Medium", -200, 30)
    draw_button("Cooper", -200, -40)

    # Wait for a click to start the game based on level selection
    screen.onscreenclick(start_game)

# Function to start the game based on level
def start_game(x, y):
    clear_screen()
    winsound.PlaySound('button_press.wav', winsound.SND_ASYNC)
    time.sleep(0.5)
    winsound.PlaySound('loading.wav', winsound.SND_ASYNC)
    if -200 <= x <= -100 and 80 <= y <= 120:  # Easy level
        run_level("game_easy")
    elif -200 <= x <= -100 and 10 <= y <= 50:  # Medium level
        run_level("game_med")
    elif -200 <= x <= -100 and -60 <= y <= -20:  # Hard level
        run_level("game_hard")
    else:
        pass


# Function to dynamically load and start the maze game based on the level
def run_level(level_name):
    try:
        level_module = importlib.import_module(level_name)
        if hasattr(level_module, "main"):
            level_module.main()
        else:
            print(f"Error: {level_name} does not have a `main` function.")
    except ModuleNotFoundError:
        print(f"Error: {level_name}.py file not found.")
    except Exception as e:
        print(f"Error running {level_name}: {e}")

# Show the title screen
show_title_screen()
screen.mainloop()
