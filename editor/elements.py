import pygame

class Text:
    def __init__(self):
        self.NAME = "text"
        self.text_surfaces = list()
        self.font = None
        self.text = ""
        self.split_text = self.text
        self.color  = "black"
        self.rects = list()
        self.pos = (0,0)
        self.alignement = "middle"
        self.pos_name = "topleft"
        
    def get_pos(self):
        return self.pos
        
    def apply_default(self,center):
        self.pos = center
        self.pos_name = "center"
        self.set_text("Text Content")
        self.set_font()
        self.make_surfaces()
        self.make_rects()
        
    def get_str(self):
        self.pos = (int(self.pos[0]),int(self.pos[1]))
        final = "\n< text"
        final += "\n|"+self.text.replace("\n","\\n")+"|"
        final += "\n$ color "+str(self.color).replace("[","(").replace("]",")")
        final += "\n$ font "+self.fontname+","+str(self.fontsize)
        final += "\n$ "+self.pos_name+" "+str(self.pos).replace("(","").replace(")","")
        final += "\n$ align "+self.alignement
        return final+"\n>"
        
    def set_font(self,name="Segoe UI",size=20):
        self.fontname = name
        self.fontsize = size
        self.font = pygame.font.SysFont(name,size)
        
    def set_text(self,text):
        self.text = text
        self.split_text = self.text.split("\n")
        
    def make_surfaces(self):
        self.text_surfaces.clear()
        for t in self.split_text:
            self.text_surfaces.append(self.font.render(t,True,self.color))
            
    def update_pos(self,pos):
        self.pos = pos
        self.make_rects()
        
    def make_rects(self):
        self.rects.clear()
        for surf in self.text_surfaces:
            self.rects.append(surf.get_rect(**{self.pos_name:self.pos}))
        numrects = len(self.rects)
        if numrects % 2 == 0:
            if "top" in self.pos_name:
                first = self.rects[0]
                for ii,r in enumerate(self.rects):
                    if r != first:
                        r.y += first.h*ii
            elif "bottom" in self.pos_name:
                last = self.rects[-1]
                for iii,r in enumerate(reversed(self.rects)):
                    if r != last:
                        r.y -= last.h * iii
            else:
                amount = numrects/2
                h = self.rects[0].h
                for i,r in enumerate(self.rects):
                    if i+1 <= amount:
                        r.y -= h*i+h/2
                    else:
                        r.y += h*(i-amount)+h/2
        else:
            if "top" in self.pos_name:
                first = self.rects[0]
                for ii,r in enumerate(self.rects):
                    if r != first:
                        r.y += first.h*ii
            elif "bottom" in self.pos_name:
                last = self.rects[-1]
                for iii,r in enumerate(reversed(self.rects)):
                    if r != last:
                        r.y -= last.h * iii
            else:
                crect = self.rects[int(numrects/2)]
                amount = int(numrects/2)
                for i in range(amount):
                    #print(self.rects[i].y,crect.h,crect.h*(i+1))
                    self.rects[i].y -= crect.h*(i+1)
                    #print(self.rects[i].y)
                a = 0
                for o in range(amount+1,amount*2+1):
                    #print(o)
                    self.rects[o].y += crect.h*(a+1)
                    a += 1
        longest = None
        cmax = 0
        for r in self.rects:
            if r.w > cmax:
                cmax = r.w
                longest = r
        if self.alignement == "middle":
            cx = longest.centerx
            for rr in self.rects:
                rr.centerx = cx
        elif self.alignement == "left":
            lx = longest.left
            for rr in self.rects:
                rr.left = lx
        else:
            rx = longest.right
            for rr in self.rects:
                rr.right = rx
                
    def get_box(self):
        top = self.rects[0].top
        bottom = self.rects[-1].bottom
        longest = None
        cmax = 0
        for r in self.rects:
            if r.w > cmax:
                cmax = r.w
                longest = r
        return pygame.Rect(longest.left,top,longest.w,bottom-top)
         
    def render(self,surface):
        for i,s in enumerate(self.text_surfaces):
            surface.blit(s,self.rects[i])
    
class Image:
    def __init__(self):
        self.NAME = "image"
        self.image = None
        self.rect = None
        self.pos_name = "center"
        self.pos = (0,0)
        
    def get_pos(self):
        return self.pos
        
    def apply_default(self,center):
        self.pos = center
        self.pos_name = "center"
        self.set_image("placeholder.jpg")
        self.resize("100","100")
        self.set_rect()
        
    def get_box(self):
        return self.rect
        
    def get_str(self):
        self.pos = (int(self.pos[0]),int(self.pos[1]))
        final = "\n< image"
        final += "\n|"+self.path+"|"
        final += "\n$ "+self.pos_name+" "+str(self.pos).replace("(","").replace(")","")
        final += "\n$ size "+self.size
        return final+"\n>"
        
    def set_image(self,path):
        self.path = path
        self.image = pygame.image.load(path).convert_alpha()
        
    def resize(self,w,h):
        w = int(eval(w.replace("width",str(self.image.get_width()))))
        h = int(eval(h.replace("height",str(self.image.get_height()))))
        self.size = str(w)+","+str(h)
        self.image = pygame.transform.scale(self.image,(w,h))
        
    def set_rect(self):
        self.rect = self.image.get_rect(**{self.pos_name:self.pos})
        
    def update_pos(self,pos):
        self.pos = pos
        setattr(self.rect,self.pos_name,self.pos)
        
    def render(self,surface):
        surface.blit(self.image,self.rect)
        
