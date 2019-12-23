import pygame
import boton
import draw

import datetime

class SetAlarm:
    def __init__(self):
        self.App = None
        self.botones = []

        self.pulsado = 0
        self.iniPulsado = datetime.datetime.today()

    def menosHoras(self):
        self.App.config["Alarmas"][self.currAlarm]["Hora"] -= 1
        if self.App.config["Alarmas"][self.currAlarm]["Hora"] < 0:
            self.App.config["Alarmas"][self.currAlarm]["Hora"] = 23

    def menosMinutos(self):
        self.App.config["Alarmas"][self.currAlarm]["Minuto"] -= 1
        if self.App.config["Alarmas"][self.currAlarm]["Minuto"] < 0:
            self.App.config["Alarmas"][self.currAlarm]["Minuto"] = 59

    def masHoras(self):
        self.App.config["Alarmas"][self.currAlarm]["Hora"] += 1
        if self.App.config["Alarmas"][self.currAlarm]["Hora"] > 23:
            self.App.config["Alarmas"][self.currAlarm]["Hora"] = 0

    def masMinutos(self):
        self.App.config["Alarmas"][self.currAlarm]["Minuto"] += 1
        if self.App.config["Alarmas"][self.currAlarm]["Minuto"] > 59:
            self.App.config["Alarmas"][self.currAlarm]["Minuto"] = 0

    def on_init(self, app, n):
        self.App = app
        self.texto = pygame.font.SysFont("DroidSansMono", 72)
        self.currAlarm = n

        self.horaInicial = app.config["Alarmas"][self.currAlarm]["Hora"]
        self.minutoInicial = app.config["Alarmas"][self.currAlarm]["Minuto"]

        self._image_surf = pygame.image.load("fondo.jpg").convert()

        self.botones.append(boton.Boton(app, (self.App._display_surf.get_width() - 65, 5, 60, 30), self.cerrar))

        self.botones.append(boton.Boton(app, (50, 30, 60, 30), self.menosHoras))
        self.botones.append(boton.Boton(app, (150, 30, 60, 30), self.menosMinutos))

        self.botones.append(boton.Boton(app, (50, 100, 60, 30), self.masHoras))
        self.botones.append(boton.Boton(app, (150, 100, 60, 30), self.masMinutos))

    def cerrar(self):
        self.App.config["Alarmas"][self.currAlarm]["Last"] = str(datetime.date.today())
        if self.horaInicial != self.App.config["Alarmas"][self.currAlarm]["Hora"] or self.minutoInicial != self.App.config["Alarmas"][self.currAlarm]["Minuto"]:
            if self.App.config["Alarmas"][self.currAlarm]["Hora"] > datetime.datetime.today().hour or \
                    (self.App.config["Alarmas"][self.currAlarm]["Hora"] == datetime.datetime.today().hour
                     and self.App.config["Alarmas"][self.currAlarm]["Minuto"] > datetime.datetime.today().minute):
                self.App.config["Alarmas"][self.currAlarm]["Last"] = str(datetime.date.today()+datetime.timedelta(days=-1))

        self.App.go_alarmas()

    def doProc(self):
        if pygame.mouse.get_pressed()[0]:
            for b, btn in enumerate(self.botones[1:]):
                pos = pygame.mouse.get_pos()
                x = pos[0]
                y = pos[1]

                if (x >= btn.pos[0]) and (x <= btn.pos[0] + btn.pos[2]) and (y >= btn.pos[1]) and (
                        y <= btn.pos[1] + btn.pos[3]):
                    if b + 1 != self.pulsado or self.iniPulsado is None:
                        self.pulsado = b + 1
                        self.iniPulsado = datetime.datetime.today()

                    else:
                        if (datetime.datetime.today()-self.iniPulsado).microseconds > 300000:
                            self.iniPulsado = datetime.datetime.today()
                            self.click()
        else:
            self.pulsado = 0
            self.iniPulsado = None

    def click(self):
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        for b in self.botones:
            if (x >= b.pos[0]) and (x <= b.pos[0] + b.pos[2]) and (y >= b.pos[1]) and (
                    y <= b.pos[1] + b.pos[3]):
                b.click()

    def render(self):
        self.App._display_surf.blit(self._image_surf, (0, 0))
        draw.drawTextShadow(self.App.config["Alarmas"][self.currAlarm]["Nombre"], self.App, (255, 255, 255),
                            (10, 10, 100, 100))
        draw.drawTextShadow(str(self.App.config["Alarmas"][self.currAlarm]["Hora"]) + ":" +
                            str(self.App.config["Alarmas"][self.currAlarm]["Minuto"]), self.App, (255, 255, 255),
                            (60, 80, 200, 100))
        for b in self.botones:
            b.render()
