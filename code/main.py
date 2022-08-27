import pygame


class mainScreen:
    Windows = None
    width = 500
    height = 600

    myTrank = None

    def __init__(self):
        pygame.display.init()
        mainScreen.Windows = pygame.display.set_mode(size=[mainScreen.height, mainScreen.width])
        mainScreen.Windows.fill(pygame.Color(255, 255, 255))
        mainScreen.myTrank = Trank(10, 10)
        self.startGame()

    def startGame(self):
        while True:
            mainScreen.Windows.fill(pygame.Color(255, 255, 255))
            self.getEvent()
            mainScreen.myTrank.display('U')
            pygame.display.update()

    def endGame(self):
        print('quit!')
        exit()

    def getEvent(self):
        event_lists = pygame.event.get()
        for event in event_lists:
            if event.type == pygame.QUIT:
                self.endGame()
            if event.type == pygame.KEYUP:
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    mainScreen.myTrank.direction = 'R'
                    mainScreen.myTrank.move('R', mainScreen.myTrank.speed)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    mainScreen.myTrank.direction = 'L'
                    mainScreen.myTrank.move('L', mainScreen.myTrank.speed)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    mainScreen.myTrank.direction = 'U'
                    mainScreen.myTrank.move('U', mainScreen.myTrank.speed)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    mainScreen.myTrank.direction = 'D'
                    mainScreen.myTrank.move('D', mainScreen.myTrank.speed)
                pass


class Trank:
    def __init__(self, left, top):
        self.images = {
            'U': pygame.image.load('../resource/img/U.JPG')
        }
        self.direction = 'U'
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top

        self.status = True
        self.speed = 5
        pass

    def move(self, dir, sp):
        if dir == 'U':
            self.rect.top -=sp
        elif dir == 'D':
            self.rect.top += sp
        elif dir == 'L':
            self.rect.left += sp
        elif dir == 'R':
            self.rect.left -= sp
        pass

    def display(self, dir):
        self.image = self.images[dir]
        mainScreen.Windows.blit(self.image, self.rect)

class My_Trank(Trank):
    def __init__(self, h, w):
        super.__init__(self, h, w)


if __name__ == '__main__':
    screen = mainScreen()
    screen.startGame()
