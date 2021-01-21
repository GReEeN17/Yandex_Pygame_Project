import pygame
import random
import sqlite3
import datetime

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
sound1 = pygame.mixer.Sound('hit.wav')
sound1.set_volume(0.5)
sound2 = pygame.mixer.Sound('click.mp3')
sound2.set_volume(0.5)
sound3 = pygame.mixer.Sound('lose.wav')
sound3.set_volume(0.5)
sound4 = pygame.mixer.Sound('hit2.wav')
sound4.set_volume(0.3)
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.set_volume(0.1)
con = sqlite3.connect('pygame.db')
spis_of_scores = []
slov_of_scores_and_dates = {}
number_of_additions = 0
now = datetime.datetime.now()
num_lvl = 0


def print_text(message, x, y, font_color=(0, 0, 0), font_type='PingPong.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


def download_from_table():
    global spis_of_scores, slov_of_scores_and_dates
    res = con.cursor().execute('SELECT * FROM records').fetchall()
    for i in res:
        spis_of_scores.append(int(i[0]))
        slov_of_scores_and_dates[int(i[0])] = i[1]
    spis_of_scores = sorted(spis_of_scores, reverse=True)


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

    def draw(self, x, y, text='', action=None, font_size=30):
        global show, running, show_selec, show_statistics
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
                    elif action == show_selector:
                        show_selec = True
                        show_selector()
                    elif action == statistics:
                        show_statistics = True
                        show = False
                    else:
                        action()
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
        print_text(message=text, x=x + 10, y=y + 10, font_size=font_size)


def statistics():
    global show_statistics, show
    screen.fill((0, 0, 0))
    x, y = WIDTH // 3, HEIGHT // 5
    color = pygame.Color(255, 255, 255)
    while show_statistics:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_statistics = False
                show = True
        screen.fill((0, 0, 0))
        for i in range(4):
            pygame.draw.line(screen, color, (0, (i + 1) * y), (WIDTH, (i + 1) * y), 1)
        for i in range(3):
            pygame.draw.line(screen, color, ((i + 1) * x, 0), ((i + 1) * x, HEIGHT), 1)
        kol = 1
        for i in spis_of_scores:
            if kol > 5:
                break
            print_text(str(kol), 0, (kol - 1) * y, (17, 132, 7), font_size=100)
            print_text(str(i), x, (kol - 1) * y, (17, 132, 7), font_size=100)
            print_text(str(slov_of_scores_and_dates[i]), 2 * x, (kol - 1) * y, (17, 132, 7), font_size=100)
            kol += 1
        pygame.display.flip()


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
        statistics_btn.draw(390, 400, 'Statistics', statistics, 50)
        start_btn.draw(370, 300, 'Start game', show_selector, 50)
        quit_btn.draw(450, 500, 'Quit', quit, 50)
        pygame.display.update()


def show_selector():
    global show_selec
    menu_background = pygame.image.load('fon.jpg')
    lvl1_btn = Button(150, 150)
    lvl1_image = pygame.transform.scale(pygame.image.load('lvl1.png'), (150, 150))
    lvl2_btn = Button(150, 150)
    lvl2_image = pygame.transform.scale(pygame.image.load('lvl2.png'), (150, 150))
    lvl3_btn = Button(150, 150)
    lvl3_image = pygame.transform.scale(pygame.image.load('lvl3.png'), (150, 150))
    lvl4_btn = Button(150, 150)
    lvl4_image = pygame.transform.scale(pygame.image.load('lvl4.png'), (150, 150))
    lvl5_btn = Button(150, 150)
    lvl5_image = pygame.transform.scale(pygame.image.load('lvl5.png'), (150, 150))
    lvl6_btn = Button(150, 150)
    lvl6_image = pygame.transform.scale(pygame.image.load('lvl6.png'), (150, 150))
    lvl7_btn = Button(150, 150)
    lvl7_image = pygame.transform.scale(pygame.image.load('lvl7.png'), (150, 150))
    lvl8_btn = Button(150, 150)
    lvl8_image = pygame.transform.scale(pygame.image.load('lvl8.png'), (150, 150))
    lvl9_btn = Button(150, 150)
    lvl9_image = pygame.transform.scale(pygame.image.load('lvl9.png'), (150, 150))
    lvl10_btn = Button(150, 150)
    lvl10_image = pygame.transform.scale(pygame.image.load('lvl10.png'), (150, 150))
    randomlvl_btn = Button(125, 50)
    return_btn = Button(125, 50)
    while show_selec:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.blit(menu_background, (0, 0))
        lvl1_btn.draw(12, 10, action=level_1_arrangement)
        screen.blit(lvl1_image, (12, 10))
        lvl2_btn.draw(212, 10, action=level_2_arrangement)
        screen.blit(lvl2_image, (212, 10))
        lvl3_btn.draw(412, 10, action=level_3_arrangement)
        screen.blit(lvl3_image, (412, 10))
        lvl4_btn.draw(612, 10, action=level_4_arrangement)
        screen.blit(lvl4_image, (612, 10))
        lvl5_btn.draw(812, 10, action=level_5_arrangement)
        screen.blit(lvl5_image, (812, 10))
        lvl6_btn.draw(12, 210, action=level_6_arrangement)
        screen.blit(lvl6_image, (12, 210))
        lvl7_btn.draw(212, 210, action=level_7_arrangement)
        screen.blit(lvl7_image, (212, 210))
        lvl8_btn.draw(412, 210, action=level_8_arrangement)
        screen.blit(lvl8_image, (412, 210))
        lvl9_btn.draw(612, 210, action=level_9_arrangement)
        screen.blit(lvl9_image, (612, 210))
        lvl10_btn.draw(812, 210, action=level_10_arrangement)
        screen.blit(lvl10_image, (812, 210))
        randomlvl_btn.draw(12, 410, text='Random', action=create_blocks)
        return_btn.draw(12, 660, text='Back', action=show_menu)
        pygame.display.update()


def random_addition(button, x, y):
    list_of_buttons.append(button)
    x = x + block_width // 2 - block_height // 2
    addition = Addition(x, y)
    list_of_additions.append(addition)


def random_generate():
    global location, kol_hits, kol_blocks, show_selec, running, show
    show_selec = False
    running = True
    show = False
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
    global kol_blocks, num_lvl
    num_lvl = 0
    random_generate()
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
    global show_selec, running, show, kol_blocks, kol_hits, num_lvl
    reset_parameters_for_additions()
    show_selec = False
    running = True
    show = False
    number_of_additions = 1
    num_lvl = 1
    for i in range(6):
        for j in range(10):
            if addition_yes_or_no(number_of_additions) and i != 0 and j != 0:
                number_of_additions -= 1
                random_addition(bl, 12 + 100 * j, 10 + 50 * i)
            if i == 0 or i == 1:
                color = pygame.Color('white')
            elif i == 2 or i == 3:
                color = pygame.Color('blue')
            else:
                color = pygame.Color('red')
            bl = Block(12 + 100 * j, 10 + 50 * i, block_width, block_height, color)
            kol_blocks += 1


def level_2_arrangement():
    global show_selec, running, show, kol_blocks, kol_hits, num_lvl
    reset_parameters_for_additions()
    show_selec = False
    running = True
    show = False
    number_of_additions = 2
    num_lvl = 2
    for i in range(6):
        for j in range(10):
            if addition_yes_or_no(number_of_additions) and i != 0 and j != 0:
                number_of_additions -= 1
                random_addition(bl, 12 + 100 * j, 10 + 50 * i)
            if (i == 1 and j == 1) or (i == 2 and j == 1) or (i == 1 and j == 2) or (i == 2 and j == 2):
                color = pygame.Color('yellow')
            else:
                color = pygame.Color('red')
            bl = Block(12 + 100 * j, 10 + 50 * i, block_width, block_height, color)
            kol_blocks += 1


def level_3_arrangement():
    global show_selec, running, show, kol_blocks, kol_hits, num_lvl
    reset_parameters_for_additions()
    show_selec = False
    running = True
    show = False
    number_of_additions = 3
    num_lvl = 3
    for i in range(6):
        for j in range(10):
            if addition_yes_or_no(number_of_additions) and i != 0 and j != 0:
                number_of_additions -= 1
                random_addition(bl, 12 + 100 * j, 10 + 50 * i)
            if (i == 0 and j == 0) or (i == 0 and j == 2) or (i == 1 and j == 1) or (i == 2 and j == 0) \
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
            kol_blocks += 1


def level_4_arrangement():
    global show_selec, running, show, kol_blocks, kol_hits, num_lvl
    reset_parameters_for_additions()
    show_selec = False
    running = True
    show = False
    number_of_additions = 4
    num_lvl = 4
    for i in range(6):
        for j in range(10):
            if addition_yes_or_no(number_of_additions) and i != 0 and j != 0:
                number_of_additions -= 1
                random_addition(bl, 12 + 100 * j, 10 + 50 * i)
            if j == 0 or j == 1 or j == 2 or j == 3:
                color = pygame.Color('blue')
            elif j == 4 or j == 5 or j == 6:
                color = pygame.Color('white')
            else:
                color = pygame.Color('red')
            bl = Block(12 + 100 * j, 10 + 50 * i, block_width, block_height, color)
            kol_blocks += 1


def level_5_arrangement():
    global show_selec, running, show, kol_blocks, kol_hits, num_lvl
    reset_parameters_for_additions()
    show_selec = False
    running = True
    show = False
    number_of_additions = 5
    num_lvl = 5
    for i in range(6):
        for j in range(10):
            if addition_yes_or_no(number_of_additions) and i != 0 and j != 0:
                number_of_additions -= 1
                random_addition(bl, 12 + 100 * j, 10 + 50 * i)
            if i == 0 or i == 1:
                color = pygame.Color('black')
            elif i == 2 or i == 3:
                color = pygame.Color('red')
            else:
                color = pygame.Color('yellow')
            bl = Block(12 + 100 * j, 10 + 50 * i, block_width, block_height, color)
            kol_blocks += 1


def level_6_arrangement():
    global show_selec, running, show, kol_blocks, kol_hits, num_lvl
    reset_parameters_for_additions()
    show_selec = False
    running = True
    show = False
    number_of_additions = 6
    num_lvl = 6
    for i in range(6):
        for j in range(10):
            if addition_yes_or_no(number_of_additions) and i != 0 and j != 0:
                number_of_additions -= 1
                random_addition(bl, 12 + 100 * j, 10 + 50 * i)
            if i == 0 or i == 5 or j == 0 or j == 9:
                color = pygame.Color('red')
            elif (i == 2 and 2 <= j <= 7) or (i == 3 and 2 <= j <= 7):
                color = pygame.Color('red')
            elif (2 <= i <= 3 and j == 2) or (2 <= i <= 3 and j == 7):
                color = pygame.Color('red')
            else:
                color = pygame.Color('yellow')
            bl = Block(12 + 100 * j, 10 + 50 * i, block_width, block_height, color)
            kol_blocks += 1


def level_7_arrangement():
    global show_selec, running, show, kol_blocks, kol_hits, num_lvl
    reset_parameters_for_additions()
    show_selec = False
    running = True
    show = False
    number_of_additions = 7
    num_lvl = 7
    for i in range(6):
        for j in range(10):
            if addition_yes_or_no(number_of_additions) and i != 0 and j != 0:
                number_of_additions -= 1
                random_addition(bl, 12 + 100 * j, 10 + 50 * i)
            if i == j or (i == 4 and j == 6) or (i == 3 and j == 7):
                color = pygame.Color('blue')
            elif (i == 2 and j == 8) or (i == 1 and j == 9):
                color = pygame.Color('blue')
            else:
                color = pygame.Color('orange')
            bl = Block(12 + 100 * j, 10 + 50 * i, block_width, block_height, color)
            kol_blocks += 1


def level_8_arrangement():
    global show_selec, running, show, kol_blocks, kol_hits, num_lvl
    reset_parameters_for_additions()
    show_selec = False
    running = True
    show = False
    number_of_additions = 8
    num_lvl = 8
    for i in range(6):
        for j in range(10):
            if addition_yes_or_no(number_of_additions) and i != 0 and j != 0:
                number_of_additions -= 1
                random_addition(bl, 12 + 100 * j, 10 + 50 * i)
            if (i == 0 or i == 2 or i == 4) and (j % 2 == 0):
                color = pygame.Color('green')
            elif (i == 1 or i == 3 or i == 5) and (j % 2 != 0):
                color = pygame.Color('green')
            else:
                color = pygame.Color('red')
            bl = Block(12 + 100 * j, 10 + 50 * i, block_width, block_height, color)
            kol_blocks += 1


def level_9_arrangement():
    global show_selec, running, show, kol_blocks, kol_hits, num_lvl
    reset_parameters_for_additions()
    show_selec = False
    running = True
    show = False
    number_of_additions = 9
    num_lvl = 9
    for i in range(6):
        for j in range(10):
            if addition_yes_or_no(number_of_additions) and i != 0 and j != 0:
                number_of_additions -= 1
                random_addition(bl, 12 + 100 * j, 10 + 50 * i)
            if i == j or i + 5 == j or i == 5 - j or i == 10 - j:
                color = pygame.Color('purple')
            else:
                color = pygame.Color('red')
            bl = Block(12 + 100 * j, 10 + 50 * i, block_width, block_height, color)
            kol_blocks += 1


def level_10_arrangement():
    global show_selec, running, show, kol_blocks, kol_hits, num_lvl
    reset_parameters_for_additions()
    show_selec = False
    running = True
    show = False
    number_of_additions = 10
    num_lvl = 10
    for i in range(6):
        for j in range(10):
            if addition_yes_or_no(number_of_additions) and i != 0 and j != 0:
                number_of_additions -= 1
                random_addition(bl, 12 + 100 * j, 10 + 50 * i)
            if i == 5 and j % 2 != 0:
                color = pygame.Color('red')
            elif j + 2 == i or j - 2 == i or 2 - j == i or 6 - j == i or 10 - j == i or j - 6 == i:
                color = pygame.Color('red')
            else:
                color = pygame.Color('green')
            bl = Block(12 + 100 * j, 10 + 50 * i, block_width, block_height, color)
            kol_blocks += 1


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
                sound1.play()
                self.vy = -self.vy
            if pygame.sprite.spritecollideany(self, vertical_borders):
                sound1.play()
                self.vx = -self.vx
            if pygame.sprite.spritecollideany(self, platforms):
                sound4.play()
                if x_ball - x_platform <= platform_width // 2:
                    self.vx = -2
                else:
                    self.vx = 2
                self.vy = -self.vy
            hits = pygame.sprite.spritecollide(self, blocks, True)
            for _ in hits:
                kol_hits += 1
                points += 10
            if hits:
                sound1.play()
                if hits[0] in list_of_buttons:
                    addition = list_of_additions[list_of_buttons.index(hits[0])]
                    addition.dropping = True
                if hits[0].x1 - abs(self.vx) <= x_ball <= hits[0].x1 + abs(self.vx) or hits[0].x1 + block_width \
                        - abs(self.vx) <= x_ball <= hits[0].x1 + block_width + abs(self.vx):
                    self.vx = -self.vx
                elif hits[0].x1 - abs(self.vx) <= x_ball + 2 * radius <= hits[0].x1 + abs(self.vx) or hits[0].x1 \
                        + block_width - abs(self.vx) <= x_ball + 2 * radius <= hits[0].x1 + block_width + abs(self.vx):
                    self.vx = -self.vx
                elif hits[0].y1 - abs(self.vy) <= y_ball <= hits[0].y1 + abs(self.vy) or hits[0].y1 \
                        + block_height - abs(self.vy) <= y_ball <= hits[0].y1 + block_height + abs(self.vy):
                    self.vy = -self.vy
                elif hits[0].y1 - abs(self.vy) <= y_ball + 2 * radius <= hits[0].y1 + abs(self.vy) or hits[0].y1 \
                        + block_height - abs(self.vy) <= y_ball + 2 * radius <= hits[0].y1 \
                        + block_height + abs(self.vy):
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
    pygame.mixer.music.play(loops=999)
    show_menu()
    statistics()
    game_background = pygame.image.load('fon_game.png')
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
        print(num_lvl)
        if (kol_hits == kol_blocks) and (y_ball > 10 + (50 * 5)):
            if num_lvl == 1:
                level_2_arrangement()
            if num_lvl == 2:
                level_3_arrangement()
            if num_lvl == 3:
                level_4_arrangement()
            if num_lvl == 4:
                level_5_arrangement()
            if num_lvl == 5:
                level_6_arrangement()
            if num_lvl == 6:
                level_7_arrangement()
            if num_lvl == 7:
                level_8_arrangement()
            if num_lvl == 8:
                level_9_arrangement()
            if num_lvl == 9:
                level_10_arrangement()
            if num_lvl == 10 or num_lvl == 0:
                create_blocks()
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
            sound3.play()
            running = False
            game_over()
        screen.blit(game_background, (0, 0))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.display.flip()
    if points != 0:
        con.cursor().execute("""INSERT INTO records(score, date) Values(?, ?)""", (points, str(now.day) + '.'
                                                                                   + str(now.month)))
        con.commit()


while running_program:
    spis_of_scores = []
    slov_of_scores_and_dates = {}
    download_from_table()
    x_platform, y_platform = WIDTH // 2 - platform_width // 2, HEIGHT - 100
    x_ball, y_ball = WIDTH // 2 - radius, HEIGHT - 100 - 2 * radius
    Border(5, 5, WIDTH - 5, 5)
    Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
    Border(5, 5, 5, HEIGHT - 5)
    Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)
    ball = Ball(x_ball, y_ball)
    platform = Platform(x_platform, y_platform, platform_width, platform_height)
    running = False
    show = True
    show_selec = False
    show_statistics = False
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