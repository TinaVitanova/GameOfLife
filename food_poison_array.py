class FoodArray:
    def __init__(self):
        self.food = []

    def add_food(self, *args):
        self.food.append(*args)

    def remove_food(self, index):
        self.food.pop(index)

    def get_food(self):
        return self.food


class PoisonArray:
    def __init__(self):
        self.poison = []

    def add_poison(self, *args):
        self.poison.append(*args)

    def remove_poison(self, index):
        self.poison.pop(index)

    def get_poison(self):
        return self.poison
