from pygameUI import pygameUI
import pygame
from .settings import *

class Menu:
    def __init__(self,manager,editor):
        self.editor = editor
        self.manager = manager
        self.presentation_list = pygameUI.UISelectionList(pygame.Rect(M_SL_TOPLEFT,M_SL_SIZE),self.manager,[],False)
        self.presentations_title = pygameUI.UILabel(pygame.Rect(M_T_POS,M_T_SIZE),self.manager,"DSlides Presentations",id="title")
        self.load_btn = pygameUI.UIButton(pygame.Rect(M_LB_POS,M_BUTTON_SIZE),self.manager,text="Load Selected",id="load")
        self.view_btn = pygameUI.UIButton(pygame.Rect(M_VB_POS,M_BUTTON_SIZE),self.manager,text="View Selected",id="view")
        self.create_new_btn = pygameUI.UIButton(pygame.Rect(M_CNB_POS,M_BUTTON_SIZE),self.manager,text="Create New",id="toggle_create")
        self.new_name_entry = pygameUI.UIEntryLine(pygame.Rect(M_CI_POS,M_ENTRYLINE_SIZE),self.manager,characters_limit=30,visible=False)
        self.final_create_btn = pygameUI.UIButton(pygame.Rect(M_CCB_POS,M_S_BTN_SIZE),self.manager,text="Create",id="create",visible=False)
        self.quit_btn = pygameUI.UIButton(pygame.Rect(M_QB_POS,M_S_BTN_SIZE),self.manager,text="Quit",id="quit")
        
    def event(self,event):
        if event.type == pygameUI.BUTTON_PRESSED:
            if event.element_ID == "toggle_create":
                self.new_name_entry.visible = not self.new_name_entry.visible
                self.final_create_btn.visible = self.new_name_entry.visible
            elif event.element_ID == "load":
                if self.presentation_list.get_selection() != None:
                    selected = self.presentation_list.get_selection()
                    self.editor.load_presentation(selected)
            elif event.element_ID == "create":
                txt = self.new_name_entry.get_text()
                if txt.strip() != "":
                    created = self.editor.create_new(txt.strip(),self.presentation_list._items_list)
                    if created:
                        self.presentation_list.set_item_list(self.presentation_list._items_list+[txt.strip()])
            elif event.element_ID == "quit":
                self.editor.quit()
            elif event.element_ID == "view":
                if self.presentation_list.get_selection() != None:
                    selected = self.presentation_list.get_selection()
                    self.editor.view(selected)
                    
            
    def load(self,presentations_names):
        self.presentation_list.set_item_list(presentations_names)