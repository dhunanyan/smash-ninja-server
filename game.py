import sys
import random
import pygame

from components.tilemap import Tilemap
from components.player import Player

from config.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_SCALE, BACKGROUND_SHADOWS_LIST, FPS, PLAYER_DIM, RENDER_SCALE
from config.utils import Animation, load_image, load_images

class Game:
  def __init__(self) -> None:
    pygame.init()
    pygame.display.set_caption("Smash Royal")
    
    self.screen = pygame.display.set_mode((
      SCREEN_WIDTH,
      SCREEN_HEIGHT
    ))
    self.display = pygame.Surface((
      SCREEN_WIDTH / SCREEN_SCALE,
      SCREEN_HEIGHT / SCREEN_SCALE
    ), pygame.SRCALPHA)
    self.display_2 = pygame.Surface((
      SCREEN_WIDTH / SCREEN_SCALE,
      SCREEN_HEIGHT / SCREEN_SCALE
    ))
    
    self.clock = pygame.time.Clock()
    self.movement = [False, False]
    
    self.tilemap = Tilemap(self, tile_size=16)
    
    self.assets = {
      "icon": load_image('icon.png'),
      "background": load_image('background.jpg'),
      
      "player/idle": Animation(load_images('entities/player/idle'), img_dur=5),
      "player/run": Animation(load_images('entities/player/run'), img_dur=4),
      "player/jump": Animation(load_images('entities/player/jump')),
      "player/attack": Animation(load_images('entities/player/attack'), img_dur=3),
      "player/dead": Animation(load_images('entities/player/dead'), img_dur=3),
      "player/door-in": Animation(load_images('entities/player/door-in'), img_dur=5),
      "player/door-out": Animation(load_images('entities/player/door-out'), img_dur=5),
    }
    pygame.display.set_icon(self.assets['icon'])
    
    player_pos = (50, 50)
    self.player = Player(self, player_pos, PLAYER_DIM)
    
    self.screenshake = 0
    self.load_level()
      
  def load_level(self) -> None:
    spawners = self.tilemap.extract([
      ('spawners', 0)
    ])
    for spawner in spawners:
      if spawner['variant'] == 0:
        self.player.pos = spawner['pos']
        self.player.air_time = 0
    
    self.scroll = [0, 0]
    self.background_image = pygame.transform.scale(
      self.assets['background'], (
        SCREEN_WIDTH / SCREEN_SCALE,
        SCREEN_HEIGHT / SCREEN_SCALE
      )
    )
  
  def run(self) -> None:
    while True:
      self.display.fill((0, 0, 0, 0))
      self.display_2.blit(self.background_image, (0, 0))
      self.screenshake = max(0, self.screenshake - 1)
      
      self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / RENDER_SCALE - self.scroll[0]) / 30
      self.scroll[1] += (self.player.rect().centery - self.display.get_height() / RENDER_SCALE - self.scroll[1]) / 30
      render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
      
      display_mask = pygame.mask.from_surface(self.display)
      display_sillhouette = display_mask.to_surface(
        setcolor=(0, 0, 0, 180),
        unsetcolor=(0, 0, 0, 0)
      )
      
      self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
      self.player.render(self.display, offset=render_scroll)
      
      for offset in BACKGROUND_SHADOWS_LIST:
        self.display_2.blit(display_sillhouette, offset)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_a:
            self.movement[0] = True
          if event.key == pygame.K_d:
            self.movement[1] = True
          if event.key == pygame.K_w:
            self.player.jump()
          if event.key == pygame.K_s:
            self.player.velocity[1] = 3
        if event.type == pygame.KEYUP:
          if event.key == pygame.K_a:
            self.movement[0] = False
          if event.key == pygame.K_d:
            self.movement[1] = False

      self.display_2.blit(self.display, (0, 0))

      screen_shake_offset = (
        random.random() * self.screenshake - self.screenshake / 2,
        random.random() * self.screenshake - self.screenshake / 2
      )
      self.screen.blit(pygame.transform.scale(
        self.display_2, self.screen.get_size()
      ), screen_shake_offset)
      pygame.display.update()
      self.clock.tick(FPS)

Game().run()
