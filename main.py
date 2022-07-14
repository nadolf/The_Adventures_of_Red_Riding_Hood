import pygame

pygame.init()

clock = pygame.time.Clock()
FPS = 60
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
scroll = 0


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Adventures of Red Riding Hood!")

background_imgs = []
for i in range(1, 3):
    background_image = pygame.image.load(
        f"Assets/background_layer_{i}.png").convert_alpha()
    background_imgs.append(background_image)
    bg_width = background_imgs[0].get_width()


def background():
    for x in range(5):
        speed = 1
        for i in background_imgs:
            screen.blit(i, ((x * bg_width) - scroll * speed, 0))
            speed += 0.25

run = True
while run:
    clock.tick(FPS)

    background()
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and scroll > 0:
        scroll -= 5
    if key[pygame.K_RIGHT] and scroll < 3000:
        scroll += 5

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()