import pygame,sys,os
from pygameUI import pygameUI
from .settings import *
from .menu import Menu
from .presentation import Presentation
from .viewer import Viewer

class Editor:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZES)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("DSlides Editor")
        self.menu_manager = pygameUI.UIManager(SIZES,False,settings=MENU_SETTINGS)
        self.manager = pygameUI.UIManager(SIZES,False,settings=EDITOR_SETTINGS)
        self.bg_color = (20,20,20)
        self.status = 0
        self.menu = Menu(self.menu_manager,self)
        self.viewer = Viewer(self)
        self.current_presentation = None
        #self.load_presentation("TestPresentation")
        
    def load_presentation(self,name):
        self.status = 1
        self.current_presentation = Presentation(self.manager,self,name)
        
    def to_menu(self):
        self.status = 0
        self.current_presentation = None
        
    def view(self,name):
        self.status = 2
        temp = Presentation(self.manager,self,name)
        self.viewer.reset(temp.converter.renderer.finals)
        temp.destroy_all()
        del temp
    
    def load(self):
        found = list()
        files = os.listdir(PRESENTATIONS_FOLDER)
        for file in files:
            if "." not in file:
                found.append(file)
        self.menu.load(found)
        
    def create_new(self,name,current):
        created = False
        if name.strip() not in current:
            try:
                name = name.strip()
                if not os.path.exists(PRESENTATIONS_FOLDER+"/"+name):
                    os.mkdir(PRESENTATIONS_FOLDER+"/"+name)
                with open(PRESENTATIONS_FOLDER+"/"+name+"/"+"save.ds","w") as file:
                    file.write(NEW_STARTING_CONTENT.replace("P_NAME",name))
                if not os.path.exists(PRESENTATIONS_FOLDER+"/"+name+"/"+"output"):
                    os.mkdir(PRESENTATIONS_FOLDER+"/"+name+"/"+"output")
                created = True
            except Exception as e:
                print(f"Error while creating presentation: {e}")
        return created
    
    def save(self):
        if self.current_presentation:
            self.current_presentation.save()
    
    def events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.save()
                self.quit()
            if self.status == 0:
                self.menu_manager.handle_events(e)
                self.menu.event(e)
            elif self.status == 1:
                self.manager.handle_events(e)
                if self.current_presentation:
                    self.current_presentation.event(e)
            else:
                self.viewer.event(e)
    
    def draw(self):
        self.screen.fill(self.bg_color)
        if self.status == 0:
            self.menu_manager.draw_ui(self.screen)
        elif self.status == 1:
            self.manager.draw_ui(self.screen)
        else:
            self.viewer.draw(self.screen)
        pygame.display.update()
    
    def update(self):
        dt = 1/self.clock.tick(60)
        if self.status == 0:
            self.menu_manager.update_ui(dt)
        elif self.status == 1:
            self.manager.update_ui(dt)
            if self.current_presentation:
                self.current_presentation.update()
    
    def quit(self):
        pygame.quit()
        sys.exit()
    
    def run(self):
        while True:
            self.events()
            self.update()
            self.draw()