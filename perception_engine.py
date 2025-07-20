class PerceptionEngine:
    @staticmethod
    def detect_nearby(player, others):
        px, py = player["position"]
        perception = player["stats"].get("perception", 5)
        hearing = player["stats"].get("hearing", 5)
        detected = []

        for other in others:
            if other["id"] == player["id"]:
                continue
            ox, oy = other["position"]
            dx = abs(ox - px)
            dy = abs(oy - py)
            distance = max(dx, dy)
            if 0 < distance <= 1:
                stealth = other["stats"].get("stealth", 3)
                if perception + hearing >= stealth * 2:
                    detected.append(other)
        return detected
