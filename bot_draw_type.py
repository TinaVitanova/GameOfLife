import pygame
# from pygame import gfxdraw


def draw_bot_by_type(bot, game_display):
    #   grass eating
    if bot.bot_type == 1:
        # pygame.gfxdraw.aacircle(game_display, int(bot.position[0]), int(bot.position[1]), 10, bot.colour)
        # pygame.gfxdraw.filled_circle(game_display, int(bot.position[0]), int(bot.position[1]), 5, bot.colour)
        pygame.draw.circle(game_display, bot.colour, (int(bot.position[0]), int(bot.position[1])), 8)
    #   bot eating
    elif bot.bot_type == 2:
        # pygame.gfxdraw.aaellipse(game_display, int(bot.position[0]), int(bot.position[1]), 10, 5, bot.colour)
        # pygame.gfxdraw.filled_ellipse(game_display, int(bot.position[0]), int(bot.position[1]), 10, 5, bot.colour)
        pygame.draw.ellipse(game_display, bot.colour, ((int(bot.position[0]) - 8), (int(bot.position[1]) - 7), 17, 12))
    else:
        pygame.draw.circle(game_display, bot.colour, (int(bot.position[0]), int(bot.position[1])), 8)
