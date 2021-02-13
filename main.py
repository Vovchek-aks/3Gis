import pygame as pg
from settings import *
import requests
import sys
import os
import pygame_gui
import pygame

WIDTH = 600
HEIGHT = 450
coords = '133.125502,-28.306867'
scale = '50,30'
sat = ['', '&l', 'l=sat%2Cskl&l']

map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords}&spn={scale}&l=sat{sat}"
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)


def start_screen():
    manager = pygame_gui.UIManager((WIDTH, HEIGHT), os.path.join('data', 'menu_theme.json'))
    outlook_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 75, HEIGHT // 3 + 55), (150, 50)),
        text='спутник',
        manager=manager
    )
    while True:
        sat_choice = sat[0]
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == outlook_btn:
                        sat_choice = sat[1]
            manager.process_events(event)
        manager.draw_ui(screen)
        pygame.display.flip()

pg.init()
sc = pg.display.set_mode(size)

pg.display.set_caption('3Gis')
sc.blit(pg.image.load(map_file), (0, 0))

pg.display.flip()
while pg.event.wait().type != pg.QUIT:
    pass
pg.quit()

os.remove(map_file)

