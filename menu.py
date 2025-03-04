import pygame
import pygame.freetype
from fontTools.ttLib.tables.C_P_A_L_ import Color


# ASSETS INITIALIZE
class Colors:
    white = (255, 255, 255)
    gray = (168, 168, 168)
    dark_gray = (36, 36, 36)
    muted_gray = (124, 124, 124)


class Texts:
    def __init__(self, text, posX, posY, color, font_size):
        self.text = text
        self.color = color
        self.posX = posX
        self.posY = posY
        self.size = font_size

    def displayText(self):
        height, width = self.posY, self.posX
        text_font = pygame.font.Font('assets/PressStart2P-Regular.ttf', self.size)
        text_surface = text_font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=(width, height))
        screen.blit(text_surface, text_rect)


class Buttons:
    def __init__(self, text, posX, posY, width, height, background_color, hover_color, text_color, action=None):
        self.text = text
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.background_color = background_color
        self.text_color = text_color
        self.h_color = hover_color

        self.action = None

    def displayButton(self):
        content = Texts(self.text, self.posX, self.posY, self.text_color, 30)
        action = self.action
        width = self.width
        height = self.height
        x = self.posX - width // 2
        y = self.posY - height // 2
        h_color = self.h_color
        background_color = self.background_color

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (x < mouse[0] < x + width and y < mouse[1] < y + height):
            pygame.draw.rect(screen, h_color, (x, y, width, height))
            if click[0] == 1 and action:
                action()
        else:
            pygame.draw.rect(screen, background_color, (x, y, width, height))

        content.displayText()


pygame.init()
pygame.display.set_caption('CShot')
pygame.font.init()
font = pygame.font.Font('assets/PressStart2P-Regular.ttf', 50)

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(144)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(Colors.dark_gray)

    gameName = Texts('CShot', 640, 72, Colors.white, 50)
    gameName.displayText()
    startButton = Buttons("Start", 640, 305, 180, 70, Colors.muted_gray, Colors.gray, Colors.dark_gray)
    exitButton = Buttons("Exit", 640, 425, 180, 70, Colors.muted_gray, Colors.gray, Colors.dark_gray)
    startButton.displayButton()
    exitButton.displayButton()
    pygame.display.flip()
pygame.quit()
