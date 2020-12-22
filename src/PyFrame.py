import pygame, random
from pygame.locals import *
import os
import stat

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FADE_SPEED = 10
transition_time_seg = 1
photo_time_seg = 5

class Photo(pygame.sprite.Sprite):

    def __init__(self, photopath):
        self.start_time = pygame.time.get_ticks()
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(photopath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = 0
        self.rect[1] = 0


def time_out(sprite, duration):
    return (pygame.time.get_ticks() - sprite.start_time) >= duration * 1000

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

def complete_list(assets, photos):
    completeList = []
    for x in range(len(photos)):
        randomint = random.randint(0, len(assets)-1)
        completeList.append(photos[x])
        completeList.append(assets[randomint])
    return completeList

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#, pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    duration = transition_time_seg
    photoindex = 0
    photo_group = pygame.sprite.Group()
    photosList = get_files_from_directory(os.path.join('..', 'photos'))
    assetList = get_files_from_directory(os.path.join('..', 'assets'))
    completeList = complete_list(assetList, photosList)
    print(completeList)
    for y in range(2):
        photo = Photo(completeList[y])
        photo_group.add(photo)

    while True:
        clock.tick(3)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    pygame.quit()

        if time_out(photo_group.sprites()[-1],duration):
            if photoindex % 2 == 0:
                duration = photo_time_seg
            else:
                duration = transition_time_seg
            photo_group.remove(photo_group.sprites()[-1])
            photo = Photo(completeList[photoindex])
            photo_group.add(photo)
            photoindex += 1
            if photoindex == len(completeList):
                photoindex = 0

        photo_group.draw(screen)
        pygame.display.update()

if __name__ == '__main__':
    main()