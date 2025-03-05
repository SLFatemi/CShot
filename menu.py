from sys import winver
from pygame import mixer
import pygame, sys, subprocess
import pygame.freetype


class Colors:
    # Helper class for colors
    white = (255, 255, 255)
    gray = (168, 168, 168)
    dark_gray = (36, 36, 36)
    muted_gray = (124, 124, 124)
    muted_red = (150, 50, 50)
    muted_green = (50, 150, 50)
    muted_blue = (50, 50, 150)


class Texts:
    # Helper class for displaying Texts
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
    # Helper class for displaying Buttons
    def __init__(self, text, posX, posY, width, height, background_color, hover_color, text_color, text_size,
                 action=None):
        self.text = text
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.background_color = background_color
        self.text_color = text_color
        self.h_color = hover_color
        self.font_size = text_size
        self.action = action

    def displayButton(self):
        content = Texts(self.text, self.posX, self.posY, self.text_color, self.font_size)
        width = self.width
        height = self.height
        x = self.posX - width // 2
        y = self.posY - height // 2
        h_color = self.h_color
        background_color = self.background_color

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (x < mouse[0] < x + width and y < mouse[1] < y + height):
            pygame.draw.rect(screen, h_color, (x, y, width, height), border_radius=2)
            if click[0] == 1 and self.action:
                self.action()
        else:
            pygame.draw.rect(screen, background_color, (x, y, width, height), border_radius=2)

        content.displayText()


class Actions:
    @staticmethod
    def exit_game():
        pygame.quit()
        sys.exit()

    @staticmethod
    def start_game():
        subprocess.Popen(["python", "login.py"])
        pygame.quit()
        sys.exit()


class Images:
    def __init__(self, size, posX, posY, src):
        self.size = size
        self.posX = posX
        self.posY = posY
        self.src = f"assets/{src}"

    def displayImage(self):
        emoji_img = pygame.image.load(self.src)
        emoji_img = pygame.transform.smoothscale(emoji_img, (self.size, self.size))
        screen.blit(emoji_img, (self.posX, self.posY))


# //////////////////////////////////////////// ASSETS INITIALIZE ////////////////////////////////////////////
if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Menu')
    pygame.font.init()
    font = pygame.font.Font('assets/PressStart2P-Regular.ttf', 50)
    mixer.music.load('assets/menu.sf.mp3')
    mixer.music.play(-1)
    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    running = True
    
    # //////////////////////////////////////////// MAIN DRIVER CODE ////////////////////////////////////////////
    while running:
        clock.tick(144)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(Colors.dark_gray)
        gameName = Texts('C', 560, 172, Colors.muted_red, 210)
        gameName.displayText()
        gameName = Texts('Shot', 677, 162, Colors.white, 75)
        gameName.displayText()
        gameName_emoji = Images(118, WIDTH // 2 + 33, 94, 'logo.png')
        gameName_emoji.displayImage()
        startButton = Buttons("Start", WIDTH // 2, 395, 320, 90, Colors.muted_gray, Colors.gray, Colors.dark_gray, 48,
                              Actions.start_game)
        exitButton = Buttons("Exit", WIDTH // 2, 495, 210, 70, Colors.dark_gray, Colors.dark_gray, Colors.muted_gray,
                             36,
                             Actions.exit_game)
        startButton.displayButton()
        exitButton.displayButton()
        pygame.display.flip()
    pygame.quit()

