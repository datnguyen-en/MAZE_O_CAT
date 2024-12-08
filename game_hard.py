import turtle
import math
import random
import time
import pygame

# Add music for the game
pygame.mixer.init()
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Load sound effect
pickaxe_hit_sound = pygame.mixer.Sound("background.mp3")
pickaxe_hit_sound.set_volume(0.5)   

# Create the UI for the game
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("The Maze")
wn.setup(700, 700)
wn.tracer(0)

# Register shapes
images = ['wall2.gif', 'cookie.gif', 'enemy.gif', 'char.gif', 'door.gif', 'pickaxe.gif']
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
        
    # Mine wall if the player got package    
    def mine_wall(self, x, y):
        if self.has_pickaxe and (x, y) in walls:
            walls.remove((x, y))
            stamp_id = wall_stamps.pop((x,y), None)
            if stamp_id is not None:
                pen.clearstamp(stamp_id)


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

# Create Pickaxe
class Pickaxe(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape('pickaxe.gif')
        self.color("green")
        self.penup()
        self.speed(0)
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
# lighting = Lighting()



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
    # for i in range(random.randint(1, 5)):
    #     tx, ty = random.randrange(1, cols, 2), random.randrange(1, rows, 2)
    #     if maze[ty][tx] == " ":
    #         maze[ty][tx] = "T"

    # Add random enemies
    for i in range(4):
        ex, ey = random.randrange(1, cols, 2), random.randrange(1, rows, 2)
        if maze[ey][ex] == " ":
            maze[ey][ex] = "E"

    return maze

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
]

# Create wall barrier list
walls = []

# Add treasures list
treasures = []

# Add pickaxes list
pickaxes = []

# Add door list
doors = []

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
            
            # Check if it is a 'T' (representing treasure)
            # if character == 'T': 
            #     treasures.append(Treasure(screen_x,screen_y))

            # Check if it is a 'D' (representing Door)
            if character == 'D':
                doors.append(Door(screen_x, screen_y))

            # Check if it is a 'E' (representing enemies)
            if character == 'E':
                enemy = Enemy(screen_x, screen_y)
                enemies.append(enemy)
                # Start moving the enemy
                enemy.move()

            if character == 'K':
                pickaxes.append(Pickaxe(screen_x, screen_y))


# Update Lighting
# def update_lighting():
#     lighting.draw_light(player.position(), 200)
 
# Keyboard binding
turtle.listen()
turtle.onkey(player.go_left, "Left")
turtle.onkey(player.go_right, "Right")
turtle.onkey(player.go_up, "Up")
turtle.onkey(player.go_down, "Down")


def mine():
    x, y = player.xcor(), player.ycor()
    for dx, dy in [(-24, 0), (24, 0), (0, -24), (0, 24)]:
        wall_x, wall_y = x + dx, y + dy
        if (wall_x, wall_y) in walls:
            player.mine_wall(wall_x, wall_y)
            pickaxe_hit_sound.play()
            break

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
    hud_pen.write(f"Cookies Left: {len(treasures)}", align="left", font=("Arial", 14, "bold"))

# After gameplay
def game_over():
    # Display Game Over message and stop the game.
    pen.goto(0, 0)
    pen.color("red")
    pen.write("GAME OVER", align="center", font=("Arial", 36, "bold"))
    wn.update()
    time.sleep(3)
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
        # update_lighting()
        # Display timer
        remain_time = showtime()
        if remain_time <= 0:
            game_over()

        # Display HUD
        show_hud()

        for pickaxe in pickaxes:
            if player.is_collision(pickaxe):
                print("You found a pickaxe!")
                player.has_pickaxe = True
                pickaxe.destroy()
                pickaxes.remove(pickaxe)
                display_message("Wow, you received a pickaxe!", 3000)

        
        for door in doors:
            if player.is_collision(door):
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