import pygame
import random

#initialize pygame
pygame.init()

#game constants
width = 600
height = 400
tile = 20
white, green, red, black = (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0)

#game window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("snake game")

#snake and food
snake = [(100, 100)]
path = (tile, 0)
food = (random.randrange(0, width, tile), random.randrange(0, height, tile))

#game loop variables
crawling = True
clock = pygame.time.Clock()

while crawling:
    screen.fill(black) #clear screen

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
    else:
        snake.pop() #remove tile if no food eaten

    # game over conditions
    if new_head in snake[1:] or not (0 <= new_head[0] < width and 0 <= new_head[1] < height):
        crawling = False #snake hit itself or the wall

    #draw snake
    for segment in snake:
        pygame.draw.rect(screen, green, (segment[0], segment[1], tile, tile))

    #draw food
    pygame.draw.rect(screen, red, (food[0], food[1], tile, tile))

    pygame.display.update()
    clock.tick(10) #control game speed

pygame.quit()
