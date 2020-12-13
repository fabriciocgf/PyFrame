import pygame, random
from pygame.locals import *
import os

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 486
FADE_SPEED = 10


class Photo(pygame.sprite.Sprite):

    def __init__(self, photopath):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(photopath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.alpha = self.image.get_alpha()

        self.rect = self.image.get_rect()
        self.rect[0] = 0
        self.rect[1] = 0

    def update(self):
        self.alpha -= FADE_SPEED
        self.image.set_alpha(self.alpha)


def is_off_screen(sprite):
    return sprite.alpha <= 0

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

    photo_group = pygame.sprite.Group()
    assetlist = ['assets/noise_1.bmp','assets/noise_2.bmp','assets/noise_3.bmp']
    for i in range(2):
        photo = Photo(assetlist[i])
        photo_group.add(photo)

    clock = pygame.time.Clock()
    i=0
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    photo.update()


        if is_off_screen(photo_group.sprites()[0]):
            photo_group.remove(photo_group.sprites()[0])
            new_photo = Photo(assetlist[i])
            photo_group.add(new_photo)
            i += 1
            if i==3:
                i=1

        photo.update()
        photo_group.draw(screen)
        pygame.display.update()

if __name__ == '__main__':
    main()