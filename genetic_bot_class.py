import pygame
import random
import math
import numpy
import bot_draw_type
import util_functions
import constants


class BotClass:
    def __init__(self, x, y, bot_type, dna=None, max_vel=constants.max_vel_const,
                 health=constants.health_const, mutation_rate=constants.mutation_rate_const,
                 steering_weights=constants.steering_weights_const,
                 perception_radius_mutation_range=constants.perception_radius_mutation_range_const,
                 initial_max_force=constants.initial_max_force_const,
                 initial_perception_radius=constants.initial_perception_radius_const,
                 reproduction_rate=constants.reproduction_rate_const, nutrition=constants.nutrition_const):
        self.position = numpy.array([x, y], dtype='float64')
        self.velocity = numpy.array([random.uniform(-max_vel, max_vel), random.uniform(-max_vel, max_vel)],
                                    dtype='float64')
        self.acceleration = numpy.array([0, 0], dtype='float64')
        self.colour = constants.green_const
        self.health = health
        self.max_vel = 2
        self.max_force = 0.5
        self.age = 1
        self.bot_type = bot_type
        self.reproduction_rate = reproduction_rate
        self.nutrition = nutrition

        # dna=[attracted to green, attracted to red, see green, see red]
        if dna:
            self.dna = []
            for dna_property in range(len(dna)):
                if random.random() < mutation_rate:
                    if dna_property < 2:
                        self.dna.append(dna[dna_property] + random.uniform(-steering_weights, steering_weights))
                    else:
                        self.dna.append(dna[dna_property] + random.uniform(-perception_radius_mutation_range,
                                                                           perception_radius_mutation_range))

                else:
                    self.dna.append(dna[dna_property])
        else:
            self.dna = [random.uniform(-initial_max_force, initial_max_force),
                        random.uniform(-initial_max_force, initial_max_force),
                        random.uniform(0, initial_perception_radius), random.uniform(0, initial_perception_radius)]
        # print(self.dna)

    def update(self):
        self.velocity += self.acceleration

        self.velocity = util_functions.normalise(self.velocity) * self.max_vel

        self.position += self.velocity
        self.acceleration *= 0
        self.health -= 0.2
        self.colour = util_functions.lerp(self)
        self.age += 1

    def reproduce(self, bots):
        if random.random() < self.reproduction_rate:
            bots.append(BotClass(self.position[0], self.position[1], 1, self.dna))

    def dead(self, food):
        if self.health > 0:
            return False
        else:
            if constants.game_width_const - constants.boundary_size_const > self.position[0] > \
                    constants.boundary_size_const and \
                    constants.game_height_const - constants.boundary_size_const > \
                    self.position[1] > constants.boundary_size_const:
                food.append(self.position)
            return True

    def apply_force(self, force):
        self.acceleration += force

    def be_eaten(self, ):
        self.health = 0

    def seek(self, target):
        desired_vel = numpy.add(target, -self.position)
        desired_vel = util_functions.normalise(desired_vel) * self.max_vel
        steering_force = numpy.add(desired_vel, -self.velocity)
        steering_force = util_functions.normalise(steering_force) * self.max_force
        return steering_force

    def seek_bot(self, target):
        desired_vel = numpy.add(target.position, -self.position)
        desired_vel = util_functions.normalise(desired_vel) * self.max_vel
        steering_force = numpy.add(desired_vel, -self.velocity)
        steering_force = util_functions.normalise(steering_force) * self.max_force
        return steering_force

    def eat(self, list_of_food_or_poison, index):
        closest = None
        closest_distance = max(constants.game_width_const, constants.game_height_const)
        bot_x = self.position[0]
        bot_y = self.position[1]
        item_number = len(list_of_food_or_poison) - 1
        for food_or_poison in list_of_food_or_poison[::-1]:
            item_x = food_or_poison[0]
            item_y = food_or_poison[1]
            distance = math.hypot(bot_x - item_x, bot_y - item_y)
            if distance < 5:
                list_of_food_or_poison.pop(item_number)
                self.health += self.nutrition[index]
            if distance < closest_distance:
                closest_distance = distance
                closest = food_or_poison
            item_number -= 1
        if closest_distance < self.dna[2 + index]:
            seek = self.seek(closest)  # index)
            seek *= self.dna[index]
            seek = util_functions.normalise(seek) * self.max_force
            self.apply_force(seek)

    def eat_bot(self, list_of_bots, index, edible_bot_type):
        closest = None
        closest_distance = max(constants.game_width_const, constants.game_height_const)
        # print('closest_distance')
        # print(closest_distance)
        bot_x = self.position[0]
        bot_y = self.position[1]
        for bot_food in list_of_bots:
            if bot_food == self:
                break
            # print('alllooo')
            # print(bot_food.position[0])
            # print(bot_food.position[1])
            item_x = bot_food.position[0]
            item_y = bot_food.position[1]
            distance = math.hypot(bot_x - item_x, bot_y - item_y)
            # print('distance')
            # print(distance)
            if distance < 5:
                if bot_food.bot_type != edible_bot_type:
                    break
                list_of_bots.remove(bot_food)
                self.health += self.nutrition[index]
                break
            if distance < closest_distance:
                # print('AHAAAA')
                if bot_food.bot_type != edible_bot_type:
                    # print('tuka?')
                    break
                closest_distance = distance
                closest = bot_food
        if closest_distance < self.dna[2 + index]:
            seek = self.seek_bot(closest)  # index)
            seek *= self.dna[index]
            seek = util_functions.normalise(seek) * self.max_force
            self.apply_force(seek)

    def boundaries(self):
        x_pos = self.position[0]
        y_pos = self.position[1]
        if x_pos < constants.boundary_size_const:
            desired = numpy.array([self.max_vel, self.velocity[1]])
            steer = desired - self.velocity
            steer = util_functions.normalise(steer) * self.max_force
            self.apply_force(steer)
        elif x_pos > constants.game_width_const - constants.boundary_size_const:
            desired = numpy.array([-self.max_vel, self.velocity[1]])
            steer = desired - self.velocity
            steer = util_functions.normalise(steer) * self.max_force
            self.apply_force(steer)
        if y_pos < constants.boundary_size_const:
            desired = numpy.array([self.velocity[0], self.max_vel])
            steer = desired - self.velocity
            steer = util_functions.normalise(steer) * self.max_force
            self.apply_force(steer)
        elif y_pos > constants.game_height_const - constants.boundary_size_const:
            desired = numpy.array([self.velocity[0], -self.max_vel])
            steer = desired - self.velocity
            steer = util_functions.normalise(steer) * self.max_force
            self.apply_force(steer)
        '''if desired != None:
            steer = desired-self.velocity
            steer = normalise(steer)*self.max_force
            self.apply_force(steer)'''

    def draw_bot(self, game_display):
        bot_draw_type.draw_bot_by_type(self, game_display)
        pygame.draw.circle(game_display, constants.green_const,
                           (int(self.position[0]), int(self.position[1])),
                           abs(int(self.dna[2])), abs(int(min(2, self.dna[2]))))
        pygame.draw.circle(game_display, constants.red_const,
                           (int(self.position[0]), int(self.position[1])), abs(int(self.dna[3])),
                           abs(int(min(2, self.dna[3]))))
        pygame.draw.line(game_display, constants.green_const,
                         (int(self.position[0]), int(self.position[1])), (
                             int(self.position[0] + (self.velocity[0] * self.dna[0] * 25)),
                             int(self.position[1] + (self.velocity[1] * self.dna[0] * 25))), 3)
        pygame.draw.line(game_display, constants.red_const,
                         (int(self.position[0]), int(self.position[1])), (
                             int(self.position[0] + (self.velocity[0] * self.dna[1] * 25)),
                             int(self.position[1] + (self.velocity[1] * self.dna[1] * 25))), 2)
