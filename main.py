import pygame, sys, subprocess
import pygame.freetype
import emoji

users = sys.argv[1:]


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


class Emojis:
    def __init__(self, size, posX, posY, src):
        self.size = size
        self.posX = posX
        self.posY = posY
        self.src = f"assets/{src}"

    def displayEmoji(self):
        emoji_img = pygame.image.load(self.src)
        emoji_img = pygame.transform.smoothscale(emoji_img, (self.size, self.size))
        screen.blit(emoji_img, (self.posX, self.posY))


def display_GUI_STATIC():
    player1_text = Texts('Player1', 145, 80, Colors.muted_red, 20)
    player1_text.displayText()
    player1_emoji = Emojis(36, 18, 60, 'player.png')
    player1_emoji.displayEmoji()
    player2_text = Texts('Player2', WIDTH - 90, 80, Colors.muted_blue, 20)
    player2_text.displayText()
    player2_emoji = Emojis(36, WIDTH - 218, 60, 'player.png')
    player2_emoji.displayEmoji()


def display_GUI_UPDATE(p1_bullet_count=10, p1_score=0, p2_bullet_count=10, p2_score=0):
    timer_text = Texts(f"Timer : {int(e_time)}s", WIDTH // 2, 30, Colors.white, 18)
    timer_text.displayText()
    timer_emoji = Emojis(36, 495, 10, 'stopwatch.png')
    timer_emoji.displayEmoji()
    # ///////////////////////////////////// PLAYER 1 GUI /////////////////////////////////////
    player1_bullets = Texts('Bullets', 105, 123, Colors.muted_gray, 14)
    player1_bullets.displayText()
    player1_bullets_count = Texts(f"{p1_bullet_count}", 185, 123, Colors.muted_gray, 14)
    player1_bullets_count.displayText()
    player1_bullets_emoji = Emojis(24, 20, 110, 'bullet.png')
    player1_bullets_emoji.displayEmoji()
    player1_score = Texts('Score', 90, 163, Colors.muted_gray, 14)
    player1_score.displayText()
    player1_score_count = Texts(f"{p1_score}", 185, 163, Colors.muted_gray, 14)
    player1_score_count.displayText()
    player1_score_emoji = Emojis(24, 24, 150, 'score.png')
    player1_score_emoji.displayEmoji()
    # ///////////////////////////////////// PLAYER 2 GUI /////////////////////////////////////
    player2_bullets = Texts('Bullets', WIDTH - 127, 123, Colors.muted_gray, 14)
    player2_bullets.displayText()
    player2_bullets_count = Texts(f"{p2_bullet_count}", WIDTH - 50, 123, Colors.muted_gray, 14)
    player2_bullets_count.displayText()
    player2_bullets_emoji = Emojis(24, WIDTH - 215, 110, 'bullet.png')
    player2_bullets_emoji.displayEmoji()
    player2_score = Texts('Score', WIDTH - 140, 163, Colors.muted_gray, 14)
    player2_score.displayText()
    player2_score_count = Texts(f"{p2_score}", WIDTH - 50, 163, Colors.muted_gray, 14)
    player2_score_count.displayText()
    player2_score_emoji = Emojis(24, WIDTH - 210, 150, 'score.png')
    player2_score_emoji.displayEmoji()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('CShot')
    pygame.font.init()
    font = pygame.font.Font('assets/PressStart2P-Regular.ttf', 50)
    start_time = pygame.time.get_ticks()
    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    running = True
    # //////////////////////////////////////////// MAIN DRIVER CODE ////////////////////////////////////////////
    while running:
        clock.tick(30)
        screen.fill(Colors.dark_gray)
        e_time = (pygame.time.get_ticks() - start_time) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        display_GUI_STATIC()
        display_GUI_UPDATE()
        pygame.display.flip()
    pygame.quit()
