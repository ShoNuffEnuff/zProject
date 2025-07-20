class MovementEngine:
    def __init__(self, player_position, map_grid):
        self.player_position = player_position
        self.map_grid = map_grid

    def move_player(self, direction):
        x, y = self.player_position
        if direction == "up":
            y -= 1
        elif direction == "down":
            y += 1
        elif direction == "left":
            x -= 1
        elif direction == "right":
            x += 1

        if 0 <= x < len(self.map_grid[0]) and 0 <= y < len(self.map_grid):
            self.player_position = (x, y)
            tile = self.map_grid[y][x]
            if not tile["flipped"]:
                tile["flipped"] = True
            return self.player_position, tile
        else:
            return self.player_position, None
