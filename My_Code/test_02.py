import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen information
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

SPEED = 5

DISPLAYSURF = pygame.display.set_mode((400, 600))  # 常见的表面对象
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.status = True
        self.image = pygame.image.load("Enemy.png")
        # self.image = pygame.image.load("Player.png")
        # self.r = self.image.get_size()
        self.rect = self.image.get_rect()  # This function is able to automatically create a rectangle of the same size as the image.
        # 返回一个矩形(0, 0, w, h)
        # (此功能能够自动创建与图像大小相同的矩形(top, bottom, left, right))
        print(self.rect)
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)  # defines a starting position for the Rect
        # 指定中心点距离左上角(0, 0)的w和h
        print(self.rect.center)
        print(self.rect)
        # Later we’ll use the Rect’s coordinates to draw the image to the exact same location.

    def move(self):
        self.rect.move_ip(0, SPEED)  # (w, h) 中心点向左右或上下移动的像素数(正数为右和下，负数为左和上)
        if self.rect.bottom > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)

    def draw(self, surface):
        if self.status:
            surface.blit(self.image, self.rect)  # 根据self.rect在surface上画出self.image
        else:
            pygame.draw.rect(color=WHITE, rect=self.rect, surface=surface)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.status = True
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        # print(self.rect)
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

    def draw(self, surface):
        if self.status:
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(color=WHITE, rect=self.rect, surface=surface)


# Setting up Sprites
P1 = Player()
E1 = Enemy()
E2 = Enemy()

# Creating Sprites Groups
enemies = pygame.sprite.Group()  # A Sprite group is sort of like a classification.
enemies.add(E1)  # To add a Sprite to a group, you just have to use the add() function.
enemies.add(E2)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(E2)

# Adding a new User event
INC_SPEED = pygame.USEREVENT + 1  # create custom events (add one to ensure that it will have a unique ID)
pygame.time.set_timer(INC_SPEED, 1000)  # call the INC_SPEED event object every 1000 milliseconds

while True:
    DISPLAYSURF.fill(WHITE)  # 写在循环里面

    # Cycles through all events occuring
    for event in pygame.event.get():
        if event.type == INC_SPEED:  # 触发INC_SPEED事件时， SPEED加2
            SPEED += 2

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Moves and Re-draws all Sprites
    for entity in all_sprites:
        # print(entity.alive())
        entity.draw(DISPLAYSURF)  # DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
        '''
        # P1.draw(DISPLAYSURF)
        # E1.draw(DISPLAYSURF)
        # P1.update()
        # E1.move()
        '''

    # To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):  # 第一个参数必须是常规的 Sprite。第二个必须是精灵组.
        # 此函数判断第一个参数中的sprite，是否触及在第二个参数中的组中的任何成员
        DISPLAYSURF.fill(RED)
        for entity in all_sprites:
            entity.kill()
            # entity.status = entity.alive()
            # entity.draw(DISPLAYSURF)
        pygame.display.update()
        time.sleep(2)

        P1 = Player()
        E1 = Enemy()
        E2 = Enemy()
        enemies = pygame.sprite.Group()
        enemies.add(E1)
        enemies.add(E2)
        all_sprites = pygame.sprite.Group()
        all_sprites.add(P1)
        all_sprites.add(E1)
        all_sprites.add(E2)
        SPEED = 5


    pygame.display.update()
    FramePerSec.tick(FPS)
