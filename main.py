import pygame as pg
from settings import *
import requests
import sys
import os

coords = '133.125502,-28.306867'
scale = 1


def load_image(f=False):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords}&spn={(width / scale) / 10},{(height / scale) / 10}&l=sat&size={width},{height}"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    if f:
        os.remove(map_file)
    with open(map_file, "wb") as file:
        file.write(response.content)


load_image()

pg.init()
sc = pg.display.set_mode(size)

pg.display.set_caption('3Gis')

while True:
    load_image(True)
    sc.blit(pg.image.load(map_file), (0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            os.remove(map_file)
            exit(0)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_PAGEDOWN:
                scale //= 2
            elif event.key == pg.K_PAGEUP:
                scale *= 2

    if scale > 1024:
        scale = 1024
    elif scale < 1:
        scale = 1

    pg.display.flip()


