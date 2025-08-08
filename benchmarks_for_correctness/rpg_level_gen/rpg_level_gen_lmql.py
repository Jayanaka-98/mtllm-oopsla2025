import lmql
from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int


@dataclass
class Wall:
    start_pos: Position
    end_pos: Position


@dataclass
class Level:
    name: str
    difficulty: int
    width: int
    height: int
    num_wall: int
    num_enemies: int
    time_countdown: int
    n_retries_allowed: int


@dataclass
class Map:
    level: Level
    walls: list[Wall]
    small_obstacles: list[Position]
    enemies: list[Position]
    player_pos: Position


@lmql.query
def get_next_level(last_levels, difficulty, level_width, level_height):
    """lmql
    "Create the Next Level\n"
    "last_levels: {last_levels}\n"
    "difficulty: {difficulty}\n"
    "level_width: {level_width}\n"
    "level_height: {level_height}\n"
    "Structured: [NEXT_LEVEL]\n" where type(NEXT_LEVEL) is Level
    return NEXT_LEVEL
    """


@lmql.query
def get_map(map):
    """lmql
    "Get the map of the level\n"
    "map: {map}\n"
    "Structured: [MAP]\n" where type(MAP) is Map
    return MAP
    """


class LevelManager:
    current_level: int = 0
    current_difficulty: int = 1
    prev_levels: list[Level] = []
    prev_level_maps: list[Map] = []

    def get_next_level(self) -> tuple[Level, Map]:
        """Get the Next Level"""
        self.current_level += 1

        # Keeping Only the Last 3 Levels
        if len(self.prev_levels) > 3:
            self.prev_levels.pop(0)
            self.prev_level_maps.pop(0)

        # Generating the New Level
        new_level = get_next_level(
            last_levels=str(self.prev_levels),
            difficulty=self.current_difficulty,
            level_width=20,
            level_height=20,
        )
        print(new_level)
        self.prev_levels.append(new_level)

        # Generating the Map of the New Level
        new_level_map = get_map(str(new_level))
        print(new_level_map is None)
        self.prev_level_maps.append(new_level_map)

        # Increasing the Difficulty for end of every 2 Levels
        if self.current_level % 2 == 0:
            self.current_difficulty += 1

        return new_level, new_level_map


def get_map(map: Map) -> list[str]:
    """Get the map of the level"""
    map_tiles = [["." for _ in range(map.level.width)] for _ in range(map.level.height)]

    for wall in map.walls:
        for x in range(wall.start_pos.x, wall.end_pos.x + 1):
            for y in range(wall.start_pos.y, wall.end_pos.y + 1):
                map_tiles[y][x] = "B"

    for obs in map.small_obstacles:
        map_tiles[obs.y][obs.x] = "B"

    for enemy in map.enemies:
        map_tiles[enemy.y][enemy.x] = "E"

    map_tiles[map.player_pos.y][map.player_pos.x] = "P"
    map_tiles = [["B"] + row + ["B"] for row in map_tiles]
    map_tiles = (
        [["B" for _ in range(map.level.width + 2)]]
        + map_tiles
        + [["B" for _ in range(map.level.width + 2)]]
    )
    return ["".join(row) for row in map_tiles]


level_manager = LevelManager()
for _ in range(2):
    new_level, new_level_map = level_manager.get_next_level()
    print(new_level)
    print("\n".join(get_map(new_level_map)))