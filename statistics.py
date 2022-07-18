from datetime import datetime
import matplotlib.dates as md


class Statistics:
    def __init__(self):
        self.num_c_bots = []
        self.num_h_bots = []
        self.num_food = []
        self.num_poison = []
        self.avg_attr_food_c = []
        self.avg_attr_food_h = []
        self.avg_attr_poison_h = []
        self.avg_perception_food_c = []
        self.avg_perception_food_h = []
        self.avg_perception_poison_h = []
        self.avg_repr_rate_c = []
        self.avg_repr_rate_h = []
        self.avg_mutation_rate_c = []
        self.avg_mutation_rate_h = []
        self.avg_velocity_c = []
        self.avg_velocity_h = []
        self.avg_health_c = []
        self.avg_health_h = []
        self.avg_nutrition_food_c = []
        self.avg_nutrition_food_h = []
        self.avg_nutrition_poison_h = []
        self.avg_health_depletion_c = []
        self.avg_health_depletion_h = []
        self.avg_age_h = []
        self.avg_age_c = []

    def update(self, var, value, suffix, action='add'):
        attr = getattr(self, f'avg_{var}', None)
        if attr is not None:
            stat_value = None
            latest_stat_value = attr[-1][1] if len(attr) != 0 else 0

            if suffix == '_c':
                num_bots = 0 if not self.num_c_bots else self.num_c_bots[-1][1]
            else:
                num_bots = 0 if not self.num_h_bots else self.num_h_bots[-1][1]
            if action == 'add':
                stat_value = 0 if num_bots == 0 else ((latest_stat_value * (num_bots - 1)) + value)/num_bots
            elif action == 'remove':
                stat_value = 0 if num_bots == 0 else ((latest_stat_value * (num_bots + 1)) - value)/num_bots
            dt = datetime.now()
            attr.append((md.date2num(dt), stat_value))
            setattr(self, f'avg_{var}', attr)

    def update_bots(self, var, action='add'):
        attr = getattr(self, var, 0)
        num_bots = 0 if not attr else attr[-1][1]
        dt = md.date2num(datetime.now())
        if action == 'add':
            attr.append((dt, num_bots + 1))
        else:
            attr.append((dt, num_bots - 1))
        setattr(self, var, attr)

    def update_age(self, var, value):
        attr = getattr(self, var, [])
        dt = md.date2num(datetime.now())
        attr.append((dt, value))
        setattr(self, var, attr)

    def update_foodstuffs(self, var, action='add'):
        attr = getattr(self, var, 0)
        num_foodstuffs = 0 if not attr else attr[-1][1]
        dt = md.date2num(datetime.now())
        if action == 'add':
            attr.append((dt, num_foodstuffs + 1))
        else:
            attr.append((dt, num_foodstuffs - 1))
        setattr(self, var, attr)

    def get_statistics(self, stat):
        return getattr(self, stat, [])


stats = Statistics()
