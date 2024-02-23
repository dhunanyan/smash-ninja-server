from typing import List, Tuple, Dict

# GLOBAL
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
SCREEN_SCALE: int = 2
FPS: int = 60
RENDER_SCALE: float = 2.0
BASE_IMG_PATH: str = 'assets/images/'

BACKGROUND_SHADOWS_LIST = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# TILEMAP
NEIGHBOR_OFFSET: List[Tuple[int]] = [
  (-1, 0), (-1, -1), (0, -1),
  (1, 0), (0, 0), (0, 1),
  (-1, 1), (1, 1), (1, -1)
]
PHYSICS_TILE_TYPES = {"grass", "stone"}

# PHYSICS
Y_MAX_VELOCITY: int = 5

# PLAYER
PLAYER_DIM: Tuple[int] = (21, 25)
PLAYER_JUMPS: int = 2
PLAYER_WALL_JUMP_X: float = 3.5
PLAYER_WALL_JUMP_Y: float = -2.5
PLAYER_MAX_AIR_TIME: int = 120

# TILEMAP
AUTOTILE_NEIGHBORS: List[Tuple[int]] = [
  (1, 0), (-1, 0), (0, -1), (0, 1)
]
AUTOTILE_TYPES: set[str] = {"grass", "stone"}
AUTOTILE_MAP: Dict[Tuple[int, int], int] = {
  tuple(sorted([(1, 0), (0, 1)])): 0,
  tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
  tuple(sorted([(-1, 0), (0, 1)])): 2,
  tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
  tuple(sorted([(-1, 0), (0, -1)])): 4,
  tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
  tuple(sorted([(1, 0), (0, -1)])): 6,
  tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
  tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}