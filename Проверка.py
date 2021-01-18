import pygame

WIDTH = 1024
HEIGHT = 800
pygame.init()
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
sound2 = pygame.mixer.Sound('click.mp3')


def print_text(message, x, y, font_color=(0, 0, 0), font_type='PingPong.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


"""def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print_text('Пауза.Нажмите Enter для продолжения')"""


class Button():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (17, 132, 7)
        self.active_color = (42, 184, 29)

    def draw(self, x, y, text, action=None, font_size=30):
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
                    else:
                        action()
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
        print_text(message=text, x=x + 10, y=y + 10, font_size=font_size)


def show_menu():
    menu_background = pygame.image.load('fon.jpg')
    start_btn = Button(288, 70)
    quit_btn = Button(120, 70)
    statistics_btn = Button(250, 70)
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.blit(menu_background, (0, 0))
        statistics_btn.draw(390, 400, 'Statistics', None, 50)
        start_btn.draw(370, 300, 'Start game', None, 50)
        quit_btn.draw(450, 500, 'Quit', quit, 50)
        pygame.display.update()


show_menu()
