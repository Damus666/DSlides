import pygame, os

class Renderer:
    def __init__(self,outputfolder):
        pygame.init()
        self.screen = None
        self.w = 0
        self.h = 0
        self.slides = list()
        self.finals = list()
        self.output_name = ""
        self.outputfolder = outputfolder
        
    def set_size(self,size):
        self.screen = pygame.Surface(size)
        self.screen.fill("black")
        self.w = size[0]
        self.h = size[1]
        
    def render(self):
        i = 0
        self.finals.clear()
        for slide in self.slides:
            self.screen.fill("black")
            slide.render(self.screen)
            self.finals.append(self.screen.copy())
            i += 1
    
    def save(self):
        i = 0
        for fil in os.listdir(self.outputfolder):
            try:
                os.remove(self.outputfolder+"/"+fil)
            except:
                pass
        for final in self.finals:
            pygame.image.save(final,self.outputfolder+"/"+str(i)+".png")
            i += 1