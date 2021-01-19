import pygame
import random

WIDTH = 1024
HEIGHT = 720
FPS = 60
pygame.init()
size = WIDTH, HEIGHT
running_program = True
lose = True
radius = 8
platform_width = 100
platform_height = 4
platform_speed = 5
block_width = 95
block_height = 45
list_of_buttons = []
list_of_additions = []
image = pygame.image.load('question.png')
image.set_colorkey(image.get_at((0, 0)))
image = pygame.transform.scale(image, (block_height, block_height))
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
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print_text('Paused.Press Enter to continue', 150, 300, (17, 132, 7), font_size=50)
        pygame.display.flip()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False


class Button:
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


def random_addition(button, x, y):
    list_of_buttons.append(button)
    x = x + block_width // 2 - block_height // 2
    addition = Addition(x, y)
    list_of_additions.append(addition)


def random_generate():
    global location, kol_hits, kol_blocks
    kol_hits = 0
    kol_blocks = 0
    location = []
    digit = random.randint(0, 1)
    if digit == 0:
        location = [[], [], [], []]
    else:
        location = [[], [], [], [], []]
    for i in range(4 + digit):
        for j in range(10):
            digit2 = random.randint(0, 1)
            location[i].append(digit2)


def create_blocks():
    global kol_blocks
    for i in range(len(location)):
        for j in range(len(location[0])):
            if location[i][j] == 1:
                kol_blocks += 1
                Block(12 + 100 * j, 10 + 50 * i, block_width, block_height,
                      pygame.Color((random.choice(
                          ['blue', 'yellow', 'green', 'orange', 'purple', ]))))


def addition_yes_or_no(number_of_additions):
    if number_of_additions:
        number = random.randint(1, 4)
        if number == 1:
            return True


def action_of_addition(action):
    global platform_width, platform_speed, ball, platform
    if action == 'broad':
        platform_width = 150
        platform.kill()
        platform = Platform(x_platform, y_platform, platform_width, platform_height)
    elif action == 'narrow':
        platform_width = 50
        platform.kill()
        platform = Platform(x_platform, y_platform, platform_width, platform_height)
    elif action == 'speed of platform higher':
        platform_speed = 10
    elif action == 'speed of platform lower':
        platform_speed = 2
    elif action == 'speed of ball higher':
        ball.vy = int((ball.vy / abs(ball.vy)) * 9)
        ball.vx = int((ball.vx / abs(ball.vx)) * 3)
    elif action == 'speed of ball lower':
        ball.vy = int((ball.vy / abs(ball.vy)) * 3)
        ball.vx = int((ball.vx / abs(ball.vx)) * 1)


def reset_parameters_for_additions():
    global platform_width, platform_speed, ball, platform
    platform_speed = 5
    platform_width = 100
    platform.kill()
    platform = Platform(x_platform, y_platform, platform_width, platform_height)
    ball.vy = int((ball.vy / abs(ball.vy)) * 6)
    ball.vx = int((ball.vx / abs(ball.vx)) * 2)


def level_1_arrangement():
    number_of_additions = 1
    for i in range(6):
        for j in range(10):
            if i == 0 or i == 1:
                color = pygame.Color('white')
            elif i == 2 or i == 3:
                color = pygame.Color('blue')
            else:
                color = pygame.Color('red')
            bl = Block(12 + 100 * j, 10 + 50 * i, block_width, block_height, color)
            if addition_yes_or_no(number_of_additions):
                number_of_additions -= 1
                random_addition(bl, 12 + 100 * j, 10 + 50 * i)


def level_2_arrangement():
    number_of_additions = 2
    for i in range(6):
        for j in range(10):
            if (i == 1 and j == 1) or (i == 2 and j == 1) or (i == 1 and j == 2) or (i == 2 and j == 2):
                color = pygame.Color('yellow')
            else:
                color = pygame.Color('red')
            bl = Block(12 + 100 * j, 10 + 50 * i, block_width, block_height, color)
            if addition_yes_or_no(number_of_additions):
                number_of_additions -= 1
                random_addition(bl, 12 + 100 * j, 10 + 50 * i)


