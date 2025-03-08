import pygame
import random
import math

# Initialize pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 600, 400
TILE = 20
WHITE, GREEN, RED, BLACK = (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0)
BLUE, BROWN = (0, 0, 255), (139, 69, 19)

# Game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Load images
menu_bg = pygame.image.load("game_bg.jpg")
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))
background = pygame.image.load("backgroung.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
game_over_bg = pygame.image.load("game_over.jpg")
game_over_bg = pygame.transform.scale(game_over_bg, (WIDTH, HEIGHT))

# Fonts
font = pygame.font.Font(None, 30)
menu_font = pygame.font.Font(None, 50)


# Function to create buttons
def draw_button(text, x, y, width_b, height_b, color, hover_color):
    """Draws a button and returns True if clicked"""
    mouse_x, mouse_y = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()[0]  # Left mouse button

    is_hover = x < mouse_x < x + width_b and y < mouse_y < y + height_b
    pygame.draw.rect(screen, hover_color if is_hover else color, (x, y, width_b, height_b))

    # Draw button text
    text_surface = menu_font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width_b // 2, y + height_b // 2))
    screen.blit(text_surface, text_rect)

    return clicked if is_hover else False


# Function to show the main menu
def show_main_menu():
    """Displays the main menu and handles button clicks"""
    while True:
        screen.blit(menu_bg, (0, 0))
        play_clicked = draw_button("Play", 180, 170, 200, 60, GREEN, (0, 200, 0))
        quit_clicked = draw_button("Quit", 180, 250, 200, 60, RED, (200, 0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if play_clicked:
                return
            if quit_clicked:
                pygame.quit()
                exit()


# Function to draw the snake
def draw_snake(snake):
    """Draw the snake with a simple face on its head"""
    for i, (x, y) in enumerate(snake):
        pygame.draw.rect(screen, BLUE, (x, y, TILE, TILE), border_radius=8 if i == 0 else 5)
        if i == 0:
            draw_snake_face(x, y)


# Function to draw snake face
def draw_snake_face(x, y):
    """Draws a simple face on the snake head"""
    pygame.draw.circle(screen, WHITE, (x + 6, y + 6), 3)  # Left eye
    pygame.draw.circle(screen, WHITE, (x + TILE - 6, y + 6), 3)  # Right eye
    pygame.draw.arc(screen, BLACK, (x + 4, y + 10, 10, 6), math.pi, 2 * math.pi, 2)  # Smile


# Function to draw the apple
def draw_apple(x, y, pulse_size):
    """Draw an apple with a pulsing effect"""
    pygame.draw.circle(screen, RED, (x + TILE // 2, y + TILE // 2), pulse_size)
    pygame.draw.rect(screen, GREEN, (x + TILE // 3, y - 5, 6, 6), border_radius=3)
    pygame.draw.line(screen, BROWN, (x + TILE // 2, y - 3), (x + TILE // 2, y + 3), 3)


# Run menu before starting the game
show_main_menu()

# Game variables
snake = [(100, 100)]
direction = (TILE, 0)
food = (random.randrange(0, WIDTH, TILE), random.randrange(0, HEIGHT, TILE))
score = 0
pulse_angle = 0
crawling = True
clock = pygame.time.Clock()

# Game loop
while crawling:
    screen.blit(background, (0, 0))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crawling = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, TILE):
                direction = (0, -TILE)
            elif event.key == pygame.K_DOWN and direction != (0, -TILE):
                direction = (0, TILE)
            elif event.key == pygame.K_LEFT and direction != (TILE, 0):
                direction = (-TILE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-TILE, 0):
                direction = (TILE, 0)

    # Move snake
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, new_head)

    # Check for collisions
    if new_head in snake[1:] or not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
        crawling = False

    # Eat food
    if new_head == food:
        food = (random.randrange(0, WIDTH, TILE), random.randrange(0, HEIGHT, TILE))
        score += 10
    else:
        snake.pop()

    # Draw elements
    draw_snake(snake)
    draw_apple(food[0], food[1], TILE // 2 + int(math.sin(pulse_angle) * 3))
    pulse_angle += 0.1
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(10)

# Game over screen
screen.blit(game_over_bg, (0, 0))
game_over_text = font.render(f"Game Over! Final Score: {score}", True, RED)
screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 2))
pygame.display.update()
pygame.time.delay(3000)
pygame.quit()
