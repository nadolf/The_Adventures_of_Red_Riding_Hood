from numpy import append
import pygame

pygame.init()

clock = pygame.time.Clock()
FPS = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 432

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Parallax")

bg_images = []
for i in range (1,3):
    bg_image=pygame.image.load(f"Assets/background_layer_{i}.png").convert_alpha()
    bg_images.append(bg_image)

def draw_bg():
    for i in bg_images:
        screen.blit(i, (0,0))

run = True
while run:
    clock.tick(FPS)

    draw_bg()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()
pygame.quit()