import pygame
import random

pygame.init()

KEPERNYO_SZELESSEG = 400
KEPERNYO_MAGASSAG = 600
kepernyo = pygame.display.set_mode((KEPERNYO_SZELESSEG, KEPERNYO_MAGASSAG))
pygame.display.set_caption("Ugráló Madár")

FEHER = (255, 255, 255)
FEKETE = (0, 0, 0)
ZOLD = (0, 255, 0)

ido = pygame.time.Clock()
FPS = 60

MADAR_KEP = pygame.image.load('bird.png').convert_alpha()
MADAR_KEP = pygame.transform.scale(MADAR_KEP, (70, 70))
AKADALY_SZELESSEG = 70
AKADALY_KIMARADAS = 220

class Madar:
    def __init__(self):
        self.x = 50
        self.y = KEPERNYO_MAGASSAG // 2
        self.width = 40
        self.height = 40
        self.velocity = 0
        self.gravity = 0.5
        self.lift = -8
        
    def draw(self, kepernyo):
        kepernyo.blit(MADAR_KEP, (self.x, self.y))
        
    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        elif self.y + self.height > KEPERNYO_MAGASSAG:
            self.y = KEPERNYO_MAGASSAG - self.height
            self.velocity = 0
            
    def flap(self):
        self.velocity = self.lift
        
class Akadaly:
    def __init__(self):
        self.x = KEPERNYO_SZELESSEG
        self.height = random.randint(100, 400)
        self.width = AKADALY_SZELESSEG
        self.gap = AKADALY_KIMARADAS
        self.speed = 5
        
    def draw(self, kepernyo):
        pygame.draw.rect(kepernyo, ZOLD, (self.x, 0, self.width, self.height))
        pygame.draw.rect(kepernyo, ZOLD, (self.x, self.height + self.gap, self.width, KEPERNYO_MAGASSAG - self.height - self.gap))
        
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

    while running:
        kepernyo.fill(FEHER)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                madar.flap()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
                game_loop()

        if not game_over:
            madar.update()
            madar.draw(kepernyo)

            for akadaly in akadalyok:
                akadaly.update()
                akadaly.draw(kepernyo)

                if (madar.x + madar.width > akadaly.x and madar.x < akadaly.x + akadaly.width) and \
                        ((madar.y < akadaly.height) or (madar.y + madar.height > akadaly.height + akadaly.gap)):
                    if madar.y < akadaly.height or madar.y + madar.height > akadaly.height + akadaly.gap:
                        game_over = True

                if akadaly.x + akadaly.width < madar.x and not hasattr(akadaly, 'scored'):
                    pont += 1
                    akadaly.scored = True

            akadalyok = [akadaly for akadaly in akadalyok if not akadaly.offscreen()]
            if akadalyok[-1].x < KEPERNYO_SZELESSEG - 200:
                akadalyok.append(Akadaly())

            font = pygame.font.SysFont(None, 40)
            text = font.render(f"Pontok: {pont}", True, FEKETE)
            kepernyo.blit(text, (10, 10))

        else:
            font = pygame.font.SysFont(None, 60)
            text = font.render("Meghaltál!", True, FEKETE)
            kepernyo.blit(text, (KEPERNYO_SZELESSEG // 2 - 100, KEPERNYO_MAGASSAG // 2 - 30))

            font = pygame.font.SysFont(None, 30)
            text = font.render("R az újrakezdéshez", True, FEKETE)
            kepernyo.blit(text, (KEPERNYO_SZELESSEG // 2 - 100, KEPERNYO_MAGASSAG // 2 + 30))

        pygame.display.flip()

        ido.tick(FPS)

def menu_screen():
    running = True
    while running:
        kepernyo.fill(FEHER)

        font = pygame.font.SysFont(None, 60)
        text = font.render("Ugráló Madár", True, FEKETE)
        kepernyo.blit(text, (KEPERNYO_SZELESSEG // 2 - 150, KEPERNYO_MAGASSAG // 2 - 100))

        font = pygame.font.SysFont(None, 30)
        text = font.render("Nyomj egy gombot!", True, FEKETE)
        kepernyo.blit(text, (KEPERNYO_SZELESSEG // 2 - 150, KEPERNYO_MAGASSAG // 2 - 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                game_loop()

        pygame.display.flip()

        ido.tick(FPS)

menu_screen()
game_loop()