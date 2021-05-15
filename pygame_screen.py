import pygame
from constants import *

pygame.init()

game_display = pygame.display.set_mode((game_width_const, game_height_const))


def get_game_display():
    return game_display
