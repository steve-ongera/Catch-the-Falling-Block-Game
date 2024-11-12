import pygame
import random
import sqlite3
import os

# Initialize Pygame
pygame.init()

# SQLite database file
DB_FILE = 'game_scores.db'

# Function to initialize the database
def initialize_db():
    # Check if the database file exists, if not, create it
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Create the scores table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT,
                score INTEGER
            )
        ''')
        conn.commit()
        conn.close()

# Initialize the database
initialize_db()

# Connect to the SQLite database
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 192, 203)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
LIGHT_YELLOW = (255, 255, 224)
LIGHT_RED = (255, 99, 71)

# Block dimensions
BLOCK_WIDTH = 50
BLOCK_HEIGHT = 50
BASKET_WIDTH = 100
BASKET_HEIGHT = 20

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the Falling Block")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Define font for score and pause text
font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 60)

# Load pause icon image (you need to have a pause icon file, e.g., 'pause_icon.png')
pause_icon = pygame.image.load('pause_icon.png')
pause_icon = pygame.transform.scale(pause_icon, (40, 40))  # Scale to desired size

# Basket class
class Basket:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2 - BASKET_WIDTH // 2
        self.y = SCREEN_HEIGHT - BASKET_HEIGHT - 10
        self.speed = 10

    def move(self, dx):
        self.x += dx
        if self.x < 0:
            self.x = 0
        elif self.x + BASKET_WIDTH > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - BASKET_WIDTH

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, BASKET_WIDTH, BASKET_HEIGHT))

# Block class
class Block:
    def __init__(self, speed):
        self.x = random.randint(0, SCREEN_WIDTH - BLOCK_WIDTH)
        self.y = -BLOCK_HEIGHT
        self.speed = speed  # Speed of the block depends on the score
        self.color, self.score = self.random_color_and_score()  # Assign a random color and score

    def random_color_and_score(self):
        """Randomly assign a block color and corresponding score."""
        color_scores = [
            (PINK, 1),
            (RED, 2),
            (GREEN, 5),
            (YELLOW, 4),
            (BLUE, 10)
        ]
        return random.choice(color_scores)

    def update(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, BLOCK_WIDTH, BLOCK_HEIGHT))

    def off_screen(self):
        return self.y > SCREEN_HEIGHT

    def caught_by(self, basket):
        # Check if any part of the block overlaps with the basket
        return (self.y + BLOCK_HEIGHT >= basket.y and
                basket.x <= self.x + BLOCK_WIDTH and self.x <= basket.x + BASKET_WIDTH)

# Function to draw buttons with rounded corners and different colors
def draw_button(text, x, y, width, height, color, text_color=BLACK):
    # Draw the button with rounded corners
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, button_rect, border_radius=15)
    # Draw the text on the button
    text_surface = font.render(text, True, text_color)
    screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))

# Function to save the score to the database
def save_score(player_name, score):
    cursor.execute('''
        INSERT INTO scores (player_name, score)
        VALUES (?, ?)
    ''', (player_name, score))
    conn.commit()

# Main game loop
def game_loop():
    basket = Basket()
    blocks = []
    score = 0
    missed_blocks = 0
    max_missed_blocks = 10  # Game ends after missing 10 blocks
    game_over = False
    block_speed = 5  # Initial speed of falling blocks
    paused = False  # Game pause state

    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            # Toggle pause when 'P' is pressed or when the pause icon is clicked
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = not paused
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if the pause icon is clicked
                if 760 <= mouse_x <= 800 and 10 <= mouse_y <= 50:
                    paused = not paused

        # If paused, display pause message and skip game updates
        if paused:
            screen.fill(WHITE)
            pause_text = font.render("Game Paused. Press 'P' to resume.", True, BLACK)
            screen.blit(pause_text, [SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2])
            screen.blit(pause_icon, (SCREEN_WIDTH - 60, 10))  # Draw the pause icon
            pygame.display.flip()
            clock.tick(5)  # Slow down frame rate during pause
            continue  # Skip updating the game while paused

        # Move basket with arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            basket.move(-basket.speed)
        if keys[pygame.K_RIGHT]:
            basket.move(basket.speed)

        # Add new blocks periodically
        if random.randint(1, 20) == 1:
            blocks.append(Block(block_speed))  # Pass the current block speed

        # Update and draw blocks
        screen.fill(WHITE)

        # Draw and move the basket
        basket.draw()

        # List to hold blocks to remove after the loop
        blocks_to_remove = []

        for block in blocks:
            block.update()
            block.draw()

            # Check if block is caught by the basket (even if partially)
            if block.caught_by(basket):
                blocks_to_remove.append(block)
                score += block.score  # Add block's score to total score
                missed_blocks = 0  # Reset missed block count if the player catches a block

                # Increase speed every 5 points
                if score % 5 == 0:
                    block_speed += 0.5  # Gradually increase the falling speed

            # Check if block hits the bottom
            elif block.off_screen():
                blocks_to_remove.append(block)
                missed_blocks += 1  # Increment the missed block count

            # Check if missed 10 blocks in a row
            if missed_blocks >= max_missed_blocks:
                game_over = True

        # Remove blocks that are either caught or off-screen
        for block in blocks_to_remove:
            if block in blocks:
                blocks.remove(block)

        # Display the score and missed blocks
        score_text = font.render(f"Score: {score}", True, BLACK)
        missed_text = font.render(f"Missed: {missed_blocks}/{max_missed_blocks}", True, RED)
        screen.blit(score_text, [10, 10])
        screen.blit(missed_text, [10, 50])

        # Draw the pause icon
        screen.blit(pause_icon, (SCREEN_WIDTH - 60, 10))

        # Update the display
        pygame.display.flip()

        # Frame rate
        clock.tick(30)

    # Game Over screen
    show_game_over_screen(score)

# Function to show the game over screen
def show_game_over_screen(score):
    game_over_text = large_font.render("Game Over!", True, BLACK)
    score_text = font.render(f"Your Score: {score}", True, BLACK)

    # Draw the Game Over text and score
    screen.fill(WHITE)
    screen.blit(game_over_text, [SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100])
    screen.blit(score_text, [SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2])

    # Draw the buttons
    draw_button("Play Again", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50, 200, 50, LIGHT_GREEN)
    draw_button("Quit", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 120, 200, 50, LIGHT_RED)

    pygame.display.flip()

    # Wait for button press
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if SCREEN_WIDTH // 2 - 150 <= mouse_x <= SCREEN_WIDTH // 2 + 50 and SCREEN_HEIGHT // 2 + 50 <= mouse_y <= SCREEN_HEIGHT // 2 + 100:
                    # Save the score and restart the game
                    player_name = "Player"  # You can make this dynamic based on user input
                    save_score(player_name, score)
                    game_loop()
                    waiting_for_input = False

                elif SCREEN_WIDTH // 2 - 150 <= mouse_x <= SCREEN_WIDTH // 2 + 50 and SCREEN_HEIGHT // 2 + 120 <= mouse_y <= SCREEN_HEIGHT // 2 + 170:
                    pygame.quit()
                    quit()

# Start the game loop
game_loop()

# Close the database connection when quitting
conn.close()
