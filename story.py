import turtle
import winsound
import time

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.setup(width=700, height=700)

# adding the cat image
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

# Function to display the title welcome screen: 
def show_title_screen():
    winsound.PlaySound('game_open.wav', winsound.SND_ASYNC)
    
    t.penup()
    t.goto(0,250)
    t.color("white")
    t.write("Maze-O-Cat", align = "center", font = ("Arial", 30, "bold"))
    t.penup()
    t.goto(0, 175)
    t.color("white")
    t.write("Welcome to the Game!", align="center", font=("Arial", 20, "bold"))
    t.penup()
    t.goto(0, 100)
    t.write("Come help Kitty, to reach her cookies...", align="center", font=("Arial", 16,"bold"))
    t.penup()
    t.goto(0, 50)
    t.write("without getting caught!!", align="center", font=("Arial", 16,"bold"))
    t.penup()
    t.goto(0, 0)
    t.write("Can you help Kitty?", align="center", font=("Arial", 16))
    
    draw_button("Play game", -200, -150)

    kitty.penup()
    kitty.goto(100,-200)
    kitty.shape('cat2.gif')
    kitty.clear()
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
    t.goto(x+50, y-30)
    t.write(label, align="center", font=("Arial", 16, "normal"))

# Function to show the level selection screen
def show_levels_screen(x, y):
    winsound.PlaySound('game_levels.wav', winsound.SND_ASYNC)
    kitty.hideturtle()
    t.clear()
    t.penup()
    # adding grass
    grass.penup()
    grass.goto(0,-100)
    grass.shape('grass.gif')
    grass.penup()

    # adding cat
    cat.penup()
    cat.goto(200,-200)
    cat.shape('cat.gif')
    cat.penup()

    # adding cookie
    cookie.penup()
    cookie.goto(100,-100)
    cookie.shape('cookie.gif')
    cookie.penup()

    # adding effect 
    t.goto(0, 200)
    t.color("lightblue")
    t.write("Choose the level:", align="center", font=("Arial", 30, "bold"))
    
    draw_button("Easy", -200, 100)
    draw_button("Medium", -200, 30)
    draw_button("Hard", -200, -40)
    
    # Wait for a click to start the game based on level selection
    screen.onscreenclick(start_game)
    

# Function to start the game based on level
def start_game(x, y):
    grass.hideturtle()
    cat.hideturtle()
    cookie.hideturtle()
    winsound.PlaySound('button_press.wav', winsound.SND_ASYNC)
    time.sleep(0.5)
    winsound.PlaySound('loading.wav', winsound.SND_ASYNC)
    if 80 <= y <= 120:  # Easy level
        start_maze_game("easy")
    elif 10 <= y <= 50:  # Medium level
        start_maze_game("medium")
    elif -60 <= y <= -20:  # Hard level
        start_maze_game("hard") 
    else:
        pass


# Function to start the maze game based on the level
def start_maze_game(level):
    t.clear()
    screen.bgcolor("green")
    t.penup()
    t.goto(0, 0)
    t.color("white")
    t.write(f"Starting {level.capitalize()} level...", align="center", font=("Arial", 24, "bold"))
    time.sleep(1)
    screen.update()
    time.sleep(2)
    t.clear()
    screen.bgcolor("black") 
    screen.bye()
         
def easy_to_mid():
    t.clear()
    screen.bgcolor("brown")
    t.penup()
    t.goto(0, 100)
    t.color("white")
    t.write("Congratulations! You have won!", align="center", font=("Arial", 24, "bold"))
    t.penup()
    t.hideturtle()
    draw_button("Quit", -200, 30)
    draw_button("Continue", 100, 30)
    screen.onscreenclick(start_game_etm)
    screen.update()

def start_game_etm(x,y):
    if 10 <= y <= 50 and -220 <= x <= -160 :  # Quit game
        turtle.bye()
    elif 10 <= y <= 5 and 80 <= x <= 120:  # Go to Medium level
        start_maze_game("medium")
    else:
        pass

def mid_to_hd():
    t.clear()
    screen.bgcolor("Blue")
    t.penup()
    t.goto(0, 100)
    t.color("white")
    t.write("Congratulations! You have won!", align="center", font=("Arial", 24, "bold"))
    t.penup()
    t.hideturtle()
  

# easy_to_mid()
# mid_to_hd()

# show_title_screen()
# screen.mainloop()

