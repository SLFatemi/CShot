import math
import random
from calendar import THURSDAY

from pygame import mixer
import pygame, sys, subprocess
import pygame.freetype

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


class Player:
    def __init__(self, score=0, bullets=20, time=60):
        self.score = score
        self.bullets = bullets
        self.posX = random.randint(100, 1200)
        self.posY = random.randint(250, 650)
        self.old_posX = self.posX
        self.old_posY = self.posY
        self.bulletHoles = []
        self.time = time
        self.extra_time = 0

    def moveUp(self):
        # DONT GO OVER UI
        if (self.posY > 200):
            self.posY -= 10

    def moveDown(self):
        if (self.posY < 680):
            self.posY += 10

    def moveLeft(self):
        if (self.posX > 30):
            self.posX -= 10

    def moveRight(self):
        if (self.posX < 1240):
            self.posX += 10

    def shoot(self, player):
        if (self.bullets > 0):
            self.bullets -= 1
            if (player == 1):
                bullet_hole = Images(8, self.posX, self.posY, 'bulletholered.png')
                self.bulletHoles.append(bullet_hole)
                self.checkHit([target1, target2, target3, ammo1, ammo2, extra_time1, bomb1, bolt1])
            elif (player == 2):
                bullet_hole = Images(8, self.posX, self.posY, 'bulletholeblue.png')
                self.bulletHoles.append(bullet_hole)
                self.checkHit([target1, target2, target3, ammo1, ammo2, extra_time1, bomb1, bolt1])
            self.old_posX = self.posX
            self.old_posY = self.posY

    def checkHit(self, targets):
        for target in targets:
            if (target.posX - 6 < self.posX < target.posX + 36 and target.posY - 6 < self.posY < target.posY + 36):
                target.reset()
                if (target.__class__.__name__ == 'Ammo'):
                    play_sound_effect('powerup.mp3', 0.5)
                    self.bullets += 15
                elif (target.__class__.__name__ == 'Time'):
                    play_sound_effect('powerup.mp3', 0.5)
                    self.extra_time += 10
                elif (target.__class__.__name__ == 'Bomb'):
                    play_sound_effect('bomb.mp3', 0.5)
                    self.score -= 3
                elif (target.__class__.__name__ == 'Bolt'):
                    global thunder_hit
                    play_sound_effect('bolt.mp3', 0.8)
                    thunder_hit = True
                    target1.reset()
                    target2.reset()
                    target3.reset()
                    self.score += 3
                else:
                    play_sound_effect('powerup.mp3', 0.5)
                    self.score += self.calScore()
                return True

    def calScore(self):
        distance = math.sqrt((self.posX - self.old_posX) ** 2 + (self.posY - self.old_posY) ** 2)
        return int((distance // 130 + 1))


class Target:
    def __init__(self):
        self.reset()

    def displayTarget(self):
        target = Images(36, self.posX, self.posY, 'target.png')
        target.displayImage()

    def reset(self):
        self.posX = random.randint(100, 1200)
        self.posY = random.randint(250, 650)


class Ammo(Target):
    def __init__(self):
        super().__init__()

    def displayTarget(self):
        target = Images(36, self.posX, self.posY, 'ammo.png')
        target.displayImage()


class Time(Target):
    def __init__(self):
        super().__init__()

    def displayTarget(self):
        target = Images(36, self.posX, self.posY, 'time.png')
        target.displayImage()


class Bomb(Target):
    def __init__(self):
        super().__init__()

    def displayTarget(self):
        target = Images(36, self.posX, self.posY, 'bomb.png')
        target.displayImage()


class Bolt(Target):
    def __init__(self):
        super().__init__()

    def displayTarget(self):
        target = Images(36, self.posX, self.posY, 'lightningBolt.png')
        target.displayImage()

    def reset(self):
        self.posX = random.randint(100, 1200)
        self.posY = random.randint(250, 650)


class Actions:
    @staticmethod
    def exit_game():
        subprocess.Popen(["python", "menu.py"])
        pygame.quit()
        sys.exit()


def play_sound_once(src):
    sound = pygame.mixer.Sound(f"assets/{src}")
    global end_game_sound_played
    if not end_game_sound_played:
        mixer.music.stop()
        sound.play()
        end_game_sound_played = True


def play_sound_effect(src, vol):
    sound = pygame.mixer.Sound(f'assets/{src}')
    sound.set_volume(vol)
    sound.play()


def display_GUI_STATIC():
    player1_text = Texts('Player1', 145, 80, Colors.muted_red, 20)
    player1_text.displayText()
    player1_emoji = Images(36, 18, 60, 'player1.png')
    player1_emoji.displayImage()
    player2_text = Texts('Player2', WIDTH - 140, 80, Colors.muted_blue, 20)
    player2_text.displayText()
    player2_emoji = Images(36, WIDTH - 268, 60, 'player2.png')
    player2_emoji.displayImage()


def display_GUI_UPDATE(p1_bullet_count=20, p1_score=0, p2_bullet_count=20, p2_score=0):
    player1_timer = Texts(f"Timer : {int(player1.time)}s", 165, 30, Colors.white, 18)
    player1_timer.displayText()
    timer_emoji = Images(36, 18, 10, 'stopwatch.png')
    timer_emoji.displayImage()
    player2_timer = Texts(f"Timer : {int(player2.time)}s", WIDTH - 115, 30, Colors.white, 18)
    player2_timer.displayText()
    timer_emoji = Images(36, WIDTH - 268, 10, 'stopwatch.png')
    timer_emoji.displayImage()
    # ///////////////////////////////////// PLAYER 1 GUI /////////////////////////////////////
    player1_bullets = Texts('Bullets', 105, 123, Colors.muted_gray, 14)
    player1_bullets.displayText()
    player1_bullets_count = Texts(f"{p1_bullet_count}", 185, 123, Colors.muted_gray, 14)
    player1_bullets_count.displayText()
    player1_bullets_emoji = Images(24, 25, 110, 'bullet.png')
    player1_bullets_emoji.displayImage()
    player1_score = Texts('Score', 90, 163, Colors.muted_gray, 14)
    player1_score.displayText()
    player1_score_count = Texts(f"{p1_score}", 185, 163, Colors.muted_gray, 14)
    player1_score_count.displayText()
    player1_score_emoji = Images(24, 24, 150, 'score.png')
    player1_score_emoji.displayImage()
    # ///////////////////////////////////// PLAYER 2 GUI /////////////////////////////////////
    player2_bullets = Texts('Bullets', WIDTH - 177, 123, Colors.muted_gray, 14)
    player2_bullets.displayText()
    player2_bullets_count = Texts(f"{p2_bullet_count}", WIDTH - 100, 123, Colors.muted_gray, 14)
    player2_bullets_count.displayText()
    player2_bullets_emoji = Images(24, WIDTH - 260, 110, 'bullet.png')
    player2_bullets_emoji.displayImage()
    player2_score = Texts('Score', WIDTH - 190, 163, Colors.muted_gray, 14)
    player2_score.displayText()
    player2_score_count = Texts(f"{p2_score}", WIDTH - 100, 163, Colors.muted_gray, 14)
    player2_score_count.displayText()
    player2_score_emoji = Images(24, WIDTH - 260, 150, 'score.png')
    player2_score_emoji.displayImage()


def display_gameOver_screen(p1_score, p2_score):
    screen.fill(Colors.dark_gray)
    go_text = Texts("The Game is Over!", WIDTH // 2, HEIGHT // 4, Colors.white, 40)
    go_text.displayText()

    p1_final_score = Texts(f"Player 1 Score: {p1_score}", WIDTH // 2, HEIGHT // 2 - 50, Colors.muted_red, 20)
    p1_final_score.displayText()
    p2_final_score = Texts(f"Player 2 Score: {p2_score}", WIDTH // 2, HEIGHT // 2 + 50, Colors.muted_blue, 20)
    p2_final_score.displayText()
    # ////Winning exception and condition
    if p1_score > p2_score:
        Win_text = Texts("Player 1 Wins! Brutal.", WIDTH // 2, HEIGHT // 2 + 150, Colors.muted_red, 25)
        Win_text.displayText()
        play_sound_once('win.sf.mp3')
    elif p2_score > p1_score:
        Win_text = Texts("Player 2 Wins! Brutal", WIDTH // 2, HEIGHT // 2 + 150, Colors.muted_blue, 25)
        Win_text.displayText()
        play_sound_once('win.sf.mp3')
    else:
        Win_text = Texts("Draw!", WIDTH // 2, HEIGHT // 2 + 150, Colors.white, 25)
        Win_text.displayText()
        play_sound_once('draw.sf.mp3')

    exit_button = Buttons("Exit", WIDTH // 2, HEIGHT - 100, 200, 50, Colors.muted_gray, Colors.gray, Colors.white, 20,
                          Actions.exit_game)
    exit_button.displayButton()


if __name__ == "__main__":
    # //////////////////////////////////////////// INITIALIZE PYGAME ////////////////////////////////////////////
    pygame.init()
    pygame.display.set_caption('CShot')
    pygame.font.init()
    icon = pygame.image.load('assets/icon.jpg')
    pygame.display.set_icon(icon)
    pygame.key.set_repeat(500, 50)
    font = pygame.font.Font('assets/PressStart2P-Regular.ttf', 50)
    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    # //////////////////////////////////////////// INITIALIZE MIXER ////////////////////////////////////////////
    mixer.music.load('assets/game.sf.mp3')
    mixer.music.set_volume(0.3)
    mixer.music.play(-1)
    # //////////////////////////////////////////// INITIALIZE OBJECTS ////////////////////////////////////////////
    end_game_sound_played = False
    thunder_hit = False
    player1 = Player()
    player2 = Player()

    target1 = Target()
    target2 = Target()
    target3 = Target()

    ammo1 = Ammo()
    ammo2 = Ammo()
    extra_time1 = Time()
    bomb1 = Bomb()
    bolt1 = Bolt()
    # //////////////////////////////////////////// CREATE CUSTOM EVENTS ////////////////////////////////////////////
    ammo_spawn = pygame.USEREVENT + 1
    time_spawn = pygame.USEREVENT + 2
    bomb_spawn = pygame.USEREVENT + 3
    pygame.time.set_timer(ammo_spawn, 10000)
    pygame.time.set_timer(time_spawn, 5000)
    pygame.time.set_timer(bomb_spawn, 15000)
    running = True
    # //////////////////////////////////////////// MAIN DRIVER CODE ////////////////////////////////////////////
    while running:
        clock.tick(90)
        screen.fill(Colors.dark_gray)
        # //////////////////////////////////////////// INITIALIZE TIMER ////////////////////////////////////////////
        e_time = 60 - (pygame.time.get_ticks() - start_time) // 1000
        player1.time = e_time + player1.extra_time if e_time + player1.extra_time > 0 else 0
        player2.time = e_time + player2.extra_time if e_time + player2.extra_time > 0 else 0
        # //////////////////////////////////////////// CHECK END GAME CONDITIONS ////////////////////////////////////////////
        if (player1.bullets == 0 and player2.bullets == 0) or (player1.time == 0 and player2.time == 0) or (
                player1.time == 0 and player2.bullets == 0) or (player1.bullets == 0 and player2.time == 0):
            display_gameOver_screen(player1.score, player2.score)
        else:
            # //////////////////////////////////////////// DISPLAY TARGETS ////////////////////////////////////////////
            target1.displayTarget()
            target2.displayTarget()
            target3.displayTarget()
            extra_time1.displayTarget()
            ammo1.displayTarget()
            ammo2.displayTarget()
            bomb1.displayTarget()
            if (e_time < 55 and e_time > 45 and thunder_hit == False):
                bolt1.displayTarget()
            pygame.draw.rect(screen, Colors.muted_gray, (30, 195, 1220, 495), 2)
            #  //////////////////////////////////////////// DISPLAY SHOTS ////////////////////////////////////////////
            for bulletHoleP1 in player1.bulletHoles:
                bulletHoleP1.displayImage()

            for bulletHoleP2 in player2.bulletHoles:
                bulletHoleP2.displayImage()
            display_GUI_STATIC()
            display_GUI_UPDATE(player1.bullets, player1.score, player2.bullets, player2.score)
        # ///////////////////////////////////////// END OF ELSE ///////////////////////////////////////////////
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # USER USED A KEY
            elif (event.type == pygame.KEYDOWN):
                if (player1.time > 0):
                    # ///////////////////////////////////////// SPACE (PLAYER 1 SHOOTING) /////////////////////////////////////////
                    if (event.key == pygame.K_SPACE):
                        play_sound_effect('shot.mp3', 0.2)
                        player1.shoot(1)
                    # ///////////////////////////////////////// PLAYER 1 MOVEMENTS /////////////////////////////////////////
                    if (event.key == pygame.K_w):
                        player1.moveUp()
                    if (event.key == pygame.K_s):
                        player1.moveDown()
                    if (event.key == pygame.K_a):
                        player1.moveLeft()
                    if (event.key == pygame.K_d):
                        player1.moveRight()
                if (player2.time > 0):
                    # ///////////////////////////////////////// ENTER (PLAYER 2 SHOOTING) /////////////////////////////////////////
                    if (event.key == pygame.K_RETURN):
                        play_sound_effect('shot.mp3', 0.2)
                        player2.shoot(2)
                    # ///////////////////////////////////////// PLAYER 2 MOVEMENTS /////////////////////////////////////////
                    if (event.key == pygame.K_UP):
                        player2.moveUp()
                    if (event.key == pygame.K_DOWN):
                        player2.moveDown()
                    if (event.key == pygame.K_LEFT):
                        player2.moveLeft()
                    if (event.key == pygame.K_RIGHT):
                        player2.moveRight()
            # //////////////////////////////////////////// CALL CUSTOM EVENTS ////////////////////////////////////////////
            elif (event.type == ammo_spawn):
                ammo1.reset()
                ammo2.reset()
            elif (event.type == time_spawn):
                extra_time1.reset()
            elif (event.type == bomb_spawn):
                bomb1.reset()
        pygame.display.flip()

    pygame.quit()
