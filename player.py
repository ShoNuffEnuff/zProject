class Player:
    def __init__(self, id, name, position, stats, effects=None, inventory=None):
        self.id = id
        self.name = name
        self.position = position  # (x, y)
        self.stats = stats        # e.g., {"health": 50, "stealth": 3}
        self.effects = effects or []
        self.inventory = inventory or []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "position": self.position,
            "stats": self.stats,
            "effects": self.effects,
            "inventory": self.inventory
        }
