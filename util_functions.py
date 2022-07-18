import constants


def magnitude_calc(vector):
    x = sum(index ** 2 for index in vector)
    return x ** 0.5


def normalise(vector):
    magnitude = magnitude_calc(vector)
    if magnitude != 0:
        vector = vector / magnitude
    return vector


def lerp(bot):
    # Change color of bot according to it's health
    percent_health = bot.health / constants.botsValues.get_attr("health" + bot.suffix)
    return (
        int(max(min((1 - percent_health) * 255, 255), 0)),
        int(max(min(percent_health * 255, 255), 0)),
        0,
    )


def validate_dna(new_value, old_value, validation=''):
    if validation == 'greater_than_zero':
        return new_value if new_value > 0 else old_value
    if validation == 'zero_or_above:':
        return new_value if new_value >= 0 else old_value
    return new_value


def get_plot_values(plot_data):
    x_val = [x[0] for x in plot_data]
    y_val = [x[1] for x in plot_data]
    return x_val, y_val


def are_array_values_increasing(arr):
    # Calculating length
    n = len(arr)

    # Array has one or no element or the
    # rest are already checked and approved.
    if n == 1 or n == 0:
        return True

    # Recursion applied till last element
    return arr[0] < arr[1] and are_array_values_increasing(arr[1:])
