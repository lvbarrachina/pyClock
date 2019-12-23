import pygame
import boton
import draw

# from reloj import Reloj
from pygame.locals import *
import time
import os


class ConfigMenu:
    def __init__(self):
        self.App = None
        self._image_surf = None
        self.botones = []
        self.texto = None

        self.pulsado = False
        self.currPos = None
        self.tiempo = None

    def dummy(self):
        print("Nada")

    def cerrar(self):
        print("Reloj")
        self.App.go_mainSCR()

    def alarmas(self):
        print("Alarmas")
        self.App.go_alarmas()

    def on_init(self, app):
        self.App = app
        self.texto = pygame.font.SysFont("DroidSansMono", 72)

        self._image_surf = pygame.image.load("fondo.jpg").convert()

        self.botones.append(boton.Boton(app, (self.App._display_surf.get_width() - 65, 5, 60, 30), self.cerrar))
        self.botones.append(boton.Boton(app, (10, 50, 400, 50), self.dummy, None, "Reloj"))
        self.botones.append(boton.Boton(app, (10, 110, 400, 50), self.alarmas, None, "Alarmas"))
        self.botones.append(boton.Boton(app, (10, 170, 400, 50), self.dummy, None, "Musica"))
        self.botones.append(boton.Boton(app, (10, 230, 400, 50), self.dummy, None, "Imagenes"))
        self.botones.append(boton.Boton(app, (10, 290, 400, 50), self.dummy, None, "Calendario"))
        self.botones.append(boton.Boton(app, (10, 350, 400, 50), self.cerrar, None, "Salir"))

    def doProc(self):
        if self.pulsado:
            antPos = self.currPos

            self.currPos = pygame.mouse.get_pos()
            diff = self.currPos[1] - antPos[1]
            #print(diff)

            for b in self.botones[1:]:
                b.pos[1] += diff
                b.posIcono[1] += diff

        if not pygame.mouse.get_pressed()[0] and self.pulsado:
            self.pulsado = False

            if (int(round(time.time() * 1000))-self.tiempo) < 250:
                pos = pygame.mouse.get_pos()
                x = pos[0]
                y = pos[1]

                for b in self.botones:
                    if (x >= b.pos[0]) and (x <= b.pos[0] + b.pos[2]) and (y >= b.pos[1]) and (
                            y <= b.pos[1] + b.pos[3]):
                        b.click()

    def click(self):
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]

        for b in self.botones[0:1]:
            if (x >= b.pos[0]) and (x <= b.pos[0] + b.pos[2]) and (y >= b.pos[1]) and (y <= b.pos[1] + b.pos[3]):
                b.click()
                return

        if pygame.mouse.get_pressed()[0] and not self.pulsado:
            self.pulsado = True
            self.currPos = pygame.mouse.get_pos()
            self.tiempo = int(round(time.time() * 1000))

    def render(self):
        self.App._display_surf.blit(self._image_surf, (0, 0))
        draw.drawTextShadow("Menu", self.App, (255, 255, 255), (10, 10, 100, 100))

        self.botones[0].render()

        self.App._display_surf.set_clip((0, 50, 480, 380))
        for b in self.botones[1:]:
            b.render()

        self.App._display_surf.set_clip(None)

