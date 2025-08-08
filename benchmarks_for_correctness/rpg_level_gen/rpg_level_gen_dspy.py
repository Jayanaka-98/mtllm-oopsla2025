import dspy
from pydantic import BaseModel, Field
from typing import List


llm = dspy.LM('openai/gpt-4o', cache=False, )
dspy.settings.configure(lm=llm)


class Position(BaseModel):
    x: int = Field(description="X Coordinate")
    y: int = Field(description="Y Coordinate")


class Wall(BaseModel):
    start_pos: Position = Field(description="Start Position of the Wall")
    end_pos: Position = Field(description="End Position of the Wall")


class Level(BaseModel):
    name: str = Field(description="Name of the Level")
    difficulty: int = Field(description="Difficulty of the Level")
    width: int = Field(description="Width of the Map")
    height: int = Field(description="Height of the Map")
    num_wall: int = Field(description="Number of Walls in the Map")
    num_enemies: int = Field(description="Number of Enemies in the Map")
    time_countdown: int = Field(description="Time Countdown of the Level")
    n_retries_allowed: int = Field(description="Number of Retries Allowed")


class Map(BaseModel):
    level: Level = Field(description="Level of the Map")
    walls: list[Wall] = Field(description="Walls in the Map Other than Edges")
    small_obstacles: List[Position] = Field(description="Obstacles in the Map")
    enemies: list[Position] = Field(description="Enemies in the Map")
    player_pos: Position = Field(description="Player Position in the Map")


class CreateNextLevel(dspy.Signature):
    """Create Next Level"""

    last_levels: list[Level] = dspy.InputField(desc="Last Played Levels")
    difficulty: int = dspy.InputField(desc="Difficulty of the New Level")
    level_width: int = dspy.InputField(desc="Width of the Level")
    level_height: int = dspy.InputField(desc="Height of the Level")
    next_level: Level = dspy.OutputField(desc="Next Level")


class CreateMap(dspy.Signature):
    """Create Map for the Level"""

    level: Level = dspy.InputField(desc="Level")
    map: Map = dspy.OutputField(desc="Map")


class LevelManager:
    current_level: int = 0
    current_difficulty: int = 1
    prev_levels: List[Level] = []
    prev_level_maps: List[Map] = []

    def get_next_level(self) -> tuple[Level, Map]:
        """Get the Next Level"""
        self.current_level += 1

        # Keeping Only the Last 3 Levels
        if len(self.prev_levels) > 3:
            self.prev_levels.pop(0)
            self.prev_level_maps.pop(0)

        # Generating the New Level
        new_level = dspy.TypedPredictor(CreateNextLevel)(
            last_levels=self.prev_levels,
            difficulty=self.current_difficulty,
            level_width=20,
            level_height=20,
        ).next_level
        self.prev_levels.append(new_level)

        # Generating the Map of the New Level
        new_level_map = dspy.TypedPredictor(CreateMap)(level=new_level).map
        self.prev_level_maps.append(new_level_map)

        # Increasing the Difficulty for end of every 2 Levels
        if self.current_level % 2 == 0:
            self.current_difficulty += 1

        return new_level, new_level_map


def get_map(map: Map) -> List[str]:
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
