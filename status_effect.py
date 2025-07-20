class StatusEffect:
    def __init__(self, name, duration, apply_func):
        self.name = name
        self.duration = duration
        self.apply_func = apply_func

    def apply(self, target):
        return self.apply_func(target)
