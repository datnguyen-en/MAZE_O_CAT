import turtle
import math
import random
import time
import winsound
# from story import *

# Create the UI for the game
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("The Maze")
wn.setup(700, 700)
wn.tracer(0)

# Register shapes
images = ['wall2.gif', 'cookie.gif', 'enemy.gif', 'char.gif', 'door.gif']
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

# Class Door
class Door(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("door.gif")
        self.color("green")
        self.penup()
        self.speed(0)
        self.goto(x,y)    

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()    

class Enemy(turtle.Turtle):
    def __init__(self, x, y, player, treasures):
        turtle.Turtle.__init__(self)
        self.shape("enemy.gif")
        self.color("red")
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.player = player
        self.treasures = treasures
        self.direction = random.choice(["up", "down", "left", "right"])

    def move(self):
        # Default movement direction (up, down, left, right)
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

        # If close to the player, chase the player
        def some():
            if self.is_close(self.player):
                if self.player.xcor() < self.xcor():
                    self.direction = "left"
                elif self.player.xcor() > self.xcor():
                    self.direction = "right"
                elif self.player.ycor() < self.ycor():
                    self.direction = "down"
                else:
                    self.direction = "up"
            # If there are treasures, move towards the nearest one
            elif self.treasures:  
                nearest_treasure = min(self.treasures, key=lambda treasure: self.distance(treasure))
                if nearest_treasure.xcor() < self.xcor():
                    self.direction = "left"
                elif nearest_treasure.xcor() > self.xcor():
                    self.direction = "right"
                elif nearest_treasure.ycor() < self.ycor():
                    self.direction = "down"
                else:
                    self.direction = "up"
        some()
        # Move to the next position in the chosen direction
        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        # Avoid walls (this assumes that walls are defined somewhere)
        if not self.is_collision_with_walls(move_to_x, move_to_y):
            self.goto(move_to_x, move_to_y)
        else:
            some()
            self.direction = random.choice(["up", "down", "left", "right"])
        
        # Continue moving after a short delay
        turtle.ontimer(self.move, t=150)

    def is_close(self, other):
        # Calculate distance between the enemy and the player
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt(a**2 + b**2)
        return distance < 1000 # Consider proximity within 24 pixels

    def is_collision_with_walls(self, x, y):
        # Check if the next position collides with a wall
        for wall in walls:  # Assumes `walls` is a global list of wall coordinates
            if (x, y) == wall:
                return True
        return False

# Create class instances
pen = Pen()
player = Player()


# generate maze
def generate_random_maze(rows, cols):
    # Initial maze with all walls
    maze = [['X' for i in range(cols)] for i in range(rows)]

    # Backtracking to create path
    def carve_walls(x, y):
        direction = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(direction)

        for dx, dy in direction:
            nx = x + dx
            ny = y + dy
            if 1 <= nx < rows and 1 <= ny < cols and maze[ny][nx] == 'X':
                maze[y + dy//2][x + dx//2] = ' '
                maze[ny][nx] = ' '
                carve_walls(nx, ny)

    # Start carving from a random point
    start_x = random.randrange(1, cols, 2)
    start_y = random.randrange(1, rows, 2)
    maze[start_y][start_x] = " " 
    carve_walls(start_x, start_y)

    # Add player at the start position
    maze[start_y][start_x] = "P"

    # Perform BFS to find the furthest point
    def bfs_furthest_point(start_x, start_y):

        # Initialize
        visited = set()
        furthest = (start_x, start_y, 0)  
        
        def dfs(x, y, dist):
            nonlocal furthest
            # Mark visited node
            visited.add((x,y))

            # Update the furthest point 
            if dist > furthest[2]:
                furthest = (x, y, dist)

            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nx = dx + x
                ny = dy + y
                if 1 <= nx < rows and 1 <= ny < cols and maze[ny][nx] == ' ' and (nx,ny) not in visited:
                    dfs(nx,ny, dist + 1)

        dfs(start_x, start_y, 0)

        return furthest 

    # Get furthest point and place the door
    fx, fy, _ = bfs_furthest_point(start_x, start_y)
    maze[fy][fx] = "D" 

    # Add random treasures
    for i in range(random.randint(1, 5)):
        tx, ty = random.randrange(1, cols, 2), random.randrange(1, rows, 2)
        if maze[ty][tx] == " ":
            maze[ty][tx] = "T"

    # Add random enemies
    for i in range(random.randint(1, 3)):
        ex, ey = random.randrange(1, cols, 2), random.randrange(1, rows, 2)
        if maze[ey][ex] == " ":
            maze[ey][ex] = "E"

    return maze

# Create levels list
levels = []


level_1 = generate_random_maze(25,25)

# Create wall barrier list
walls = []

# Add treasure list
treasures = []

# Add door list
doors = []

# Add enemies list
enemies = []

# Add maze to mazes list
levels.append(level_1)

# Set up maze and initialize player, enemies, treasures, etc.
def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]

            # calculate the screen x, y coordinates     
            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)

            # Check if it is a 'X' (representing the wall)
            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.stamp()
                # Add barriers to wall list
                walls.append((screen_x, screen_y))
            
            # Check if it is a 'P' (representing player)
            if character == 'P':
                player.goto(screen_x, screen_y)
            
            # Check if it is a 'T' (representing treasure)
            if character == 'T': 
                treasure = Treasure(screen_x, screen_y)
                treasures.append(treasure)

            # Check if it is a 'D' (representing Door)
            if character == 'D':
                doors.append(Door(screen_x, screen_y))

            # Check if it is a 'E' (representing enemies)
            if character == 'E':
                # Create enemies, passing player and treasures so they can move towards them
                enemy = Enemy(screen_x, screen_y, player, treasures)
                enemies.append(enemy)
                # Start moving the enemy
                enemy.move()


