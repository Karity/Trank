import pygame
from pygame.locals import *
import sys
import random, time
from tkinter import filedialog
from tkinter import *

pygame.init()  # Begin pygame

# Declaring variables to be used through the program
vec = pygame.math.Vector2
HEIGHT = 350
WIDTH = 700
ACC = 0.3
FRIC = -0.10  # 摩擦
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bgimage = pygame.image.load("Background.png")
        self.bgY = 0
        self.bgX = 0

    def render(self):
        displaysurface.blit(source=self.bgimage, dest=(self.bgX, self.bgY))


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Ground.png")
        self.rect = self.image.get_rect(center=(350, 350))

    def render(self):
        displaysurface.blit(self.image, (self.rect.x, self.rect.y))


player_list = {
    'RIGHT': pygame.image.load('Player_Sprite_R.png'),
    'LIFT': pygame.image.load('Player_Sprite_L.png')
}
# Run animation for the RIGHT
run_ani_R = [pygame.image.load("Player_Sprite_R.png"), pygame.image.load("Player_Sprite2_R.png"),
             pygame.image.load("Player_Sprite3_R.png"), pygame.image.load("Player_Sprite4_R.png"),
             pygame.image.load("Player_Sprite5_R.png"), pygame.image.load("Player_Sprite6_R.png"),
             pygame.image.load("Player_Sprite_R.png")]

# Run animation for the LEFT
run_ani_L = [pygame.image.load("Player_Sprite_L.png"), pygame.image.load("Player_Sprite2_L.png"),
             pygame.image.load("Player_Sprite3_L.png"), pygame.image.load("Player_Sprite4_L.png"),
             pygame.image.load("Player_Sprite5_L.png"), pygame.image.load("Player_Sprite6_L.png"),
             pygame.image.load("Player_Sprite_L.png")]
# Attack animation for the RIGHT
attack_ani_R = [pygame.image.load("Player_Sprite_R.png"), pygame.image.load("Player_Attack_R.png"),
                pygame.image.load("Player_Attack2_R.png"), pygame.image.load("Player_Attack2_R.png"),
                pygame.image.load("Player_Attack3_R.png"), pygame.image.load("Player_Attack3_R.png"),
                pygame.image.load("Player_Attack4_R.png"), pygame.image.load("Player_Attack4_R.png"),
                pygame.image.load("Player_Attack5_R.png"), pygame.image.load("Player_Attack5_R.png"),
                pygame.image.load("Player_Sprite_R.png")]

# Attack animation for the LEFT
attack_ani_L = [pygame.image.load("Player_Sprite_L.png"), pygame.image.load("Player_Attack_L.png"),
                pygame.image.load("Player_Attack2_L.png"), pygame.image.load("Player_Attack2_L.png"),
                pygame.image.load("Player_Attack3_L.png"), pygame.image.load("Player_Attack3_L.png"),
                pygame.image.load("Player_Attack4_L.png"), pygame.image.load("Player_Attack4_L.png"),
                pygame.image.load("Player_Attack5_L.png"), pygame.image.load("Player_Attack5_L.png"),
                pygame.image.load("Player_Sprite_L.png")]

