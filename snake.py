import pygame
import random

#initialize pygame
pygame.init()

#game constants
width = 600
height = 400
tile = 20
white, green, red, black = (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0)
blue = (0, 0, 255)

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

#game loop variables
crawling = True
clock = pygame.time.Clock()

def draw_snake(snake):
    """draw the snake with the styled design"""
    for i, segment in enumerate(snake):
        if i == 0:
            pygame.draw.rect(screen, blue, (segment[0], segment[1], tile, tile), border_radius=8) #head
        else:
            pygame.draw.rect(screen, blue, (segment[0], segment[1], tile, tile), border_radius=5)  # head

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
    pygame.draw.rect(screen, red, (food[0], food[1], tile, tile))

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
pygame.time.delay(2000) #show for 2 seconds before closing
pygame.quit()
