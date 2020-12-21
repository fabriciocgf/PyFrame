import pygame, random
from pygame.locals import *
import os
import stat

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
FADE_SPEED = 10
duration_millis = 1 * 1000
i=2

class Photo(pygame.sprite.Sprite):

    def __init__(self, photopath):
        self.start_time = pygame.time.get_ticks()
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(photopath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))


        self.rect = self.image.get_rect()
        self.rect[0] = 0
        self.rect[1] = 0


def time_out(sprite):
    return (pygame.time.get_ticks() - sprite.start_time) >= duration_millis

def get_files_from_directory(path: str):
    files = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        file_mode = os.stat(file_path)[stat.ST_MODE]
        if stat.S_ISDIR(file_mode):
            files.extend(FileLoader.get_files_from_directory(file_path))
        elif stat.S_ISREG(file_mode):
            _, ext = os.path.splitext(file)
            if ext.lower() in ['.bmp']:
                files.append(file_path)
    return files

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#, pygame.FULLSCREEN)

    photo_group = pygame.sprite.Group()
    assetlist = get_files_from_directory(os.path.join('..', 'photos'))
    print(assetlist)
    for i in range(2):
        photo = Photo(assetlist[i])
        photo_group.add(photo)

    clock = pygame.time.Clock()
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    pygame.quit()



        if time_out(photo_group.sprites()[-1]):
            photo_group.remove(photo_group.sprites()[0])
            photo = Photo(assetlist[i])
            photo_group.add(photo)
            i += 1
            if i==len(assetlist):
                i=1

        photo_group.draw(screen)
        pygame.display.update()

if __name__ == '__main__':
    main()