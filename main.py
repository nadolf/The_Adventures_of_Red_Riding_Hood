import pygame
import os

pygame.init()

clock = pygame.time.Clock()
FPS = 60
GRAVITY = 0.75
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
scroll = 0
moving_left = False
moving_right = False

class Character(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        animation_types = ['Idle', 'Run', 'Jump']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f"Assets/{self.char_type}/{animation}"))
            for i in range(num_of_frames):
                img = pygame.image.load(
                    f"Assets/{self.char_type}/{animation}/image_{i}.png")
                img = pygame.transform.scale(
                    img,
                    (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        if self.jump == True and self.in_air ==False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y
        if self.rect.bottom + dy > 415:
            dy = 415 - self.rect.bottom
            self.in_air = False
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        ANIMATION_COOLDOWN = 100  #ANIMATION TIMER
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False),
                    self.rect)


player = Character('player', 100, 350, 2, 2)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Adventures of Red Riding Hood!")

background_imgs = []
for i in range(1, 3):
    background_image = pygame.image.load(
        f"Assets/background/background_layer_{i}.png").convert_alpha()
    background_imgs.append(background_image)
    bg_width = background_imgs[0].get_width()

BLACK = (0, 0, 0)

def background():
    for x in range(5):
        speed = 1
        for i in background_imgs:
            screen.blit(i, ((x * bg_width) - scroll * speed, 0))
            speed += 0.25
    pygame.draw.line(screen, BLACK, (0, 400), (SCREEN_WIDTH, 400))


run = True
while run:
    clock.tick(FPS)

    background()
    player.update_animation()
    player.draw()

    if player.alive:
        if player.in_air:
            player.update_action(2)
        elif moving_left or moving_right:
            player.update_action(1)
        else:
            player.update_action(0)
        player.move(moving_left, moving_right)

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and scroll > 0:
        scroll -= 5
    if key[pygame.K_RIGHT] and scroll < 3000:
        scroll += 5

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_UP and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False

    pygame.display.update()
pygame.quit()