import pygame, sys, subprocess
import pygame.freetype
import pygame_textinput


class Colors:
    # Helper class for colors
    white = (255, 255, 255)
    gray = (168, 168, 168)
    dark_gray = (36, 36, 36)
    muted_gray = (124, 124, 124)


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
    def start_game():
        if (player1_input.value != '' and player2_input.value != ''):
            player1 = User(player1_input.value)
            player2 = User(player2_input.value)
            player1.login()
            player2.login()
            subprocess.Popen(["python", "main.py"])
            pygame.quit()
            sys.exit()


users = []


class User:
    def __init__(self, username):
        self.username = username

    def login(self):
        userObj = {
            'username': self.username
        }
        users.append(userObj)


def initializeInputs():
    # INITIALIZE INPUTS
    player1_input.font_color = Colors.white
    player1_input.font_object = font
    player1_input.cursor_color = Colors.dark_gray
    player2_input.font_color = Colors.white
    player2_input.font_object = font
    player2_input.cursor_color = Colors.dark_gray


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Login')
    pygame.font.init()
    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.Font('assets/PressStart2P-Regular.ttf', 24)

    # INITIALIZE INPUTS
    player1_input = pygame_textinput.TextInputVisualizer()
    player2_input = pygame_textinput.TextInputVisualizer()
    initializeInputs()

    clock = pygame.time.Clock()
    running = True
    active_input = 0
    while running:
        clock.tick(30)
        events = pygame.event.get()
        valid_inputs = []
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # CHECK IF TAB IS PRESSED
                if event.key == pygame.K_TAB:
                    active_input = 1 - active_input
                # CHECK IF THE INPUT IS VALID (NO SPECIAL CHARACTER ALLOWED)
                elif event.unicode.isalnum():
                    # FIND THE ACTIVE INPUT
                    input_text = player1_input.value if active_input == 0 else player2_input.value
                    # CHECK IF THE INPUT HAS VALID LENGTH
                    if len(input_text) < 8:
                        valid_inputs.append(event)
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    # SHOULD STILL BE ABLE TO DELETE CHARACTERS
                    valid_inputs.append(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # JUMP OVER INPUTS WITH MOUSE
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 108 < mouse_x < 778 and 170 < mouse_y < 260:
                    active_input = 0
                elif 108 < mouse_x < 778 and 470 < mouse_y < 560:
                    active_input = 1

        screen.fill(Colors.dark_gray)
        player1_text = Texts('Player 1 :', 218, 200, Colors.white, 28)
        player1_text.displayText()
        player2_text = Texts('Player 2 :', 218, 500, Colors.white, 28)
        player2_text.displayText()

        startBtn = Buttons('Start', 1080, 360, 160, 60, Colors.muted_gray, Colors.gray, Colors.dark_gray, 24,
                           Actions.start_game)
        startBtn.displayButton()

        if active_input == 0:
            player1_input.update(valid_inputs)
            pygame.draw.rect(screen, (255, 255, 255), (368, 178, 300, 44), 3)
        else:
            player2_input.update(valid_inputs)
            pygame.draw.rect(screen, (255, 255, 255), (368, 478, 300, 44), 3)

        screen.blit(player1_input.surface, (378, 188))
        screen.blit(player2_input.surface, (378, 488))
        pygame.display.flip()
    pygame.quit()
