import pygame
import random
import math
import numpy
import time
import constants
import pygame_screen
import food_array
import bots_array
import genetic_bot_class


poison = []


def main():
    oldest_ever = 0
    oldest_ever_dna = []
    clock = pygame.time.Clock()

    # initially start with 10 random bots (random dna)
    for i in range(10):
        bots_array.add_bots(genetic_bot_class.BotClass(random.uniform(0, constants.game_width_const), random.uniform(0, constants.game_height_const), 1))
    for i in range(1):
        bots_array.add_bots(genetic_bot_class.BotClass(random.uniform(0, constants.game_width_const), random.uniform(0, constants.game_height_const), 2))
    running = True
    while running:
        time.sleep(0.05)
        pygame_screen.game_display.fill(constants.black_const)

        # if len(bots_array.get_bots) < 10 or random.random() < 0.0001:
        #     bots_array.add_bots(BotClass(random.uniform(0, game_width), random.uniform(0, game_height), 2))
        if random.random() < 0.1:
            food_array.add_food(numpy.array([random.uniform(constants.boundary_size_const,
                                                            constants.game_width_const - constants.boundary_size_const),
                                             random.uniform(constants.boundary_size_const,
                                                            constants.game_height_const - constants.boundary_size_const)], dtype='float64'))
        if random.random() < 0.01:
            poison.append(numpy.array([random.uniform(constants.boundary_size_const, constants.game_width_const - constants.boundary_size_const),
                                       random.uniform(constants.boundary_size_const, constants.game_height_const - constants.boundary_size_const)],
                                      dtype='float64'))
        if len(poison) > constants.max_poison_const:
            poison.pop(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for bot in bots_array.get_bots()[::-1]:
            if bot.bot_type == 1:
                bot.eat(food_array.get_food(), 0)
                bot.eat(poison, 1)
            if bot.bot_type == 2:
                bot.eat_bot(bots_array.get_bots(), 0, 1)
            bot.boundaries()
            # bot.seek(pygame.mouse.get_pos())
            bot.update()
            if bot.age > oldest_ever:
                oldest_ever = bot.age
                oldest_ever_dna = bot.dna
                # print(oldest_ever, oldest_ever_dna)
            bot.draw_bot(pygame_screen.game_display)
            if bot.dead(food_array.get_food()):
                bots_array.get_bots().remove(bot)
            else:
                bot.reproduce(bots_array.get_bots())

        for i in food_array.get_food():
            pygame.draw.circle(pygame_screen.game_display, (0, 255, 0), (int(i[0]), int(i[1])), 3)
        for i in poison:
            pygame.draw.circle(pygame_screen.game_display, (255, 0, 0), (int(i[0]), int(i[1])), 3)
        pygame.display.update()
        clock.tick(constants.fps_const)

    pygame.quit()
    quit()


main()
