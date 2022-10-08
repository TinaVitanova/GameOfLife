import random
import threading
import bisect
from datetime import datetime, timedelta

import numpy
import pygame
import matplotlib.pyplot as plt
import matplotlib.dates as md
import csv

import bots_array
import constants
import pygame_screen
from genetic_bot_class import BotClass
from button import Button
from food_poison_array import FoodArray, PoisonArray
from input import InputBox
from statistics import stats
from interval import ThreadJob
from util_functions import are_array_values_increasing

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 180, 0)

getValue = constants.botsValues.get_attr

# The button can be styled in a manner similar to CSS.
BUTTON_STYLE = {"hover_color": (0, 180, 0),
                "text": "Start Game",
                "hover_font_color": WHITE,
                # "hover_sound": pygame.mixer.Sound("blip-short1.wav")
                }
# running is used for the pygame window
running = True
# game_set is used for switching between set game window and the game window
game_set = False
# which bot to show data for, if it's empty will show nothing
show_data_bot = None

event = threading.Event()


def save_statistics():
    threading.Timer(5.0, save_statistics).start()


def set_stats():
    sum_age_c = 0
    sum_age_h = 0
    num_bots_h = 0
    num_bots_c = 0
    for bot in bots_array.get_bots()[::-1]:
        if bot.bot_type == 1:
            sum_age_h += bot.age
            num_bots_h += 1
        else:
            sum_age_c += bot.age
            num_bots_c += 1
    avg_age_c = 0 if num_bots_c == 0 else sum_age_c / num_bots_c
    avg_age_h = 0 if num_bots_h == 0 else sum_age_h / num_bots_h
    stats.update_age('avg_age_c', avg_age_c)
    stats.update_age('avg_age_h', avg_age_h)


