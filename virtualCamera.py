_author__ = 'marcin'

import pygame
import pygame.gfxdraw as draw
import sys
from model import ObjectBuilder, VirtualCamera


def drawLines(surface, lines, color):
    size = surface.get_size()
    for s, e in lines:
        pygame.draw.line(surface, color,
                         (size[0] / 2 + s[0][0], size[1] / 2 + s[1][0]),
                         (size[0] / 2 + e[0][0], size[1] / 2 + e[1][0])
        )


pygame.init()
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

clock = pygame.time.Clock()

lines = ObjectBuilder.build_cuboid((0, 125, 0), 100, 250, 100)
lines += ObjectBuilder.build_cuboid((-70, 50, -70), 50, 100, 50)
lines += ObjectBuilder.build_cuboid((70, 50, 70), 50, 100, 50)
lines += ObjectBuilder.build_cuboid((-70, 50, 70), 50, 100, 50)
lines += ObjectBuilder.build_cuboid((70, 50, -70), 50, 100, 50)
lines += ObjectBuilder.build_cuboid((0, 300, 0), 75, 100, 75)

virtCam = VirtualCamera()
virtCam.setFocalLen(300)

screen = pygame.display.set_mode((500, 500))
screen.fill((255, 0, 0))
s = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
black = (0, 0, 0)
white = (255, 255, 255)
colored = (127, 100, 200)
drawLines(s, lines, black)
screen.blit(s, (0, 0))
pygame.display.flip()


def move(x, y):
    for ps, pe in lines:
        ps[0][0] += x
        pe[0][0] += x
        ps[1][0] -= y
        pe[1][0] -= y


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            x, y = pygame.mouse.get_rel()
            virtCam.ang_x += x / 40.0
            virtCam.ang_y -= y / 40.0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_DOWN:
                virtCam.y -= 30
            if event.key == pygame.K_UP:
                virtCam.y += 30

            if event.key == pygame.K_RIGHT:
                virtCam.x -= 30
            if event.key == pygame.K_LEFT:
                virtCam.x += 30

            if event.key == pygame.K_KP_PLUS:
                virtCam.focalLen += 5
            if event.key == pygame.K_KP_MINUS:
                virtCam.focalLen -= 5

            if event.key == pygame.K_w:
                virtCam.z += 30
            if event.key == pygame.K_s:
                virtCam.z -= 30

            if event.key == pygame.K_q:
                virtCam.ang_z += 10
            if event.key == pygame.K_e:
                virtCam.ang_z -= 10
            if event.key == pygame.K_z:
                virtCam.move_camera(30, 0, 0)
            if event.key == pygame.K_x:
                virtCam.move_camera(-30, 0, 0)
            if event.key == pygame.K_a:
                virtCam.move_camera(0, 30, 0)
            if event.key == pygame.K_d:
                virtCam.move_camera(0, -30, 0)

    s.fill(colored)
    res = virtCam.get2Dcast(lines)
    drawLines(s, res, black)
    screen.blit(s, (0, 0))
    pygame.display.flip()
    clock.tick(60)





