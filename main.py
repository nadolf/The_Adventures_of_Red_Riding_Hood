import pygame
import os

pygame.init()

clock = pygame.time.Clock()
FPS = 60
GRAVITY = 0.75
TILE_SIZE = 40
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
BLACK = (0, 0, 0)
scroll = 0
moving_left = False
moving_right = False
shoot = False
greenArrow = False
greenArrow_thrown = False
arrow_img = pygame.image.load("Assets/arrow.png")
arrow2_img = pygame.image.load("Assets/arrow2.png")
arrow2_img = pygame.transform.scale(
    arrow2_img,
    (int(arrow2_img.get_width() / 15), int(arrow2_img.get_height() / 15)))
arrow_img = pygame.transform.scale(
    arrow_img,
    (int(arrow_img.get_width() / 15), int(arrow_img.get_height() / 15)))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Adventures of Red Riding Hood!")

background_imgs = []
for i in range(1, 3):
    background_image = pygame.image.load(
        f"Assets/background/background_layer_{i}.png").convert_alpha()
    background_imgs.append(background_image)
    bg_width = background_imgs[0].get_width()


def background():
    for x in range(5):
        speed = 0.5
        for i in background_imgs:
            screen.blit(i, ((x * bg_width) - scroll * speed, 0))
            speed += 0.25
    pygame.draw.line(screen, BLACK, (0, 400), (SCREEN_WIDTH, 400))


class Character(pygame.sprite.Sprite):

    def __init__(self, char_type, x, y, scale, speed, ammo, greenArrows):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.health = 100
        self.max_health = self.health
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.greenArrows = greenArrows
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        animation_types = ['Idle', 'Run', 'Jump', 'Death', 'Attack', 'Attack2']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(
                os.listdir(f"Assets/{self.char_type}/{animation}"))
            for i in range(num_of_frames):
                img = pygame.image.load(
                    f"Assets/{self.char_type}/{animation}/image_{i}.png"
                ).convert_alpha()
                img = pygame.transform.scale(img, (int(
                    img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

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
        if self.jump == True and self.in_air == False:
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

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            arrow = Arrow(
                self.rect.centerx + (0.5 * self.rect.size[0] * self.direction),
                self.rect.centery, self.direction)
            arrow_group.add(arrow)
            self.ammo -= 1

    def update_animation(self):
        ANIMATION_COOLDOWN = 100  #ANIMATION TIMER
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False),
                    self.rect)


class Arrow(pygame.sprite.Sprite):

    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = arrow_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.x += (self.direction * self.speed)
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        if pygame.sprite.spritecollide(player, arrow_group, False):
            if player.alive:
                player.health -= 5
        for wolf in enemy_group:
            if pygame.sprite.spritecollide(wolf, arrow_group, False):
                if wolf.alive:
                    wolf.health -= 25
                    self.kill()


class GreenArrow(pygame.sprite.Sprite):

    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -9
        self.speed = 5
        self.image = arrow2_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom + dy > 415:
            dy = 415 - self.rect.bottom
            self.speed = 0
        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
            self.direction *= -1
            dx = self.direction * self.speed

        self.rect.x += dx
        self.rect.y += dy
        if pygame.sprite.spritecollide(player, greenArrow_group, False):
            if player.alive:
                player.health -= 1
        if pygame.sprite.spritecollide(wolf, greenArrow_group, False):
            if wolf.alive:
                wolf.health -= 50
                self.kill()


enemy_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
greenArrow_group = pygame.sprite.Group()

player = Character('player', 100, 350, 2, 5, 10, 3)
wolf = Character('wolf', 400, 350, 2, 2, 10, 0)
enemy_group.add(wolf)

run = True
while run:
    clock.tick(FPS)

    background()
    player.update()
    player.draw()
    for wolf in enemy_group:
        wolf.update()
        wolf.draw()

    arrow_group.update()
    greenArrow_group.update()

    arrow_group.draw(screen)
    greenArrow_group.draw(screen)

    if player.alive:
        if shoot:
            player.shoot()
        elif greenArrow and greenArrow_thrown == False and player.greenArrows > 0:
            greenArrow = GreenArrow(player.rect.centerx + (0.3 * player.rect.size [0] * player.direction),\
                         player.rect.top, player.direction)
            greenArrow_group.add(greenArrow)
            greenArrow_thrown = True
            player.greenArrows -= 1
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
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_c:
                greenArrow = True
            if event.key == pygame.K_UP and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_c:
                greenArrow = False
                greenArrow_thrown = False
    pygame.display.update()
pygame.quit()