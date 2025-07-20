import random
from item import ITEM_REGISTRY

class CombatEngine:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.log = []

    def apply_status_effects(self, actor):
        if "poison" in actor.get("effects", []):
            actor["stats"]["health"] -= 2
            self.log.append(f"{actor['name']} takes 2 poison damage.")

    def resolve_turn(self):
        p_speed = self.player["stats"].get("speed", 5)
        e_speed = self.enemy["stats"].get("speed", 5)

        self.apply_status_effects(self.player)
        self.apply_status_effects(self.enemy)

        if p_speed >= e_speed:
            self.attack(self.player, self.enemy)
            if self.enemy["stats"]["health"] > 0:
                self.attack(self.enemy, self.player)
        else:
            self.attack(self.enemy, self.player)
            if self.player["stats"]["health"] > 0:
                self.attack(self.player, self.enemy)

        return {
            "player": self.player,
            "enemy": self.enemy,
            "log": self.log
        }

    def attack(self, attacker, defender):
        atk = attacker["stats"].get("attack", 5)
        defn = defender["stats"].get("defense", 3)
        bonus = 0

        # Check for items
        for item_id in attacker.get("inventory", []):
            item = ITEM_REGISTRY.get(item_id)
            if item and "+2 damage" in item.effects:
                bonus += 2

        damage = max(1, atk + bonus - defn)
        defender["stats"]["health"] -= damage
        self.log.append(f"{attacker['name']} deals {damage} damage to {defender['name']}.")

    def run_combat_loop(self):
        while self.player["stats"]["health"] > 0 and self.enemy["stats"]["health"] > 0:
            result = self.resolve_turn()
            if self.player["stats"]["health"] <= 0 or self.enemy["stats"]["health"] <= 0:
                break
        return result

    def attempt_retreat(self):
        self.log.append(f"{self.player['name']} attempts to retreat...")
        if random.random() < 0.5:
            self.log.append("Retreat successful.")
            self.enemy["stats"]["health"] = -999
        else:
            self.log.append("Retreat failed.")
