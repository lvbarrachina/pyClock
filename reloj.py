import pygame
import pygame.mixer
import boton

from datetime import date, datetime
import os
from random import seed, randint

class Reloj:
    def __init__(self):
        self.App = None
        self._image_surf = None
        self.texto = None
        self.files = []
        self.botones = []
        self.alarmON = False

    def config(self):
        print("Config")
        self.App.go_configSCR()
        del self

    def alarm1(self):
        if self.alarmON == False:
            self.alarmON = True
            pygame.mixer.music.load("data/music.mp3")
            pygame.mixer.music.play()
        else:
            self.alarmON = False
            pygame.mixer.music.stop()
        print("Alarma 1")

    def on_init(self, app):
        self.App = app

        self.texto = pygame.font.SysFont("DroidSansMono", 72)

        formatos = [".bmp", ".png", "jpeg", ".jpg"]
        for r, d, f in os.walk("data"):
            for file in f:
                if any(formato in file for formato in formatos):
                    self.files.append(os.path.join(r, file))
                    print(file)

        seed()
        self._image_surf = pygame.image.load(self.files[randint(0, len(self.files)-1)]).convert()

        self.botones.append(boton.Boton(app, (self.App._display_surf.get_width() - 65, 5, 60, 30), self.config))
        self.botones.append(boton.Boton(app, (self.App._display_surf.get_width() - (65 * 2), 5, 60, 30), self.alarm1,
                                        "icons/bell-2x.png"))

    def click(self):
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]

        for b in self.botones:
            if (x >= b.pos[0]) and (x <= b.pos[0] + b.pos[2]) and (y >= b.pos[1]) and (y <= b.pos[1] + b.pos[3]):
                b.click()

    def doProc(self):
        pass

    def render(self):
        if (datetime.now().second % 2) == 1:
            if datetime.now().second < 30:
                strHora = datetime.now().strftime("%H %M")
            else:
                strHora = datetime.now().strftime("%H.%M")
        else:
            strHora = datetime.now().strftime("%H:%M")

        self.App._display_surf.blit(self._image_surf, (0, 0))
        horaSurface = self.texto.render(strHora, True, (255, 255, 255))
        surface = pygame.Surface(self.texto.size(strHora))

        surface.fill((0, 0, 0))
        surface.set_colorkey((0, 0, 0))
        surface.blit(horaSurface, (0, 0))
        surface.set_alpha(50)

        self.App._display_surf.blit(surface, (4, 4))
        surface.set_alpha(255)

        self.App._display_surf.blit(surface, (0, 0))

        for b in self.botones:
            b.render()

        pygame.display.flip()
