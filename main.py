import os

import pygame
from reloj import Reloj
from config import ConfigMenu
from alarmas import Alarmas
from pygame.locals import *
#from datetime import date, datetime
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

    def test_alarm(self):
        t1=datetime.datetime.today()
        for a in self.config['Alarmas']:
            #print(a['Dias'])
            if t1.weekday() in a['Dias']:
                if t1.hour==a["Hora"] and t1.minute==a["Minuto"]:
                    print("Es el momento de "+a["Nombre"])

    def on_init(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        if os.path.exists('config.txt'):
            with open('config.txt') as json_file:
                self.config = json.load(json_file)
        else:
            self.config['Alarmas'] = [{"Nombre": "Alarma 1", "Hora": 9, "Minuto":51, "Dias": [0,2,4,6], "Last":str(datetime.datetime.today())},
                                      {"Nombre": "Alarma 2", "Hora": 10, "Minuto":0, "Dias": [1,3,5], "Last":str(datetime.datetime.today())}]

        t1=datetime.datetime.today()
        for a in self.config['Alarmas']:
            #print(a['Dias'])
            if t1.weekday() in a['Dias']:
                if t1.hour==a["Hora"] and t1.minute==a["Minuto"]:
                    print("Es el momento de "+a["Nombre"])


        self.texto = pygame.font.Font("DroidSansMono.ttf", 48)
        #self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

        self.actual = Reloj()
        self.actual.on_init(self)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.actual.click()

    def on_loop(self):
        self.actual.doProc()
        self.test_alarm()
        pass

    def on_render(self):
        self.actual.render()
        pass

    def on_cleanup(self):
        with open('config.txt', 'w') as outfile:
            json.dump(self.config, outfile)

        pygame.quit()

    def go_configSCR(self):
        self.actual=ConfigMenu()
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
