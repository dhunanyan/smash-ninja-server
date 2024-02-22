import os
import pygame

from typing import List

from config.constants import BASE_IMG_PATH

ImageType = pygame.Surface
ImagesType = List[ImageType]

def load_image(path: str) -> ImageType:
  img = pygame.image.load(BASE_IMG_PATH + path).convert()
  img.set_colorkey((0, 0, 0))
  
  return img

def load_images(path: str) -> ImagesType:
  images = []
  for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
    images.append(load_image(path + '/' + img_name))
  return images

class Animation:
  def __init__(self, images: ImagesType, img_dur: int = 5, loop: bool = True) -> None:
    self.images = images
    self.loop: bool = loop
    self.img_duration: int = img_dur
    self.done: bool = False
    self.frame: int = 0
    
  def copy(self) -> 'Animation':
    return Animation(self.images, self.img_duration, self.loop)
  
  def update(self) -> None:
    if self.loop:
      self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
    else:
      self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
      if self.frame >= self.img_duration * len(self.images) - 1:
        self.done = True
  
  def img(self) -> ImageType:
    return self.images[int(self.frame / self.img_duration)]
