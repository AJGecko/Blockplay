import pygame
from pygame_markdown import MarkdownRenderer
import lang
import essentials as es
import ingame
from pathlib import Path

#set assets path
BASE_DIR = Path(__file__).resolve().parent
pixelfont_path = es.pixelfont_path
buttonfont = pygame.font.Font(str(pixelfont_path), 64)
font = pygame.font.Font(str(pixelfont_path), 32)

#update essentials variables
def update():
    global screen,midx,midy,width,height,events,scale,mouse,buttonfont
    screen = pygame.display.get_surface()

    es.settings["number_platforms"] = settingsmenu.built["number_platforms"]()
    es.settings["difficulty"] = settingsmenu.built["difficulty"]()
    es.settings["language"] = settingsmenu.built["language"]()
    es.settings["skin"] = settingsmenu.built["skin"]()
    es.settings["color_scheme"] = settingsmenu.built["color_scheme"]()
    es.settings["fly"] = settingsmenu.built["fly"]()

    midx,midy,width,height,events,scale = es.basis()
    mouse = es.mouse
    text_surface = font.render(str(mouse.pressed(1)), True, (255, 255, 255))
    screen.blit(text_surface, (700, 100))

# background for the menus (checkerboard patterne based on color scheme)
def backround(width, height, tile_size, scale):
    WIDTH, HEIGHT, TILE_SIZE = width, height, int(tile_size*scale)
    COLOR = es.appearance("color")
    LIGHT_COLOR = COLOR[0]
    DARK_COLOR = COLOR[1]
    
    offset_x = (width % TILE_SIZE) // 2
    offset_y = (height % TILE_SIZE) // 2

    for x in range(offset_x-TILE_SIZE,(WIDTH-offset_x)+TILE_SIZE,TILE_SIZE):
        for y in range(offset_y-TILE_SIZE,(HEIGHT-offset_y)+TILE_SIZE,TILE_SIZE):
            row = y // TILE_SIZE
            col = x // TILE_SIZE
            if (row + col) % 2 == 0:
                color = LIGHT_COLOR
            else:
                color = DARK_COLOR
            pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))

#backround that is just a solid color
def backroundcolor(color):
    screen.fill(color)

#button class
class button:
    #initializes the button with a texture, size, and text key for localization
    def __init__(self, texture_path, size_x, size_y, text):
        self.path = Path(texture_path)
        if not self.path.is_absolute():
            self.path = (BASE_DIR / self.path).resolve()
        self.sizex = size_x
        self.sizey = size_y
        self.out_original = pygame.image.load(str(self.path)).convert_alpha()
        self.lscale = 1
        self.pos = (0, 0)
        self.font = pygame.font.Font(None, 64)
        self.text_key = text
    
    #updates the button's position based on the center of the screen
    def update(self,x,y):
        self.pos = (midx+x-((self.sizex*self.lscale)/2), midy-y-(self.sizey*self.lscale)/2) 

    #generates a hitbox for the button
    def hitbox(self,input):
        temp_rect = pygame.Rect(self.pos[0], self.pos[1], self.sizex*self.lscale,self.sizey*self.lscale) 
        return temp_rect.collidepoint(input)

    #shows the button on the screen and changes its scale if the mouse is hovering over it if responsive is 1        
    def show(self,x,y,responsive):
        global lang
        self.update(x,y)
        if self.hitbox(mouse.pos) and responsive==1:
            self.lscale = 1.05
        else:
            self.lscale = 1
        self.out = pygame.transform.scale(self.out_original, (self.sizex*self.lscale,self.sizey*self.lscale))
        screen.blit(self.out, self.pos)
        self.text(0,-120,lang.currentlang.get(self.text_key, self.text_key))
    
    #displays text on the button based on the current language
    def text(self,x,y,text):
        output = self.font.render(text, True, (255, 255, 255))
        text_rect = output.get_rect()
        button_center_x = self.pos[0] + (self.sizex * self.lscale) / 2
        button_center_y = self.pos[1] + (self.sizey * self.lscale) / 2
    
        text_rect.center = (button_center_x, button_center_y)
        screen.blit(output, text_rect) # text_rect

    #checks if the button is being clicked
    def click(self,x,y,input):
        self.update(x,y)
        if input == 1 and self.hitbox(mouse.pos):
            return True
        else:
            return False

