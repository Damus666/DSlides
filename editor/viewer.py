from pygameUI import pygameUI
from .settings import *
import pygame

class Viewer:
    def __init__(self,editor):
        self.editor = editor
        self.images = list()
        self.current = None
        self.index = 0
    
    def reset(self,images):
        self.index = 0
        self.images.clear()
        for img in images:
            d = img.get_width()/W
            h = img.get_height()/d
            if h > H:
                h = H
            self.images.append(pygame.transform.scale(img,(W,h)))
        if len(images) > 0:
            self.current = self.images[self.index]
        else:
            self.editor.to_menu()
        
    def event(self,e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RIGHT or e.key == pygame.K_SPACE:
                if self.index < len(self.images)-1:
                    self.index += 1
                    self.current = self.images[self.index]
            elif e.key == pygame.K_LEFT:
                if self.index > 0:
                    self.index -= 1
                    self.current = self.images[self.index]
            elif e.key == pygame.K_ESCAPE or e.key == pygame.K_RETURN:
                self.editor.to_menu()
                del self
    
    def draw(self,surface):
        surface.blit(self.current,(0,0))