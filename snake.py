import pygame
import random
import math

#initialize pygame
pygame.init()

#game constants
width = 600
height = 400
tile = 20
white, green, red, black = (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0)
blue = (0, 0, 255)
brown = (139, 69, 19)

#game window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("snake game")

#load background
background = pygame.image.load("backgroung.jpg") #add background image
background = pygame.transform.scale(background, (width, height))

game_over_bg = pygame.image.load("game_over.jpg") #add game over background
game_over_bg = pygame.transform.scale(game_over_bg, (width, height))

#snake and food
snake = [(100, 100)]
path = (tile, 0)
food = (random.randrange(0, width, tile), random.randrange(0, height, tile))

#score
score = 0
font = pygame.font.Font(None, 30)

#adding pulse effect
pulse_size = tile // 2
pulse_speed = 0.1
pulse_angle = 0

#game loop variables
crawling = True
clock = pygame.time.Clock()

#function to draw snake
def draw_snake(snake):
    """draw the snake with the styled design"""
    for i, segment in enumerate(snake):
        x, y = segment
        if i == 0:
            pygame.draw.rect(screen, blue, (segment[0], segment[1], tile, tile), border_radius=8) #head
            draw_snake_face(x, y)
        else:
            pygame.draw.rect(screen, blue, (segment[0], segment[1], tile, tile), border_radius=5)  # head

#function to draw snake face
def draw_snake_face(x, y):
    """draw a simple face on the snake head"""
    eye_radius = 4
    eye_x_offset = 6
    eye_y_offset = 5

    #eyes
    pupil_radius = 3
    pygame.draw.circle(screen, white, (int(x + eye_x_offset), int(y + eye_y_offset)), pupil_radius) #left eye
    pygame.draw.circle(screen, white, (int(x + tile - eye_x_offset), int(y + eye_y_offset)), pupil_radius) #right eye

    #mouth
    pygame.draw.arc(screen, black, (int(x + 4), int(y + 10), 10, 6), math.pi, 2 * math.pi, 2) #smiling mouth

# function to draw apple
def draw_apple(x, y):
    """draw an apple using pygame shapes"""
    global pulse_size, pulse_angle

    pulse_size = tile // 2 + int(math.sin(pulse_angle) * 3)
    pulse_angle += pulse_speed

    pygame.draw.circle(screen, red, (int(x + tile // 2), int(y + tile // 2)), int(pulse_size))
    pygame.draw.rect(screen, green, (x + tile // 3, y - 5, 6, 6), border_radius=3)
    pygame.draw.line(screen, brown, (x + tile // 2, y - 3), (x + tile // 2, y + 3), 3)

while crawling:
    screen.blit(background, (0, 0)) #clear screen

    #handle keyboard presses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crawling = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and path != (0, tile):
                path = (0, -tile)
            elif event.key == pygame.K_DOWN and path != (0, -tile):
                path = (0, tile)
            elif event.key == pygame.K_LEFT and path != (tile, 0):
                path = (-tile, 0)
            elif event.key == pygame.K_RIGHT and path != (-tile, 0):
                path = (tile, 0)

    #move snake
    new_head = (snake[0][0] + path[0], snake[0][1] + path[1])
    snake.insert(0, new_head)

    #collision
    if new_head == food:
        food = (random.randrange(0, width, tile), random.randrange(0, height, tile))
        score += 10
    else:
        snake.pop() #remove tile if no food eaten

    # game over conditions
    if new_head in snake[1:] or not (0 <= new_head[0] < width and 0 <= new_head[1] < height):
        crawling = False #snake hit itself or the wall

    #draw snake
    draw_snake(snake)

    #draw food
    draw_apple(food[0], food[1])

    #display score
    score_text = font.render(f"score: {score}", True, white)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(10) #control game speed

#game over screen
screen.blit(game_over_bg, (0, 0))
game_over_text = font.render(f"Game over! final score: {score}", True, red)
screen.blit(game_over_text, (width // 4, height // 2))
pygame.display.update()
pygame.time.delay(3000) #show for 2 seconds before closing
pygame.quit()
