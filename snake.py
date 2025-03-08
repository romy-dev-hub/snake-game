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
