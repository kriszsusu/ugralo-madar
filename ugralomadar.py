import pygame, gif_pygame
import random

pygame.init()

W = 400
H = 600
screen = pygame.display.set_mode((W, H))

BIRDIMG = pygame.image.load("assets/bird.png").convert_alpha()
BIRDIMG = pygame.transform.scale(BIRDIMG, (50, 50))

GAMEOVER_GIF = gif_pygame.load("assets/gameover.gif")
gif_pygame.transform.scale(
    GAMEOVER_GIF, (GAMEOVER_GIF.get_size()[0] * 2, GAMEOVER_GIF.get_size()[1] * 2)
)
LOGO_GIF = gif_pygame.load("assets/logo.gif")
BG_GIF = gif_pygame.load("assets/bg.gif")
gif_pygame.transform.scale(BG_GIF, (W, H))

death_sound = pygame.mixer.Sound("assets/death.wav")
flap_sound = pygame.mixer.Sound("assets/flap.wav")
score_sound = pygame.mixer.Sound("assets/score.wav")

pygame.display.set_icon(BIRDIMG)
pygame.display.set_caption("Ugráló Madár")

FEHER = (255, 255, 255)
KEK = (200, 200, 255)
FEKETE = (0, 0, 0)
ZOLD = (0, 255, 0)

clock = pygame.time.Clock()
FPS = 60

OBS_WIDTH = 70
OBS_GAP = 300


class SpriteNumber:
    def __init__(self):
        self.spritesheet = pygame.image.load("assets/numbers.png").convert_alpha()
        self.char_size = (16, 16)
        self.char_map = {
            "1": (0, 0),
            "2": (1, 0),
            "3": (2, 0),
            "4": (3, 0),
            "5": (4, 0),
            "6": (5, 0),
            "7": (6, 0),
            "8": (7, 0),
            "9": (8, 0),
            "0": (9, 0),
        }

    def get_char(self, x, y):
        rect = pygame.Rect(
            x * self.char_size[0],
            y * self.char_size[1],
            self.char_size[0],
            self.char_size[1],
        )
        char_image = pygame.Surface(self.char_size, pygame.SRCALPHA)
        char_image.blit(self.spritesheet, (0, 0), rect)

        return self.trim(char_image)

    def trim(self, image):
        mask = pygame.mask.from_surface(image)
        if mask.count() == 0:
            return image

        rect = mask.get_bounding_rects()[0]

        trimmed_image = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        trimmed_image.blit(image, (0, 0), rect)

        return trimmed_image

    def render_text(self, screen, text, x, y, scale=3, spacing=0):
        pos_x = x
        for i, char in enumerate(text):
            if char in self.char_map:
                char_image = self.get_char(*self.char_map[char])

                if scale != 1:
                    char_image = pygame.transform.scale(
                        char_image,
                        (
                            int(char_image.get_width() * scale),
                            int(char_image.get_height() * scale),
                        ),
                    )

                screen.blit(char_image, (pos_x, y))
                pos_x += char_image.get_width() + spacing

    def size(self, text, scale=3, spacing=0):
        total_width = 0
        max_height = 0
        for char in text:
            if char in self.char_map:
                char_image = self.get_char(*self.char_map[char])

                char_width = char_image.get_width() * scale
                char_height = char_image.get_height() * scale

                total_width += char_width + spacing

                if char_height > max_height:
                    max_height = char_height

        total_width -= spacing
        return total_width, max_height


class Madar:
    def __init__(self):
        self.x = 50
        self.y = H // 2
        self.width = 50
        self.height = 50
        self.velocity = 0
        self.gravity = 0.5
        self.lift = -8
        self.data = []

    def draw(self, kepernyo):
        kepernyo.blit(BIRDIMG, (self.x, self.y))

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        if self.y < 0:
            self.y = 0
            self.velocity = 0
        elif self.y + self.height > H:
            self.y = H - self.height
            self.velocity = 0

    def flap(self):
        pygame.mixer.Sound.play(flap_sound)
        self.velocity = self.lift


