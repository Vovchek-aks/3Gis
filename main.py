import pygame as pg
from settings import *
import requests
import sys
import os
import pygame_gui

coords = [133, -28]
scale = 3
x = 1



def tuple_to_str(tpl):
    return f'{tpl[0]},{tpl[1]}'


def load_image(f=False):
    global scale
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={tuple_to_str(coords)}" \
                  f"&z={scale}&l={sat[x]},skl&size={tuple_to_str((600, 450))}"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        scale -= 1
        return

    if f:
        os.remove(map_file)
    with open(map_file, "wb") as file:
        file.write(response.content)

    return True


def change_name():
    global x
    if outlook_btn.text == 'гибрид':
        outlook_btn.set_text('схема')
        x = 2
    elif outlook_btn.text == 'схема':
        outlook_btn.set_text('спутник')
        x = 0
    elif outlook_btn.text == 'спутник':
        outlook_btn.set_text('гибрид')
        x = 1


load_image()

pg.init()
sc = pg.display.set_mode(size)

manager = pygame_gui.UIManager(size, os.path.join('menu_theme.json'))
outlook_btn = pygame_gui.elements.UIButton(
    relative_rect=pg.Rect((10, 10), (100, 30)),
    text='гибрид',
    manager=manager)
font = pg.font.Font(None, 24)
pg.display.set_caption('3Gis')

while True:
    if load_image(True):
        sc.blit(pg.transform.scale(pg.image.load(map_file), size), (0, 0))
    # sc.blit(font.render(tuple_to_str(coords), False, red), (10, 10))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            os.remove(map_file)
            exit(0)
        elif event.type == pg.USEREVENT:
            if event.user_type == 3:
                if event.ui_element == outlook_btn:
                    change_name()
        elif event.type == pg.KEYDOWN:
            if event.key in {pg.K_PAGEDOWN, pg.K_PAGEUP}:
                scale += -1 if event.key == pg.K_PAGEDOWN else 1
                if scale > 17:
                    scale = 17
                elif scale < 0:
                    scale = 0
            elif event.key in {pg.K_LEFT, pg.K_RIGHT}:
                x = mtsh / scale ** 4
                coords[0] += x if event.key == pg.K_RIGHT else -x
                if coords[0] > 180:
                    coords[0] = -180
                elif coords[0] < -180:
                    coords[0] = 180
            elif event.key in {pg.K_UP, pg.K_DOWN}:
                x = mtsh / scale ** 4
                coords[1] += x if event.key == pg.K_UP else -x
                if coords[1] < -85:
                    coords[1] = -85
                # elif coords[1] < 0:
                #     coords[1] = 180
    manager.update(FPS / 1000)
    manager.draw_ui(sc)
    pg.display.flip()