class Line:
    def __init__(self):
        self.NAME = "line"
        self.start = (0,0)
        self.end = (0,0)
        self.width = 2
        self.color = "black"
        
    def get_pos(self):
        return self.get_box_original().center
        
    def apply_default(self,center):
        self.start = (center[0]-100,center[1])
        self.end = (center[0]+100,center[1])
        
    def update_pos(self,pos):
        box = self.get_box()
        diff = (pos[0]-box.centerx,pos[1]-box.centery)
        self.start = (self.start[0]+diff[0],self.start[1]+diff[1])
        self.end = (self.end[0]+diff[0],self.end[1]+diff[1])
        
    def get_box(self):
        return pygame.Rect(min(self.start[0],self.end[0]),min(self.start[1],self.end[1]),abs(self.start[0]-self.end[0])+2,abs(self.start[1]-self.end[1])+2)
    
    def get_box_original(self):
        return pygame.Rect(min(self.start[0],self.end[0]),min(self.start[1],self.end[1]),abs(self.start[0]-self.end[0]),abs(self.start[1]-self.end[1]))
        
    def get_str(self):
        self.start = (int(self.start[0]),int(self.start[1]))
        self.end = (int(self.end[0]),int(self.end[1]))
        final = "\n< line"
        final += "\n$ color "+str(self.color).replace("[","(").replace("]",")")
        final += "\n$ width "+str(self.width)
        final += "\n$ start "+str(self.start).replace("(","").replace(")","")
        final += "\n$ end  "+str(self.end).replace("(","").replace(")","")
        return final+"\n>"
        
    def render(self,surface):
        pygame.draw.line(surface,self.color,self.start,self.end,self.width)

class Rect:
    def __init__(self,posname,pos,color,roundness,outline,outlinecolor,size,w):
        self.NAME = "rect"
        self.color = color
        self.outlinesize = outline
        self.outlinecolor = outlinecolor
        self.roundness = roundness
        self.w = w
        self.rect = pygame.Rect(0,0,size[0],size[1])
        self.posname = posname
        setattr(self.rect,posname,pos)
        
    def get_pos(self):
        return self.rect.center
        
    def apply_default(self,center):
        pass
        
    def update_pos(self,pos):
        setattr(self.rect,self.posname,pos)
        
    def get_box(self):
        return self.rect
        
    def get_str(self):
        self.rect.center = (int(self.rect.centerx),int(self.rect.centery))
        final = "\n< rect"
        final += "\n$ "+self.posname+" "+str(getattr(self.rect,self.posname)).replace("(","").replace(")","")
        final += "\n$ size "+f"{self.rect.w},{self.rect.h}"
        final += "\n$ width "+str(self.w)
        final += "\n$ roundness "+str(self.roundness)
        final += "\n$ outline "+str(self.outlinesize)+", "+str(self.outlinecolor).replace("[","(").replace("]",")")
        final += "\n$ color "+str(self.color).replace("[","(").replace("]",")")
        return final+"\n>"
        
    def render(self,surface):
        pygame.draw.rect(surface,self.color,self.rect,self.w,self.roundness)
        if self.outlinesize != 0 and self.w == 0:
            pygame.draw.rect(surface,self.outlinecolor,self.rect,self.outlinesize,self.roundness)
            
class Circle:
    def __init__(self,pos,color,outline,outlinecolor,rad,w):
        self.NAME = "circle"
        self.color = color
        self.outlinesize = outline
        self.outlinecolor = outlinecolor
        self.w = w
        self.radius = rad
        self.pos = pos
        
    def get_pos(self):
        return self.pos
        
    def apply_default(self,center):
        pass
        
    def update_pos(self,pos):
        self.pos = pos
        
    def get_box(self):
        return pygame.Rect(self.pos[0]-self.radius,self.pos[1]-self.radius,self.radius*2,self.radius*2)
        
    def get_str(self):
        self.pos = (int(self.pos[0]),int(self.pos[1]))
        final = "\n< circle"
        final += "\n$ position "+str(self.pos).replace("(","").replace(")","")
        final += "\n$ radius "+str(self.radius)
        final += "\n$ width "+str(self.w)
        final += "\n$ outline "+str(self.outlinesize)+", "+str(self.outlinecolor).replace("[","(").replace("]",")")
        final += "\n$ color "+str(self.color).replace("[","(").replace("]",")")
        return final+"\n>"
        
    def render(self,surface):
        pygame.draw.circle(surface,self.color,self.pos,self.radius,self.w)
        if self.outlinesize != 0 and self.w == 0:
            pygame.draw.circle(surface,self.outlinecolor,self.pos,self.radius,self.outlinesize)
    
class Slide:
    def __init__(self):
        self.color = "white"
        self.elements = list()
        
    def render(self,surface):
        #print(self.color)
        surface.fill(self.color)
        for el in self.elements:
            el.render(surface)
            
    def add_element(self,element):
        self.elements.append(element)