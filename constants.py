#  PYGAME constants
game_width = 1450
game_height = 800
fps = 30
boundary_size = 10
#   Color constants
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


class BotsValues:
    def __init__(self):
        # suffix _c is for carnivore bots
        # suffix _h is for herbivore bots
        # number of bots
        self.num_of_herbivore_bots = "10"
        self.num_of_carnivore_bots = "4"
        # attr_to_food - initial values for attraction to food for first gen of bots (not children)
        self.attr_to_food_c = "0.02"
        self.attr_to_food_h = "0.02"
        # attr_to_poison - initial values for attraction to poison for first gen of bots (not children)
        self.attr_to_poison_c = "0.0002"
        self.attr_to_poison_h = "0.0002"
        # steering_attr - range (from to) to change dna of mutated child (attracted to green/red)
        self.steering_attr_c = "0.001"
        self.steering_attr_h = "0.001"
        # perception_food - max values for food perception radius for first gen of bots (not children)
        self.perception_food_c = "100"
        self.perception_food_h = "100"
        # perception_poison - max values for poison perception radius for first gen of bots (not children)
        self.perception_poison_c = "100"
        self.perception_poison_h = "100"
        # steering_perception - range (from to) to change dna of mutated child (perception red/green)
        self.steering_perception_c = "30"
        self.steering_perception_h = "30"
        # reproduction_rate - chance of bot to reproduce
        self.reproduction_rate_c = "0.00025"
        self.reproduction_rate_h = "0.00025"
        # steering reproduction_rate - range to change dna of chance of bot to reproduce
        self.steering_reproduction_rate_c = "0.00001"
        self.steering_reproduction_rate_h = "0.00001"
        # mutation_rate - chance for child of parent to have a mutation
        self.mutation_rate_c = "0.15"
        self.mutation_rate_h = "0.15"
        # steering mutation_rate - range to change the chance for child of parent to have a mutation
        self.steering_mutation_rate_c = "0.01"
        self.steering_mutation_rate_h = "0.01"
        # velocity - constant that determines speed of bot
        self.velocity_c = "1.0"
        self.velocity_h = "0.8"
        # steering_velocity - range to change speed of bot
        self.steering_velocity_c = "0.01"
        self.steering_velocity_h = "0.01"
        # max health of bots
        self.health_c = "100"
        self.health_h = "100"
        # health - range to change health of bots
        self.steering_health_c = "5"
        self.steering_health_h = "5"
        # nutrition_food - impact on health eating bot/food will have
        self.nutrition_food_c = "20"
        self.nutrition_food_h = "20"
        # nutrition_poison - impact on health eating poison will have
        self.nutrition_poison_c = "80"
        self.nutrition_poison_h = "80"
        # steering_nutrition - range to change impact on health eating foodstuffs will have
        self.steering_nutrition_c = "1"
        self.steering_nutrition_h = "1"
        # health depletion - deplete some health every update
        self.health_depletion_c = "0.1"
        self.health_depletion_h = "0.1"
        # steering health depletion - range to change depletion of some health every update
        self.steering_depletion_c = "0.01"
        self.steering_depletion_h = "0.01"
        # Basic game constants
        self.max_food = "100"
        self.max_poison = "20"
        # Chance for foodstuff to be created
        self.food_chance = "0.1"
        self.poison_chance = "0.01"

    def set_attr(self, attr, value):
        try:
            setattr(self, attr, round(float(value), 10))
        except ValueError:
            print(f'Can not set attribute {attr} with value {value}')

    def get_attr(self, attr, number_type='FLOAT'):
        if number_type == 'INT':
            return int(getattr(self, attr, 0))
        if number_type == 'STR':
            return getattr(self, attr, 0)
        return round(float(getattr(self, attr, 0)), 10)

    def get_all_attr(self):
        return (
            (
                self.get_attr("num_of_herbivore_bots", "STR"),
                "num_of_herbivore_bots",
            ),
            (self.get_attr("attr_to_food_h", "STR"), "attr_to_food_h"),
            (self.get_attr("attr_to_poison_h", "STR"), "attr_to_poison_h"),
            (self.get_attr("steering_attr_h", "STR"), "steering_attr_h"),
            (self.get_attr("perception_food_h", "STR"), "perception_food_h"),
            (self.get_attr("perception_poison_h", "STR"), "perception_poison_h"),
            (
                self.get_attr("steering_perception_h", "STR"),
                "steering_perception_h",
            ),
            (self.get_attr("reproduction_rate_h", "STR"), "reproduction_rate_h"),
            (
                self.get_attr("steering_reproduction_rate_h", "STR"),
                "steering_reproduction_rate_h",
            ),
            (self.get_attr("mutation_rate_h", "STR"), "mutation_rate_h"),
            (
                self.get_attr("steering_mutation_rate_h", "STR"),
                "steering_mutation_rate_h",
            ),
            (self.get_attr("velocity_h", "STR"), "velocity_h"),
            (self.get_attr("steering_velocity_h", "STR"), "steering_velocity_h"),
            (self.get_attr("health_h", "STR"), "health_h"),
            (self.get_attr("steering_health_h", "STR"), "steering_health_h"),
            (self.get_attr("nutrition_food_h", "STR"), "nutrition_food_h"),
            (self.get_attr("nutrition_poison_h", "STR"), "nutrition_poison_h"),
            (self.get_attr("steering_nutrition_h", "STR"), "steering_nutrition_h"),
            (self.get_attr("health_depletion_h", "STR"), "health_depletion_h"),
            (self.get_attr("steering_depletion_h", "STR"), "steering_depletion_h"),
            (
                self.get_attr("num_of_carnivore_bots", "STR"),
                "num_of_carnivore_bots",
            ),
            (self.get_attr("attr_to_food_c", "STR"), "attr_to_food_c"),
            (self.get_attr("steering_attr_c", "STR"), "steering_attr_c"),
            (self.get_attr("perception_food_c", "STR"), "perception_food_c"),
            (
                self.get_attr("steering_perception_c", "STR"),
                "steering_perception_c",
            ),
            (self.get_attr("reproduction_rate_c", "STR"), "reproduction_rate_c"),
            (
                self.get_attr("steering_reproduction_rate_c", "STR"),
                "steering_reproduction_rate_c",
            ),
            (self.get_attr("mutation_rate_c", "STR"), "mutation_rate_c"),
            (
                self.get_attr("steering_mutation_rate_c", "STR"),
                "steering_mutation_rate_c",
            ),
            (self.get_attr("velocity_c", "STR"), "velocity_c"),
            (self.get_attr("steering_velocity_c", "STR"), "steering_velocity_c"),
            (self.get_attr("health_c", "STR"), "health_c"),
            (self.get_attr("steering_health_c", "STR"), "steering_health_c"),
            (self.get_attr("nutrition_food_c", "STR"), "nutrition_food_c"),
            (self.get_attr("steering_nutrition_c", "STR"), "steering_nutrition_c"),
            (self.get_attr("health_depletion_c", "STR"), "health_depletion_c"),
            (self.get_attr("steering_depletion_c", "STR"), "steering_depletion_c"),
            (self.get_attr("max_food", "STR"), "max_food"),
            (self.get_attr("max_poison", "STR"), "max_poison"),
            (self.get_attr("food_chance", "STR"), "food_chance"),
            (self.get_attr("poison_chance", "STR"), "poison_chance"),
        )


botsValues = BotsValues()
