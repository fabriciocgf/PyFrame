import pygame, random
from pygame.locals import *
import os
import stat

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 486
FADE_SPEED = 10
duration_millis = 1 * 1000

class Photo(pygame.sprite.Sprite):

    def __init__(self, photopath):
        self.start_time = pygame.time.get_ticks()
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
    # pygame.init()
    #
    # disp_no = os.getenv('DISPLAY')
    # if disp_no:
    #     print
    #     "I'm running under X display = {0}".format(disp_no)
    #
    # driver = 'directfb'
    # if not os.getenv('SDL_VIDEODRIVER'):
    #     os.putenv('SDL_VIDEODRIVER', driver)
    #
    # drivers = ['directfb', 'fbcon', 'svgalib']
    #
    # found = False
    # for driver in drivers:
    #     if not os.getenv('SDL_VIDEODRIVER'):
    #         os.putenv('SDL_VIDEODRIVER', driver)
    #     try:
    #         pygame.display.init()
    #     except pygame.error:
    #         print
    #         'Driver: {0} failed.'.format(driver)
    #         continue
    #     found = True
    #     break
    #
    # if not found:
    #     raise Exception('No suitable video driver found!')
    #
    # size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    # screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    photo_group = pygame.sprite.Group()
    assetlist = get_files_from_directory(os.path.join('..', 'assets'))
    print(assetlist)
    for i in range(2):
        photo = Photo(assetlist[i])
        photo_group.add(photo)

    clock = pygame.time.Clock()
    i=2
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    photo.update()

        if time_out(photo_group.sprites()[0]):
            photo_group.remove(photo_group.sprites()[0])
            photo = Photo(assetlist[i])
            photo_group.add(photo)
            i += 1
            if i==len(assetlist):
                i=1

        photo.update()
        photo_group.draw(screen)
        pygame.display.update()

if __name__ == '__main__':
    main()