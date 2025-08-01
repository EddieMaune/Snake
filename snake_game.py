import tkinter as tk
import random

# Game settings
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
GAME_WIDTH = 500
GAME_HEIGHT = 500
SPEED = 100
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        
        # Create initial snake body coordinates
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])
        
        # Draw the snake on canvas
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, 
                                           fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        
        self.coordinates = [x, y]
        
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, 
                          fill=FOOD_COLOR, tag="food")
                          
def change_direction(new_direction):
    global direction
    
    # Prevent snake from going backwards into itself
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

# Create the main window
window = tk.Tk()
window.title("Snake Game")
window.resizable(False, False)

# Keyboard controls
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<space>', lambda event: restart_game())
window.focus_set()  # Make sure window can receive key events

def game_over():
    canvas.delete("all")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                      font=('consolas', 70), text="GAME OVER", fill="red")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 + 50,
                      font=('consolas', 20), text="Press SPACE to restart", fill="white")

def restart_game():
    global snake, food, direction
    
    # Clear the canvas
    canvas.delete("all")
    
    # Reset direction
    direction = 'down'
    
    # Create new snake and food
    snake = Snake()
    food = Food()
    
    # Start the game again
    next_turn()

def next_turn():
    global food
    
    x, y = snake.coordinates[0]
    
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    
    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)
    
    # Check if food is eaten
    if x == food.coordinates[0] and y == food.coordinates[1]:
        canvas.delete("food")
        food = Food()  # Create new food
    else:
        # Remove tail only if no food eaten (snake grows when eating)
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    
    # Check wall collisions
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        game_over()
        return
    
    # Check self collision
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            game_over()
            return
    
    window.after(SPEED, next_turn)


# Create the canvas (game board)
canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Create the snake
snake = Snake()
# Create food
food = Food()

# Movement direction
direction = 'down'

# Start the game loop
next_turn()
window.mainloop()