health_ani = [pygame.image.load("heart0.png"), pygame.image.load("heart.png"),
              pygame.image.load("heart2.png"), pygame.image.load("heart3.png"),
              pygame.image.load("heart4.png"), pygame.image.load("heart5.png")]


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player_Sprite_R.png")
        self.rect = self.image.get_rect()

        # Position and direction
        self.vx = 0
        self.pos = vec((340, 240))  # 玩家的位置
        self.vel = vec(0, 0)  # 玩家的速度
        self.acc = vec(0, 0)  # 玩家的加速度
        self.direction = "RIGHT"
        # Movement
        self.jumping = False
        self.running = False
        self.move_frame = 0  # 正在显示的角色的当前帧
        # Combat
        self.attacking = False
        self.attack_frame = 0
        self.cooldown = False  # 冷却

        self.health = 5

    def move(self):
        # Keep a constant acceleration of 0.5 in the downwards direction (gravity)
        self.acc = vec(0, 0.5)
        self.gravity_check()
        # 奔跑判断
        if abs(self.vel.x) > 0.3:
            self.running = True
        else:
            self.running = False
        # 越界判断
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos  # Update rect with new pos
        # self.rect.left = self.pos.x
        # self.rect.top = self.pos.y
        # 按键事件处理
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:  # 加速度与self.direction保持一致
            # self.image = player_list['LIFT']
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            # self.image = player_list['RIGHT']
            self.acc.x = ACC
        # 计算速度同时考虑摩擦力的公式
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc  # Updates Position with new values

    def gravity_check(self):
        hits = pygame.sprite.spritecollide(player, ground_group, False)  # 判断人物与地面是否碰撞，并返回发生碰撞的组
        if self.vel.y > 0:
            if hits:
                lowest = hits[0]
                if self.pos.y < lowest.rect.bottom:
                    self.pos.y = lowest.rect.top + 1
                    self.vel.y = 0
                    self.jumping = False

    def jump(self):
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, ground_group, False)
        self.rect.x -= 1
        # If touching the ground, and not currently jumping, cause the player to jump.
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12

    def update(self):
        # 一共6帧
        if self.move_frame > 6:  # “6”的原因是因为我们有7帧（我们从 0 开始）。
            self.move_frame = 0
            return
        # 如果满足条件，将角色移动到下一帧
        if self.jumping == False and self.running == True:
            if self.vel.x > 0:
                self.image = run_ani_R[self.move_frame]
                self.direction = "RIGHT"
            else:
                self.image = run_ani_L[self.move_frame]
                self.direction = "LEFT"
            self.move_frame += 1
        # 如果静止不动，返回静止状态
        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                self.image = run_ani_R[self.move_frame]
            elif self.direction == "LEFT":
                self.image = run_ani_L[self.move_frame]

    def attack(self):
        # while self.attack_frame < 10 and self.attacking:  # 执行所有攻击帧
        #     # 检查方向以显示正确的动画
        #     if self.direction == "RIGHT":
        #         time.sleep(0.004)
        #         self.image = attack_ani_R[self.attack_frame]
        #         displaysurface.blit(source=self.image, dest=self.rect)
        #         pygame.display.update()
        #     elif self.direction == "LEFT":
        #         # self.correction()
        #         time.sleep(0.004)
        #         self.image = attack_ani_L[self.attack_frame]
        #         displaysurface.blit(source=self.image, dest=self.rect)
        #         pygame.display.update()
        #     self.attack_frame += 1
        # self.attack_frame = 0
        # self.attacking = False
        # # 检查方向以显示正确的动画
        # if self.direction == "RIGHT":
        #     self.image = attack_ani_R[self.attack_frame]
        #     displaysurface.blit(source=self.image, dest=self.rect)
        # elif self.direction == "LEFT":
        #     # self.correction()
        #     self.image = attack_ani_L[self.attack_frame]
        #     displaysurface.blit(source=self.image, dest=self.rect)
        # 如果攻击帧已到达序列末尾，则返回基本帧
        if self.attack_frame > 10:
            self.attack_frame = 0
            self.attacking = False
        # 检查方向以显示正确的动画
        if self.direction == "RIGHT":
            self.image = attack_ani_R[self.attack_frame]
        elif self.direction == "LEFT":
            self.correction()
            self.image = attack_ani_L[self.attack_frame]
        self.attack_frame += 1

    def correction(self):
        # 函数用于纠正错误 角色位置在左攻击帧
        if self.attack_frame == 1:
            self.pos.x -= 20
        if self.attack_frame == 10:
            self.pos.x += 20

    def player_hit(self):
        if self.cooldown == False:
            self.cooldown = True  # 开启冷却
            pygame.time.set_timer(hit_cooldown, 1000)  # 1秒内重置冷却时间
            print("player being hit")

            self.health = self.health - 1
            health.image = health_ani[self.health]
            if self.health <= 0:
                self.kill()
                pygame.display.update()


class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("heart5.png")

    def render(self):
        displaysurface.blit(self.image, (10, 10))


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.pos = vec(0, 0)  # 位置
        self.vel = vec(0, 0)  # 速度
        self.direction = random.randint(0, 1)  # 0 for Right, 1 for Left
        self.vel.x = random.randint(2, 6) / 2  # Randomized velocity of the generated enemy
        # 设置敌人的初始位置
        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 235
        if self.direction == 1:
            self.pos.x = 700
            self.pos.y = 235

    def move(self):
        # 使敌人在到达屏幕末端时改变方向
        if self.pos.x >= (WIDTH - 20):
            self.direction = 1
        elif self.pos.x <= 0:
            self.direction = 0
        # 用新值更新位置
        if self.direction == 0:
            self.pos.x += self.vel.x
        if self.direction == 1:
            self.pos.x -= self.vel.x
        self.rect.center = self.pos  # Updates rect

    def render(self):
        # Displayed the enemy on screen
        displaysurface.blit(self.image, (self.pos.x, self.pos.y))

    def update(self):
        # Checks for collision with the Player
        hits = pygame.sprite.spritecollide(self, Playergroup, False)
        # Activates upon either of the two expressions being true
        if hits and player.attacking == True:
            self.kill()
            print("Enemy being hit")

        # If collision has occured and player not attacking, call "hit" function
        elif hits and player.attacking == False:
            player.player_hit()