#picture class
class picture:
    #initializes the picture with a texture and size
    def __init__(self, path):
        self.path = Path(path)
        if not self.path.is_absolute():
            self.path = (BASE_DIR / self.path).resolve()
        self.out_original = pygame.image.load(str(self.path)).convert_alpha()
        self.sizex, self.sizey = self.out_original.get_size()

    #displays the picture on the screen based on the center of the screen
    def show(self, x, y, lscale):
        width = int(self.sizex * lscale)
        height = int(self.sizey * lscale)
        self.out = pygame.transform.scale(self.out_original, (width, height))
        out_rect = self.out.get_rect(center=(midx + x, midy - y))
        screen.blit(self.out, out_rect)

#settings menu build dictionary
settingsbuild = {
    "title": "settings",
    "number_platforms": (10,300,es.settings["number_platforms"]),
    "volume": (0,100,es.settings["volume"]),
    "difficulty": ["normal","easy"],
    "language": ["en","de","fr","es"],
    "skin": list(ingame.folder_names) if len(ingame.folder_names) > 0 else [es.settings["skin"]],
    "color_scheme": sorted(es.color_schemes.keys()),
    "fly": es.settings["fly"],
}

#menu class
class menu:
    #text class
    class text:
        #initializes the text with a key for localization
        def __init__(self, value):
            self.value = value

        #returns the set key for localization
        def __call__(self):
            return self.value

        #returns the height of the text element for layout purposes
        def layout_height(self, lscale):
            return int(34 * lscale)

        #returns the center offset for the text element to align it properly in the menu
        def label_center_offset(self, lscale):
            return int(17 * lscale)

        #displays the text on the screen
        def load(self, x, y, lscale, placeholder):
            text_font = pygame.font.Font(str(pixelfont_path), max(int(24 * lscale), 16))
            text_value = lang.currentlang.get(self.value, self.value)
            text_surface = text_font.render(text_value, True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.midtop = (screen.get_width() // 2, int(y))
            screen.blit(text_surface, text_rect)

    #slider class
    class slider:
        #initializes the slider
        def __init__(self,min,max,value,color):
            self.x = 0
            self.y = 0
            self.lscale = 1
            self.max = max
            self.min = min
            self.default = value
            if value == "none":
                self.value = min
            else:
                self.value = value
            if color == "none":
                self.color = (0,0,255)
            else:
                self.color = (0,0,255)

        #returns the current value of the slider
        def __call__(self):
            return self.value
        
        #returns the height of the slider element for layout purposes
        def layout_height(self, lscale):
            return int(42 * lscale)
        
        #returns the center offset for the slider element to align it properly in the menu
        def label_center_offset(self, lscale):
            return int(7 * lscale)
        
        #loads the slider
        def load(self,x,y,lscale,length):
            #size and hitbox
            upper = self.max
            lower = self.min
            value_range = upper - lower
            min_text_size = 24
            max_text_size = 34
            min_text_px = int(min_text_size * lscale)
            max_text_px = int(max_text_size * lscale)
            if value_range <= 0:
                value_range = 1
            track_height = 14 * lscale
            knob_size = 18 * lscale
            rect = pygame.Rect(int(x), int(y), int(length*lscale), int(track_height))
            hitbox = rect.inflate(int(128 * lscale), int(16 * lscale))
            knob_x = x + (((self.value - lower) / value_range) * length * lscale) - (knob_size / 2)
            rect2 = pygame.Rect(int(knob_x), int(y-((knob_size-track_height)/2)), int(knob_size), int(knob_size))

            #click logic
            if (hitbox.collidepoint(mouse.pos) or rect2.collidepoint(mouse.pos)) and mouse.pressed(1):
                tempvalue = (mouse.x - x) / lscale
                if tempvalue < 0:
                    tempvalue = 0
                elif tempvalue > length:
                    tempvalue = length
                self.value = int(lower + ((tempvalue / length) * value_range))
            
            if value_range == 0:
                interp = 0.0
                text_size = min_text_px
            else:
                interp = (self.value - lower) / value_range
                text_size = int((min_text_size + (max_text_size - min_text_size) * interp) * lscale)
                text_size = max(min_text_px, min(max_text_px, text_size))
            tempfont = pygame.font.Font(str(pixelfont_path), text_size)
            text_surface = tempfont.render(str(self.value), True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.midleft = (x + length*lscale + 14*lscale, y + (track_height / 2))

            #drawing logic
            pygame.draw.rect(screen, self.color, rect)
            pygame.draw.rect(screen, (150, 150, 150), rect2)
            screen.blit(text_surface, text_rect)

    #toggle class
    class toggle:
        #initializes the toggle
        def __init__(self, condition):
            self.condition = condition
            self.default = condition
            self.knobx = 0
            self.lock = 0
            self.speed = 1 

        #returns the current state of the toggle   
        def __call__(self):
            return self.condition
        
        #returns the height of the toggle element for layout purposes
        def layout_height(self, lscale):
            return int(36 * lscale)
        
        #returns the center offset for the toggle element to align it properly in the menu
        def label_center_offset(self, lscale):
            return int(10 * lscale)
        
        #loads the toggle
        def load(self,x,y,lscale, placeholder):
            #size and hitbox
            track_width = int(56 * lscale)
            track_height = int(20 * lscale)
            knob_size = int(28 * lscale)
            rect = pygame.Rect(int(x), int(y), track_width, track_height)
            hitbox = rect.inflate(int(24 * lscale), int(24 * lscale))

            #click logic
            if hitbox.collidepoint(mouse.pos) and mouse.pressed(1) and self.lock == 0:
                if self.condition == True:
                    self.condition = False
                elif self.condition == False:
                    self.condition = True
                else:
                    self.condition = self.default
                self.lock = 1     
            if not mouse.pressed(1):
                self.lock = 0
            
            #animation logic
            if self.condition == True:
                self.knob_x = track_width - knob_size
            elif self.condition == False:
                self.knob_x = 0
            else:
                self.condition = self.default
            
            if self.knobx < self.knob_x:
                self.knobx = min(self.knobx + 8 * self.speed, self.knob_x)
            elif self.knobx > self.knob_x:
                self.knobx = max(self.knobx - 8 * self.speed, self.knob_x)

            max_knob = track_width - knob_size
            if max_knob <= 0:
                self.green = 0
            else:
                self.green = int((255 / max_knob) * self.knobx)
                self.green = max(0, min(self.green, 255))
            self.red = 255 - self.green

            #drawing logic
            pygame.draw.rect(screen, (self.red,self.green,0), rect)
            pygame.draw.rect(screen,(150,150,150),(int(x + self.knobx), int(y-((knob_size-track_height)/2)), knob_size, knob_size))

    #dropdown menu class
    class dropdown:
        #initializes the dropdown menu with a list of selectable options
        def __init__(self, options):
            self.options = list(options)
            self.selected = self.options[0]
            self.open = False
            self.lock = 0
        
        #returns the currently selected option
        def __call__(self):
            return self.selected
        
        #returns the height of the dropdown element for layout purposes
        #when open, the dropdown needs room for every option; when closed, only one row
        def layout_height(self, lscale):
            row_height = 30 * lscale
            if self.open:
                return int(row_height * len(self.options))
            return int(row_height)
        
        #returns the label offset so the menu label stays aligned with the visible row
        def label_center_offset(self, lscale):
            return int(15 * lscale)

        #draws the dropdown and handles open/close and option selection
        def load(self,x,y,lscale, placeholder):
            lx = x
            ly = y
            row_width = 200 * lscale
            row_height = 30 * lscale
            arrow_col_width = max(int(24 * lscale), 18)

            #reset click lock when mouse is released
            if not mouse.pressed(1):
                self.lock = 0

            #open state: draw all options and allow selection
            if self.open:
                counter = 0
                ordered_options = [self.selected] + [opt for opt in self.options if opt != self.selected]
                for option in ordered_options:
                    counter += 1
                    if counter % 2 == 1:
                        color = (166, 115, 68)
                    else:
                        color = (133, 94, 58)

                    rect_y = ly + ((counter - 1) * row_height)
                    hover = lx <= mouse.pos[0] < lx + row_width and rect_y <= mouse.pos[1] < rect_y + row_height
                    if hover:
                        if mouse.pressed(3) and self.lock == 0:
                            self.selected = option
                            self.open = False
                            self.lock = 1
                        color = (
                            min(color[0] + 10, 255),
                            min(color[1] + 10, 255),
                            min(color[2] + 10, 255),
                        )

                    tempfont = pygame.font.Font(str(pixelfont_path), 26*lscale)
                    display_key = f"color_scheme_{option}" if isinstance(option, int) else option
                    text_surface = tempfont.render(lang.currentlang.get(display_key, str(option)), True, (255, 255, 255))

                    pygame.draw.rect(screen, color, (lx, rect_y, row_width, row_height))
                    pygame.draw.rect(screen, (112, 78, 48), (lx, rect_y, arrow_col_width, row_height))
                    pygame.draw.line(screen, (199, 150, 98), (lx + arrow_col_width, rect_y), (lx + arrow_col_width, rect_y + row_height), 1)

                    if counter == 1:
                        arrow_center_x = lx + (arrow_col_width // 2)
                        arrow_center_y = rect_y + (row_height // 2)
                        arrow_size = max(int(4 * lscale), 3)
                        arrow_points = [
                            (arrow_center_x, arrow_center_y - arrow_size),
                            (arrow_center_x - arrow_size, arrow_center_y + arrow_size),
                            (arrow_center_x + arrow_size, arrow_center_y + arrow_size),
                        ]
                        pygame.draw.polygon(screen, (235, 235, 235), arrow_points)

                    text_height = text_surface.get_height()
                    text_y = rect_y + (row_height - text_height) // 2
                    screen.blit(text_surface, (lx + arrow_col_width + 6, text_y - 6))

            #closed state: draw selected option and open arrow
            else:
                rect_y = ly
                color = (166, 115, 68)
                hover = lx <= mouse.pos[0] < lx + row_width and rect_y <= mouse.pos[1] < rect_y + row_height
                if hover:
                    if mouse.pressed(3) and self.lock == 0:
                        self.open = True
                        self.lock = 1
                    color = (
                        min(color[0] + 10, 255),
                        min(color[1] + 10, 255),
                        min(color[2] + 10, 255),
                    )

                tempfont = pygame.font.Font(str(pixelfont_path), 26*lscale)
                display_key = f"color_scheme_{self.selected}" if isinstance(self.selected, int) else self.selected
                text_surface = tempfont.render(lang.currentlang.get(display_key, str(self.selected)), True, (255, 255, 255))

                pygame.draw.rect(screen, color, (lx, rect_y, row_width, row_height))
                pygame.draw.rect(screen, (112, 78, 48), (lx, rect_y, arrow_col_width, row_height))
                pygame.draw.line(screen, (199, 150, 98), (lx + arrow_col_width, rect_y), (lx + arrow_col_width, rect_y + row_height), 1)

                arrow_center_x = lx + (arrow_col_width // 2)
                arrow_center_y = rect_y + (row_height // 2)
                arrow_size = max(int(4 * lscale), 3)
                arrow_points = [
                    (arrow_center_x - arrow_size, arrow_center_y - arrow_size),
                    (arrow_center_x + arrow_size, arrow_center_y - arrow_size),
                    (arrow_center_x, arrow_center_y + arrow_size),
                ]
                pygame.draw.polygon(screen, (235, 235, 235), arrow_points)

                text_height = text_surface.get_height()
                text_y = rect_y + (row_height - text_height) // 2
                screen.blit(text_surface, (lx + arrow_col_width + 6, text_y - 6))

    #initializes the menu
    def __init__(self,name):
        self.name = name
        self.built = {}
        self.empty = 0
        self.scroll_offset = 0
        self.scroll_step = 48
        self.scroll_button_hold = None
        self.scroll_hold_next = 0
        self.scroll_hold_delay = 300
        self.scroll_hold_interval = 80
        self.scroll_key_hold = None
        self.scroll_key_next = 0
        self.scroll_key_delay = 300
        self.scroll_key_interval = 80

    #builds the menu based on a provided dictionary of elements to build
    #uses the type of each value to determine which element class to use and how to initialize it
    def build(self, di):
        for key in di:
            optional1 = "none"
            optional2 = "none"

            if isinstance(di[key], str):
                given = di[key]
                out = self.text(given)
                self.built[key] = out

            if isinstance(di[key], tuple):
                given = di[key]
                if len(given) > 2:
                    if isinstance(given[2], int):
                        optional1 = given[2]
                    elif isinstance(given[2], tuple):
                        optional2 = given[2]
                if len(given) > 3:
                    if isinstance(given[3], tuple):
                        optional2 = given[3]
                    elif isinstance(given[3], int):
                        optional1 = given[3]

                out = self.slider(given[0], given[1], optional1, optional2)
                self.built[key] = out

            if isinstance(di[key], bool):
                given = di[key]
                out = self.toggle(given)
                self.built[key] = out
            
            if isinstance(di[key], list):
                given = di[key]
                out = self.dropdown(given)
                if key in es.settings and es.settings[key] in out.options:
                    out.selected = es.settings[key]
                self.built[key] = out
        
    #displays the menu on the screen and handles scrolling
    def show(self):
        midx, midy, width, height, events, scale = es.basis()
        backroundcolor((200, 160, 80))
        lscale = scale * 2
        element_gap = int(12 * lscale)
        dropdown_extra_gap = int(16 * lscale)
        label_font = pygame.font.Font(str(pixelfont_path), max(int(16 * lscale), 14))
        center_offset = int(50 * lscale)
        control_x = midx + center_offset
        label_right_x = midx - center_offset

        #calculate total menu height to determine scrolling bounds.
        total_height = 0
        for element in self.built:
            current = self.built[element]
            if hasattr(current, "layout_height"):
                total_height += current.layout_height(lscale) + element_gap
            else:
                total_height += int(60 * lscale)
            if isinstance(current, self.dropdown):
                total_height += dropdown_extra_gap
        if total_height > 0:
            total_height -= element_gap

        top_margin = 100
        button_size = int(48 * lscale)
        button_gap = int(16 * lscale)
        #reserve space for the fixed main menu button at the bottom of the settings screen.
        footer_reserved = int(120 * lscale)
        bottom_margin = max(int(40 * lscale), footer_reserved)
        max_offset = 0
        min_offset = min(0, height - top_margin - bottom_margin - total_height)
        self.scroll_offset = max(min_offset, min(max_offset, self.scroll_offset))

        #right-side arrow buttons for scrolling in the vertical center.
        arrow_x = width - 40 - button_size
        arrow_y = height // 2 - ((button_size * 2 + button_gap) // 2)
        up_rect = pygame.Rect(arrow_x, arrow_y, button_size, button_size)
        down_rect = pygame.Rect(arrow_x, arrow_y + button_size + button_gap, button_size, button_size)
        can_scroll = min_offset < max_offset

        hover_up = up_rect.collidepoint(mouse.pos)
        hover_down = down_rect.collidepoint(mouse.pos)
        base_color = (160, 120, 60) if can_scroll else (110, 90, 60)
        hover_color = (220, 190, 120)
        inactive_color = (100, 80, 50)
        up_color = hover_color if hover_up and can_scroll else (base_color if can_scroll else inactive_color)
        down_color = hover_color if hover_down and can_scroll else (base_color if can_scroll else inactive_color)
        border_color = (90, 64, 34)
        pygame.draw.rect(screen, border_color, up_rect, border_radius=10)
        pygame.draw.rect(screen, border_color, down_rect, border_radius=10)
        pygame.draw.rect(screen, up_color, up_rect.inflate(-8, -8), border_radius=8)
        pygame.draw.rect(screen, down_color, down_rect.inflate(-8, -8), border_radius=8)

        up_center = up_rect.center
        down_center = down_rect.center
        arrow_length = int(10 * lscale)
        up_triangle = [
            (up_center[0], up_center[1] - arrow_length),
            (up_center[0] - arrow_length, up_center[1] + arrow_length // 2),
            (up_center[0] + arrow_length, up_center[1] + arrow_length // 2),
        ]
        down_triangle = [
            (down_center[0], down_center[1] + arrow_length),
            (down_center[0] - arrow_length, down_center[1] - arrow_length // 2),
            (down_center[0] + arrow_length, down_center[1] - arrow_length // 2),
        ]
        triangle_color = (255, 243, 217) if can_scroll else (200, 180, 150)
        pygame.draw.polygon(screen, triangle_color, up_triangle)
        pygame.draw.polygon(screen, triangle_color, down_triangle)

        scroll_events = getattr(es, "events_list", None)
        if scroll_events is None:
            scroll_events = [events] if events is not None else []
        for event in scroll_events:
            if event.type == pygame.MOUSEWHEEL and can_scroll:
                self.scroll_offset += -event.y * self.scroll_step
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and can_scroll:
                if up_rect.collidepoint(event.pos):
                    self.scroll_offset += self.scroll_step
                elif down_rect.collidepoint(event.pos):
                    self.scroll_offset -= self.scroll_step
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button in (4, 5) and can_scroll:
                if event.button == 4:
                    self.scroll_offset += self.scroll_step
                elif event.button == 5:
                    self.scroll_offset -= self.scroll_step
            self.scroll_offset = max(min_offset, min(max_offset, self.scroll_offset))

        #scrolling (buttons and arrow keys)
        current_time = pygame.time.get_ticks()
        if can_scroll and mouse.pressed(1) and (hover_up or hover_down):
            held_button = 'up' if hover_up else 'down'
            if self.scroll_button_hold != held_button:
                self.scroll_button_hold = held_button
                self.scroll_hold_next = current_time + self.scroll_hold_delay
            elif current_time >= self.scroll_hold_next:
                if held_button == 'up':
                    self.scroll_offset += self.scroll_step
                else:
                    self.scroll_offset -= self.scroll_step
                self.scroll_hold_next = current_time + self.scroll_hold_interval
            self.scroll_offset = max(min_offset, min(max_offset, self.scroll_offset))
        else:
            self.scroll_button_hold = None

        #support holding the arrow keys.
        keys = pygame.key.get_pressed()
        key_scroll = None
        if can_scroll and keys[pygame.K_UP]:
            key_scroll = 'up'
        elif can_scroll and keys[pygame.K_DOWN]:
            key_scroll = 'down'

        if key_scroll is not None:
            if self.scroll_key_hold != key_scroll:
                self.scroll_key_hold = key_scroll
                self.scroll_key_next = current_time + self.scroll_key_delay
                if key_scroll == 'up':
                    self.scroll_offset += self.scroll_step
                else:
                    self.scroll_offset -= self.scroll_step
            elif current_time >= self.scroll_key_next:
                if key_scroll == 'up':
                    self.scroll_offset += self.scroll_step
                else:
                    self.scroll_offset -= self.scroll_step
                self.scroll_key_next = current_time + self.scroll_key_interval
            self.scroll_offset = max(min_offset, min(max_offset, self.scroll_offset))
        else:
            self.scroll_key_hold = None

        ly = top_margin + self.scroll_offset
        for element in self.built:
            current = self.built[element]
            if isinstance(current, self.text):
                current.load(midx, ly, lscale, 0)
                ly += current.layout_height(lscale) + element_gap
                continue

            label_text = lang.currentlang.get(element, element)
            label_surface = label_font.render(label_text, True, (255, 255, 255))
            label_rect = label_surface.get_rect()
            if hasattr(current, "label_center_offset"):
                label_center_y = ly + current.label_center_offset(lscale)
            else:
                label_center_y = ly + int(current.layout_height(lscale) / 2)
            label_rect.midright = (label_right_x, label_center_y)
            screen.blit(label_surface, label_rect)

            current.load(control_x, ly, lscale, 140)

            #keep runtime settings synchronized with the menu controls.
            if element in es.settings:
                if isinstance(current, self.slider):
                    es.settings[element] = int(current())
                elif isinstance(current, self.toggle):
                    es.settings[element] = bool(current())
                elif isinstance(current, self.dropdown):
                    es.settings[element] = current()

            if lang.getlang() != es.settings["language"]:
                lang.setlang(es.settings["language"])
                lang.updatelang()

            if hasattr(current, "layout_height"):
                ly += current.layout_height(lscale) + element_gap
            else:
                ly += int(60 * lscale)
            if isinstance(current, self.dropdown):
                ly += dropdown_extra_gap
            pass

#create the settings menu using the build dictionary
settingsmenu = menu("settings")
settingsmenu.build(settingsbuild)

#initialize the markdown renderer
md = MarkdownRenderer()
current_info_file = None

#function to display markdown files as info screens
def info(mdfile_path):
    global screen, width, height, current_info_file

    if not Path(mdfile_path).exists():
        print(f"Error: File {mdfile_path} not found.")
        return

    if screen is None:
        screen = pygame.display.get_surface()

    if width is None or height is None:
        width, height = screen.get_size()

    screen.fill((10, 10, 10))

    font_scale = max(1.0, min(width, height) / 500)
    md.set_font_sizes(
        h1=int(32 * font_scale),
        h2=int(28 * font_scale),
        h3=int(24 * font_scale),
        text=int(20 * font_scale),
        code=int(20 * font_scale),
        quote=int(20 * font_scale),
    )
    md.set_color_font(255, 255, 255)
    md.set_color_background(18, 18, 22)
    md.set_line_gaps(10, 40)
    md.set_area(screen, 0, 0, width=width, height=height)

    if mdfile_path != current_info_file:
        md.set_markdown(mdfile_path)
        md.pixel_first_showable = 0
        current_info_file = mdfile_path

    info_events = es.events_list if hasattr(es, 'events_list') else []
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    md.display(info_events, mouse_x, mouse_y, mouse_pressed)

