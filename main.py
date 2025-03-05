import pygame as pg
from settings import *
import requests
import os
import pygame_gui

coords = [133, -28]
overlook = 'sat,skl'


class Button:
    def __init__(self, pos, btn_size, text, mg, func):
        self.btn = pygame_gui.elements.UIButton(
            relative_rect=pg.Rect(pos, btn_size),
            text=text,
            manager=mg)
        self.func = func
        self.cursor_on_self = False

    def object_event(self, ev):
        if ev.type == pg.USEREVENT:
            if ev.ui_element == self.btn:
                if ev.type == 32866:
                    self.cursor_on_self = not self.cursor_on_self
        elif ev.type == pg.MOUSEBUTTONDOWN:
            if ev.button == 1 and self.cursor_on_self:
                self.func()


class BabyBtn(Button):
    def __init__(self, pos, btn_size, text, mg):
        super().__init__(pos, btn_size, text, mg, self.change_name)

    def change_name(self):
        global overlook
        print(overlook)
        if self.btn.text == 'схема':
            self.btn.set_text('спутник')
            overlook = 'map'
        elif self.btn.text == 'спутник':
            self.btn.set_text('гибрид')
            overlook = 'sat'
        elif self.btn.text == 'гибрид':
            self.btn.set_text('схема')
            overlook = 'sat,skl'


class ElementManager:
    def __init__(self, elements_list):
        self.elements = elements_list

    def manager_event(self, ev):
        for i in self.elements:
            i.object_event(ev)


class Scaler:
    def __init__(self, scale=3):
        self.scale = scale

    def set_scale(self, value):
        self.scale = value
        if self.scale > 17:
            self.scale = 17
        elif self.scale < 2:
            self.scale = 2

    def up_scale(self):
        self.set_scale(self.scale + 1)

    def down_scale(self):
        self.set_scale(self.scale - 1)


def tuple_to_str(tpl):
    return f'{tpl[0]},{tpl[1]}'


def load_image(f=False, ll=None):
    global scale
    if ll is not None:
        map_request = ll
    else:
        map_request = link
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return

    if f:
        os.remove(map_file)
    with open(map_file, "wb") as file:
        file.write(response.content)

    return True


scaler = Scaler()


link = ''

load_image(ll=f"http://static-maps.yandex.ru/1.x/?ll={tuple_to_str(coords)}" \
              f"&z={scaler.scale}&l={overlook}&size={tuple_to_str((600, 450))}")

pg.init()
sc = pg.display.set_mode(size)

panel = pg.Surface((width, 55))
panel.fill((255, 255, 255))
panel.set_alpha(100)

gui_manager = pygame_gui.UIManager(size, os.path.join('menu_theme.json'))
font = pg.font.Font(None, 24)
pg.display.set_caption('3Gis')
manager = ElementManager([BabyBtn((10, 10), (100, 35), 'схема', gui_manager)])

while True:

    old_l = link

    link = f"http://static-maps.yandex.ru/1.x/?ll={tuple_to_str(coords)}" \
           f"&z={scaler.scale}&l={overlook}&size={tuple_to_str((600, 450))}"

    if old_l != link and load_image(True):
        sc.blit(pg.transform.scale(pg.image.load(map_file), size), (0, 0))
        sc.blit(panel, (0, 0))
    # sc.blit(font.render('Ошибка', False, red), (100, height // 2))

    for event in pg.event.get():
        manager.manager_event(event)
        if event.type == pg.QUIT:
            os.remove(map_file)
            exit(0)
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:
                scaler.up_scale()
            elif event.button == 5:
                scaler.down_scale()

        elif event.type == pg.KEYDOWN:
            if event.key in {pg.K_PAGEDOWN, pg.K_PAGEUP}:
                if event.key == pg.K_PAGEUP:
                    scaler.up_scale()
                else:
                    scaler.down_scale()

            elif event.key in {pg.K_LEFT, pg.K_RIGHT}:
                x = mtsh / scaler.scale ** 4
                coords[0] += x if event.key == pg.K_RIGHT else -x
                if coords[0] > 180:
                    coords[0] = -180
                elif coords[0] < -180:
                    coords[0] = 180
            elif event.key in {pg.K_UP, pg.K_DOWN}:
                x = mtsh / scaler.scale ** 4
                coords[1] += x if event.key == pg.K_UP else -x
                if coords[1] < -70:
                    coords[1] = -70
                elif coords[1] > 80:
                    coords[1] = 80
    gui_manager.update(FPS / 1000)
    gui_manager.draw_ui(sc)
    pg.display.flip()
