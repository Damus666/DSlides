from pygameUI import pygameUI
from .settings import *
import pygame
from .converter import Converter
from .elements import *

class Presentation:
    def __init__(self,manager,editor,name):
        self.editor = editor
        self.manager = manager
        
        # SLIDE VIEW
        self.slide_view_cont = pygameUI.UIContainer(pygame.Rect(SLIDES_C_W,TOPBAR_H,W-SLIDES_C_W-INSPECTOR_W,H-TOPBAR_H),self.manager,colored=True)
        self.slide_view_cont._shape_renderer.only_outline = True
        self.move_button = None
        self.slide_view = None
        
        # TOP BAR
        self.topbar_cont = pygameUI.UIContainer(pygame.Rect(0,0,W,TOPBAR_H),self.manager,colored=True)
        self.topbar_cont._shape_renderer.only_outline = True
        self.quit_btn = pygameUI.UIButton(pygame.Rect(W-BTN_SIZE_S[0]-BTNOFFSET,BTNOFFSET,BTN_SIZE_S[0],BTN_SIZE_S[1]),self.manager,self.topbar_cont,text="Quit",id="quit_only")
        self.quit_btn_2 = pygameUI.UIButton(pygame.Rect(W-BTN_SIZE_S[0]-BTNOFFSET*2-BTN_SIZE_SL[0],BTNOFFSET,BTN_SIZE_SL[0],BTN_SIZE_S[1]),self.manager,self.topbar_cont,text="Save & Quit",id="quit")
        self.save_btn = pygameUI.UIButton(pygame.Rect((BTNOFFSET,BTNOFFSET),BTN_SIZE_S),self.manager,self.topbar_cont,text="Save",id="save")
        self.menu_btn = pygameUI.UIButton(pygame.Rect((BTNOFFSET*2+BTN_SIZE_S[0],BTNOFFSET),BTN_SIZE_S),self.manager,self.topbar_cont,text="Menu",id="back_to_menu")
        self.new_slide_btn = pygameUI.UIButton(pygame.Rect((BTNOFFSET*3+BTN_SIZE_S[0]*2,BTNOFFSET),BTN_SIZE_SL),self.manager,self.topbar_cont,"Add Slide",id="add_slide")
        self.new_element_btn = pygameUI.UIDropDown(pygame.Rect((BTNOFFSET*4+BTN_SIZE_S[0]*2+BTN_SIZE_SL[0],BTNOFFSET),BTN_SIZE_SL),self.manager,["Text","Image","Rect","Line","Circle"],"Add Element","down",id="add_element")
        
        # SLIDES
        self.slides_cont = pygameUI.UIScrollableContainer(pygame.Rect(0,TOPBAR_H,SLIDES_C_W,H-TOPBAR_H),self.manager,colored=True)
        self.slides_cont._shape_renderer.only_outline = True
        scrollbar1 = pygameUI.UIVerticalScrollbar(pygame.Rect(SLIDES_C_W-24,0,24,H-TOPBAR_H),self.manager,self.slides_cont)
        self.slides_cont.set_vertical_scrollbar(scrollbar1)
        
        # INSPECTOR
        self.inspector_cont = pygameUI.UIContainer(pygame.Rect(W-INSPECTOR_W,TOPBAR_H,INSPECTOR_W,H-TOPBAR_H),self.manager,colored=True)
        self.inspector_cont._shape_renderer.only_outline = True
        
        # OTHER
        self.current_slide = 0
        self.slides_preview = list()
        self.multiplier = 0
        self.selected_element = None
        self.prev = (0,0)
        
        # SLIDE INSPECTOR
        self.slide_inspector_cont = pygameUI.UIContainer(pygame.Rect(0,0,INSPECTOR_W,H-TOPBAR_H),self.manager,self.inspector_cont,visible=False)
        self.slide_inspector_title = pygameUI.UILabel(pygame.Rect(20,20,INSPECTOR_W-20,50),self.manager,"Slide Inspector",self.slide_inspector_cont,id="inspector_title")
        self.slideI_c_s = pygameUI.UILabel(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H,100,40),self.manager,"Color:",self.slide_inspector_cont,id="inspector_setting")
        self.slideI_color_entry = pygameUI.UIEntryLine(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H+INTER_OFFSET,INSP_ENTRY_W,INSP_EL_H),self.manager,self.slide_inspector_cont)
        self.slideI_infotxt = pygameUI.UILabel(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*2+INTER_OFFSET,INSP_SETTING_W*3,INSP_EL_H),self.manager,"To change the slides size edit 'save.ds'",self.slide_inspector_cont)
        self.slideI_move_back = pygameUI.UIButton(pygame.Rect((INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*3+INTER_OFFSET*2+APPLY_OFFSET),BTN_SIZE_SL),self.manager,self.slide_inspector_cont,"Move Behind",id="move_slide_behind")
        self.slideI_move_front = pygameUI.UIButton(pygame.Rect((INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*4+INTER_OFFSET*3+APPLY_OFFSET),BTN_SIZE_SL),self.manager,self.slide_inspector_cont,"Move In Front",id="move_slide_front")
        self.slideI_apply_btn = pygameUI.UIButton(pygame.Rect((INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*5+INTER_OFFSET*4+APPLY_OFFSET),BTN_SIZE_S),self.manager,self.slide_inspector_cont,"Apply",id="slide_apply")
        self.slideI_delete_btn = pygameUI.UIButton(pygame.Rect((INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*6+INTER_OFFSET*5+APPLY_OFFSET*2),BTN_SIZE_S),self.manager,self.slide_inspector_cont,"Delete",id="delete_slide")
        
        # TEXT INSPECTOR
        self.text_inspector_cont = pygameUI.UIContainer(pygame.Rect(0,0,INSPECTOR_W,H-TOPBAR_H),self.manager,self.inspector_cont,visible=False)
        self.text_inspector_title = pygameUI.UILabel(pygame.Rect(20,20,INSPECTOR_W-20,50),self.manager,"Text Inspector",self.text_inspector_cont,id="inspector_title")
        self.textI_c_s = pygameUI.UILabel(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H,100,40),self.manager,"Color:",self.text_inspector_cont,id="inspector_setting")
        self.textI_color_entry = pygameUI.UIEntryLine(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H+INTER_OFFSET,INSP_ENTRY_W,INSP_EL_H),self.manager,self.text_inspector_cont)
        self.textI_f_s = pygameUI.UILabel(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*2+INTER_OFFSET*1,100,40),self.manager,"Font:",self.text_inspector_cont,id="inspector_setting")
        self.textI_font_entry = pygameUI.UIEntryLine(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*3+INTER_OFFSET*2,INSP_ENTRY_W,INSP_EL_H),self.manager,self.text_inspector_cont)
        self.textI_a_s = pygameUI.UILabel(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*4+INTER_OFFSET*3,100,40),self.manager,"Align:",self.text_inspector_cont,id="inspector_setting")
        self.textI_align_entry = pygameUI.UIEntryLine(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*5+INTER_OFFSET*4,INSP_ENTRY_W,INSP_EL_H),self.manager,self.text_inspector_cont)
        self.textI_t_s = pygameUI.UILabel(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*6+INTER_OFFSET*5,100,40),self.manager,"Content:",self.text_inspector_cont,id="inspector_setting")
        self.textI_content_entry = pygameUI.UIEntryLine(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*7+INTER_OFFSET*6,INSP_ENTRY_W,INSP_EL_H),self.manager,self.text_inspector_cont)
        self.textI_move_back = pygameUI.UIButton(pygame.Rect((INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*8+INTER_OFFSET*7+APPLY_OFFSET),BTN_SIZE_SL),self.manager,self.text_inspector_cont,"Move Behind",id="move_behind")
        #print(self.textI_move_back._ID)
        self.textI_move_front = pygameUI.UIButton(pygame.Rect((INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*9+INTER_OFFSET*8+APPLY_OFFSET),BTN_SIZE_SL),self.manager,self.text_inspector_cont,"Move In Front",id="move_front")
        self.textI_apply_btn = pygameUI.UIButton(pygame.Rect((INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*10+INTER_OFFSET*9+APPLY_OFFSET),BTN_SIZE_S),self.manager,self.text_inspector_cont,"Apply",id="text_apply")
        
        self.textI_delete_btn = pygameUI.UIButton(pygame.Rect((INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*11+INTER_OFFSET*10+APPLY_OFFSET*2),BTN_SIZE_S),self.manager,self.text_inspector_cont,"Delete",id="delete_element")
        
        # IMAGE INSPECTOR
        self.image_inspector_cont = pygameUI.UIContainer(pygame.Rect(0,0,INSPECTOR_W,H-TOPBAR_H),self.manager,self.inspector_cont,visible=False)
        self.image_inspector_title = pygameUI.UILabel(pygame.Rect(20,20,INSPECTOR_W-20,50),self.manager,"Image Inspector",self.image_inspector_cont,id="inspector_title")
        self.imageI_p_s = pygameUI.UILabel(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H,100,40),self.manager,"Path:",self.image_inspector_cont,id="inspector_setting")
        self.imageI_path_entry = pygameUI.UIEntryLine(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H+INTER_OFFSET,INSP_ENTRY_W,INSP_EL_H),self.manager,self.image_inspector_cont)
        self.imageI_s_s = pygameUI.UILabel(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*2+INTER_OFFSET*1,100,40),self.manager,"Size:",self.image_inspector_cont,id="inspector_setting")
        self.imageI_size_entry = pygameUI.UIEntryLine(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*3+INTER_OFFSET*2,INSP_ENTRY_W,INSP_EL_H),self.manager,self.image_inspector_cont)
        self.imageI_move_back = pygameUI.UIButton(pygame.Rect((INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*4+INTER_OFFSET*3+APPLY_OFFSET),BTN_SIZE_SL),self.manager,self.image_inspector_cont,"Move Behind",id="move_behind")
        self.imageI_move_front = pygameUI.UIButton(pygame.Rect((INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*5+INTER_OFFSET*4+APPLY_OFFSET),BTN_SIZE_SL),self.manager,self.image_inspector_cont,"Move In Front",id="move_front")
        self.imageI_apply_btn = pygameUI.UIButton(pygame.Rect((INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*6+INTER_OFFSET*5+APPLY_OFFSET),BTN_SIZE_S),self.manager,self.image_inspector_cont,"Apply",id="image_apply")
        self.imageI_delete_btn = pygameUI.UIButton(pygame.Rect((INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*7+INTER_OFFSET*6+APPLY_OFFSET*2),BTN_SIZE_S),self.manager,self.image_inspector_cont,"Delete",id="delete_element_104")
        
        # RECT INSPECTOR
        self.rect_inspector_cont = pygameUI.UIContainer(pygame.Rect(0,0,INSPECTOR_W,H-TOPBAR_H),self.manager,self.inspector_cont,visible=False)
        self.rect_inspector_title = pygameUI.UILabel(pygame.Rect(20,20,INSPECTOR_W-20,50),self.manager,"Rect Inspector",self.rect_inspector_cont,id="inspector_title")
        self.rectI_c_s = pygameUI.UILabel(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H,100,40),self.manager,"Color:",self.rect_inspector_cont,id="inspector_setting")
        self.rectI_color_entry = pygameUI.UIEntryLine(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H+INTER_OFFSET,INSP_ENTRY_W,INSP_EL_H),self.manager,self.rect_inspector_cont)
        self.rectI_s_s = pygameUI.UILabel(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*2+INTER_OFFSET*1,100,40),self.manager,"Size:",self.rect_inspector_cont,id="inspector_setting")
        self.rectI_size_entry = pygameUI.UIEntryLine(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*3+INTER_OFFSET*2,INSP_ENTRY_W,INSP_EL_H),self.manager,self.rect_inspector_cont)
        self.rectI_o_s = pygameUI.UILabel(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*4+INTER_OFFSET*3,100,40),self.manager,"Outline:",self.rect_inspector_cont,id="inspector_setting")
        self.rectI_outline_entry = pygameUI.UIEntryLine(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*5+INTER_OFFSET*4,INSP_ENTRY_W,INSP_EL_H),self.manager,self.rect_inspector_cont)
        self.rectI_r_s = pygameUI.UILabel(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*6+INTER_OFFSET*5,100,40),self.manager,"Roundness:",self.rect_inspector_cont,id="inspector_setting")
        self.rectI_roundness_entry = pygameUI.UIEntryLine(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*7+INTER_OFFSET*6,INSP_ENTRY_W,INSP_EL_H),self.manager,self.rect_inspector_cont)
        self.rectI_w_s = pygameUI.UILabel(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*8+INTER_OFFSET*7,100,40),self.manager,"Width:",self.rect_inspector_cont,id="inspector_setting")
        self.rectI_width_entry = pygameUI.UIEntryLine(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*9+INTER_OFFSET*8,INSP_ENTRY_W,INSP_EL_H),self.manager,self.rect_inspector_cont)
        self.rectI_move_back = pygameUI.UIButton(pygame.Rect((INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*10+INTER_OFFSET*9+APPLY_OFFSET),BTN_SIZE_SL),self.manager,self.rect_inspector_cont,"Move Behind",id="move_behind")
        self.rectI_move_front = pygameUI.UIButton(pygame.Rect((INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*11+INTER_OFFSET*10+APPLY_OFFSET),BTN_SIZE_SL),self.manager,self.rect_inspector_cont,"Move In Front",id="move_front")
        self.rectI_apply_btn = pygameUI.UIButton(pygame.Rect((INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*12+INTER_OFFSET*11+APPLY_OFFSET),BTN_SIZE_S),self.manager,self.rect_inspector_cont,"Apply",id="rect_apply")
        self.rectI_delete_btn = pygameUI.UIButton(pygame.Rect((INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*13+INTER_OFFSET*12+APPLY_OFFSET*2),BTN_SIZE_S),self.manager,self.rect_inspector_cont,"Delete",id="delete_element")
        
        # CIRCLE INSPECTOR
        self.circle_inspector_cont = pygameUI.UIContainer(pygame.Rect(0,0,INSPECTOR_W,H-TOPBAR_H),self.manager,self.inspector_cont,visible=False)
        self.circle_inspector_title = pygameUI.UILabel(pygame.Rect(20,20,INSPECTOR_W-20,50),self.manager,"Circle Inspector",self.circle_inspector_cont,id="inspector_title")
        self.circleI_c_s = pygameUI.UILabel(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H,100,40),self.manager,"Color:",self.circle_inspector_cont,id="inspector_setting")
        self.circleI_color_entry = pygameUI.UIEntryLine(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H+INTER_OFFSET,INSP_ENTRY_W,INSP_EL_H),self.manager,self.circle_inspector_cont)
        self.circleI_r_s = pygameUI.UILabel(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*2+INTER_OFFSET*1,100,40),self.manager,"Radius:",self.circle_inspector_cont,id="inspector_setting")
        self.circleI_radius_entry = pygameUI.UIEntryLine(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*3+INTER_OFFSET*2,INSP_ENTRY_W,INSP_EL_H),self.manager,self.circle_inspector_cont)
        self.circleI_o_s = pygameUI.UILabel(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*4+INTER_OFFSET*3,100,40),self.manager,"Outline:",self.circle_inspector_cont,id="inspector_setting")
        self.circleI_outline_entry = pygameUI.UIEntryLine(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*5+INTER_OFFSET*4,INSP_ENTRY_W,INSP_EL_H),self.manager,self.circle_inspector_cont)
        self.circleI_w_s = pygameUI.UILabel(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*6+INTER_OFFSET*5,100,40),self.manager,"Width:",self.circle_inspector_cont,id="inspector_setting")
        self.circleI_width_entry = pygameUI.UIEntryLine(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*7+INTER_OFFSET*6,INSP_ENTRY_W,INSP_EL_H),self.manager,self.circle_inspector_cont)
        self.circleI_move_back = pygameUI.UIButton(pygame.Rect((INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*8+INTER_OFFSET*7+APPLY_OFFSET),BTN_SIZE_SL),self.manager,self.circle_inspector_cont,"Move Behind",id="move_behind")
        self.circleI_move_front = pygameUI.UIButton(pygame.Rect((INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*9+INTER_OFFSET*8+APPLY_OFFSET),BTN_SIZE_SL),self.manager,self.circle_inspector_cont,"Move In Front",id="move_front")
        self.circleI_apply_btn = pygameUI.UIButton(pygame.Rect((INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*10+INTER_OFFSET*9+APPLY_OFFSET),BTN_SIZE_S),self.manager,self.circle_inspector_cont,"Apply",id="circle_apply")
        self.circleI_delete_btn = pygameUI.UIButton(pygame.Rect((INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*11+INTER_OFFSET*10+APPLY_OFFSET*2),BTN_SIZE_S),self.manager,self.circle_inspector_cont,"Delete",id="delete_element")
        
        # LINE INSPECTOR
        self.line_inspector_cont = pygameUI.UIContainer(pygame.Rect(0,0,INSPECTOR_W,H-TOPBAR_H),self.manager,self.inspector_cont,visible=False)
        self.line_inspector_title = pygameUI.UILabel(pygame.Rect(20,20,INSPECTOR_W-20,50),self.manager,"Line Inspector",self.line_inspector_cont,id="inspector_title")
        self.lineI_c_s = pygameUI.UILabel(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H,100,40),self.manager,"Color:",self.line_inspector_cont,id="inspector_setting")
        self.lineI_color_entry = pygameUI.UIEntryLine(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H+INTER_OFFSET,INSP_ENTRY_W,INSP_EL_H),self.manager,self.line_inspector_cont)
        self.lineI_s_s = pygameUI.UILabel(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*2+INTER_OFFSET*1,100,40),self.manager,"Start Offset:",self.line_inspector_cont,id="inspector_setting")
        self.lineI_start_entry = pygameUI.UIEntryLine(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*3+INTER_OFFSET*2,INSP_ENTRY_W,INSP_EL_H),self.manager,self.line_inspector_cont)
        self.lineI_e_s = pygameUI.UILabel(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*4+INTER_OFFSET*3,100,40),self.manager,"End Offset:",self.line_inspector_cont,id="inspector_setting")
        self.lineI_end_entry = pygameUI.UIEntryLine(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*5+INTER_OFFSET*4,INSP_ENTRY_W,INSP_EL_H),self.manager,self.line_inspector_cont)
        self.lineI_w_s = pygameUI.UILabel(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*6+INTER_OFFSET*5,100,40),self.manager,"Width:",self.line_inspector_cont,id="inspector_setting")
        self.lineI_width_entry = pygameUI.UIEntryLine(pygame.Rect(INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*7+INTER_OFFSET*6,INSP_ENTRY_W,INSP_EL_H),self.manager,self.line_inspector_cont)
        self.lineI_move_back = pygameUI.UIButton(pygame.Rect((INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*8+INTER_OFFSET*7+APPLY_OFFSET),BTN_SIZE_SL),self.manager,self.line_inspector_cont,"Move Behind",id="move_behind")
        self.lineI_move_front = pygameUI.UIButton(pygame.Rect((INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*9+INTER_OFFSET*8+APPLY_OFFSET),BTN_SIZE_SL),self.manager,self.line_inspector_cont,"Move In Front",id="move_front")
        self.lineI_apply_btn = pygameUI.UIButton(pygame.Rect((INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*10+INTER_OFFSET*9+APPLY_OFFSET),BTN_SIZE_S),self.manager,self.line_inspector_cont,"Apply",id="line_apply")
        self.lineI_delete_btn = pygameUI.UIButton(pygame.Rect((INSP_OFFSET,INSPECTOR_START_H+INSP_EL_H*11+INTER_OFFSET*10+APPLY_OFFSET*2),BTN_SIZE_S),self.manager,self.line_inspector_cont,"Delete",id="delete_element")
        
        self.inspectors = [self.slide_inspector_cont,self.text_inspector_cont,self.image_inspector_cont,self.rect_inspector_cont,self.circle_inspector_cont,self.line_inspector_cont]
        
        # LOAD
        self.name = name
        self.load(name)
        
    def re_render(self):
        self.converter.renderer.render()
        self.slide_view.change_image(self.converter.renderer.finals[self.current_slide].copy())
        if self.current_slide <= len(self.slides_preview)-1:
            self.slides_preview[self.current_slide].change_image(self.converter.renderer.finals[self.current_slide].copy())
        
    def rebuild_slides_images(self):
        for s in self.slides_preview:
            s.destroy()
        self.slides_preview.clear()
        for i,f in enumerate(self.converter.renderer.finals):
            img = pygameUI.UIImage(pygame.Rect((SLIDE_LEFT_OFFSET,SLIDE_LEFT_OFFSET+SLIDE_PREVIEW_SIZE[1]*i+SLIDE_LEFT_OFFSET*i),SLIDE_PREVIEW_SIZE),self.manager,f.copy(),self.slides_cont,id=f"slide_preview_{i}")
            self.slides_preview.append(img)
        
    def save(self):
        self.converter.renderer.save()
        final = ""
        for i,s in enumerate(self.converter.renderer.slides):
            if i == 0:
                final += "= "+self.name+","+str(self.converter.renderer.w)+","+str(self.converter.renderer.h)+","+str(s.color).replace("[","(").replace("]",")")+" ="
            else:
                final += "\n= "+str(s.color).replace("[","(").replace("]",")")+" ="
            for el in s.elements:
                final += el.get_str()
        final += "\n=="
        with open(PRESENTATIONS_FOLDER+"/"+self.name+"/save.ds","w") as file:
            file.write(final)
    
    def load(self,name):
        c = ""
        with open(PRESENTATIONS_FOLDER+"/"+name+"/save.ds","r") as file:
            c = file.read()
        self.converter = Converter(c,PRESENTATIONS_FOLDER+"/"+name+"/output")
        self.converter.convert()
        hisw = self.converter.renderer.w
        d = hisw/MAX_VIEW_WIDTH
        self.multiplier = d
        h = self.converter.renderer.h/d
        if h > MAX_VIEW_HEIGHT:
            h = MAX_VIEW_HEIGHT
        if self.slide_view != None:
            self.slide_view.destroy()
        self.slide_view = pygameUI.UIImage(pygame.Rect(VIEW_OFFSET,VIEW_OFFSET,MAX_VIEW_WIDTH,h),self.manager,self.converter.renderer.screen.copy(),self.slide_view_cont)
        self.slide_view.set_center_relative(0.5,0.5)
        if self.move_button != None:
            self.move_button.destroy()
        self.move_button = pygameUI.UIImage(pygame.Rect((0,0),(80,80)),self.manager,pygame.image.load("arrows.png").convert_alpha(),self.slide_view_cont,id="arrows")
        self.re_render()
        self.rebuild_slides_images()
        self.inspector_for_slide()
        
    def inspector_for_slide(self):
        self.move_button.hide()
        self.selected_element = None
        self.slide_inspector_cont.visible = True
        self.deactivate_others(self.slide_inspector_cont)
        self.slideI_color_entry.set_text(str(self.converter.renderer.slides[self.current_slide].color).replace("[","(").replace("]",")"))
        
    def deactivate_others(self,cont):
        for c in self.inspectors:
            if c != cont:
                c.visible = False
        
    def inspector_for_text(self):
        self.text_inspector_cont.visible = True
        self.deactivate_others(self.text_inspector_cont)
        self.textI_color_entry.set_text(str(self.selected_element.color).replace("[","(").replace("]",")"))
        self.textI_font_entry.set_text(f"{self.selected_element.fontname}, {self.selected_element.fontsize}")
        self.textI_align_entry.set_text(self.selected_element.alignement)
        self.textI_content_entry.set_text(self.selected_element.text.replace("\n","\\n"))
    
    def inspector_for_image(self):
        self.image_inspector_cont.visible = True
        self.deactivate_others(self.image_inspector_cont)
        self.imageI_path_entry.set_text(self.selected_element.path)
        self.imageI_size_entry.set_text(self.selected_element.size)
        
    def inspector_for_rect(self):
        self.rect_inspector_cont.visible = True
        self.deactivate_others(self.rect_inspector_cont)
        self.rectI_color_entry.set_text(str(self.selected_element.color).replace("[","(").replace("]",")"))
        self.rectI_size_entry.set_text(f"{self.selected_element.rect.w},{self.selected_element.rect.h}")
        self.rectI_outline_entry.set_text(f"{self.selected_element.outlinesize},{self.selected_element.outlinecolor.replace('[','(').replace(']',')')}")
        self.rectI_roundness_entry.set_text(str(self.selected_element.roundness))
        self.rectI_width_entry.set_text(str(self.selected_element.w))
        
    def inspector_for_circle(self):
        self.circle_inspector_cont.visible = True
        self.deactivate_others(self.circle_inspector_cont)
        self.circleI_color_entry.set_text(str(self.selected_element.color).replace("[","(").replace("]",")"))
        self.circleI_radius_entry.set_text(f"{self.selected_element.radius}")
        self.circleI_outline_entry.set_text(f"{self.selected_element.outlinesize},{self.selected_element.outlinecolor.replace('[','(').replace(']',')')}")
        self.circleI_width_entry.set_text(str(self.selected_element.w))
    
    def inspector_for_line(self):
        self.line_inspector_cont.visible = True
        self.deactivate_others(self.line_inspector_cont)
        self.lineI_color_entry.set_text(str(self.selected_element.color).replace("[","(").replace("]",")"))
        self.lineI_width_entry.set_text(str(self.selected_element.width))
        p = self.selected_element.get_pos()
        so = (int(self.selected_element.start[0]-p[0]),int(self.selected_element.start[1]-p[1]))
        eo = (int(self.selected_element.end[0]-p[0]),int(self.selected_element.end[1]-p[1]))
        self.lineI_start_entry.set_text(str(so).replace("(","").replace(")",""))
        self.lineI_end_entry.set_text(str(eo).replace("(","").replace(")",""))
    
    def apply_slide(self):
        old = self.converter.renderer.slides[self.current_slide].color
        try:
            txt = self.slideI_color_entry.get_text().strip()
            if txt != "":
                col = txt
                if "," in col:
                    col = [int(v) for v in txt.replace("(","").replace(")","").split(",")]
                self.converter.renderer.slides[self.current_slide].color = col
                self.re_render()
        except:
            self.converter.renderer.slides[self.current_slide].color = old
           
    def apply_text(self):
        old = {
            "color":self.selected_element.color,
            "text":self.selected_element.text,
            "font":(self.selected_element.fontname,self.selected_element.fontsize),
            "align":self.selected_element.alignement
        }
        try:
            self.selected_element.set_text(self.textI_content_entry.get_text().replace("\\n","\n"))
        except:
            self.selected_element.set_text(old["text"])
        try:
            col = self.textI_color_entry.get_text().strip()
            if col != "":
                if "," in col:
                    col = [int(v) for v in col.replace("(","").replace(")","").split(",")]
                self.selected_element.color = col
        except:
            self.selected_element.color = old["color"]
        try:
            txt = self.textI_font_entry.get_text().strip()
            if txt != "":
                name,size = txt.split(",")
                size = int(eval(size.strip()))
                self.selected_element.set_font(name.strip(),size)
        except:
            self.selected_element.set_font(old["font"][0],old["font"][1])
        try:
            txt = self.textI_align_entry.get_text().strip()
            if txt != "":
                self.selected_element.alignement = txt
        except:
            self.selected_element.alignement = old["align"]
        self.selected_element.make_surfaces()
        self.selected_element.make_rects()
        p = self.selected_element.get_pos()
        pos = ((p[0]/self.multiplier+self.slide_view.relative_rect.x),(p[1]/self.multiplier+self.slide_view.relative_rect.y))
        self.move_button.set_center(pos)
        self.re_render()
    
    def apply_image(self):
        old = {
            "path":self.selected_element.path,
            "size":self.selected_element.size
        }
        try:
            self.selected_element.set_image(self.imageI_path_entry.get_text().strip())
        except:
            self.selected_element.set_image(old["path"])
        try:
            siz = self.imageI_size_entry.get_text().strip()
            if siz != "":
                w,h = siz.split(",")
                self.selected_element.resize(w.strip(),h.strip())
                self.selected_element.set_rect()
        except:
            siz = old["size"]
            w,h = siz.split(",")
            self.selected_element.resize(w.strip(),h.strip())
            self.selected_element.set_rect()
        p = self.selected_element.get_pos()
        pos = ((p[0]/self.multiplier+self.slide_view.relative_rect.x),(p[1]/self.multiplier+self.slide_view.relative_rect.y))
        self.move_button.set_center(pos)
        self.re_render()
    
    def apply_rect(self):
        t = self.rectI_color_entry.get_text().strip()
        if t != "":
            if "," in t:
                    t = [int(v) for v in t.replace("(","").replace(")","").split(",")]
            self.selected_element.color = t
        t = self.rectI_size_entry.get_text().strip()
        if t != "":
            if "," in t:
                try:
                    w,h = t.split(",")
                    w = int(eval(w.strip()))
                    h = int(eval(h.strip()))
                    prev = self.selected_element.rect.center
                    self.selected_element.rect.w = w
                    self.selected_element.rect.h = h
                    self.selected_element.rect.center = prev
                except:
                    pass
        t = self.rectI_outline_entry.get_text().strip()
        if t != "":
            if "," in t:
                s,col = t.split(",")
                try:
                    s = int(eval(s.strip()))
                    if "," in col:
                        col = [int(v) for v in col.replace("(","").replace(")","").split(",")]
                    self.selected_element.outlinesize = s
                    self.selected_element.outlinecolor = col
                except:
                    pass
        t = self.rectI_roundness_entry.get_text().strip()
        if t != "":
            try:
                v = int(eval(t.strip()))
                self.selected_element.roundness = v
            except:
                pass
        t = self.rectI_width_entry.get_text().strip()
        if t != "":
            try:
                v = int(eval(t.strip()))
                self.selected_element.w = v
            except:
                pass
        p = self.selected_element.get_pos()
        pos = ((p[0]/self.multiplier+self.slide_view.relative_rect.x),(p[1]/self.multiplier+self.slide_view.relative_rect.y))
        self.move_button.set_center(pos)
        self.re_render()
    
    def apply_circle(self):
        t = self.circleI_color_entry.get_text().strip()
        if t != "":
            if "," in t:
                    t = [int(v) for v in t.replace("(","").replace(")","").split(",")]
            self.selected_element.color = t
        t = self.circleI_radius_entry.get_text().strip()
        if t != "":
            try:
                v = int(eval(t))
                self.selected_element.radius = v
            except:
                pass
        t = self.circleI_outline_entry.get_text().strip()
        if t != "":
            if "," in t:
                s,col = t.split(",")
                try:
                    s = int(eval(s.strip()))
                    if "," in col:
                        col = [int(v) for v in col.replace("(","").replace(")","").split(",")]
                    self.selected_element.outlinesize = s
                    self.selected_element.outlinecolor = col
                except:
                    pass
        t = self.circleI_width_entry.get_text().strip()
        if t != "":
            try:
                v = int(eval(t.strip()))
                self.selected_element.w = v
            except:
                pass
        p = self.selected_element.get_pos()
        pos = ((p[0]/self.multiplier+self.slide_view.relative_rect.x),(p[1]/self.multiplier+self.slide_view.relative_rect.y))
        self.move_button.set_center(pos)
        self.re_render()
    
    def apply_line(self):
        t = self.lineI_color_entry.get_text().strip()
        if t != "":
            if "," in t:
                    t = [int(v) for v in t.replace("(","").replace(")","").split(",")]
            self.selected_element.color = t
        t = self.lineI_width_entry.get_text().strip()
        if t != "":
            try:
                v = int(eval(t.strip()))
                self.selected_element.width = v
            except:
                pass
        so = self.lineI_start_entry.get_text().strip()
        eo = self.lineI_end_entry.get_text().strip()
        p = self.selected_element.get_pos()
        if so != "":
            if "," in so:
                try:
                    x,y = so.split(",")
                    x = int(eval(x.strip()))
                    y = int(eval(y.strip()))
                    newso = (int(p[0]+x),int(p[1]+y))
                    self.selected_element.start = newso
                except:
                    pass
        if eo != "":
            if "," in eo:
                try:
                    x,y = eo.split(",")
                    x = int(eval(x.strip()))
                    y = int(eval(y.strip()))
                    neweo = (int(p[0]+x),int(p[1]+y))
                    self.selected_element.end = neweo
                except:
                    pass
        
        pos = ((p[0]/self.multiplier+self.slide_view.relative_rect.x),(p[1]/self.multiplier+self.slide_view.relative_rect.y))
        self.move_button.set_center(pos)
        self.re_render()
    
    def move_back(self,isSlide=False):
        if not isSlide:
            cur = self.converter.renderer.slides[self.current_slide].elements.index(self.selected_element)
            if cur > 0:
                self.converter.renderer.slides[self.current_slide].elements.remove(self.selected_element)
                self.converter.renderer.slides[self.current_slide].elements.insert(cur-1,self.selected_element)
                self.re_render()
        else:
            if self.current_slide > 0:
                slide = self.converter.renderer.slides.pop(self.current_slide)
                self.current_slide -= 1
                self.converter.renderer.slides.insert(self.current_slide,slide)
                self.re_render()
                self.rebuild_slides_images()
                self.inspector_for_slide()
    
    def move_front(self,isSlide = False):
        if not isSlide:
            cur = self.converter.renderer.slides[self.current_slide].elements.index(self.selected_element)
            if cur < len(self.converter.renderer.slides[self.current_slide].elements)-1:
                self.converter.renderer.slides[self.current_slide].elements.remove(self.selected_element)
                self.converter.renderer.slides[self.current_slide].elements.insert(cur+1,self.selected_element)
                self.re_render()
        else:
            if self.current_slide < len(self.converter.renderer.slides)-1:
                slide = self.converter.renderer.slides.pop(self.current_slide)
                self.current_slide += 1
                self.converter.renderer.slides.insert(self.current_slide,slide)
                self.re_render()
                self.rebuild_slides_images()
                self.inspector_for_slide()
            
    def search_clicked_element(self):
        found = False
        mouse = pygame.mouse.get_pos()
        offsetted = (mouse[0]-self.slide_view.absolute_rect.x,mouse[1]-self.slide_view.absolute_rect.y)
        offsetted = (offsetted[0]*self.multiplier,offsetted[1]*self.multiplier)
        for element in reversed(self.converter.renderer.slides[self.current_slide].elements):
            if element.get_box().collidepoint(offsetted):
                self.selected_element = element
                p = self.selected_element.get_pos()
                self.move_button.visible = True
                pos = ((p[0]/self.multiplier+self.slide_view.relative_rect.x),(p[1]/self.multiplier+self.slide_view.relative_rect.y))
                self.move_button.set_center(pos)
                if element.NAME == "text":
                    self.inspector_for_text()
                elif element.NAME == "image":
                    self.inspector_for_image()
                elif element.NAME == "rect":
                    self.inspector_for_rect()
                elif element.NAME == "circle":
                    self.inspector_for_circle()
                elif element.NAME == "line":
                    self.inspector_for_line()
                found = True
                break
        return found
    
    def update(self):
        if self.move_button._is_clicking:
            cur = pygame.mouse.get_pos()
            rel = (cur[0]-self.prev[0],cur[1]-self.prev[1])
            if rel[0] != 0 or rel[1] != 0:
                self.move_button.update_position(rel[0],rel[1])
                new = ((self.move_button.relative_rect.centerx-self.slide_view.relative_rect.x)*self.multiplier,(self.move_button.relative_rect.centery-self.slide_view.relative_rect.y)*self.multiplier)
                self.selected_element.update_pos(new)
                self.re_render()
            self.prev = cur
        else:
            self.prev = pygame.mouse.get_pos()
            
    def spawn_new(self,name):
        if name == "text":
            new = Text()
            new.apply_default((self.converter.renderer.w/2,self.converter.renderer.h/2))
            self.converter.renderer.slides[self.current_slide].elements.append(new)
        elif name == "rect":
            new = Rect("center",(self.converter.renderer.w/2,self.converter.renderer.h/2),"white",5,2,"black",(100,100),0)
            self.converter.renderer.slides[self.current_slide].elements.append(new)
        elif name == "line":
            new = Line()
            new.apply_default((self.converter.renderer.w/2,self.converter.renderer.h/2))
            self.converter.renderer.slides[self.current_slide].elements.append(new)
        elif name == "image":
            new = Image()
            new.apply_default((self.converter.renderer.w/2,self.converter.renderer.h/2))
            self.converter.renderer.slides[self.current_slide].elements.append(new)
        elif name == "circle":
            new = Circle((self.converter.renderer.w/2,self.converter.renderer.h/2),"white",2,"black",50,0)
            self.converter.renderer.slides[self.current_slide].elements.append(new)
            
        self.re_render()
        
    def destroy_all(self):
        self.topbar_cont.destroy()
        self.slides_cont.destroy()
        self.slide_view_cont.destroy()
        self.inspector_cont.destroy()
    
    def event(self,event):
        
        if event.type == pygameUI.BUTTON_PRESSED:
            if event.element_ID == "quit":
                self.save()
                self.editor.quit()
            elif event.element_ID == "quit_only":
                self.editor.quit()
            elif event.element_ID == "save":
                self.save()
            elif event.element_ID == "back_to_menu":
                self.save()
                self.destroy_all()
                self.editor.to_menu()
                del self
            elif event.element_ID == "add_element":
                pass
            elif event.element_ID == "add_slide":
                self.converter.renderer.slides.append(Slide())
                self.re_render()
                self.rebuild_slides_images()
            elif event.element_ID == "slide_apply":
                self.apply_slide()
            elif event.element_ID == "text_apply":
                self.apply_text()
            elif event.element_ID == "image_apply":
                self.apply_image()
            elif event.element_ID == "rect_apply":
                self.apply_rect()
            elif event.element_ID == "circle_apply":
                self.apply_circle()
            elif event.element_ID == "line_apply":
                self.apply_line()
            elif event.element_ID == "move_behind":
                #print(self.selected_element)
                self.move_back(False)
            elif event.element_ID == "move_front":
                self.move_front(False)
            elif event.element_ID == "move_slide_behind":
                self.move_back(True)
            elif event.element_ID == "move_slide_front":
                self.move_front(True)
            elif event.element_ID == "delete_element":
                self.converter.renderer.slides[self.current_slide].elements.remove(self.selected_element)
                del self.selected_element
                self.selected_element = None
                self.inspector_for_slide()
                self.re_render()
            elif event.element_ID == "delete_element_104":
                if self.selected_element.NAME == "image":
                    self.converter.renderer.slides[self.current_slide].elements.remove(self.selected_element)
                    del self.selected_element
                    self.selected_element = None
                    self.inspector_for_slide()
                    self.re_render()
            elif event.element_ID == "delete_slide":
                if len(self.slides_preview) > 1:
                    self.converter.renderer.slides.pop(self.current_slide)
                    if self.current_slide >= len(self.converter.renderer.slides):
                        self.current_slide-= 1
                    self.rebuild_slides_images()
                    self.re_render()
                    self.rebuild_slides_images()
                    self.inspector_for_slide()
        elif event.type == pygameUI.ELEMENT_PRESSED:
            if event.element_ID.startswith("slide_preview_"):
                index = int(event.element_ID.replace("slide_preview_",""))
                self.current_slide = index
                self.inspector_for_slide()
                self.re_render()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.slide_view.is_hovering():
                if not self.move_button.is_hovering():
                    if not self.search_clicked_element():
                        self.inspector_for_slide()
                    else:
                        self.slide_inspector_cont.visible = False
            else:
                if not self.inspector_cont.is_hovering() and not self.move_button.is_hovering():
                    self.inspector_for_slide()
        elif event.type == pygameUI.DROPDOWN_SELECTED:
            if event.element_ID == "add_element":
                name = event.new
                self.new_element_btn.set_selected("Add Element")
                self.spawn_new(name.lower())