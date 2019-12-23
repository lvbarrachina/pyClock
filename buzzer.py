import pygame
import datetime
import boton


class Buzzer():
    def __init__(self, a, app):
        self.alarm = a
        self.iniciado = datetime.datetime.today();

        pygame.mixer.music.load("data/music.mp3")
        pygame.mixer.music.play()

        self.App = app
        self.bStop = boton.Boton(app, (15, 50, 60, 50), self.stop)

    def stop(self):
        pygame.mixer.music.stop()
        self.App.do_stopAlarm()

    def click(self):
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]

        b = self.bStop
        if (x >= b.pos[0]) and (x <= b.pos[0] + b.pos[2]) and (y >= b.pos[1]) and (y <= b.pos[1] + b.pos[3]):
            b.click()

    def render(self):
        self.bStop.render()

    def doProc(self):
        pass
