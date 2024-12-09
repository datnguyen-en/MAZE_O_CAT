import turtle
import math
import random
import time
import pygame
import winsound

# Add music for the game
pygame.mixer.init()
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Load sound effect
pickaxe_hit_sound = pygame.mixer.Sound("pickup_sound.mp3")
pickaxe_hit_sound.set_volume(0.5)   

# Create the UI for the game
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("The Maze")
wn.setup(700, 700)
wn.tracer(0)

# Register shapes
images = ['wall2.gif', 'cookie.gif', 'enemy.gif', 'char.gif', 'door.gif', 'pickaxe.gif', 'teleport.gif']
for image in images:
    wn.addshape(image)


def convert_to_list_of_lists(level):
    return [list(row) for row in level]

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
        self.pickaxe = 0
        self.has_pickaxe = False
       
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
        
    def mine_wall(self, x, y):
        if self.has_pickaxe and self.pickaxe > 0:
            # Convert screen coordinates to maze grid coordinates
            grid_x = (x + 288) // 24
            grid_y = (288 - y) // 24

            # Ensure the wall is not part of the outer border
            if grid_x == 0 or grid_y == 0 or grid_x == len(level_hard[0]) - 1 or grid_y == len(level_hard) - 1:
                display_message("Cannot mine the border!", 2000)
                return
            
            if (x, y) in walls:
                self.pickaxe -= 1
                walls.remove((x, y))
                stamp_id = wall_stamps.pop((x, y), None)
                if stamp_id is not None:
                    pen.clearstamp(stamp_id)

                if self.pickaxe == 0:
                    self.has_pickaxe = False
                    display_message("No pickaxes left!", 2000)
                    
    def teleport(self, rows, cols, maze):
        while True:
            tx, ty = random.randrange(1, rows, 2), random.randrange(1, cols, 2)
            
            # Check if the location in the maze is open space
            if maze[ty][tx] == ' ':
                # Update the player's position in the maze
                for y in range(len(maze)):
                    for x in range(len(maze[y])):
                        if maze[y][x] == 'P':  # Clear the current position
                            maze[y][x] = ' '
                
                maze[ty][tx] = 'P'  # Set new player position
                self.goto(-288 + (tx * 24), 288 - (ty * 24))
                print(f"Teleported to: ({tx}, {ty})")
                break



# Create Teleportation
class Teleportation(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("teleport.gif")
        self.penup()
        self.speed(0)
        self.goto(x, y)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

# Create Pickaxe
class Pickaxe(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape('pickaxe.gif')
        self.color("green")
        self.penup()
        self.speed(0)
        self.have = 2
        self.goto(x, y)
    
    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

          


# Add the heuristic and A* pathfinding functions
def heuristic(a, b):
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_pathfinding(start, goal, walls):
    # Nodes to explore
    open_list = []  
    # Explored nodes
    closed_list = set()
    # For reconstructing the path
    came_from = {} 

    # Cost from start to current node
    g_score = {start: 0} 
    # Estimated total cost
    f_score = {start: heuristic(start, goal)}

    open_list.append((f_score[start], start))  # Add the starting node

    while open_list:
        # Sort by f_score (lowest first)
        open_list.sort() 
        # Get the node with the lowest f_score
        _, current = open_list.pop(0)  

        # If we've reached the goal, reconstruct the path
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            # Return the path from start to goal
            return path 

        closed_list.add(current)

        # Explore neighbors
        for dx, dy in [(-24, 0), (24, 0), (0, -24), (0, 24)]:
            neighbor = (current[0] + dx, current[1] + dy)

            # Skip if neighbor is a wall or already explored
            if neighbor in walls or neighbor in closed_list:
                continue

            # Tentative g_score for this neighbor
            tentative_g_score = g_score[current] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:

                # This path to neighbor is better
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)

                # Add to open list if not already there
                if neighbor not in [n[1] for n in open_list]:
                    open_list.append((f_score[neighbor], neighbor))

    # Return empty path if no path exists
    return [] 


# Update the Enemy class
class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("enemy.gif")
        self.color("red")
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.path = []  # Store the path to the player

    def move(self):
        # Get the current position and player's position
        current_pos = (self.xcor(), self.ycor())
        player_pos = (player.xcor(), player.ycor())

        # If the path is empty or player has moved, recalculate path
        if not self.path or self.path[-1] != player_pos:
            self.path = a_star_pathfinding(current_pos, player_pos, walls)

        # Follow the path if it exists
        if self.path:
            next_step = self.path.pop(0)  # Get the next position
            self.goto(next_step)

        # Continue moving periodically
        turtle.ontimer(self.move, t = 400)

    
    def is_close(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a**2) + (b**2))

        if distance < 35:
            return True
        else:
            return False
        
