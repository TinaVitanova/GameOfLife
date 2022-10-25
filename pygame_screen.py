import pygame
from constants import *

pygame.init()
pygame.font.init()

game_display = pygame.display.set_mode((game_width, game_height))
pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.KEYDOWN, pygame.KEYUP])


def get_game_display():
    return game_display
