bots = []


def add_bots(*args):
    bots.append(*args)


def get_bots():
    return bots


def reset_bots():
    global bots
    bots = []
    return bots


def get_bots_by_type(bot_type):
    return [bot for bot in bots if bot.bot_type == bot_type]
