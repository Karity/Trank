import sys
import pygame
from pygame.locals import *
import random

'''
#Game loop begins and quit
while True:
    # Code
    # More Code
    .
    .
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
'''
# pygame.draw.rect(surface, color, rectangle_tuple, width)
# '''
#     surface: on which pygame will draw the shape.
#     width: an optional parameter, determines the size of the outline of the shape.
# '''
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def game_base(w=500, h=500):
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((w, h))  # a tuple containing the width and height
    DISPLAYSURF.fill(color=(255, 255, 255))
    pygame.display.set_caption('test_01')
    return DISPLAYSURF


def game_loop(DISPLAYSURF, FPS):
    FramePerSec = pygame.time.Clock()  # Frames per second (FPS, 帧率)
    while True:
        # DISPLAYSURF.fill(WHITE)  # 相当于背景，要写在循环中
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:  # The type attribute tells us what kind of event the object represents.
                pygame.quit()
                sys.exit()
        FramePerSec.tick(FPS)


def base_surface():
    DISPLAYSURF = game_base()

    # FPS = 60
    # FramePerSec = pygame.time.Clock()  # Frames per second (FPS, 帧率)
    # FramePerSec.tick(FPS)

    mySurface = pygame.Surface((40, 50))  # 创建 Surface 对象
    mySurface.fill(color=(0, 0, 0))
    DISPLAYSURF.blit(mySurface, (1, 1))  # 将mySurface在DISPLAYSURF的(1,1)位置显示

    # Creating Lines and Shapes
    pygame.draw.line(DISPLAYSURF, BLUE, (150, 130), (130, 170))
    pygame.draw.line(DISPLAYSURF, BLUE, (150, 130), (170, 170))
    pygame.draw.line(DISPLAYSURF, GREEN, (130, 170), (170, 170))
    pygame.draw.circle(DISPLAYSURF, BLACK, (100, 50), 30)
    pygame.draw.circle(DISPLAYSURF, BLACK, (200, 50), 30)
    pygame.draw.rect(DISPLAYSURF, RED, (100, 200, 100, 50), width=2)
    pygame.draw.rect(DISPLAYSURF, BLACK, (110, 260, 80, 5))

    game_loop(DISPLAYSURF, 60)


def load_surface_rect():
    DISPLAYSURF = game_base()

    img = pygame.image.load('Player.png')
    DISPLAYSURF.blit(source=img, dest=(100, 50))
    img_rect = img.get_rect()
    print('img\'s rect1:', img_rect)
    print(img_rect.center)

    print('----change center----')
    img_rect.center = (22, 48)  # 通过改变矩形(surface)的中心点, 可以改变矩形(surface)的位置
    print('img\'s rect2:', img_rect)
    print(img_rect.center)
    DISPLAYSURF.blit(source=img, dest=img_rect)

    print('----change center----')
    img_rect.move_ip(10, -10)  # (w, h) 中心点向左右或上下移动的像素数(正数为右和下，负数为左和上)
    print('img\'s rect3:', img_rect)
    print(img_rect.center)
    DISPLAYSURF.blit(source=img, dest=img_rect)
    game_loop(DISPLAYSURF, 60)


def font_background():
    background = pygame.image.load('AnimatedStreet.png')
    (w, h) = background.get_size()
    DISPLAYSURF = game_base(w, h)
    # Setting up Fonts
    font = pygame.font.SysFont("Verdana", 60)
    font_small = pygame.font.SysFont("Verdana", 20)
    game_over = font.render("Game Over", True, BLACK)

    DISPLAYSURF.blit(source=background, dest=(0, 0))  # 先绘制背景，并且放在循环中
    DISPLAYSURF.blit(source=game_over, dest=(50, 50))

    game_loop(DISPLAYSURF, 60)


if __name__ == '__main__':
    # base_surface()
    # load_surface_rect()
    font_background()
