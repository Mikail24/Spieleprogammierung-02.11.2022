import os
import pygame
import time
import random


class Settings():                                   # Statische Klasse
    SCREENRECT = pygame.rect.Rect(0, 0, 1000, 600)
    FPS = 60
    PATHFILE = os.path.dirname(os.path.abspath(__file__))
    PATHIMG = os.path.join(PATHFILE, "images")

    @staticmethod
    def get_imagepath(filename):
        return os.path.join(Settings.PATHIMG, filename)


class playground(pygame.sprite.Sprite):
    def __init__(self, filename, colorkey=None) -> None:
        super().__init__()
        if colorkey is None:
            self.image = pygame.image.load(Settings.get_imagepath(filename)).convert_alpha()
        else:
            self.image = pygame.image.load(Settings.get_imagepath(filename)).convert()
            self.image.set_colorkey(colorkey)

        self.image = pygame.transform.scale(self.image, (100, 100))

        self.rect = self.image.get_rect()
        self.vel = [0, 0]

    def update(self) -> None:
        self.rect.left += self.vel[0]
        self.rect.top += self.vel[1]
        if self.rect.right >= Settings.SCREENRECT.width or self.rect.left < 0:
            self.vel[0] *= -1
        if self.rect.bottom >= Settings.SCREENRECT.height or self.rect.top < 0:
            self.vel[1] *= -1
        return super().update()


class Game():
    def __init__(self) -> None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()                                   # Subsysteme starten
        self.screen = pygame.display.set_mode(Settings.SCREENRECT.size)    # Bildschirm/Fenster dimensionieren
        self.clock = pygame.time.Clock()                     # Taktgeber

        self.all_forms = pygame.sprite.Group()
        self.all_obstacles = pygame.sprite.Group()
        self.test_run = pygame.sprite.Group()

        self.background = pygame.image.load(Settings.get_imagepath("background03.png")).convert()
        self.background = pygame.transform.scale(self.background, Settings.SCREENRECT.size)

        cactus = playground("icons8-kaktus-100.png")
        cactus.rect.right = random.randint(200, 800)
        cactus.rect.bottom = random.randint(200, 800)
        cactus.vel = [0, 0]
        self.all_forms.add(cactus)
        self.test_run.add(cactus)

        rectangle1 = playground("icons8-gestrichenes-rechteck-64.png")
        rectangle1.rect.right = 500
        rectangle1.rect.bottom = 200
        rectangle1.vel = [0, 0]
        self.all_obstacles.add(rectangle1)

        ycircle = playground("icons8-yellow-circle-48.png")
        ycircle.rect.right = 200
        ycircle.rect.bottom = 550
        ycircle.vel = [0, 0]
        self.all_obstacles.add(ycircle)

        rectangle2 = playground("icons8-gestrichenes-rechteck-64.png")
        rectangle2.rect.right = 700
        rectangle2.rect.bottom = 350
        rectangle2.vel = [0, 0]
        self.all_obstacles.add(rectangle2)

        gcircle = playground("icons8-green-circle-48.png")
        gcircle.rect.right = 500
        gcircle.rect.bottom = 450
        gcircle.vel = [0, 0]
        self.all_obstacles.add(gcircle)

        form = playground("icons8-unmögliche-formen-48.png")
        form.rect.right = 900
        form.rect.bottom = 200
        form.vel = [0, 0]
        self.all_obstacles.add(form)

        self.entry_before = 0
        self.running = True                                  # Flagvariable

    def start(self):
        while self.running:                                  # Hauptprogrammschleife
            self.clock.tick(Settings.FPS)                    # Auf mind. 1/60s takten
            self.watch_for_events()
            self.update()
            self.draw()
            self.disappear()

            for sprite in self.all_forms.sprites():
                if pygame.sprite.spritecollideany(sprite, self.all_obstacles):
                    self.test_run.draw(self.screen)

        pygame.quit()                                   # Subssysteme stoppen

    def watch_for_events(self):
        for event in pygame.event.get():            # Einlesen der Message-Queue
            if event.type == pygame.QUIT:           # Ist X angeklickt worden?
                self.running = False                     # Toggle Flag
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        self.all_forms.update()
        self.all_obstacles.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.all_forms.draw(self.screen)
        self.all_obstacles.draw(self.screen)
        pygame.display.flip()

    def disappear(self):
        for sprite in self.all_forms.sprites():
            if pygame.sprite.spritecollideany(sprite, self.all_obstacles):
                sprite.kill()

def main():
    game = Game()
    game.start()

if __name__ == "__main__":
    main()