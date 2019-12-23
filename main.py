import os

import pygame
from reloj import Reloj
from config import ConfigMenu
from alarmas import Alarmas
from buzzer import Buzzer

from pygame.locals import *
# from datetime import date, datetime
import datetime
import json


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 480, 320
        self.actual = None
        self.texto = None
        self.config = {}
        self.buzzerActivo = None

    def test_alarm(self):
        d1 = datetime.date.today()
        t1 = datetime.datetime.today()

        for i, a in enumerate(self.config['Alarmas']):
            d2 = datetime.datetime.strptime(str(a["Last"]), "%Y-%m-%d").date()

            if d1 > d2:
                if t1.weekday() in a['Dias']:
                    if t1.hour == a["Hora"] and t1.minute == a["Minuto"]:
                        print("Es el momento de " + a["Nombre"])
                        self.config["Alarmas"][i]["Last"] = str(datetime.date.today())
                        print(self.config["Alarmas"][i]["Last"])
                        self.buzzerActivo = Buzzer(a, self)

    def do_stopAlarm(self):
        self.buzzerActivo = None
        pass

    def on_init(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        if os.path.exists('config.txt'):
            with open('config.txt') as json_file:
                self.config = json.load(json_file)
        else:
            self.config['Alarmas'] = [{"Nombre": "Alarma 1", "Hora": 13, "Minuto": 2, "Dias": [0, 2, 4, 6],
                                       "Last": str(datetime.date.today()+datetime.timedelta(days=-1))},
                                      {"Nombre": "Alarma 2", "Hora": 13, "Minuto": 3, "Dias": [1, 3, 5],
                                       "Last": str(datetime.date.today()+datetime.timedelta(days=-1))},
                                      {"Nombre": "Alarma 3", "Hora": 13, "Minuto": 4, "Dias": [0, 3, 5],
                                       "Last": str(datetime.date.today()+datetime.timedelta(days=-1))}]

        self.texto = pygame.font.Font("DroidSansMono.ttf", 48)
        # self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

        self.actual = Reloj()
        self.actual.on_init(self)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.buzzerActivo is None:
                self.buzzerActivo.click()

            self.actual.click()

    def on_loop(self):
        self.actual.doProc()
        self.test_alarm()

        if not (self.buzzerActivo is None):
            self.buzzerActivo.doProc()
        pass

    def on_render(self):
        self.actual.render()
        if not (self.buzzerActivo is None):
            self.buzzerActivo.render()

        pygame.display.flip()
        pass

    def on_cleanup(self):
        with open('config.txt', 'w') as outfile:
            json.dump(self.config, outfile)

        pygame.quit()

    def go_configSCR(self):
        self.actual = ConfigMenu()
        self.actual.on_init(self)

    def go_mainSCR(self):
        self.actual = Reloj()
        self.actual.on_init(self)

    def go_alarmas(self):
        self.actual = Alarmas()
        self.actual.on_init(self)

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
