
W = 1920
H = 1080
MYW = 1920
MYH = 1080
SIZES = (W,H)
PRESENTATIONS_FOLDER = "Presentations"

MENU_SETTINGS = [
    {
        "element_ids":"title",
        "settings":{
            "font_size":45
        }
    }
]

EDITOR_SETTINGS = [
    {
        "element_ids":"inspector_title",
        "settings":{
            "font_size":35,
            "alignment":"left"
        }
    },
    {
        "element_ids":"inspector_setting",
        "settings":{
            "text_alignment":"left"
        }
    },
    {
        "element_ids":"arrows",
        "settings":{
            "outline_enabled":False
        }
    }
]

NEW_STARTING_CONTENT = f"""= P_NAME, {W},{H},white =

==
"""

def size_width(desired):
    d = MYW/desired
    return W/d

def size_height(desired):
    d = MYH/desired
    return H/d

M_BUTTON_SIZE = (150,40)
M_S_BTN_SIZE = (100,40)
M_ENTRYLINE_SIZE = (250,40)
M_SL_TOPLEFT = (W/10,H/8)
M_SL_SIZE = (W/2.2-M_SL_TOPLEFT[0],H-M_SL_TOPLEFT[1]-50)
M_T_POS = (W/10,H/20)
M_T_SIZE = (W/2.2-M_T_POS[0],50)
M_LB_POS = (W/2,H/3)
M_VB_POS = (W/2,H/3+M_BUTTON_SIZE[1]+10)
M_CNB_POS = (W/2,H/3+M_BUTTON_SIZE[1]*2+10*2)
M_CI_POS = (W/2,H/2)
M_CCB_POS = (W/2+M_ENTRYLINE_SIZE[0]+10,H/2)
M_QB_POS = (W/2,H/1.5)

BTN_SIZE_S = (100,40)
BTN_SIZE_SL = (150,40)
SLIDE_PREVIEW_SIZE = (size_width(200),size_height(150))
TOPBAR_H = 50
BTNOFFSET = 5
SLIDES_C_W = size_width(250)+24
SLIDE_LEFT_OFFSET = ((SLIDES_C_W-24)-SLIDE_PREVIEW_SIZE[0])/2
INSPECTOR_W = size_width(350)
VIEW_OFFSET = 80
MAX_VIEW_WIDTH = W-INSPECTOR_W-SLIDES_C_W-VIEW_OFFSET*2
MAX_VIEW_HEIGHT = H-TOPBAR_H-VIEW_OFFSET*2

INSP_OFFSET = 20
INTER_OFFSET = 5
APPLY_OFFSET = 50
INSP_EL_H = 40
INSP_SETTING_W = 100
INSP_ENTRY_W = INSPECTOR_W-INSP_OFFSET*2
INSPECTOR_START_H = 20+50+10