def level_3_arrangement():
    number_of_additions = 3
    for i in range(6):
        for j in range(10):
            if (i == 0 and j == 0) or (i == 0 and j == 2) or (i == 1 and j == 1) or (i == 2 and j == 0)\
                    or (i == 2 and j == 2):
                color = pygame.Color('blue')
            elif (i == 0 and j == 1) or (i == 1 and j == 0) or (i == 1 and j == 2) or (i == 2 and j == 1):
                color = pygame.Color('white')
            elif (i == 0 or i == 2) and (j != 0 and j != 1 and j != 2):
                color = pygame.Color('white')
            elif i == 1 and (j != 0 and j != 1 and j != 2):
                color = pygame.Color('red')
            elif i == 4:
                color = pygame.Color('white')
            else:
                color = pygame.Color('red')
            bl = Block(12 + 100 * j, 10 + 50 * i, block_width, block_height, color)
            if addition_yes_or_no(number_of_additions):
                number_of_additions -= 1
                random_addition(bl, 12 + 100 * j, 10 + 50 * i)


def level_4_arrangement():
    number_of_additions = 4
    for i in range(6):
        for j in range(10):
            if j == 0 or j == 1 or j == 2 or j == 3:
                color = pygame.Color('blue')
            elif j == 4 or j == 5 or j == 6:
                color = pygame.Color('white')
            else:
                color = pygame.Color('red')
            bl = Block(12 + 100 * j, 10 + 50 * i, block_width, block_height, color)
            if addition_yes_or_no(number_of_additions):
                number_of_additions -= 1
                random_addition(bl, 12 + 100 * j, 10 + 50 * i)


def level_5_arrangement():
    number_of_additions = 5
    for i in range(6):
        for j in range(10):
            if i == 0 or i == 1:
                color = pygame.Color('black')
            elif i == 2 or i == 3:
                color = pygame.Color('red')
            else:
                color = pygame.Color('yellow')
            bl = Block(12 + 100 * j, 10 + 50 * i, block_width, block_height, color)
            if addition_yes_or_no(number_of_additions):
                number_of_additions -= 1
                random_addition(bl, 12 + 100 * j, 10 + 50 * i)


def level_6_arrangement():
    number_of_additions = 6
    for i in range(6):
        for j in range(10):
            if i == 0 or i == 5 or j == 0 or j == 9:
                color = pygame.Color('red')
            elif (i == 2 and 2 <= j <= 7) or (i == 3 and 2 <= j <= 7):
                color = pygame.Color('red')
            elif (2 <= i <= 3 and j == 2) or (2 <= i <= 3 and j == 7):
                color = pygame.Color('red')
            else:
                color = pygame.Color('yellow')
            bl = Block(12 + 100 * j, 10 + 50 * i, block_width, block_height, color)
            if addition_yes_or_no(number_of_additions):
                number_of_additions -= 1
                random_addition(bl, 12 + 100 * j, 10 + 50 * i)


def level_7_arrangement():
    number_of_additions = 7
    for i in range(6):
        for j in range(10):
            if i == j or (i == 4 and j == 6) or (i == 3 and j == 7):
                color = pygame.Color('blue')
            elif (i == 2 and j == 8) or (i == 1 and j == 9):
                color = pygame.Color('blue')
            else:
                color = pygame.Color('orange')
            bl = Block(12 + 100 * j, 10 + 50 * i, block_width, block_height, color)
            if addition_yes_or_no(number_of_additions):
                number_of_additions -= 1
                random_addition(bl, 12 + 100 * j, 10 + 50 * i)


def level_8_arrangement():
    number_of_additions = 8
    for i in range(6):
        for j in range(10):
            if (i == 0 or i == 2 or i == 4) and (j % 2 == 0):
                color = pygame.Color('green')
            elif (i == 1 or i == 3 or i == 5) and (j % 2 != 0):
                color = pygame.Color('green')
            else:
                color = pygame.Color('red')
            bl = Block(12 + 100 * j, 10 + 50 * i, block_width, block_height, color)
            if addition_yes_or_no(number_of_additions):
                number_of_additions -= 1
                random_addition(bl, 12 + 100 * j, 10 + 50 * i)


def level_9_arrangement():
    number_of_additions = 9
    for i in range(6):
        for j in range(10):
            if i == j or i + 5 == j or i == 5 - j or i == 10 - j:
                color = pygame.Color('purple')
            else:
                color = pygame.Color('red')
            bl = Block(12 + 100 * j, 10 + 50 * i, block_width, block_height, color)
            if addition_yes_or_no(number_of_additions):
                number_of_additions -= 1
                random_addition(bl, 12 + 100 * j, 10 + 50 * i)


def level_10_arrangement():
    number_of_additions = 10
    for i in range(6):
        for j in range(10):
            if i == 5 and j % 2 != 0:
                color = pygame.Color('red')
            elif j + 2 == i or j - 2 == i or 2 - j == i or 6 - j == i or 10 - j == i or j - 6 == i:
                color = pygame.Color('red')
            else:
                color = pygame.Color('green')
            bl = Block(12 + 100 * j, 10 + 50 * i, block_width, block_height, color)
            if addition_yes_or_no(number_of_additions):
                number_of_additions -= 1
                random_addition(bl, 12 + 100 * j, 10 + 50 * i)


