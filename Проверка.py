import pygame

WIDTH = 1024
HEIGHT = 720
FPS = 60
pygame.init()
size = WIDTH, HEIGHT
running = True#отвечает за основной цикл игры
show = True
flying = False#Для того чтобы когда произошло нажатие пробела мячик полетел
lose = True#это уже нужно для того чтобы показывать экран с проигрышами, надо бужет это заменить на обратное возвращение в меню
points = 0#подсчёт чков, не знаю понадобится или не
radius = 10#Радиус шарика которым будем играть
motion = 'STOP'#это для зажатия клавиш
platform_width = 100
platform_height = 1
platform_speed = 5
block_width = 100
block_height = 20
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
screen = pygame.display.set_mode(size)
sound2 = pygame.mixer.Sound('click.mp3')


def print_text(message, x, y, font_color=(0, 0, 0), font_type='PingPong.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            while pygame.event.wait().type != pygame.QUIT or pygame.event.wait().type != pygame.K_RETURN:
                pass
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.K_RETURN:
                paused = False
        print_text('Пауза.Нажмите Enter для продолжения', 200, 200)


class Button():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (17, 132, 7)
        self.active_color = (42, 184, 29)

    def draw(self, x, y, text, action=None, font_size=30):
        global show, running
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
            if click[0] == 1:
                sound2.play()
                pygame.time.delay(300)
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    elif action == 'play':
                        show = False
                        running = True
                    else:
                        action()
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
        print_text(message=text, x=x + 10, y=y + 10, font_size=font_size)


def show_menu():
    global show
    menu_background = pygame.image.load('fon.jpg')
    start_btn = Button(288, 70)
    quit_btn = Button(120, 70)
    statistics_btn = Button(250, 70)
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.blit(menu_background, (0, 0))
        statistics_btn.draw(390, 400, 'Statistics', None, 50)
        start_btn.draw(370, 300, 'Start game', 'play', 50)
        quit_btn.draw(450, 500, 'Quit', quit, 50)
        pygame.display.update()


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        global radius
        super().__init__(all_sprites)
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = 2
        self.vy = -6

    def update(self):
        global flying, radius, x_ball, y_ball, x_platform, y_platform, platform_width
        if flying:
            x_ball += self.vx
            y_ball += self.vy
            self.rect = self.rect.move(self.vx, self.vy)
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.vy = -self.vy
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.vx = -self.vx
            if pygame.sprite.spritecollideany(self, platforms):
                if x_ball - x_platform <= platform_width // 2:
                    self.vx = -2
                else:
                    self.vx = 2
                self.vy = -self.vy
            hits = pygame.sprite.spritecollide(self, blocks, True)
            if hits:
                if hits[0].x1 - 2 <= x_ball <= hits[0].x1 + 2 or hits[0].x1 + block_width - 2 <= x_ball <= \
                        hits[0].x1 + block_width + 2:
                    self.vx = -self.vx
                elif hits[0].y1 - 2 <= y_ball <= hits[0].y1 + 2 or hits[0].y1 + block_height - 2 <= y_ball <= \
                        hits[0].y1 + block_height + 2:
                    self.vy = -self.vy
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)


horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        self.color = pygame.Color(255, 255, 255)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1], pygame.SRCALPHA, 32)
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
        pygame.draw.rect(self.image, self.color, [[0, 0], [x2, y2]], 1)

    def update(self):
        pygame.draw.rect(self.image, self.color, [[0, 0], [self.x2, self.y2]], 1)


blocks = pygame.sprite.Group()


class Block(pygame.sprite.Sprite):
    def __init__(self, x1, y1, w, h, color):
        self.visible = True
        super().__init__(all_sprites)
        self.color = color
        self.add(blocks)
        self.image = pygame.Surface([w, h], pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(x1, y1, w, h)
        self.x1, self.y1, self.w, self.h = x1, y1, w, h
        pygame.draw.rect(self.image, self.color, [0, 0, w, h])

    def update(self):
        pygame.draw.rect(self.image, self.color, [0, 0, self.w, self.h])
        global points
        if not self.visible:
            self.kill()
            points += 10


platforms = pygame.sprite.Group()


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(all_sprites)
        self.add(platforms)
        self.image = pygame.Surface([w, h], pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(x, y, w, h)
        self.w, self.h = w, h
        pygame.draw.rect(self.image, pygame.Color('red'), [0, 0, w, h])

    def update(self):
        global x_platform, y_platform
        pygame.draw.rect(self.image, pygame.Color('red'), [0, 0, self.w, self.h])


x_platform, y_platform = WIDTH // 2 - platform_width // 2, HEIGHT - 100
x_ball, y_ball = WIDTH // 2 - radius, HEIGHT - 100 - 2 * radius
Border(5, 5, WIDTH - 5, 5)
Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
Border(5, 5, 5, HEIGHT - 5)
Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)
ball = Ball(x_ball, y_ball)
platform = Platform(x_platform, y_platform, platform_width, platform_height)
block = Block(300, 300, block_width, block_height, pygame.Color('blue'))
block_2 = Block(500, 300, block_width, block_height, pygame.Color('green'))
screen.fill((0, 0, 0))
show_menu()
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if x_platform >= 15:
                    platform.rect = platform.rect.move(-platform_speed, 0)
                    x_platform -= platform_speed
                    motion = 'LEFT'
                    if not flying:
                        x_ball -= platform_speed
                        ball.rect = ball.rect.move(-platform_speed, 0)
            if event.key == pygame.K_RIGHT:
                if x_platform <= WIDTH - platform_width - 15:
                    platform.rect = platform.rect.move(platform_speed, 0)
                    x_platform += platform_speed
                    motion = 'RIGHT'
                    if not flying:
                        x_ball += platform_speed
                        ball.rect = ball.rect.move(platform_speed, 0)
            if event.key == pygame.K_SPACE:
                flying = True
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT,
                             pygame.K_RIGHT]:
                motion = 'STOP'
            '''if event.key == pygame.K_p: //пауза не работает, посмотри как лучше сделать
                pause()'''
    if motion == 'LEFT' and x_platform >= 15:
        x_platform -= platform_speed
        platform.rect = platform.rect.move(-platform_speed, 0)
        if not flying:
            x_ball -= platform_speed
            ball.rect = ball.rect.move(-platform_speed, 0)
    elif motion == 'RIGHT' and x_platform <= WIDTH - platform_width - 15:
        x_platform += platform_speed
        platform.rect = platform.rect.move(platform_speed, 0)
        if not flying:
            x_ball += platform_speed
            ball.rect = ball.rect.move(platform_speed, 0)
    if y_ball >= HEIGHT - 99:
        running = False
        lose = True
    screen.fill((0, 0, 0))
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
screen.fill((0, 0, 0))
pygame.display.flip()
while lose:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lose = False
    screen.fill((0, 0, 0))
    pygame.display.flip()
    print_text('YOU LOSE', 300, 300)#Надо придумать здесь возвращение в меню
pygame.quit()
