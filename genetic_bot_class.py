import math
import random

import numpy
import pygame

import bot_draw_type
import constants
import util_functions

from statistics import stats

getValue = constants.botsValues.get_attr

dna_values = [
    "attr_food",
    "attr_poison",
    "perception_food",
    "perception_poison",
    "repr_rate",
    "mutation_rate",
    "velocity",
    "health",
    "nutrition_food",
    "nutrition_poison",
    "health_depletion",
]


class BotClass:
    def __init__(self, x, y, bot_type, dna=None):
        self.suffix = '_h' if bot_type == 1 else '_c'
        self.position = numpy.array([x, y], dtype='float32')
        # where to move towards
        self.step_movement = numpy.array(
            [random.SystemRandom().uniform(-10, 10), random.SystemRandom().uniform(-10, 10)], dtype='float32')
        self.acceleration = numpy.array([0, 0], dtype='float32')
        self.colour = constants.green
        self.health = 0
        # Turning speed and angle
        self.max_force = 0.5
        self.age = 1
        self.bot_type = bot_type

        # dna=[1 - attracted to food, 2 - attracted to poison, 3 - see food, 4 - see poison, 5 - reproduction rate,
        # 6 - mutation rate, 7 - velocity, 8 - health, 9 - nutrition food, 10 - nutrition poison, 11 - health depletion]
        # if dna is sent as a prop, then this is a child being spawned from a parent bot
        if dna:
            self.dna = []
            for dna_property in range(len(dna)):
                if random.SystemRandom().random() < dna[5]:
                    if dna_property in [0, 1]:
                        new_value = dna[dna_property] + round(random.SystemRandom().uniform(
                            -getValue(f"steering_attr{self.suffix}"),
                            getValue(f"steering_attr{self.suffix}")), 10)
                        self.dna.append(util_functions.validate_dna(new_value, dna[dna_property]))
                    elif dna_property in [2, 3]:
                        new_value = dna[dna_property] + round(random.SystemRandom().uniform(
                            -getValue(f"steering_perception{self.suffix}"),
                            getValue(f"steering_perception{self.suffix}")), 10)
                        self.dna.append(util_functions.validate_dna(new_value, dna[dna_property], 'greater_than_zero'))
                    elif dna_property == 4:
                        new_value = dna[dna_property] + round(random.SystemRandom().uniform(
                            -getValue(f"steering_reproduction_rate{self.suffix}"),
                            getValue(f"steering_reproduction_rate{self.suffix}")), 10)
                        self.dna.append(util_functions.validate_dna(new_value, dna[dna_property], 'zero_and_above'))
                    elif dna_property == 5:
                        new_value = dna[dna_property] + round(random.SystemRandom().uniform(
                            -getValue(f"steering_mutation_rate{self.suffix}"),
                            getValue(f"steering_mutation_rate{self.suffix}")), 10)
                        self.dna.append(util_functions.validate_dna(new_value, dna[dna_property], 'zero_and_above'))
                    elif dna_property == 6:
                        new_value = dna[dna_property] + round(random.SystemRandom().uniform(
                            -getValue(f"steering_velocity{self.suffix}"),
                            getValue(f"steering_velocity{self.suffix}")), 10)
                        self.dna.append(util_functions.validate_dna(new_value, dna[dna_property], 'greater_than_zero'))
                    elif dna_property == 7:
                        new_value = dna[dna_property] + round(random.SystemRandom().uniform(
                            -getValue(f"steering_health{self.suffix}"),
                            getValue(f"steering_health{self.suffix}")), 10)
                        self.dna.append(util_functions.validate_dna(new_value, dna[dna_property], 'greater_than_zero'))
                    elif dna_property in [8, 9]:
                        new_value = dna[dna_property] + round(random.SystemRandom().uniform(
                            -getValue(f"steering_nutrition{self.suffix}"),
                            getValue(f"steering_nutrition{self.suffix}")), 10)
                        self.dna.append(util_functions.validate_dna(new_value, dna[dna_property], 'greater_than_zero'))
                    elif dna_property == 10:
                        new_value = dna[dna_property] + round(random.SystemRandom().uniform(
                            -getValue(f"steering_depletion{self.suffix}"),
                            getValue(f"steering_depletion{self.suffix}")), 10)
                        self.dna.append(util_functions.validate_dna(new_value, dna[dna_property], 'greater_than_zero'))
                else:
                    self.dna.append(dna[dna_property])
        else:
            attr_to_food = util_functions.validate_dna(round(random.SystemRandom().uniform(
                getValue(f"attr_to_food{self.suffix}") - getValue(f"steering_attr{self.suffix}"),
                getValue(f"attr_to_food{self.suffix}") + getValue(f"steering_attr{self.suffix}"),
            ), 10), getValue(f"attr_to_food{self.suffix}"))
            attr_to_poison = util_functions.validate_dna(round(random.SystemRandom().uniform(
                -getValue(f"attr_to_poison{self.suffix}") - getValue(f"steering_attr{self.suffix}"),
                -getValue(f"attr_to_poison{self.suffix}") + getValue(f"steering_attr{self.suffix}"),
            ), 10), -getValue(f"attr_to_poison{self.suffix}"))
            perception_food = util_functions.validate_dna(round(random.SystemRandom().uniform(
                getValue(f"perception_food{self.suffix}") - getValue(f"steering_perception{self.suffix}"),
                getValue(f"perception_food{self.suffix}") + getValue(f"steering_perception{self.suffix}")
            ), 10), getValue(f"perception_food{self.suffix}"), 'greater_than_zero')
            perception_poison = util_functions.validate_dna(round(random.SystemRandom().uniform(
                getValue(f"perception_poison{self.suffix}") - getValue(f"steering_perception{self.suffix}"),
                getValue(f"perception_poison{self.suffix}") + getValue(f"steering_perception{self.suffix}")
            ), 10), getValue(f"perception_poison{self.suffix}"), 'greater_than_zero')
            reproduction_rate = util_functions.validate_dna(round(random.SystemRandom().uniform(
                getValue(f"reproduction_rate{self.suffix}") - getValue(f"steering_reproduction_rate{self.suffix}"),
                getValue(f"reproduction_rate{self.suffix}") + getValue(f"steering_reproduction_rate{self.suffix}")
            ), 10), getValue(f"reproduction_rate{self.suffix}"), 'zero_and_above')
            mutation_rate = util_functions.validate_dna(round(random.SystemRandom().uniform(
                getValue(f"mutation_rate{self.suffix}") - getValue(f"steering_mutation_rate{self.suffix}"),
                getValue(f"mutation_rate{self.suffix}") + getValue(f"steering_mutation_rate{self.suffix}")
            ), 10), getValue(f"mutation_rate{self.suffix}"), 'zero_and_above')
            velocity = util_functions.validate_dna(round(random.SystemRandom().uniform(
                getValue(f"velocity{self.suffix}") - getValue(f"steering_velocity{self.suffix}"),
                getValue(f"velocity{self.suffix}") + getValue(f"steering_velocity{self.suffix}")
            ), 10), getValue(f"velocity{self.suffix}"), 'greater_than_zero')
            health = util_functions.validate_dna(round(random.SystemRandom().uniform(
                getValue(f"health{self.suffix}") - getValue(f"steering_health{self.suffix}"),
                getValue(f"health{self.suffix}") + getValue(f"steering_health{self.suffix}")
            ), 10), getValue(f"health{self.suffix}"), 'greater_than_zero')
            nutrition_food = util_functions.validate_dna(round(random.SystemRandom().uniform(
                getValue(f"nutrition_food{self.suffix}") - getValue(f"steering_nutrition{self.suffix}"),
                getValue(f"nutrition_food{self.suffix}") + getValue(f"steering_nutrition{self.suffix}")
            ), 10), getValue(f"nutrition_food{self.suffix}"), 'greater_than_zero')
            nutrition_poison = util_functions.validate_dna(round(random.SystemRandom().uniform(
                getValue(f"nutrition_poison{self.suffix}") - getValue(f"steering_nutrition{self.suffix}"),
                getValue(f"nutrition_poison{self.suffix}") + getValue(f"steering_nutrition{self.suffix}")
            ), 10), getValue(f"nutrition_poison{self.suffix}"), 'greater_than_zero')
            health_depletion = util_functions.validate_dna(round(random.SystemRandom().uniform(
                getValue(f"health_depletion{self.suffix}") - getValue(f"steering_depletion{self.suffix}"),
                getValue(f"health_depletion{self.suffix}") + getValue(f"steering_depletion{self.suffix}")
            ), 10), getValue(f"health_depletion{self.suffix}"), 'greater_than_zero')
            self.dna = [
                attr_to_food,
                attr_to_poison,
                perception_food,
                perception_poison,
                reproduction_rate,
                mutation_rate,
                velocity,
                health,
                nutrition_food,
                nutrition_poison,
                health_depletion,
            ]
        self.health = self.dna[7]
        for i, prop in enumerate(self.dna):
            stats.update(f"{dna_values[i]}{self.suffix}", prop, self.suffix, 'add')

    def update(self):
        # if bot has seen something acceleration will nudge it towards that item
        # if not acceleration is (0,0) and bot will just continue moving in it's current straight path
        self.step_movement += self.acceleration

        self.step_movement = util_functions.normalise(self.step_movement) * self.dna[6]
        self.position += self.step_movement
        self.acceleration *= 0
        # Every movement takes away health
        self.health -= self.dna[10]
        # Update color according to health
        self.colour = util_functions.lerp(self)
        # Aging :(
        self.age += 1

    def reproduce(self, bots):
        old_range = self.dna[7]
        new_range = (self.dna[4] / 10)
        normalized_health = (self.health * new_range) / old_range
        if random.SystemRandom().random() < (self.dna[4] + normalized_health):
            stats.update_bots(f'num{self.suffix}_bots', 'add')
            bots.append(BotClass(self.position[0], self.position[1], self.bot_type, self.dna))

    def dead(self):
        if self.health <= 0:
            stats.update_bots(f'num{self.suffix}_bots', 'remove')
            for i, prop in enumerate(self.dna):
                stats.update(f"{dna_values[i]}{self.suffix}", prop, self.suffix, 'remove')
        return self.health <= 0

    def apply_force(self, force):
        self.acceleration += force

    def be_eaten(self):
        self.health = 0

    def seek(self, target):
        desired_vel = numpy.add(target, -self.position)
        desired_vel = util_functions.normalise(desired_vel) * self.dna[6]
        # Get a velocity towards our object
        # Normalize it with current movement in order to get a smooth transition and return it
        steering_force = numpy.add(desired_vel, -self.step_movement)
        steering_force = util_functions.normalise(steering_force) * self.max_force
        return steering_force

    def eat(self, list_of_food_or_poison, index, remove_item):
        closest = None
        closest_distance = max(constants.game_width, constants.game_height)
        bot_x = self.position[0]
        bot_y = self.position[1]
        item_number = len(list_of_food_or_poison) - 1
        for food_or_poison in list_of_food_or_poison[::-1]:
            item_x = food_or_poison[0]
            item_y = food_or_poison[1]
            # #   Check first by x and y and then calculate hypot
            if abs(item_x - bot_x) < self.dna[2 + index] and abs(item_y - bot_y) < self.dna[2 + index]:
                #   If bot has something within it's view go towards it
                distance = math.hypot(bot_x - item_x, bot_y - item_y)
                if distance < 5:
                    # If it can catch it then eat it and remove it from foodstuffs
                    remove_item(item_number)
                    # Update to correct health according to the foodstuffs nutrition
                    if index == 0:
                        stats.update_foodstuffs('num_food', 'remove')
                        self.health += self.dna[8]
                        if self.health >= self.dna[7]:
                            self.health = self.dna[7]
                    if index == 1:
                        stats.update_foodstuffs('num_poison', 'remove')
                        self.health -= self.dna[9]
                if distance < closest_distance:
                    # Constantly check if there is a foodstuff that is closer
                    closest_distance = distance
                    closest = food_or_poison
            item_number -= 1
        return closest_distance, closest, index

    def seek_closest(self, closest_distance, closest, index):
        if closest_distance < self.dna[2 + index]:
            # Move towards closest foodstuff
            seek = self.seek(closest)  # index)
            seek *= self.dna[index]
            seek = util_functions.normalise(seek) * self.max_force
            self.apply_force(seek)

    def eat_bot(self, list_of_bots, index, edible_bot_type):
        closest = None
        closest_distance = max(constants.game_width, constants.game_height)
        bot_x = self.position[0]
        bot_y = self.position[1]
        for bot_food in list_of_bots:
            if bot_food == self or bot_food.bot_type != edible_bot_type:
                continue
            item_x = bot_food.position[0]
            item_y = bot_food.position[1]
            #   Check first by x and y and then calculate hyplot
            #   If bot has something within it's view go towards it
            if abs(item_x - bot_x) < self.dna[2 + index] and abs(item_y - bot_y) < self.dna[2 + index]:
                distance = math.hypot(bot_x - item_x, bot_y - item_y)
                if distance < 5:
                    # If it can catch it then eat it
                    self.health += self.dna[8]
                    if self.health >= self.dna[7]:
                        self.health = self.dna[7]
                    bot_food.be_eaten()
                    continue
                if distance < closest_distance:
                    # Constantly check if there is a bot that is closer
                    closest_distance = distance
                    closest = bot_food
        if closest_distance < self.dna[2 + index]:
            # Move towards closest bot
            seek = self.seek(closest.position)  # index)
            seek *= self.dna[index]
            seek = util_functions.normalise(seek) * self.max_force
            self.apply_force(seek)

    def boundaries(self):
        x_pos = self.position[0]
        y_pos = self.position[1]
        # Check all boundaries and steer bot away from them by the negative of the velocity (vector) that they have
        # come in from
        if x_pos < constants.boundary_size:
            desired = numpy.array([self.dna[6], self.step_movement[1]])
            steer = desired - self.step_movement
            steer = util_functions.normalise(steer) * self.max_force
            self.apply_force(steer)
        elif x_pos > constants.game_width - constants.boundary_size:
            desired = numpy.array([-self.dna[6], self.step_movement[1]])
            steer = desired - self.step_movement
            steer = util_functions.normalise(steer) * self.max_force
            self.apply_force(steer)
        if y_pos < constants.boundary_size:
            desired = numpy.array([self.step_movement[0], self.dna[6]])
            steer = desired - self.step_movement
            steer = util_functions.normalise(steer) * self.max_force
            self.apply_force(steer)
        elif y_pos > constants.game_height - constants.boundary_size:
            desired = numpy.array([self.step_movement[0], -self.dna[6]])
            steer = desired - self.step_movement
            steer = util_functions.normalise(steer) * self.max_force
            self.apply_force(steer)
        '''if desired != None:
            steer = desired-self.step_movement
            steer = normalise(steer)*self.max_force
            self.apply_force(steer)'''

    def check_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            distance = math.hypot(pos[0] - self.position[0], pos[1] - self.position[1])
            if distance < 10:
                return self.dna, self.position, self.health
            return

    def draw_bot(self, game_display):
        # Draw bot with different body by type
        bot_draw_type.draw_bot_by_type(self, game_display)
        num_c = stats.get_statistics('num_c_bots')[-1][-1] if stats.get_statistics('num_c_bots') else 0
        num_h = stats.get_statistics('num_h_bots')[-1][-1] if stats.get_statistics('num_h_bots') else 0
        if num_c + num_h < 500:
            # Draw circle for seeing green
            pygame.draw.circle(game_display, constants.green,
                               (int(self.position[0]), int(self.position[1])),
                               abs(int(self.dna[2])), 2)
            # Draw circle for seeing red
            if self.bot_type == 1:
                pygame.draw.circle(game_display, constants.red,
                                   (int(self.position[0]), int(self.position[1])), abs(int(self.dna[3])),
                                   2)
        # # Draw line for going towards green
        # pygame.draw.line(game_display, constants.green,
        #                  (int(self.position[0]), int(self.position[1])), (
        #                      int(self.position[0] + (self.step_movement[0] * self.dna[0] * 1000)),
        #                      int(self.position[1] + (self.step_movement[1] * self.dna[0] * 1000))), 3)
        # # Draw line for going towards red
        # pygame.draw.line(game_display, constants.red,
        #                  (int(self.position[0]), int(self.position[1])), (
        #                      int(self.position[0] + (self.step_movement[0] * self.dna[1] * 1000)),
        #                      int(self.position[1] + (self.step_movement[1] * self.dna[1] * 1000))), 2)
