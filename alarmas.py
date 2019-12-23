import pygame
import pygame.mixer
import boton
import draw
import time

class Alarmas:
    def __init__(self):
        self.App = None
        self._image_surf = None
        self.alarmas = {}
        self.texto = None
        self.botones = []

        self.pulsado = False
        self.currPos = None
        self.tiempo = None

    def cerrar(self):
        self.App.go_configSCR()
        pass

    def setAlarma(self, n):
        print(self.App.config["Alarmas"][n]["Nombre"])

    def on_init(self, app):
        self.App = app

        self.texto = pygame.font.SysFont("DroidSansMono", 72)
        self._image_surf = pygame.image.load("fondo.jpg").convert()

        self.botones.append(boton.Boton(app, (self.App._display_surf.get_width() - 65, 5, 60, 30), self.cerrar))

        for i, a in enumerate(self.App.config["Alarmas"], start=0):
            self.botones.append(boton.Boton(app, (10, 50+(i*60), 400, 50), self.setAlarma, None, a["Nombre"],i))

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

        pass

    def render(self):
        self.App._display_surf.blit(self._image_surf, (0, 0))
        draw.drawTextShadow("Menu", self.App, (255, 255, 255), (10, 10, 100, 100))

        self.botones[0].render()

        self.App._display_surf.set_clip((0, 50, 480, 380))
        for b in self.botones[1:]:
            b.render()

        self.App._display_surf.set_clip(None)

        pygame.display.flip()

        pass

    def doProc(self):
        if self.pulsado:
            antPos = self.currPos

            self.currPos = pygame.mouse.get_pos()
            diff = self.currPos[1] - antPos[1]

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
