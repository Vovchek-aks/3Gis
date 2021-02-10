import pygame as pg
from settings import *
import requests
import sys
import os


coords = '133.125502,-28.306867'
scale = '50,30'

map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords}&spn={scale}&l=sat"
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)


pg.init()
sc = pg.display.set_mode(size)

pg.display.set_caption('3Gis')
sc.blit(pg.image.load(map_file), (0, 0))

pg.display.flip()
while pg.event.wait().type != pg.QUIT:
    pass
pg.quit()

os.remove(map_file)


