import pygame
from constants import *

pygame.init()

game_display = pygame.display.set_mode((game_width, game_height))


def get_game_display():
    return game_display
