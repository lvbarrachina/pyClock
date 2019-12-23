import pygame
import draw

class Boton:
    def __init__(self, app, pos, evento, bitmap=None, nombre=None, param=None):
        self.pos = list(pos)
        self.posIcono = list(pos)
        self.App = app
        self.evento = evento
        self.icono = None
        self.nombre = None

        if bitmap is not None:
            self.icono = pygame.image.load(bitmap)

            self.posIcono[0] = self.pos[0] + (self.pos[2] / 2) - (self.icono.get_width() / 2)
            self.posIcono[1] = self.pos[1] + (self.pos[3] / 2) - (self.icono.get_height() / 2)

        if nombre is not None:
            self.nombre = nombre
            tamTexto = self.App.texto.size(nombre)
            self.posIcono[0] = self.pos[0] + (self.pos[2] / 2) - (tamTexto[0] / 2)
            self.posIcono[1] = self.pos[1] + (self.pos[3] / 2) - (tamTexto[1] / 2)

        self.param = param

    def render(self):
        if self.nombre is not None:
            nombreSurface = self.App.texto.render(self.nombre, False, (255, 255, 255))
            surface = pygame.Surface(self.App.texto.size(self.nombre))

            surface.fill((0, 0, 0))
            surface.set_colorkey((0, 0, 0))
            surface.blit(nombreSurface, (0, 0))
            surface.set_alpha(50)

            self.App._display_surf.blit(surface, self.posIcono)
            surface.set_alpha(255)

            self.App._display_surf.blit(surface, (self.posIcono[0] + 4, self.posIcono[1] + 4))

        elif self.icono is not None:
            self.App._display_surf.blit(self.icono, self.posIcono)
        # else:
        pygame.draw.rect(self.App._display_surf, (255, 255, 255), self.pos, 2)

    def click(self):
        if self.param is not None:
            self.evento(self.param)
        else:
            self.evento()
