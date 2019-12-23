import pygame

def drawTextShadow(texto,app,color,pos):
    nombreSurface = app.texto.render(texto, False, color)
    surface = pygame.Surface(app.texto.size(texto))

    surface.fill((0, 0, 0))
    surface.set_colorkey((0, 0, 0))
    surface.blit(nombreSurface, (0, 0))
    surface.set_alpha(50)

    app._display_surf.blit(surface, pos)
    surface.set_alpha(255)

    app._display_surf.blit(surface, (pos[0] + 4, pos[1] + 4))
