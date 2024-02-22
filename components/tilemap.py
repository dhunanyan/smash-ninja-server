import json
import pygame

from typing import List, Tuple, Dict, Union, Optional, cast
from game import Game

from config.constants import NEIGHBOR_OFFSET, PHYSICS_TILE_TYPES, AUTOTILE_NEIGHBORS, AUTOTILE_TYPES, AUTOTILE_MAP

TileType = Dict[str, Union[str, int, List[int]]]
TilesType = List[TileType]
TilemapType = Dict[str, TileType]
IdPairsType = List[Tuple[str, int]]

class Tilemap:
  def __init__(self, game: Game, tile_size: int = 16) -> None:
    self.game: Game = game
    self.tile_size: int = tile_size
    self.tilemap: TilemapType = {}
    self.offgrid_tiles: TilesType = []
    
  #  Keep actually keeps the spawner in tilemap - without keep we just get the pos
  def extract(self, id_pairs: IdPairsType, keep=False) -> TilesType:
    matches: TilesType = []
    for tile in self.offgrid_tiles.copy():
      if (tile['type'], tile['variant']) in id_pairs:
        matches.append(tile.copy())
        if not keep:
          self.offgrid_tiles.remove(tile)

    for loc in self.tilemap.copy():
      tile = self.tilemap[loc]
      if (tile['type'], tile['variant']) in id_pairs:
        matches.append(tile.copy())
        matches[-1]['pos'] = matches[-1]['pos'].copy()
        matches[-1]['pos'][0] *= self.tile_size
        matches[-1]['pos'][1] *= self.tile_size
        if not keep:
          del self.tilemap[loc]
          
    return matches

  def tiles_around(self, pos: List[int]) -> TilesType:
    tiles: TilesType = []
    tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
    for offset in NEIGHBOR_OFFSET:
      check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
      if check_loc in self.tilemap:
        tiles.append(self.tilemap[check_loc])
    return tiles
  
  def save(self, path: str) -> None:
    f = open(path, 'w')
    json.dump({
      'tilemap': self.tilemap,
      'tile_size': self.tile_size,
      "offgrid": self.offgrid_tiles
    }, f)
    f.close()
    
  def load(self, path) -> None:
    f = open(path, 'r')
    map_data = json.load(f)
    f.close()
    
    self.tilemap = cast(TilemapType, map_data['tilemap'])
    self.offgrid_tiles = cast(TilesType, map_data['offgrid'])
    self.tile_size = int(map_data['tile_size'])
    
  def solid_check(self, pos: List[int]) -> Optional[TileType]:
    tile_loc = str(int(pos[0] // self.tile_size)) + ';' + str(int(pos[1] // self.tile_size))
    if tile_loc in self.tilemap:
      if self.tilemap[tile_loc]['type'] in PHYSICS_TILE_TYPES:
        return self.tilemap[tile_loc]
    
  def physics_rects_around(self, pos: List[int]) -> List[pygame.Rect]:
    rects: List[pygame.Rect] = []
    for tile in self.tiles_around(pos):
      if tile['type'] in PHYSICS_TILE_TYPES:
        rects.append(pygame.Rect(
          tile['pos'][0] * self.tile_size, 
          tile['pos'][1] * self.tile_size, 
          self.tile_size, 
          self.tile_size))
    return rects
    
  def autotile(self) -> None:
    for loc in self.tilemap:
      tile = self.tilemap[loc]
      neighbors = set()
      
      for shift in AUTOTILE_NEIGHBORS:
        check_loc = str(tile['pos'][0] + shift[0]) + ";" + str(tile['pos'][1] + shift[1])
        if check_loc in self.tilemap:
          if self.tilemap[check_loc]['type'] == tile['type']:
            neighbors.add(shift)
            
      neighbors = tuple(sorted(neighbors))
      if (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
        tile['variant'] = AUTOTILE_MAP[neighbors]
  
  def render(self, surf: pygame.Surface, offset: Tuple[int] = (0, 0)) -> None:
    for tile in self.offgrid_tiles:
      surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
      
    for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
      for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
         loc = str(x) + ';' + str(y)
         if loc in self.tilemap:
           tile = self.tilemap[loc]
           surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
