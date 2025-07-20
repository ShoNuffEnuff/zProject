class Item:
    def __init__(self, id, name, type_, effects=None, icon=None, rarity="common"):
        self.id = id
        self.name = name
        self.type = type_
        self.effects = effects or []
        self.icon = icon
        self.rarity = rarity

    def apply(self, player):
        if self.name == "Medkit":
            heal_amount = 10
            player["stats"]["health"] += heal_amount
            return f"{player['name']} healed {heal_amount} HP."
        return "Nothing happened."

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "effects": self.effects,
            "icon": self.icon,
            "rarity": self.rarity
        }

ITEM_REGISTRY = {
    "medkit": Item("medkit", "Medkit", "consumable", effects=["heal"], icon="/icons/medkit.png"),
}