# wn.mainloop()


# Keyboard binding
turtle.listen()
turtle.onkey(player.go_left, "Left")
turtle.onkey(player.go_right, "Right")
turtle.onkey(player.go_up, "Up")
turtle.onkey(player.go_down, "Down")

# Call the setup maze funtion
setup_maze(levels[0])

# Turn off screen updates
# wn.tracer(0)

# Add a global timer variable
start_time = time.time()
time_limit = 120 # game durations in sec

timer_pen = Pen()  # Create a new Pen for the timer
timer_pen.penup()
timer_pen.hideturtle()
timer_pen.color("white")

def showtime():
    remain_time = max(0, time_limit - int(time.time() - start_time))
    timer_pen.goto(-300, 320)
    timer_pen.clear() # clear previous timer
    timer_pen.write(f"Time left: {remain_time}s", align="left", font=("Arial", 14, "bold"))
    return remain_time

# Add HUD elements
hud_pen = Pen()
hud_pen.penup()
hud_pen.hideturtle()
hud_pen.color("white")

def show_hud():
    hud_pen.goto(-300, 300)
    hud_pen.clear()
    hud_pen.write(f"Gold: {player.gold} | Cookies Left: {len(treasures)}", align="left", font=("Arial", 14, "bold"))

# After gameplay
def game_over():
    # Display Game Over message and stop the game.
    winsound.PlaySound("game_lose.wav", winsound.SND_ASYNC)
    pen.goto(0, 0)
    pen.color("red")
    pen.write("GAME OVER", align="center", font=("Arial", 36, "bold"))
    wn.update()
    time.sleep(3)
    turtle.bye()

def won():
    # Display 'Winner' message and stop the game.
    winsound.PlaySound("game_win.wav", winsound.SND_ASYNC)
    pen.goto(0, 0)
    pen.color("green")
    pen.write("YOU WON", align="center", font=("Arial", 36, "bold"))
    wn.update()
    time.sleep(2)
    turtle.bye()
    # easy_to_mid()


# # Main game
def main_game():
    winsound.PlaySound("game_on.wav", winsound.SND_ASYNC)
    try:
        while True:
            
            # Check for player collision with treasure

            # Display timer
            remain_time = showtime()
            if remain_time <= 0:
                game_over()

            # Display HUD
            show_hud()
        

            for treasure in treasures:
                if player.is_collision(treasure):
                    # adding music
                    # Add treasure gold to the player
                    player.gold += treasure.gold
                    winsound.PlaySound("get_gold.wav", winsound.SND_ASYNC)
                    time.sleep(0.03)
                    winsound.PlaySound("game_on.wav", winsound.SND_ASYNC)
                    print(f"Player gold: {player.gold}")
                    # Destroy the treasure
                    treasure.destroy()
                    # Remove the treasure from the treasure list
                    treasures.remove(treasure)
            
            for door in doors:  
                if player.is_collision(door) and not treasures:
                    doors.remove(door)

            # Check if all treasures are collected
            if not treasures and not doors:
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


main_game()
