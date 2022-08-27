import pygame
from pygame.locals import *
import sys
import random, time
from tkinter import filedialog
from tkinter import *
import numpy

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

# light shade of the button
color_light = (170, 170, 170)
color_dark = (100, 100, 100)
color_white = (255, 255, 255)

# defining a font
headingfont = pygame.font.SysFont("Verdana", 40)
regularfont = pygame.font.SysFont('Corbel', 25)
smallerfont = pygame.font.SysFont('Corbel', 16)
text = regularfont.render('LOAD', True, color_light)


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
        self.attack_frame = 0  # 战斗帧
        self.cooldown = False  # 冷却
        self.health = 5
        self.experiance = 0
        self.mana = 0  # 法力值
        self.magic_cooldown = 1  # 火球冷却

    def move(self):
        # 判断是否暂停
        if cursor.wait == 1: return  # 如果 cursor.wait 变量的值为 1，则该函数不会运行。它只是简单地返回自己，不做任何事情。
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
        # 判断是否暂停
        if cursor.wait == 1: return  # 如果 cursor.wait 变量的值为 1，则该函数不会运行。它只是简单地返回自己，不做任何事情。
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
        # 判断是否暂停
        if cursor.wait == 1: return  # 如果 cursor.wait 变量的值为 1，则该函数不会运行。它只是简单地返回自己，不做任何事情。
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


class FireBall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = player.direction
        if self.direction == "RIGHT":
            self.image = pygame.image.load("fireball1_R.png")
        else:
            self.image = pygame.image.load("fireball1_L.png")
        self.rect = self.image.get_rect(center=player.pos)
        self.rect.x = player.pos.x
        self.rect.y = player.pos.y - 40

    def fire(self):
        player.magic_cooldown = 0
        # Runs while the fireball is still within the screen w/ extra margin
        if -10 < self.rect.x < 710:
            if self.direction == "RIGHT":
                self.image = pygame.image.load("fireball1_R.png")
                displaysurface.blit(self.image, self.rect)
            else:
                self.image = pygame.image.load("fireball1_L.png")
                displaysurface.blit(self.image, self.rect)

            if self.direction == "RIGHT":
                self.rect.move_ip(12, 0)  # https://coderslegacy.com/python/pygame-rpg-magic-attacks/
            else:
                self.rect.move_ip(-12, 0)
        else:
            self.kill()
            player.magic_cooldown = 1
            player.attacking = False


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
        # self.mana = random.randint(1, 3)  # 杀死时获得的随机法力值
        self.mana = 49  # 杀死时获得的随机法力值

    def move(self):
        # 判断是否暂停
        if cursor.wait == 1: return  # 如果 cursor.wait 变量的值为 1，则该函数不会运行。它只是简单地返回自己，不做任何事情。
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
        # Checks for collision with Fireballs
        f_hits = pygame.sprite.spritecollide(self, Fireballs, False)
        # Activates upon either of the two expressions being true
        if hits and player.attacking == True or f_hits:
            if player.mana < 100:
                player.mana += self.mana  # Release mana
            player.experiance += 1  # Release expeiriance
            self.kill()
            handler.dead_enemy_count += 1
            print("Enemy being hit")
            rand_num = numpy.random.uniform(0, 100)
            item_no = 0
            if rand_num >= 0 and rand_num <= 50:  # 有 6% 的几率掉落健康物品
                item_no = 1
            elif rand_num > 50 and rand_num <= 150:  # 有 10% 的几率掉落硬币
                item_no = 2
            if item_no != 0:
                # Add Item to Items group
                item = Item(item_no)
                Items.add(item)
                # Sets the item location to the location of the killed enemy
                item.posx = self.pos.x
                item.posy = self.pos.y
        # If collision has occured and player not attacking, call "hit" function
        elif hits and player.attacking == False:
            player.player_hit()


