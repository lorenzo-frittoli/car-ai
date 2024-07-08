from dataclasses import dataclass


# RUST MOMENT
class Game:
    pass


class MapMaker:
    pass


@dataclass
class GameState:
    state: Game | MapMaker


# CONSTANTS
FPS = 60
DISPLAY_SIZE = (700, 700)
NET_SIZE = (1, 1)
BACKGROUND_COLOR = "white"
MAP_FILE = "map.json"

# VARIABLES
game_state: GameState = GameState(Game())
running: bool = True