# Create class instances
pen = Pen()
player = Player()

# Create levels list
levels = []

level_hard = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XP    X                       E     E  X",
    "XXXXX X XXX XXXXXXXXXXXXXXXXXXXXXXX XX X",
    "X     X K X X                         DX",
    "X XXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                      X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XP    X                       E     E  X",
    "XXXXX X XXX XXXXXXXXXXXXXXXXXXXXXXX XX X",
    "X     X K X X                         DX",
    "X XXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                      X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XP    X                       E     E  X",
    "XXXXX X XXX XXXXXXXXXXXXXXXXXXXXXXX XX X",
    "X     X K X X                         DX",
    "X XXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                      X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X     X K X X                         DX",
    "X XXXXXXXXX XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X       T                              X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
]
# Convert level_hard into a mutable format
level_hard = convert_to_list_of_lists(level_hard)

# Create wall barrier list
walls = []

# Add pickaxes list
pickaxes = []

teleports = []

# Add enemies list
enemies = []

# Add maze to mazes list
levels.append(level_hard)


wall_stamps = {}
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
                pen.goto(screen_x, screen_y)
                stamp_id = pen.stamp()

                # Add barriers to wall list
                walls.append((screen_x,screen_y))
                wall_stamps[(screen_x, screen_y)] = stamp_id
            
            # Check if it is a 'P' (representing player)
            if character == 'P':
                player.goto(screen_x, screen_y)
            

            # Check if it is a 'E' (representing enemies)
            if character == 'E':
                enemy = Enemy(screen_x, screen_y)
                enemies.append(enemy)
                # Start moving the enemy
                enemy.move()

            if character == 'K':
                pickaxes.append(Pickaxe(screen_x, screen_y))

            if character == 'T':
                teleports.append(Teleportation(screen_x, screen_y))


 
# Keyboard binding
turtle.listen()
turtle.onkey(player.go_left, "Left")
turtle.onkey(player.go_right, "Right")
turtle.onkey(player.go_up, "Up")
turtle.onkey(player.go_down, "Down")


def mine():
    if player.pickaxe > 0:
        x, y = player.xcor(), player.ycor()
        for dx, dy in [(-24, 0), (24, 0), (0, -24), (0, 24)]:
            wall_x, wall_y = x + dx, y + dy
            if (wall_x, wall_y) in walls:
                player.mine_wall(wall_x, wall_y)
                pickaxe_hit_sound.play()
                break
    
    else: 
        display_message("No pickaxes available!", 2000)

# Press "space" to mine walls
turtle.onkey(mine, "space")

# Call the setup maze funtion
setup_maze(levels[0])

# Turn off screen updates
wn.tracer(0)


# Create a pen for the message
message_pen = Pen()
message_pen.hideturtle()
message_pen.color("yellow")

def display_message(text, duration=2000):
    """Display a temporary message on the screen."""
    message_pen.clear()
    message_pen.goto(0, 0)
    message_pen.write(text, align="center", font=("Arial", 20, "bold"))
    
    # Clear the message after the specified duration
    turtle.ontimer(message_pen.clear, duration)


# Add a global timer variable
start_time = time.time()
time_limit = 60 # game durations in sec

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
    hud_pen.write(f"RUN AWAYY!! | Pickaxes left: {player.pickaxe}", align="left", font=("Arial", 14, "bold"))

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


# Main game
try:
    while True:
        # Check for player collision with treasure
        # update_lighting()
        # Display timer
        remain_time = showtime()
        if remain_time <= 0:
            won()

        # Display HUD
        show_hud()

        for pickaxe in pickaxes:
            if player.is_collision(pickaxe):
                print("You found a pickaxe!")
                player.pickaxe += pickaxe.have
                player.has_pickaxe = True
                winsound.PlaySound("get_gold.wav", winsound.SND_ASYNC)
                pickaxe.destroy()
                pickaxes.remove(pickaxe)
                display_message("Wow, a pickaxe! | Press 'Space' to use", 2000)

        
        for teleport in teleports:
            if player.is_collision(teleport):
                winsound.PlaySound("tele.wav", winsound.SND_ASYNC)
                player.teleport(25, 25, level_hard)
                teleport.destroy()
                teleports.remove(teleport)

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
