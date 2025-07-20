class Monster:
    def __init__(self, id, name, stats, abilities=None):
        self.id = id
        self.name = name
        self.stats = stats
        self.abilities = abilities or []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "stats": self.stats,
            "abilities": self.abilities
        }