def end_game():
    statistics = vars(stats)
    # xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    xfmt = md.DateFormatter('%H:%M:%S')
    for i, stat_name in enumerate(statistics):
        plt.figure(i + 1)
        ax = plt.gca()
        plt.subplots_adjust(bottom=0.2)
        plt.xticks(rotation=45)
        plt.title(stat_name.replace("_", " ").capitalize())
        ax.xaxis.set_major_formatter(xfmt)
        stat = stats.get_statistics(stat_name)
        plt.scatter(*zip(*stat))
        with open('sim3.csv', 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(['Time', stat_name.replace("_", " ").capitalize()])
            # write multiple rows
            writer.writerows([list(ele) for ele in stat])
    plt.show()
    set_game()


def check_termination_conditions():
    global game_set
    num_bots_c = stats.get_statistics('num_c_bots')
    num_bots_h = stats.get_statistics('num_h_bots')
    dt = md.date2num(datetime.now() - timedelta(minutes=2))
    datetime_arr_c, stats_arr_c = zip(*num_bots_c)
    datetime_arr_h, stats_arr_h = zip(*num_bots_h)
    index_to_check_c = bisect.bisect_left(list(datetime_arr_c), dt)
    index_to_check_h = bisect.bisect_left(list(datetime_arr_h), dt)
    are_h_bots_increasing = (len(list(stats_arr_h)[index_to_check_h:]) > 1
                             and are_array_values_increasing(list(stats_arr_h)[index_to_check_h:]))
    are_c_bots_increasing = (len(list(stats_arr_c)[index_to_check_c:]) > 1
                             and are_array_values_increasing(list(stats_arr_c)[index_to_check_c:]))
    if are_c_bots_increasing and are_h_bots_increasing:
        print('Terminated with stable env of both bot types')
        end_game()
    if (numpy.std(list(stats_arr_c)[index_to_check_c:]) < 0.1
            and numpy.std(list(stats_arr_h)[index_to_check_h:]) < 0.1):
        print('Terminated with stable-ish env of both bot types')
        end_game()
    elif are_c_bots_increasing:
        print('Terminated with stable env of carnivore bot types')
        end_game()
    elif are_h_bots_increasing:
        print('Terminated with stable env of herbivore bot types')
        end_game()
    elif numpy.std(list(stats_arr_h)[index_to_check_h:]) < 0.1:
        print('Terminated with stable-ish env of herbivore types')
        end_game()
    elif numpy.std(list(stats_arr_c)[index_to_check_c:]) < 0.1:
        print('Terminated with stable-ish env of carnivore types')
        end_game()
    elif list(stats_arr_c)[-1] == 0 and list(stats_arr_h)[-1] == 0:
        print('Terminated with no achieved stable environment (both types have died out)')
        end_game()
    else:
        print('No achieved stable environment')


def set_game():
    global event
    global game_set
    if game_set:
        for bot in bots_array.get_bots():
            bot.be_eaten()
    else:
        stats_update = ThreadJob(set_stats, event, 5)
        termination_check = ThreadJob(check_termination_conditions, event, 500)

        stats_update.start()
        termination_check.start()
        # create n random bots at the start of the game form inputs
        for _ in range(getValue("num_of_herbivore_bots", 'INT')):
            stats.update_bots('num_h_bots', 'add')
            bots_array.add_bots(BotClass(random.SystemRandom().uniform(0, constants.game_width),
                                         random.SystemRandom().uniform(0, constants.game_height), 1))
        for _ in range(getValue("num_of_carnivore_bots", 'INT')):
            stats.update_bots('num_c_bots', 'add')
            bots_array.add_bots(BotClass(random.SystemRandom().uniform(0, constants.game_width),
                                         random.SystemRandom().uniform(0, constants.game_height), 2))
        save_statistics()
    game_set = not game_set


def text_objects(text, font):
    # create a text object and rectangle for an input box
    text_surface = font.render(text, True, (0, 0, 200))
    return text_surface, text_surface.get_rect()


def show_data(text, font):
    # create a text object and rectangle for an input box
    text_surface = font.render(text, True, (0, 0, 200))
    return text_surface, text_surface.get_rect()


def message_display(text, x, y):
    large_text = pygame.font.Font(None, 20)
    text_surface, text_rect = text_objects(text, large_text)
    text_rect.bottom = y
    text_rect.left = x
    # display created text object and rectangle on screen  by x, y coordinates
    pygame_screen.game_display.blit(text_surface, text_rect)


def main():
    global game_set
    global running
    global show_data_bot
    oldest_ever = 0
    oldest_ever_dna = []

    clock = pygame.time.Clock()
    pygame.display.set_caption('Survival of the bots')

    # initiate empty Food and Poison arrays
    food_array = FoodArray()
    poison_array = PoisonArray()

    # Initiate button for start game
    button = Button((0, 0, 150, 40), (0, 200, 0), set_game,
                    **BUTTON_STYLE)
    button.rect.center = (pygame_screen.game_display.get_rect().centerx, 740)

    # Initiate inputs for bot variables
    input_num_of_herbivore_bots = InputBox(50, 100, 150, 32,
                                           getValue("num_of_herbivore_bots", "STR"),
                                           "num_of_herbivore_bots", "INT", 'zero_and_above')
    input_attr_to_food_h = InputBox(50, 160, 150, 32, getValue("attr_to_food_h", "STR"),
                                    "attr_to_food_h")
    input_attr_to_poison_h = InputBox(50, 220, 150, 32, getValue("attr_to_poison_h", "STR"),
                                      "attr_to_poison_h")
    input_steering_attr_h = InputBox(50, 280, 150, 32,
                                     getValue("steering_attr_h", "STR"),
                                     "steering_attr_h")
    input_perception_food_h = InputBox(50, 340, 150, 32,
                                       getValue("perception_food_h", "STR"),
                                       "perception_food_h")
    input_perception_poison_h = InputBox(50, 400, 150, 32,
                                         getValue("perception_poison_h", "STR"),
                                         "perception_poison_h")
    input_steering_perception_h = InputBox(50, 460, 150, 32,
                                           getValue(
                                               "steering_perception_h", "STR"),
                                           "steering_perception_h")
    input_reproduction_rate_h = InputBox(50, 520, 150, 32,
                                         getValue("reproduction_rate_h", "STR"),
                                         "reproduction_rate_h", 'FLOAT', 'zero_and_above')
    input_steering_reproduction_rate_h = InputBox(50, 580, 150, 32,
                                                  getValue("steering_reproduction_rate_h", "STR"),
                                                  "steering_reproduction_rate_h")
    input_mutation_rate_h = InputBox(50, 640, 150, 32, getValue("mutation_rate_h", "STR"),
                                     "mutation_rate_h", 'FLOAT', 'zero_and_above')
    input_steering_mutation_rate_h = InputBox(340, 100, 150, 32,
                                              getValue("steering_mutation_rate_h", "STR"),
                                              "steering_mutation_rate_h")
    input_velocity_h = InputBox(340, 160, 150, 32, getValue("velocity_h", "STR"),
                                "velocity_h")
    input_steering_velocity_h = InputBox(340, 220, 150, 32, getValue("steering_velocity_h", "STR"),
                                         "steering_velocity_h")
    input_health_h = InputBox(340, 280, 150, 32, getValue("health_h", "STR"),
                              "health_h")
    input_steering_health_h = InputBox(340, 340, 150, 32, getValue("steering_health_h", "STR"),
                                       "steering_health_h")
    input_nutrition_cost_food_h = InputBox(340, 400, 150, 32, getValue("nutrition_food_h", "STR"),
                                           "nutrition_food_h")
    input_nutrition_cost_poison_h = InputBox(340, 460, 150, 32,
                                             getValue("nutrition_poison_h", "STR"),
                                             "nutrition_poison_h")
    input_steering_nutrition_h = InputBox(340, 520, 150, 32,
                                          getValue("steering_nutrition_h", "STR"),
                                          "steering_nutrition_h")
    input_health_depletion_h = InputBox(340, 580, 150, 32,
                                        getValue("health_depletion_h", "STR"),
                                        "health_depletion_h")
    input_steering_depletion_h = InputBox(340, 640, 150, 32,
                                          getValue("steering_depletion_h", "STR"),
                                          "steering_depletion_h")
    input_num_of_carnivore_bots = InputBox(630, 100, 150, 32,
                                           getValue("num_of_carnivore_bots", "STR"),
                                           "num_of_carnivore_bots", "INT", 'zero_and_above')
    input_attr_to_food_c = InputBox(630, 160, 150, 32, getValue("attr_to_food_c", "STR"),
                                    "attr_to_food_c")
    input_steering_attr_c = InputBox(630, 220, 150, 32,
                                     getValue("steering_attr_c", "STR"),
                                     "steering_attr_c")
    input_perception_food_c = InputBox(630, 280, 150, 32,
                                       getValue("perception_food_c", "STR"),
                                       "perception_food_c")
    input_steering_perception_c = InputBox(630, 340, 150, 32,
                                           getValue(
                                               "steering_perception_c", "STR"),
                                           "steering_perception_c")
    input_reproduction_rate_c = InputBox(630, 400, 150, 32,
                                         getValue("reproduction_rate_c", "STR"),
                                         "reproduction_rate_h")
    input_steering_reproduction_rate_c = InputBox(630, 460, 150, 32,
                                                  getValue("steering_reproduction_rate_c", "STR"),
                                                  "steering_reproduction_rate_h")
    input_mutation_rate_c = InputBox(630, 520, 150, 32, getValue("mutation_rate_c", "STR"),
                                     "mutation_rate_c")
    input_steering_mutation_rate_c = InputBox(630, 580, 150, 32,
                                              getValue("steering_mutation_rate_c", "STR"),
                                              "steering_mutation_rate_c")
    input_velocity_c = InputBox(630, 640, 150, 32, getValue("velocity_c", "STR"),
                                "velocity_c")
    input_steering_velocity_c = InputBox(920, 100, 150, 32, getValue("steering_velocity_c", "STR"),
                                         "steering_velocity_c")
    input_health_c = InputBox(920, 160, 150, 32, getValue("health_c", "STR"),
                              "health_c")
    input_steering_health_c = InputBox(920, 220, 150, 32, getValue("steering_health_c", "STR"),
                                       "steering_health_c")
    input_nutrition_cost_food_c = InputBox(920, 280, 150, 32, getValue("nutrition_food_c", "STR"),
                                           "nutrition_food_c")
    input_steering_nutrition_c = InputBox(920, 340, 150, 32,
                                          getValue("steering_nutrition_c", "STR"),
                                          "steering_nutrition_c")
    input_health_depletion_c = InputBox(920, 400, 150, 32, getValue("health_depletion_c", "STR"),
                                        "health_depletion_c")
    input_steering_depletion_c = InputBox(920, 460, 150, 32,
                                          getValue("steering_depletion_c", "STR"),
                                          "steering_depletion_c")
    input_max_food = InputBox(1210, 100, 150, 32,
                              str(getValue("max_food")),
                              "max_food", "INT", 'zero_and_above')
    input_max_poison = InputBox(1210, 160, 150, 32,
                                str(getValue("max_poison")),
                                "max_poison", "INT", 'zero_and_above')
    input_food_chance = InputBox(1210, 220, 150, 32,
                                 str(getValue("food_chance")),
                                 "food_chance")
    input_poison_chance = InputBox(1210, 280, 150, 32,
                                   str(getValue("poison_chance")),
                                   "poison_chance")

    # Set all inputs into an array so we can draw them later
    input_boxes = [input_num_of_herbivore_bots, input_num_of_carnivore_bots, input_mutation_rate_h,
                   input_steering_mutation_rate_h,
                   input_steering_attr_h, input_steering_perception_h, input_reproduction_rate_h,
                   input_steering_reproduction_rate_h,
                   input_perception_food_h, input_perception_poison_h, input_velocity_h, input_steering_velocity_h,
                   input_attr_to_food_h,
                   input_attr_to_poison_h, input_health_h, input_steering_health_h, input_nutrition_cost_food_h,
                   input_nutrition_cost_poison_h,
                   input_steering_nutrition_h, input_health_depletion_h, input_steering_depletion_h,
                   input_mutation_rate_c, input_steering_mutation_rate_c, input_steering_attr_c,
                   input_steering_perception_c,
                   input_reproduction_rate_c, input_steering_reproduction_rate_c, input_perception_food_c,
                   input_velocity_c,
                   input_steering_velocity_c, input_attr_to_food_c,
                   input_health_c, input_steering_health_c, input_nutrition_cost_food_c, input_steering_nutrition_c,
                   input_health_depletion_c, input_steering_depletion_c, input_max_food, input_max_poison,
                   input_food_chance, input_poison_chance]

    # Open ended while so that the display gets updated always
    while running:
        # Set background
        pygame_screen.game_display.fill(constants.black)

        # Check if game is started with variables or not
        if game_set:
            # Go through all events and find key down == p for pausing the game
            for pygame_event in pygame.event.get():
                self_event = pygame_event
                if self_event.type == pygame.KEYUP and self_event.key == pygame.K_p:
                    end_game()

                for bot in bots_array.get_bots()[::-1]:
                    if bot.check_event(pygame_event):
                        show_data_bot = bot
                pygame.event.clear()
            # if len(bots_array.get_bots) < 10 or random.SystemRandom().random() < 0.0001:
            #     bots_array.add_bots(BotClass(random.SystemRandom().uniform(0, game_width),
            #     random.SystemRandom().uniform(0, game_height), 2))

            # Generate foodstuffs in random places if there are not above their max limit
            if random.SystemRandom().random() < getValue("food_chance") and \
                    len(food_array.get_food()) < getValue("max_food", 'INT'):
                stats.update_foodstuffs('num_food', 'add')
                # Add in num of food stat
                food_array.add_food((random.SystemRandom().uniform(constants.boundary_size,
                                                                   constants.game_width -
                                                                   constants.boundary_size),
                                     random.SystemRandom().uniform(constants.boundary_size,
                                                                   constants.game_height -
                                                                   constants.boundary_size)))
            if random.SystemRandom().random() < getValue("poison_chance") and \
                    len(poison_array.get_poison()) < getValue("max_poison", 'INT'):
                stats.update_foodstuffs('num_poison', 'add')
                # Add in num of poison stat
                poison_array.add_poison((random.SystemRandom().uniform(constants.boundary_size,
                                                                       constants.game_width -
                                                                       constants.boundary_size),
                                         random.SystemRandom().uniform(constants.boundary_size,
                                                                       constants.game_height -
                                                                       constants.boundary_size)))
            # Go through all bots and fire out eat method in order to search for food on every update
            for bot in bots_array.get_bots()[::-1]:
                if bot.bot_type == 1:
                    closest_distance_food, closest_food, index_food = bot.eat(food_array.get_food(), 0,
                                                                              food_array.remove_food)
                    closest_distance_poison, closest_poison, index_poison = bot.eat(poison_array.get_poison(), 1,
                                                                                    poison_array.remove_poison)
                    # TODO: find function to even out attraction and closeness
                    if closest_distance_food < closest_distance_poison:
                        bot.seek_closest(closest_distance_food, closest_food, index_food)
                    else:
                        bot.seek_closest(closest_distance_poison, closest_poison, index_poison)
                if bot.bot_type == 2:
                    bot.eat_bot(bots_array.get_bots_by_type(1), 0, 1)
                # Check if bot is hitting a boundary
                bot.boundaries()
                # bot.seek(pygame.mouse.get_pos())
                # Update bot movement according to info from eat and boundaries
                bot.update()
                # Track oldest bot ever
                if bot.age > oldest_ever:
                    oldest_ever = bot.age
                    oldest_ever_dna = bot.dna
                    # print(oldest_ever, oldest_ever_dna)
                # Draw all bots (necessary on every update)
                bot.draw_bot(pygame_screen.game_display)
                # Check if a bot has previously died and if so remove it from the list
                if bot.dead():
                    bots_array.get_bots().remove(bot)
                    del bot
                else:
                    # If bot isn't dead try to reproduce
                    bot.reproduce(bots_array.get_bots())

            # Draw foodstuffs
            for i in food_array.get_food():
                pygame.draw.circle(pygame_screen.game_display, (0, 255, 0), (int(i[0]), int(i[1])), 3)
            for i in poison_array.get_poison():
                pygame.draw.circle(pygame_screen.game_display, (255, 0, 0), (int(i[0]), int(i[1])), 3)

            if show_data_bot:
                message_display(f'X: {show_data_bot.position[0]}', 10, 20)
                message_display(f'Y: {show_data_bot.position[1]}', 10, 40)
                message_display(f'Health: {show_data_bot.health}', 10, 60)
                message_display(f'Max health: {show_data_bot.dna[7]}', 10, 80)
                message_display(f'Health depletion: {show_data_bot.dna[10]}', 10, 100)
                message_display(f'Age: {show_data_bot.age / constants.fps}', 10, 120)
                message_display(f'Velocity: {show_data_bot.dna[6]}', 10, 140)
                message_display(f'Mutation rate: {show_data_bot.dna[5]}', 10, 160)
                message_display(f'Reproduction rate: {show_data_bot.dna[4]}', 10, 180)
                message_display(f'Attraction food: {show_data_bot.dna[0]}', 10, 200)
                message_display(f'Nutrition food: {show_data_bot.dna[8]}', 10, 220)
                if show_data_bot.bot_type == 1:
                    message_display(f'Attraction poison: {show_data_bot.dna[1]}', 10, 240)
                    message_display(f'Nutrition poison: {show_data_bot.dna[9]}', 10, 260)
        # If the game is still not set with variables allow the user to set it
        elif not game_set:
            message_display("Number of herbivore bots", 50, 95)
            message_display("Attracted to food", 50, 155)
            message_display("Attracted to poison", 50, 215)
            message_display("Steering attraction", 50, 275)
            message_display("Perception food", 50, 335)
            message_display("Perception poison", 50, 395)
            message_display("Steering perception", 50, 455)
            message_display("Reproduction rate", 50, 515)
            message_display("Steering reproduction rate", 50, 575)
            message_display("Mutation rate", 50, 635)
            message_display("Steering mutation rate", 340, 95)
            message_display("Velocity", 340, 155)
            message_display("Steering velocity", 340, 215)
            message_display("Health", 340, 275)
            message_display("Steering health", 340, 335)
            message_display("Nutrition cost for food", 340, 395)
            message_display("Nutrition cost for poison", 340, 455)
            message_display("Steering nutrition", 340, 515)
            message_display("Health depletion", 340, 575)
            message_display("Steering depletion", 340, 635)
            message_display("Number of carnivore bots", 630, 95)
            message_display("Attracted to food", 630, 155)
            message_display("Steering attraction", 630, 215)
            message_display("Perception food", 630, 275)
            message_display("Steering perception", 630, 335)
            message_display("Reproduction rate", 630, 395)
            message_display("Steering reproduction rate", 630, 455)
            message_display("Mutation rate", 630, 515)
            message_display("Steering mutation rate", 630, 575)
            message_display("Velocity", 630, 635)
            message_display("Steering velocity", 920, 95)
            message_display("Health", 920, 155)
            message_display("Steering health", 920, 215)
            message_display("Nutrition cost for food", 920, 275)
            message_display("Steering nutrition", 920, 335)
            message_display("Health depletion", 920, 395)
            message_display("Steering depletion", 920, 455)
            message_display("Max food", 1210, 95)
            message_display("Max poison", 1210, 155)
            message_display("Food chance", 1210, 215)
            message_display("Poison chance", 1210, 275)
            # Cycle through events for the input boxes and button to get their respective events
            for pygame_event in pygame.event.get():
                button.check_event(pygame_event, input_boxes)
                for box in input_boxes:
                    box.handle_event(pygame_event)
                pygame.event.clear()
            button.update(pygame_screen.game_display)

            # Update input boxes with correct numbers and draw them
            for box in input_boxes:
                box.update()
            for box in input_boxes:
                box.draw(pygame_screen.game_display)

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         running = False
        #     pygame.event.clear()

        # Necessary for pygame to update the view screen
        pygame.display.update()
        clock.tick(constants.fps)

    # Close pygame
    pygame.quit()
    quit()


main()