class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.direction = random.randint(0, 1)  # 0 for Right, 1 for Left
        self.vel.x = random.randint(2, 6) / 3  # Randomized velocity of the generated enemy
        self.mana = random.randint(2, 3)  # Randomized mana amount obtained upon
        self.wait = 0
        self.wait_status = False
        self.turning = 0

        if self.direction == 0:
            self.image = pygame.image.load("enemy2.png")
        if self.direction == 1:
            self.image = pygame.image.load("enemy2_L.png")
        self.rect = self.image.get_rect()

        # Sets the initial position of the enemy
        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 250
        if self.direction == 1:
            self.pos.x = 700
            self.pos.y = 250

    def move(self):
        # 判断是否暂停
        if cursor.wait == 1: return  # 如果 cursor.wait 变量的值为 1，则该函数不会运行。它只是简单地返回自己，不做任何事情。
        if self.turning == 1:
            self.turn()
            return
        # 使敌人在到达屏幕末端时改变方向
        if self.pos.x >= (WIDTH - 20):
            self.direction = 1
        elif self.pos.x <= 0:
            self.direction = 0
        # Updates position with new values
        if self.wait > 50:
            self.wait_status = True
        elif int(self.wait) <= 0:
            self.wait_status = False

        if (self.direction_check()):
            self.turn()
            self.wait = 60  # 对于以 60 FPS 运行的游戏，将 self.wait 设置为 90 会使敌人在转身前暂停 1.5 秒。 （90 除以 60）。
            self.turning = 1

        if self.wait_status == True:  # 每50帧移动一次
            self.wait -= 1

        elif self.direction == 0:
            self.pos.x += self.vel.x
            self.wait += self.vel.x
        elif self.direction == 1:
            self.pos.x -= self.vel.x
            self.wait += self.vel.x

        self.rect.topleft = self.pos  # Updates rect

    def turn(self):
        '''
        To summarise, the turn()function is called 90 times, as we set self.wait to 90, when we began the turn. However,
        the turn is not executed until self.wait is back to 0. This prevents the enemy from turning around too quickly.
        总而言之，turn() 函数被调用了 90 次，因为我们在开始转弯时将 self.wait 设置为 90。
        但是，直到 self.wait 回到 0 时才会执行转弯。这可以防止敌人过快转身。

        And keep in mind, that for a game running at 60 FPS, setting self.wait to 90 makes the enemy pause for 1.5 seconds,
        before turning around. ( 90 divided by 60).
        请记住，对于以 60 FPS 运行的游戏，将 self.wait 设置为 90 会使敌人在转身前暂停 1.5 秒。 （90 除以 60）。
        '''
        if self.wait > 0:
            self.wait -= 1
            return
        elif int(self.wait) <= 0:
            self.turning = 0
        if (self.direction):
            self.direction = 0
            self.image = pygame.image.load("enemy2.png")
        else:
            self.direction = 1
            self.image = pygame.image.load("enemy2_L.png")

    def direction_check(self):  # 第一个是玩家是否在敌人身后，而敌人指向前方（这是第一个 if 语句）。第二个是如果玩家在敌人面前，但玩家指向后方。 （这是第二个如果）
        if (player.pos.x - self.pos.x < 0 and self.direction == 0):
            return 1
        elif (player.pos.x - self.pos.x > 0 and self.direction == 1):
            return 1
        else:
            return 0

    def update(self):
        # Checks for collision with the Player
        hits = pygame.sprite.spritecollide(self, Playergroup, False)
        # Checks for collision with Fireballs
        f_hits = pygame.sprite.spritecollide(self, Fireballs, False)
        # Activates upon either of the two expressions being true
        if hits and player.attacking == True or f_hits:
            self.kill()
            handler.dead_enemy_count += 1
            if player.mana < 100: player.mana += self.mana  # Release mana
            player.experiance += 1  # Release expeiriance
            rand_num = numpy.random.uniform(0, 100)
            item_no = 0
            if rand_num >= 0 and rand_num <= 5:  # 1 / 20 chance for an item (health) drop
                item_no = 1
            elif rand_num > 5 and rand_num <= 15:
                item_no = 2
            if item_no != 0:
                # Add Item to Items group
                item = Item(item_no)
                Items.add(item)
                # Sets the item location to the location of the killed enemy
                item.posx = self.pos.x
                item.posy = self.pos.y

    def render(self):
        # Displays the enemy on screen
        displaysurface.blit(self.image, self.rect)


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
        self.dead_enemy_count = 0
        self.battle = False
        self.enemy_generation = pygame.USEREVENT + 2
        self.enemy_generation2 = pygame.USEREVENT + 3
        self.stage = 1
        self.world = 0

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
        self.world = 1
        pygame.time.set_timer(self.enemy_generation, 2000)
        print("Stage: " + str(self.stage))
        print('num of enemy:',handler.stage_enemies[handler.stage - 1])
        button.imgdisp = 1
        castle.hide = True
        self.battle = True
        # stage_display.move_display()

    def world2(self):
        self.root.destroy()
        self.world = 2
        background.bgimage = pygame.image.load("desert.jpg")
        ground.image = pygame.image.load("desert_ground.png")
        pygame.time.set_timer(self.enemy_generation2, 2500)
        button.imgdisp = 1
        castle.hide = True
        self.battle = True

    def world3(self):
        self.battle = True
        button.imgdisp = 1
        # Empty for now

    def next_stage(self):  # 下一个阶段被点击时的代码
        button.imgdisp = 1
        self.stage += 1
        self.enemy_count = 0
        self.dead_enemy_count = 0
        print("Stage: " + str(self.stage))
        if self.world == 1:
            pygame.time.set_timer(self.enemy_generation, 1500 - (50 * self.stage))  # 计算每个敌人生成间隔的公式
        elif self.world == 2:
            pygame.time.set_timer(self.enemy_generation2, 1500 - (50 * self.stage))  # 计算每个敌人生成间隔的公式
        # pygame.time.set_timer(self.enemy_generation, 1500 - (50 * self.stage))  # 计算每个敌人生成间隔的公式
        print('num of enemy:',handler.stage_enemies[handler.stage - 1])

    def update(self):
        if self.dead_enemy_count == self.stage_enemies[self.stage - 1] and stage_display.clear == False:
            # self.dead_enemy_count = 0
            # stage_display.clear = True
            stage_display.stage_clear()

    def home(self):
        # Reset Battle code
        pygame.time.set_timer(self.enemy_generation, 0)
        pygame.time.set_timer(self.enemy_generation2, 0)
        self.battle = False
        self.enemy_count = 0
        self.dead_enemy_count = 0
        self.stage = 0
        self.world = 0
        # Destroy any enemies or items lying around
        for group in Enemies, Items:
            for entity in group:
                entity.kill()
        # Bring back normal backgrounds
        castle.hide = False
        background.bgimage = pygame.image.load("Background.png").convert_alpha()
        ground.image = pygame.image.load("Ground.png").convert_alpha()