class Akadaly:
    def __init__(self):
        self.x = W
        self.height = random.randint(100, H // 2)
        self.width = OBS_WIDTH
        self.gap = OBS_GAP
        self.speed = 5

    def draw(self, kepernyo):
        pygame.draw.rect(kepernyo, ZOLD, (self.x, 0, self.width, self.height))
        pygame.draw.rect(
            kepernyo, ZOLD, (self.x - 10, self.height - 10, self.width + 20, 25)
        )
        pygame.draw.rect(
            kepernyo,
            ZOLD,
            (self.x, self.height + self.gap, self.width, H - self.height - self.gap),
        )
        pygame.draw.rect(
            kepernyo,
            ZOLD,
            (self.x - 10, self.height - 10 + self.gap, self.width + 20, 25),
        )

    def update(self):
        self.x -= self.speed

    def offscreen(self):
        return self.x + self.width < 0


def game_loop():
    madar = Madar()
    akadalyok = [Akadaly()]
    pont = 0
    running = True
    game_over = False

    spritenum = SpriteNumber()

    while running:
        screen.fill(KEK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit(0)
            if event.type == pygame.KEYDOWN and event.key in [
                pygame.K_SPACE,
                pygame.K_UP,
                pygame.K_w,
            ]:
                madar.flap()
            if (
                event.type == pygame.KEYDOWN
                and event.key in [pygame.K_SPACE, pygame.K_r]
                and game_over
            ):
                game_loop()

        if not game_over:
            madar.update()
            madar.draw(screen)

            for akadaly in akadalyok:
                akadaly.update()
                akadaly.draw(screen)

                if (
                    madar.x + madar.width > akadaly.x
                    and madar.x < akadaly.x + akadaly.width
                ) and (
                    (madar.y < akadaly.height)
                    or (madar.y + madar.height > akadaly.height + akadaly.gap)
                ):
                    if (
                        madar.y < akadaly.height
                        or madar.y + madar.height > akadaly.height + akadaly.gap
                    ):
                        pygame.mixer.Sound.play(death_sound, 0)
                        game_over = True

                if madar.y >= H - madar.height:
                    pygame.mixer.Sound.play(death_sound, 0)
                    game_over = True

                if akadaly.x + akadaly.width < madar.x and not hasattr(
                    akadaly, "scored"
                ):
                    pont += 1
                    score_sound.play()
                    akadaly.scored = True

            akadalyok = [akadaly for akadaly in akadalyok if not akadaly.offscreen()]
            if akadalyok[-1].x < W - 200:
                akadalyok.append(Akadaly())

            text_width, _ = spritenum.size(f"{pont}")
            spritenum.render_text(screen, f"{pont}", W // 2 - text_width // 2, 20)
        else:
            screen.fill(FEHER)
            screen.blit(BG_GIF.blit_ready(), (0, 0))

            screen.blit(
                GAMEOVER_GIF.blit_ready(),
                (-20, H // 2 - GAMEOVER_GIF.get_size()[1] // 2 - 50),
            )

            font = pygame.font.SysFont("Comic Sans MS", 20)
            text = font.render("R az újrakezdéshez", True, FEKETE)
            text_rect = text.get_rect(center=(W // 2, H // 2 + 100))
            screen.blit(text, text_rect)

        pygame.display.flip()

        clock.tick(FPS)


def menu_screen():
    running = True
    while running:
        screen.fill(FEHER)
        screen.blit(BG_GIF.blit_ready(), (0, 0))

        screen.blit(
            LOGO_GIF.blit_ready(),
            (
                W // 2 - LOGO_GIF.get_size()[0] // 2 - 25,
                H // 2 - LOGO_GIF.get_size()[1] // 2 - 150,
            ),
        )

        font = pygame.font.SysFont("Comic Sans MS", 20)
        text = font.render("Nyomj egy gombot!", True, FEKETE)
        text_rect = text.get_rect(center=(W // 2, H // 2))
        screen.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit(0)
            if event.type == pygame.KEYDOWN:
                game_loop()

        pygame.display.flip()

        clock.tick(FPS)


menu_screen()
game_loop()
