import pygame
import random

pygame.init()


W = 400
H = 600
kepernyo = pygame.display.set_mode((W, H))

BIRDIMG = pygame.image.load('bird.png').convert_alpha()
BIRDIMG = pygame.transform.scale(BIRDIMG, (50, 50))
pygame.display.set_icon(BIRDIMG)
pygame.display.set_caption("Ugráló Madár")

FEHER = (255, 255, 255)
KEK = (200, 200, 255)
FEKETE = (0, 0, 0)
ZOLD = (0, 255, 0)

clock = pygame.time.Clock()
FPS = 60

OBS_WIDTH = 70
OBS_GAP = 250

class Madar:
    def __init__(self):
        self.x = 50
        self.y = H // 2
        self.width = 50
        self.height = 50
        self.velocity = 0
        self.gravity = 0.5
        self.lift = -8
        
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
        self.velocity = self.lift
        
class Akadaly:
    def __init__(self):
        self.x = W
        self.height = random.randint(100, 400)
        self.width = OBS_WIDTH
        self.gap = OBS_GAP
        self.speed = 5
        
    def draw(self, kepernyo):
        pygame.draw.rect(kepernyo, ZOLD, (self.x, 0, self.width, self.height))
        pygame.draw.rect(kepernyo, ZOLD, (self.x - 10, self.height - 10, self.width + 20, 25))
        pygame.draw.rect(kepernyo, ZOLD, (self.x, self.height + self.gap, self.width, H - self.height - self.gap))
        pygame.draw.rect(kepernyo, ZOLD, (self.x - 10, self.height - 10 + self.gap, self.width + 20, 25))
        
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
        kepernyo.fill(KEK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit(0)
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
                        
                if (madar.y >= H - madar.height):
                    game_over = True

                if akadaly.x + akadaly.width < madar.x and not hasattr(akadaly, 'scored'):
                    pont += 1
                    akadaly.scored = True

            akadalyok = [akadaly for akadaly in akadalyok if not akadaly.offscreen()]
            if akadalyok[-1].x < W - 200:
                akadalyok.append(Akadaly())

            font = pygame.font.SysFont(None, 40)
            text = font.render(f"p: {pont} y: {madar.y} h: {H}", True, FEKETE)
            kepernyo.blit(text, (10, 10))

        else:
            kepernyo.fill(FEHER)
            
            font = pygame.font.SysFont("Comic Sans MS", 40)
            text = font.render("Meghaltál!", True, FEKETE)
            kepernyo.blit(text, (W // 2 - font.size("Meghaltál")[0] // 2, H // 2 - font.size("Meghaltál")[1] // 2))

            font = pygame.font.SysFont("Comic Sans MS", 20)
            text = font.render("R az újrakezdéshez", True, FEKETE)
            kepernyo.blit(text, (W // 2 - font.size("R az újrakezdéshez")[0] // 2, H // 2 + 50 - font.size("R az újrakezdéshez")[1] // 2))

        pygame.display.flip()

        clock.tick(FPS)

def menu_screen():
    running = True
    while running:
        kepernyo.fill(FEHER)

        font = pygame.font.SysFont(None, 60)
        text = font.render("Ugráló Madár", True, FEKETE)
        kepernyo.blit(text, (W // 2 - 150, H // 2 - 100))

        font = pygame.font.SysFont(None, 30)
        text = font.render("Nyomj egy gombot!", True, FEKETE)
        kepernyo.blit(text, (W // 2 - 150, H // 2 - 50))

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