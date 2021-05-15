import constants


def magnitude_calc(vector):
    x = 0
    for index in vector:
        x += index ** 2
    magnitude = x ** 0.5
    return magnitude


def normalise(vector):
    magnitude = magnitude_calc(vector)
    if magnitude != 0:
        vector = vector / magnitude
    return vector


def lerp(bot):
    percent_health = bot.health / constants.health_const
    lerped_colour = (max(min((1 - percent_health) * 255, 255), 0), max(min(percent_health * 255, 255), 0), 0)
    return lerped_colour