class StageDisplay(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.text = headingfont.render("STAGE: " + str(handler.stage), True, color_dark)
        self.rect = self.text.get_rect()
        self.posx = -100
        self.posy = 100
        self.display = False
        self.clear = False

    def move_display(self):
        # Create the text to be displayed
        self.text = headingfont.render("STAGE: " + str(handler.stage) + '\nEnemy:' + str(handler.stage_enemies[handler.stage - 1]), True, color_dark)
        if self.posx < 720:
            self.posx += 5
            displaysurface.blit(self.text, (self.posx, self.posy))
        else:
            self.display = False
            # self.kill()
            self.posx = -100  # 我们不希望它被杀死。因此，我们只需将其重置为屏幕左侧的某个位置，它将等待下一个命令。
            self.posy = 100

    def stage_clear(self):
        self.text = headingfont.render("STAGE CLEAR!", True, color_dark)
        button.imgdisp = 0
        if self.posx < 720:
            self.posx += 10
            displaysurface.blit(self.text, (self.posx, self.posy))
        else:
            self.clear = True
            self.posx = -100
            self.posy = 100


class StatusBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((100, 95))
        self.rect = self.surf.get_rect(center=(505, 10))
        self.show = False

    def update_draw(self):
        # Create the text to be displayed
        text1 = smallerfont.render("STAGE: " + str(handler.stage), True, color_white)
        text2 = smallerfont.render("Enemy: " + str(handler.stage_enemies[handler.stage - 1]), True, color_white)
        text3 = smallerfont.render("Enemy extra: " + str(handler.stage_enemies[handler.stage - 1] - handler.dead_enemy_count), True, color_white)
        text4 = smallerfont.render("EXP: " + str(player.experiance), True, color_white)
        text5 = smallerfont.render("MANA: " + str(player.mana), True, color_white)
        text6 = smallerfont.render("FPS: " + str(int(FPS_CLOCK.get_fps())), True, color_white)  # 获取帧数

        # Draw the text to the status bar
        displaysurface.blit(text1, (585, 7))
        displaysurface.blit(text2, (585, 22))
        displaysurface.blit(text3, (585, 37))
        displaysurface.blit(text4, (585, 52))
        displaysurface.blit(text5, (585, 67))
        displaysurface.blit(text6, (585, 82))


class Item(pygame.sprite.Sprite):
    def __init__(self, itemtype):
        super().__init__()
        if itemtype == 1:
            self.image = pygame.image.load("heart.png")
        elif itemtype == 2:
            self.image = pygame.image.load("coin.png")
        self.rect = self.image.get_rect()
        self.type = itemtype
        self.posx = 0
        self.posy = 0

    def render(self):
        self.rect.x = self.posx
        self.rect.y = self.posy
        displaysurface.blit(self.image, self.rect)

    def update(self):
        hits = pygame.sprite.spritecollide(self, Playergroup, False)
        # Code to be activated if item comes in contact with player
        if hits:
            if player.health < 5 and self.type == 1:
                player.health += 1
                health.image = health_ani[player.health]
                self.kill()
            if self.type == 2:
                # handler.money += 1
                self.kill()


class PButton(pygame.sprite.Sprite):  # 按钮类
    def __init__(self):
        super().__init__()
        self.vec = vec(620, 300)
        self.imgdisp = 0

    def render(self, num):
        if (num == 0):
            self.image = pygame.image.load("home_small.png")
        elif (num == 1):
            if cursor.wait == 0:
                self.image = pygame.image.load("pause_small.png")
            else:
                self.image = pygame.image.load("play_small.png")

        displaysurface.blit(self.image, self.vec)


class Cursor(pygame.sprite.Sprite):  # 光标类  https://coderslegacy.com/python/pygame-rpg-pause-button/
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("cursor.png")
        self.rect = self.image.get_rect()
        self.wait = 0

    def pause(self):
        if self.wait == 1:
            self.wait = 0
        else:
            self.wait = 1

    def hover(self):
        if 620 <= mouse[0] <= 670 and 300 <= mouse[1] <= 345:
            pygame.mouse.set_visible(False)
            cursor.rect.center = pygame.mouse.get_pos()  # update position
            displaysurface.blit(cursor.image, cursor.rect)
        else:
            pygame.mouse.set_visible(True)

    def home(self):
        # Reset Battle code
        pygame.time.set_timer(self.enemy_generation, 0)
        self.battle = False
        self.enemy_count = 0
        self.dead_enemy_count = 0
        self.stage = 1

        # Destroy any enemies or items lying around
        for group in Enemies, Items:
            for entity in group:
                entity.kill()

        # Bring back normal backgrounds
        castle.hide = False
        background.bgimage = pygame.image.load("Background.png")
        ground.image = pygame.image.load("Ground.png")


castle = Castle()
handler = EventHandler()
stage_display = StageDisplay()

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
status_bar = StatusBar()
Items = pygame.sprite.Group()
Fireballs = pygame.sprite.Group()

button = PButton()
cursor = Cursor()

while True:
    # player.gravity_check()  # 或者在move()里面调用
    mouse = pygame.mouse.get_pos()  # 获取鼠标的坐标(x, y)
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
            if 620 <= mouse[0] <= 670 and 300 <= mouse[1] <= 345:
                if button.imgdisp == 1:
                    cursor.pause()
                elif button.imgdisp == 0:
                    handler.home()
        # being hit
        if event.type == hit_cooldown:
            player.cooldown = False
            pygame.time.set_timer(hit_cooldown, 0)
        # Event handling for a range of different key presses
        if event.type == pygame.KEYDOWN and cursor.wait == 0:
            if event.key == pygame.K_SPACE:  # 空格: 跳
                player.jump()
            if event.key == pygame.K_e and 450 < player.rect.x < 550:  # e并且处于地下城入口: 选关
                handler.stage_handler()
                stage_display = StageDisplay()
                stage_display.display = True
                status_bar.show = True
            if event.key == pygame.K_n:
                if handler.battle == True and len(Enemies) == 0:  # n并且在关卡中并且没有敌人: 下一关
                    handler.next_stage()
                    stage_display = StageDisplay()
                    stage_display.display = True
                    status_bar.show = True
            if event.key == pygame.K_m and player.magic_cooldown == 1:  # m并且火球非冷却,有法力值: 发射火球
                if player.mana >= 6:
                    player.mana -= 6
                    player.attacking = True
                    fireball = FireBall()
                    Fireballs.add(fireball)
        # 根据所处阶段生成敌人
        if event.type == handler.enemy_generation:
            if handler.enemy_count < handler.stage_enemies[handler.stage - 1]:
                enemy = Enemy()
                Enemies.add(enemy)
                handler.enemy_count += 1
            # print('num of enemy:', len(Enemies))
        if event.type == handler.enemy_generation2:
            if handler.enemy_count < handler.stage_enemies[handler.stage - 1]:
                enemy = Enemy2()
                Enemies.add(enemy)
                handler.enemy_count += 1

    background.render()
    ground.render()

    button.render(button.imgdisp)
    cursor.hover()

    castle.render()
    # Render stage display
    if stage_display.display == True:
        stage_display.move_display()
    # if stage_display.clear == True:
    #     stage_display.stage_clear()

    if player.health > 0:
        displaysurface.blit(player.image, player.rect)
    health.render()
    player.update()

    if status_bar.show:
        # Status bar update and render
        displaysurface.blit(status_bar.surf, (580, 5))
        status_bar.update_draw()
        handler.update()

    for entity in Enemies:
        entity.update()
        entity.move()
        entity.render()
    # enemy.render()
    # enemy.move()
    # enemy.update()

    for ball in Fireballs:
        ball.fire()

    for i in Items:
        i.render()
        i.update()

    if player.attacking == True:  # 确保所有的攻击帧都能执行完毕
        player.attack()
    player.move()

    pygame.display.update()
    FPS_CLOCK.tick(FPS)
