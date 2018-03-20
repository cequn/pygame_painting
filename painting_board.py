# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import math
from tkinter import Tk
from tkinter import filedialog
import os

Tk().withdraw()
FPS = 60
width = 800
height = 600
class Brush:
  def __init__(self, screen):
    self.screen = screen
    self.color = (0, 0, 0)
    self.size = 1
    self.drawing = False
    self.last_pos = None
    self.style = True
    self.brush = pygame.image.load("images/brush.png").convert_alpha()
    self.brush_now = self.brush.subsurface((0, 0), (1, 1)) 
  def start_draw(self, pos):
    self.drawing = True
    self.last_pos = pos 
  def end_draw(self):
    self.drawing = False
  def set_brush_style(self, style):
    print("* set brush style to", style)
    self.style = style 
  def get_brush_style(self):
    return self.style 
  def get_current_brush(self):
    return self.brush_now 
  def set_size(self, size):
    if size < 1:
      size = 1
    elif size > 32:
      size = 32
    print("* set brush size to", size)
    self.size = size
    self.brush_now = self.brush.subsurface((0, 0), (size*2, size*2)) 
  def get_size(self):
    return self.size 
  def set_color(self, color):
    self.color = color
    for i in range(self.brush.get_width()):
      for j in range(self.brush.get_height()):
        self.brush.set_at((i, j),
                 color + (self.brush.get_at((i, j)).a,)) 
  def get_color(self):
    return self.color 
  def draw(self, pos, canvas):
    if self.drawing:
      for p in self._get_points(pos):
        #因为换了个surface，position要是相对位置
        new_p = (p[0]-180,p[1]-25) 
        if self.style:
          canvas.blit(self.brush_now, new_p)
        else:         
          pygame.draw.circle(canvas, self.color, new_p, self.size)
    self.last_pos = pos

  def _get_points(self, pos):
    points = [(self.last_pos[0], self.last_pos[1])]
    len_x = pos[0] - self.last_pos[0]
    len_y = pos[1] - self.last_pos[1]
    length = math.sqrt(len_x**2 + len_y**2)
    step_x = len_x / length
    step_y = len_y / length
    for i in range(int(length)):
      points.append((points[-1][0] + step_x, points[-1][1] + step_y))
    points = map(lambda x: (int(0.5 + x[0]), int(0.5 + x[1])), points)
    return list(set(points)) 

class Menu:
  def __init__(self, screen):
    self.screen = screen
    self.brush = None
    self.colors = [
      (0xff, 0x00, 0xff), (0x80, 0x00, 0x80),
      (0x00, 0x00, 0xff), (0x00, 0x00, 0x80),
      (0x00, 0xff, 0xff), (0x00, 0x80, 0x80),
      (0x00, 0xff, 0x00), (0x00, 0x80, 0x00),
      (0xff, 0xff, 0x00), (0x80, 0x80, 0x00),
      (0xff, 0x00, 0x00), (0x80, 0x00, 0x00),
      (0xc0, 0xc0, 0xc0), (0xff, 0xff, 0xff),
      (0x00, 0x00, 0x00), (0x80, 0x80, 0x80),
    ]
    self.colors_rect = []
    for (i, rgb) in enumerate(self.colors):
      rect = pygame.Rect(10 + i % 2 * 32, 200 + i / 2 * 32, 32, 32)
      self.colors_rect.append(rect)
    self.pens = pygame.image.load("images/pen1.png").convert_alpha()
    self.pens_rect = pygame.Rect(10, 10, 64, 64)
    self.sizes = [
      pygame.image.load("images/big.png").convert_alpha(),
      pygame.image.load("images/small.png").convert_alpha()
    ]
    self.sizes_rect = []
    for (i, img) in enumerate(self.sizes):
      rect = pygame.Rect(10 + i * 32, 74, 32, 32)
      self.sizes_rect.append(rect)
    self.save_btn = pygame.image.load("images/save.png").convert_alpha()
    self.cancel_btn = pygame.image.load("images/cancel.png").convert_alpha()
    self.save_btn_rect = pygame.Rect(10, 500, 64, 32)
    self.cancel_btn_rect = pygame.Rect(10, 500 + 40, 64, 32)
    self.edit_area = pygame.Surface((550,550))
    self.edit_area.fill((255, 255, 255))

  def set_brush(self, brush):
    self.brush = brush
  
  def draw(self):
    self.screen.blit(self.pens, self.pens_rect)
    for (i, img) in enumerate(self.sizes):
      self.screen.blit(img, self.sizes_rect[i])
    self.screen.fill((255, 255, 255), (10, 116, 64, 64))
    pygame.draw.rect(self.screen, (0, 0, 0), (10, 116, 64, 64), 1)
    size = self.brush.get_size()
    x = 10 + 32
    y = 116 + 32
    pygame.draw.circle(self.screen,
                self.brush.get_color(), (x, y), size)
    for (i, rgb) in enumerate(self.colors):
      pygame.draw.rect(self.screen, rgb, self.colors_rect[i])
    self.screen.blit(self.save_btn,self.save_btn_rect)
    self.screen.blit(self.cancel_btn,self.cancel_btn_rect)
    self.screen.blit(self.edit_area,(180,25))
  def get_area(self):
    return self.edit_area
  def save_img(self):
    filename = filedialog.asksaveasfilename(initialdir = os.getcwd(),title = "保存文件",
                  defaultextension='.bmp',filetypes=[("BMP files",'*.bmp'),("JPG files",'*.jpg')])
    pygame.image.save(self.edit_area, filename)
  def click_button(self, pos):
    if self.pens_rect.collidepoint(pos):
      self.brush.set_brush_style(bool(0))
      return True
    for (i, rect) in enumerate(self.sizes_rect):
      if rect.collidepoint(pos):
        if i:
          self.brush.set_size(self.brush.get_size() - 1)
        else:
          self.brush.set_size(self.brush.get_size() + 1)
        return True
    for (i, rect) in enumerate(self.colors_rect):
      if rect.collidepoint(pos):
        self.brush.set_color(self.colors[i])
        return True
    if self.cancel_btn_rect.collidepoint(pos):
      self.edit_area.fill((255,255,255))
      return True
    if self.save_btn_rect.collidepoint(pos):
      self.save_img()
      return True
    return False

class Painter:
  def __init__(self):
    self.screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("画板--Alldream")
    self.clock = pygame.time.Clock()
    self.brush = Brush(self.screen)
    self.menu = Menu(self.screen)
    self.menu.set_brush(self.brush)

  def run(self):
    self.screen.fill((200, 200, 200))
    while True:
      self.clock.tick(FPS)
      for event in pygame.event.get():
        if event.type == QUIT:
          return
        elif event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            self.menu.get_area().fill((255, 255, 255))
          elif event.key == K_s:
            self.menu.save_img()
        elif event.type == MOUSEBUTTONDOWN:
          if (event.pos[0] < 180 or event.pos[0] > 730 or event.pos[1] > 575 or event.pos[1] < 25) and self.menu.click_button(event.pos):
            pass
          else:
            self.brush.start_draw(event.pos)
        elif event.type == MOUSEMOTION:
          self.brush.draw(event.pos,self.menu.get_area())
        elif event.type == MOUSEBUTTONUP:
          self.brush.end_draw()
      self.menu.draw()
      pygame.display.update()
def main():
  app = Painter()
  app.run()
  
if __name__ == '__main__':
  main()