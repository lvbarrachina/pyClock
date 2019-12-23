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
        t2=(datetime.datetime.today()-self.iniciado).seconds
        if t2 % 2 == 1:
            pygame.draw.rect(self.App._display_surf, (255, 0, 0), (30, 30, 200, 100), 2)
        else:
            pygame.draw.rect(self.App._display_surf, (255, 255, 255), (30,30,200,100), 2)

        if t2 > 60*2:
            self.stop()
            pass

    def doProc(self):
        pass
