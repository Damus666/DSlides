from .elements import *
from .renderer import Renderer

class Converter:
    def __init__(self,file_content,outputfolder):
        self.file_content = file_content
        
        self.renderer = Renderer(outputfolder)
        
        self.slides_text = list()
        
    def divide_slide_elements(self):
        current_slide = None
        elements_texts = list()
        
        for i,txt in enumerate(self.slides_text):
            current_slide = self.renderer.slides[i]
            elements_texts.clear()
            isString = False
            current = ""
            inThing = False
            for char in txt:
                if not isString:
                    if char == "|":
                        isString = True
                        #current += char
                    if inThing:
                        if char == ">":
                            inThing = False
                            elements_texts.append(current)
                            current = ""
                        else:
                            if char == "<":
                                raise Exception("< was not closed")
                            current += char
                    else:
                        if char == "<":
                            inThing = True
                            
                else:
                    if char == "|":
                        isString = False
                        current += char
                    else:
                        current += char
            for t in elements_texts:
                self.convert_element(t,current_slide,i)
                        
    def convert_element(self,txt:str,slide:Slide,slidenum):
        if txt.strip().startswith("text"):
            txt = txt.replace("text","",1)
            raw = ""
            
            if txt.strip().startswith("|"):
                txt = txt.replace("|","",1)
                cop = txt
                for char in cop:
                    if char == "|":
                        txt = txt[1:]
                        break
                    else:
                        txt = txt[1:]
                        raw += char
                #txt = txt.replace("|"+raw+"|","",1)
                col = "black"
                font = ["Segoe UI", 20]
                posname = "center"
                pos = (self.renderer.w/2,self.renderer.h/2)
                align = "middle"
                if txt.strip().startswith("$"):
                    txt = txt.replace("$","",1)
                    alloptions = txt.split("$")
                    for opt in alloptions:
                        opt = opt.strip()
                        if opt.startswith("font"):
                            rest = opt.replace("font","",1)
                            name,size = rest.split(",")
                            font[0] = name.strip()
                            font[1] = int(size)
                        elif opt.startswith("color"):
                            rest = opt.replace("color","",1)
                            col = rest.strip()
                            if "," in col:
                                col = [int(v) for v in col.replace("(","").replace(")","").split(",")]
                        elif opt.startswith("align"):
                            rest = opt.replace("align","",1)
                            align = rest.strip()
                        elif opt == "":
                            raise Exception("After '$' a parameter is expected")
                        else:
                            for p in ["center","topleft","topright","bottomleft","bottomright","midleft","midright","midtop","midbottom"]:
                                if opt.startswith(p):
                                    pos = self.return_win_pos(opt.replace(p,"",1).strip())
                obj = Text()
                raw = raw.replace("\\n","\n")
                obj.set_text(raw.strip())
                obj.alignement = align
                obj.color = col
                obj.set_font(font[0],font[1])
                obj.make_surfaces()
                obj.pos_name = posname
                obj.pos = pos
                obj.make_rects()
                slide.add_element(obj)
            else:
                raise Exception("After 'text', '|' is expected")
        elif txt.strip().startswith("image"):
            txt = txt.replace("image","",1)
            raw = ""
            if txt.strip().startswith("|"):
                txt = txt.replace("|","",1)
                cop = txt
                for char in cop:
                    if char == "|":
                        txt = txt[1:]
                        break
                    else:
                        txt = txt[1:]
                        raw += char
                posname = "center"
                pos = (self.renderer.w/2,self.renderer.h/2)
                width = "width"
                height = "height"
                if txt.strip().startswith("$"):
                    txt = txt.replace("$","",1)
                    alloptions = txt.split("$")
                    for opt in alloptions:
                        opt = opt.strip()
                        if opt.startswith("size"):
                            rest = opt.replace("size","",1)
                            w,h = rest.split(",")
                            width = w.strip()
                            height = h.strip()
                        elif opt == "":
                            raise Exception("After '$' a parameter is expected")
                        else:
                            for p in ["center","topleft","topright","bottomleft","bottomright","midleft","midright","midtop","midbottom"]:
                                if opt.startswith(p):
                                    pos = self.return_win_pos(opt.replace(p,"",1).strip())
                obj = Image()
                obj.pos_name = posname
                obj.pos = pos
                obj.set_image(raw.strip())
                obj.resize(width,height)
                obj.set_rect()
                slide.add_element(obj)
            else:
                raise Exception("After 'image', '|' is expected")
        elif txt.strip().startswith("line"):
            txt = txt.replace("line","",1)
            start = (0,0)
            end = (0,0)
            color = "black"
            wi = 1
            if txt.strip().startswith("$"):
                txt = txt.replace("$","",1)
                alloptions = txt.split("$")
                for opt in alloptions:
                    opt = opt.strip()
                    if opt.startswith("start"):
                        rest = opt.replace("start","",1)
                        start = self.return_win_pos(rest.strip())
                    elif opt.startswith("end"):
                        rest = opt.replace("end","",1)
                        end = self.return_win_pos(rest.strip())
                    elif opt.startswith("color"):
                        rest = opt.replace("color","",1)
                        color = rest.strip()
                        if "," in color:
                            color = [int(v) for v in color.replace("(","").replace(")","").split(",")]
                    elif opt.startswith("width"):
                        rest = opt.replace("width","",1)
                        wi = int(eval(rest.strip()))
                    elif opt == "":
                            raise Exception("After '$' a parameter is expected")
            obj = Line()
            obj.start = start
            obj.end = end
            obj.color = color
            obj.width = wi
            slide.add_element(obj)
        elif txt.strip().startswith("rect"):
            txt = txt.replace("rect","",1)
            posname = "center"
            pos = (self.renderer.w/2,self.renderer.h/2)
            w = 0
            outlinecol = "black"
            outlinesize = 0
            col = "white"
            roundness = 0
            size = (0,0)
            if txt.strip().startswith("$"):
                txt = txt.replace("$","",1)
                alloptions = txt.split("$")
                for opt in alloptions:
                    opt = opt.strip()
                    if opt.startswith("size"):
                        rest = opt.replace("size","",1)
                        ww,h = rest.split(",")
                        size = (int(eval(ww.strip())),int(eval(h.strip())))
                    elif opt.startswith("width"):
                        rest = opt.replace("width","",1)
                        w = int(eval(rest.strip()))
                    elif opt.startswith("roundness"):
                        rest = opt.replace("roundness","",1)
                        roundness = int(eval(rest.strip()))
                    elif opt.startswith("color"):
                        rest = opt.replace("color","",1)
                        col = rest.strip()
                        if "," in col:
                            col = [int(v) for v in col.replace("(","").replace(")","").split(",")]
                    elif opt.startswith("outline"):
                        rest = opt.replace("outline","",1)
                        siz,oc = rest.strip().split(",",1)
                        outlinesize = int(eval(siz.strip()))
                        outlinecol = oc.strip()
                        if "," in outlinecol:
                            outlinecol = [int(v) for v in outlinecol.replace("(","").replace(")","").split(",")]
                    elif opt == "":
                            raise Exception("After '$' a parameter is expected")
                    else:
                        for p in ["center","topleft","topright","bottomleft","bottomright","midleft","midright","midtop","midbottom"]:
                            if opt.startswith(p):
                                pos = self.return_win_pos(opt.replace(p,"",1).strip())
            obj = Rect(posname,pos,col,roundness,outlinesize,outlinecol,size,w)
            slide.add_element(obj)
        elif txt.strip().startswith("circle"):
            txt = txt.replace("circle","",1)
            pos = (self.renderer.w/2,self.renderer.h/2)
            w = 0
            outlinecol = "black"
            outlinesize = 0
            col = "white"
            radius = 5
            if txt.strip().startswith("$"):
                txt = txt.replace("$","",1)
                alloptions = txt.split("$")
                for opt in alloptions:
                    opt = opt.strip()
                    if opt.startswith("radius"):
                        rest = opt.replace("radius","",1)
                        radius = int(eval(rest.strip()))
                    elif opt.startswith("width"):
                        rest = opt.replace("width","",1)
                        w = int(eval(rest.strip()))
                    elif opt.startswith("color"):
                        rest = opt.replace("color","",1)
                        col = rest.strip()
                        if "," in col:
                            col = [int(v) for v in col.replace("(","").replace(")","").split(",")]
                    elif opt.startswith("outline"):
                        rest = opt.replace("outline","",1)
                        siz,oc = rest.strip().split(",",1)
                        outlinesize = int(eval(siz.strip()))
                        outlinecol = oc.strip()
                        if "," in outlinecol:
                            outlinecol = [int(v) for v in outlinecol.replace("(","").replace(")","").split(",")]
                    elif opt.startswith("position"):
                        rest = opt.replace("position","",1)
                        pos = self.return_win_pos(rest.strip())
                    elif opt == "":
                            raise Exception("After '$' a parameter is expected")
            obj = Circle(pos,col,outlinesize,outlinecol,radius,w)
            slide.add_element(obj)
            
    def return_win_pos(self,pos):
        if pos == "center":
            return (self.renderer.w/2,self.renderer.h/2)
        elif pos == "topleft":
            return (0,0)
        elif pos == "topright":
            return (self.renderer.w,0)
        elif pos == "bottomleft":
            return (0,self.renderer.h)
        elif pos == "bottomright":
            return (self.renderer.w,self.renderer.h)
        elif pos == "midleft":
            return (0,self.renderer.h/2)
        elif pos == "midright":
            return (self.renderer.w,self.renderer.h/2)
        elif pos == "midtop":
            return (self.renderer.w/2,0)
        elif pos == "midbottom":
            return (self.renderer.w/2,self.renderer.h)
        else:
            pos = pos.replace("top","0").replace("left","0").replace("right",str(self.renderer.w)).replace("bottom",str(self.renderer.h)).replace("centerx",str(self.renderer.w/2)).replace("centery",str(self.renderer.h/2))
            p = pos.split(",")
            x = int(eval(p[0].strip()))
            y = int(eval(p[1].strip()))
            return (x,y)
        
    def convert(self):
        self.divide_slides()
        self.divide_slide_elements()
    
    def divide_slides(self):
        current = ""
        isString = False
        isInThing = False
        isBetween = False
        between = ""
        slide = None
        for char in self.file_content:
            if not isString:
                if char == "|":
                    isString = True
                    #current += char
                if isBetween:
                    if char == "=":
                        isBetween = False
                        isInThing = True
                        if "," in between and not between.strip().startswith("("):
                            name,width,height,color = between.split(",")
                            #print(name,width,height,color)
                            self.renderer.output_name = name.strip()
                            self.renderer.set_size((int(width),int(height)))
                            slide.color = color.strip()
                        else:
                            #print(between,"b")
                            if between.strip() != "":
                                c = between.strip()
                                if not "," in c:
                                    slide.color = c
                                else:
                                    slide.color = [int(n) for n in c.replace("(","").replace(")","").split(",")]
                            else:
                                slide = None
                                self.renderer.slides.pop(-1)
                                break
                        between = ""
                    else:
                        between += char
                elif isInThing:
                    if char == "=":
                        isInThing = False
                        isBetween = True
                        self.slides_text.append(current)
                        slide = Slide()
                        self.renderer.slides.append(slide)
                        current = ""
                    else:
                        current += char
                else:
                    if char == "=":
                        isBetween = True
                        slide = Slide()
                        self.renderer.slides.append(slide)
            else:
                if char == "|":
                    isString = False
                    current += char
                else:
                    current += char