additions = pygame.sprite.Group()


class Addition(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(additions)
        self.surface = pygame.Surface((block_height, block_height), pygame.SRCALPHA, 32)
        self.image = image
        self.rect = pygame.Rect(x, y, block_height, block_height)
        self.dropping = False
        self.action = random.choice(['broad', 'narrow', 'speed of platform higher', 'speed of platform lower',
                                     'speed of ball higher', 'speed of ball lower'])
        self.v = 2

    def update(self):
        if self.dropping:
            self.surface.blit(self.image, (0, 0))
            self.rect = self.rect.move(0, self.v)
            if pygame.sprite.spritecollideany(self, platforms):
                reset_parameters_for_additions()
                action_of_addition(self.action)
                self.kill()


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
        self.vy = -5

    def update(self):
        global flying, radius, x_ball, y_ball, x_platform, y_platform, platform_width, points, kol_hits
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
                kol_hits += 1
                if hits[0] in list_of_buttons:
                    addition = list_of_additions[list_of_buttons.index(hits[0])]
                    addition.dropping = True
                if hits[0].x1 - abs(self.vx) <= x_ball <= hits[0].x1 + abs(self.vx) or hits[0].x1 + block_width\
                        - abs(self.vx) <= x_ball <= hits[0].x1 + block_width + abs(self.vx):
                    self.vx = -self.vx
                elif hits[0].x1 - abs(self.vx) <= x_ball + 2 * radius <= hits[0].x1 + abs(self.vx) or hits[0].x1\
                        + block_width - abs(self.vx) <= x_ball + 2 * radius <= hits[0].x1 + block_width + abs(self.vx):
                    self.vx = -self.vx
                elif hits[0].y1 - abs(self.vy) <= y_ball <= hits[0].y1 + abs(self.vy) or hits[0].y1\
                        + block_height - abs(self.vy) <= y_ball <= hits[0].y1 + block_height + abs(self.vy):
                    self.vy = -self.vy
                elif hits[0].y1 - abs(self.vy) <= y_ball + 2 * radius <= hits[0].y1 + abs(self.vy) or hits[0].y1\
                        + block_height - abs(self.vy) <= y_ball + 2 * radius <= hits[0].y1\
                        + block_height + abs(self.vy):
                    self.vy = -self.vy
                points += 10
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


platforms = pygame.sprite.Group()


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(all_sprites)
        self.add(platforms)
        self.image = pygame.Surface([w, h], pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(x, y, w, h)
        self.w, self.h = w, h
        pygame.draw.rect(self.image, pygame.Color('green'), [0, 0, w, h])

    def update(self):
        global x_platform, y_platform
        pygame.draw.rect(self.image, pygame.Color('green'), [0, 0, self.w, self.h])


def game_over():
    global show, running, flying, points, motion, x_ball, y_ball, x_platform, y_platform, lose
    lose = True
    while lose:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lose = False
        print_text('YOU LOSE', 275, 300, (17, 132, 7), font_size=110)
        print_text('Press Esc to exit', 260, 400, (42, 184, 29), font_size=61)
        pygame.display.flip()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            lose = False


def game():
    global running, flying, motion, x_ball, y_ball, x_platform, y_platform
    show_menu()
    game_background = pygame.image.load('fon_game.png')
    level_10_arrangement()
    '''random_generate()
    create_blocks()'''
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
                if event.key == pygame.K_p:
                    pause()
        if (kol_hits == kol_blocks) and (y_ball > 10 + (50 * 5)):
            #level_1_arrangement()
            '''random_generate()
            create_blocks()'''
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
            game_over()
        screen.blit(game_background, (0, 0))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.display.flip()


while running_program:
    x_platform, y_platform = WIDTH // 2 - platform_width // 2, HEIGHT - 100
    x_ball, y_ball = WIDTH // 2 - radius, HEIGHT - 100 - 2 * radius
    Border(5, 5, WIDTH - 5, 5)
    Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
    Border(5, 5, 5, HEIGHT - 5)
    Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)
    ball = Ball(x_ball, y_ball)
    platform = Platform(x_platform, y_platform, platform_width, platform_height)
    running = True
    show = True
    flying = False
    location = []
    kol_hits = 0
    kol_blocks = 0
    points = 0
    motion = 'STOP'
    game()
    for sprite in all_sprites:
        sprite.kill()
pygame.quit()