# Building a Dungeon Entrance 建造地下城入口
class Castle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hide = False
        self.image = pygame.image.load("castle.png")

    def render(self):
        if self.hide == False:
            displaysurface.blit(self.image, (400, 80))


# Creating a window with Tkinter
class EventHandler():
    def __init__(self):
        self.enemy_count = 0
        self.battle = False
        self.enemy_generation = pygame.USEREVENT + 2
        self.stage = 1

        self.stage_enemies = []
        for x in range(1, 21):
            self.stage_enemies.append(int((x ** 2 / 2) + 1))

    def stage_handler(self):
        # Code for the Tkinter stage selection window
        self.root = Tk()
        self.root.geometry('200x170')

        button1 = Button(self.root, text="Twilight Dungeon", width=18, height=2,
                         command=self.world1)
        button2 = Button(self.root, text="Skyward Dungeon", width=18, height=2,
                         command=self.world2)
        button3 = Button(self.root, text="Hell Dungeon", width=18, height=2,
                         command=self.world3)

        button1.place(x=40, y=15)
        button2.place(x=40, y=65)
        button3.place(x=40, y=115)

        self.root.mainloop()

    def world1(self):
        self.root.destroy()
        pygame.time.set_timer(self.enemy_generation, 2000)
        print("Stage: " + str(self.stage))
        print('num of enemy:',handler.stage_enemies[handler.stage - 1])
        castle.hide = True
        self.battle = True

    def world2(self):
        self.battle = True
        # Empty for now

    def world3(self):
        self.battle = True
        # Empty for now

    def next_stage(self):  # 下一个阶段被点击时的代码
        self.stage += 1
        self.enemy_count = 0
        print("Stage: " + str(self.stage))
        pygame.time.set_timer(self.enemy_generation, 1500 - (50 * self.stage))  # 计算每个敌人生成间隔的公式
        print('num of enemy:',handler.stage_enemies[handler.stage - 1])


castle = Castle()
handler = EventHandler()

hit_cooldown = pygame.USEREVENT + 1

background = Background()
ground = Ground()
ground_group = pygame.sprite.Group()
ground_group.add(ground)
player = Player()
Playergroup = pygame.sprite.Group()
Playergroup.add(player)
health = HealthBar()
Enemies = pygame.sprite.Group()
# enemy = Enemy()


while True:
    # player.gravity_check()  # 或者在move()里面调用
    for event in pygame.event.get():
        # Will run when the close window button is clicked
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # For events that occur upon clicking the mouse (left click)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player.attacking == False:
                player.attacking = True
                player.attack()
        # being hit
        if event.type == hit_cooldown:
            player.cooldown = False
            pygame.time.set_timer(hit_cooldown, 0)
        # Event handling for a range of different key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # 空格: 跳
                player.jump()
            if event.key == pygame.K_e and 450 < player.rect.x < 550:  # e并且处于地下城入口: 选关
                handler.stage_handler()
            if event.key == pygame.K_n:
                if handler.battle == True and len(Enemies) == 0:  # n并且在关卡中并且没有敌人: 下一关
                    handler.next_stage()
        # 根据所处阶段生成敌人
        if event.type == handler.enemy_generation:
            if handler.enemy_count < handler.stage_enemies[handler.stage - 1]:
                enemy = Enemy()
                Enemies.add(enemy)
                handler.enemy_count += 1
            # print('num of enemy:', len(Enemies))

    background.render()
    ground.render()

    castle.render()

    if player.health > 0:
        displaysurface.blit(player.image, player.rect)
    health.render()
    player.update()

    for entity in Enemies:
        entity.update()
        entity.move()
        entity.render()
    # enemy.render()
    # enemy.move()
    # enemy.update()

    if player.attacking == True:  # 确保所有的攻击帧都能执行完毕
        player.attack()
    player.move()

    pygame.display.update()
    FPS_CLOCK.tick(FPS)
