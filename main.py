import pygame

class Game:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.aliens = []
        self.rockets = []
        self.lost = False

        self.hero = Hero(self, width / 2, height - 20)
        generator = Generator(self)

        while not self.lost:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.lost = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.lost:
                    self.rockets.append(Rocket(self, self.hero.x, self.hero.y))

            self.handle_input()
            self.update_screen()
            self.check_aliens()

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        self.hero.handle_movement(pressed)

    def update_screen(self):
        pygame.display.flip()
        self.clock.tick(60)
        self.screen.fill((0, 0, 0))

    def check_aliens(self):
        if len(self.aliens) == 0:
            self.display_text("VICTORY ACHIEVED")

        for alien in self.aliens:
            alien.draw()
            alien.check_collision(self)
            if alien.y > self.height:
                self.lost = True
                self.display_text("YOU DIED")

        for rocket in self.rockets:
            rocket.draw()

        if not self.lost:
            self.hero.draw()

    def display_text(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 50)
        text_surface = font.render(text, False, (44, 0, 62))
        self.screen.blit(text_surface, (110, 160))

class Alien:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.size = 30
        self.game = game

    def draw(self):
        pygame.draw.rect(self.game.screen, (81, 43, 88), pygame.Rect(self.x, self.y, self.size, self.size))
        self.y += 0.05

    def check_collision(self, game):
        for rocket in game.rockets:
            if (self.x - self.size < rocket.x < self.x + self.size and
                self.y - self.size < rocket.y < self.y + self.size):
                game.rockets.remove(rocket)
                game.aliens.remove(self)

class Hero:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game

    def handle_movement(self, pressed):
        if pressed[pygame.K_LEFT]:
            self.x -= 2 if self.x > 20 else 0
        elif pressed[pygame.K_RIGHT]:
            self.x += 2 if self.x < self.game.width - 20 else 0

    def draw(self):
        pygame.draw.rect(self.game.screen, (210, 250, 251), pygame.Rect(self.x, self.y, 8, 5))

class Generator:
    def __init__(self, game):
        margin = 30
        width = 50
        for x in range(margin, game.width - margin, width):
            for y in range(margin, int(game.height / 2), width):
                game.aliens.append(Alien(game, x, y))

class Rocket:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game

    def draw(self):
        pygame.draw.rect(self.game.screen, (254, 52, 110), pygame.Rect(self.x, self.y, 2, 4))
        self.y -= 2

if __name__ == '__main__':
    game = Game(600, 400)
