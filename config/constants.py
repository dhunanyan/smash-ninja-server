# GLOBAL
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_SCALE = 2
FPS = 60
BASE_IMG_PATH = 'assets/images/'

BACKGROUND_SHADOWS_LIST = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# TILEMAP
NEIGHBOR_OFFSET = [(-1, 0), (-1, -1), (0, -1), 
                   (1, 0), (0, 0), (0, 1),
                   (-1, 1), (1, 1), (1, -1)]
PHYSICS_TILE_TYPES = {"grass", "stone"}

AUTOTILE_NEIGHBORS = [(1, 0), (-1, 0), (0, -1), (0, 1)]
AUTOTILE_TYPES = {"grass", "stone"}
AUTOTILE_MAP = {
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