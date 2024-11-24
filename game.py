import turtle
import math
import random
import time

# Create the UI for the game
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("A maze game")
wn.setup(700, 700)
wn.tracer(0)

# Register shapes
images = ['wall2.gif', 'cookie.gif', 'enemy.gif', 'char.gif']
for image in images:
    wn.addshape(image)
# Create Pen
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)    
        self.shape("wall2.gif")
        self.color("white")
        self.penup()
        self.speed(0)

# Create player class
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("char.gif")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.gold = 0
    
    # Method to move player if not a wall
    def go_not_walls(self, x, y):
        if (x, y) not in walls:
            self.goto(x, y)

    # Create movement for player
    def go_up(self):
        new_y = self.ycor() + 24
        self.go_not_walls(self.xcor(), new_y)
    
    def go_down(self):
        new_y = self.ycor() - 24
        self.go_not_walls(self.xcor(), new_y)
    def go_left(self):
        new_x = self.xcor() - 24
        self.go_not_walls(new_x, self.ycor())
    
    def go_right(self):
        new_x = self.xcor() + 24
        self.go_not_walls(new_x, self.ycor())

    def is_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))
        if distance < 5:
            return True
        else: 
            return False

# Create Treasure
class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("cookie.gif")
        self.color("gold")
        self.penup()
        self.speed(0)  
        self.gold = 100 
        self.goto(x, y)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()
        
# Create Enemy
class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("enemy.gif")
        self.color("red")
        self.penup()
        self.speed(0)
        self.goto(x,y)
        self.direction = random.choice(["up", "down", "left", "right"])

    # How enemy move
    def move(self):
        if self.direction == "up":
            dx = 0
            dy = 24
        elif self.direction == "down":
            dx = 0
            dy = -24
        elif self.direction == "left":
            dx = -24
            dy = 0
        elif self.direction == "right":
            dx = 24
            dy = 0
        else:
            dx = 0
            dy = 0

        # Calculate the spot to move to
        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        # Check if the player is close 
        # If so, go in that direction
        if self.is_close(player):
            if player.xcor() < self.xcor():
                self.direction = "left"
            elif player.xcor() > self.xcor():
                self.direction = "right"
            elif player.ycor() < self.ycor():
                self.direction = "down"
            else:
                self.direction = "up"
                
        # Check if the space has a wall
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

        else:
            # choose a different direction if seeing the wall
            self.direction = random.choice(["up", "down", "left", "right"])
        
        # Set timer to move again
        turtle.ontimer(self.move, t = random.randint(100, 300))
    
    def is_close(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a**2) + (b**2))

        if distance < 75:
            return True
        else:
            return False
# Create class instances
pen = Pen()
player = Player()


# Create wall barrier list
walls = []

# Create levels list
levels = []

# Define first level
level_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XP    X         X       X",
    "X     X  XXXXX  X  XXX  X",
    "X  XXXXX  X      X    X X",
    "X  X      XXXXXX XXXX X X",
    "X  X  XXXXXE    EX    X X",
    "X  X  X          XXXXXX X",
    "X  XXXX  XXXXXX        XX",
    "X     X  X      XXXXXX  X",
    "XXXXX   XXXXXXX         X",
    "X       X     XXXXXXX   X",
    "X   XXXXXXXXXXX      X  X",
    "X      X              X X",
    "XXXXX X  XXXXXXX  XXXXX X",
    "X   X X      X          X",
    "X X X XXXXX TXXXXXXXXXXXX",
    "X X X      X X          X",
    "X XXXXXXXXXX XXXXXXXXX  X",
    "X          X      X     X",
    "XXXXXXXXXX XXXXXX XXXXXXX",
    "X           X           X",
    "X XXXXXXXX  XXXXXXXXXX  X",
    "X        X             XX",
    "XXXXXXXXTXXXXXXXXXXXXXX X",
    "XXXXXXXXXXXXXXXXXXXXXXXXX"

]

# Add treasure list
treasures = []

# Add enemies list
enemies = []
# Add maze to mazes list
levels.append(level_1)

# Set up the maze
def setup_maze(level):
    for y in range(len(level)):
        for x in range (len(level[y])):
            character = level[y][x]

            # calculate the screen x, y coordinates     
            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)

            # Check if it is a 'X' (representing the wall)
            if character == "X":
                pen.goto(screen_x,screen_y)
                pen.stamp()
                # Add barriers to wall list
                walls.append((screen_x,screen_y))
            
            # Check if it is a 'P' (representing player)
            if character == 'P':
                player.goto(screen_x, screen_y)
            
            # Check if it is a 'T' (representing treasure)
            if character == 'T': 
                treasures.append(Treasure(screen_x,screen_y))

            # Check if it is a 'E' (representing enemies)
            if character == 'E':
                enemy = Enemy(screen_x, screen_y)
                enemies.append(enemy)
                # Start moving the enemy
                enemy.move()


# Keyboard binding
turtle.listen()
turtle.onkey(player.go_left, "Left")
turtle.onkey(player.go_right, "Right")
turtle.onkey(player.go_up, "Up")
turtle.onkey(player.go_down, "Down")

# Call the setup maze funtion
setup_maze(levels[0])

# Turn off screen updates
wn.tracer(0)

def game_over():
    # Display Game Over message and stop the game.
    pen.goto(0, 0)
    pen.color("red")
    pen.write("GAME OVER", align="center", font=("Arial", 36, "bold"))
    wn.update()
    time.sleep(2)
    turtle.bye()
def won():
    # Display 'Winner' message and stop the game.
    pen.goto(0, 0)
    pen.color("green")
    pen.write("YOU WON", align="center", font=("Arial", 36, "bold"))
    wn.update()
    time.sleep(2)
    turtle.bye()

# Main game
try:
    while True:
        # Check for player collision with treasure
        for treasure in treasures:
            if player.is_collision(treasure):
                # Add treasure gold to the player
                player.gold += treasure.gold
                print(f"Player gold: {player.gold}")
                # Destroy the treasure
                treasure.destroy()
                # Remove the treasure from the treasure list
                treasures.remove(treasure)
        
        # Check if all treasures are collected
        if not treasures:
            won()

        # Iterate through enemy list to see if the player collide
        for enemy in enemies:
            if player.is_collision(enemy):
                print("You're dead!")
                game_over()

        # Update screen and add delay
        wn.update()
        # time.sleep(0.05)

except turtle.Terminator:
    print("Game exited!")