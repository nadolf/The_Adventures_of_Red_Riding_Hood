import pygame
import os
import random
import csv

pygame.init()

clock = pygame.time.Clock()
FPS = 60
GRAVITY = 0.60
SCREEN_WIDTH = 700
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.7)
level = 1
ROWS = 16
COLS =150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 16
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
scroll = 0
moving_left = False
moving_right = False
shoot = False
greenArrow = False
greenArrow_thrown = False

img_list =[]
for x in range(TILE_TYPES):
    img = pygame.image.load(f'Assets/tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

health_img = pygame.image.load("Assets/health.png")
health_img = pygame.transform.scale(
    health_img,
    (int(health_img.get_width() / 15), int(health_img.get_height() / 15)))
arrow_box_img = pygame.image.load("Assets/arrow_box.png")
arrow_box_img = pygame.transform.scale(
    arrow_box_img,
    (int(arrow_box_img.get_width() / 30), int(arrow_box_img.get_height() / 30)))
arrow2_box_img = pygame.image.load("Assets/arrow2_box.png")
arrow2_box_img = pygame.transform.scale(
    arrow2_box_img,
    (int(arrow2_box_img.get_width() / 30), int(arrow2_box_img.get_height() / 30)))
item_boxes = {
    'Health' : health_img,
    'Arrow' : arrow_box_img,
    'Arrow2' : arrow2_box_img
}
arrow_img = pygame.image.load("Assets/arrow.png")
arrow_img = pygame.transform.scale(
    arrow_img,
    (int(arrow_img.get_width() / 15), int(arrow_img.get_height() / 15)))
arrow2_img = pygame.image.load("Assets/arrow2.png")
arrow2_img = pygame.transform.scale(
    arrow2_img,
    (int(arrow2_img.get_width() / 15), int(arrow2_img.get_height() / 15)))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Adventures of Red Riding Hood!")

font = pygame.font.SysFont('Times New Roman', 20)
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

background_imgs = []
for i in range(0, 8):
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
        #
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0

        animation_types = ['Idle', 'Run', 'Jump', 'Death', 'Attack']
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
        self.width = self.image.get_width()
        self.height = self.image.get_height()

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
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air =False
                    dy = tile[1].top - self.rect.bottom

        self.rect.x += dx
        self.rect.y += dy

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            arrow = Arrow(
                self.rect.centerx + (0.75 * self.rect.size[0] * self.direction),
                self.rect.centery, self.direction)
            arrow_group.add(arrow)
            self.ammo -= 1

    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 50
            if self.vision.colliderect(player.rect):
                self.update_action(4)
                player.health-=0.1
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)
                    self.move_counter += 1
                    self.vision.center = (self.rect.centerx + 50 * self.direction, self.rect.centery)
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

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
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
class World():
    def __init__(self):
        self.obstacle_list = []
    def process_data(self, data):
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect =  img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 3:
                        self.obstacle_list.append(tile_data)
                    elif tile == 4:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile >=5 and tile <= 9:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 11:
                        player = Character('player', x * TILE_SIZE, y * TILE_SIZE, 2, 2, 10, 3)
                    elif tile == 12:
                        wolf = Character('wolf', x * TILE_SIZE, y * TILE_SIZE, 2, 2, 0, 0)
                        enemy_group.add(wolf)
                    elif tile == 13:
                        item_box = ItemBox('Arrow', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 14:
                        item_box = ItemBox('Arrow2', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 15:
                        item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 10:
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
        return player
    def draw(self):
        for tile in self.obstacle_list:
            screen.blit(tile[0], tile[1])



class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type =  item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
   
    def update(self):
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'Health':
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Arrow':
                player.ammo += 3
            elif self.item_type == 'Arrow2':
                player.greenArrows +=1
            self.kill()

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

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

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
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y
        self.rect.x += dx
        self.rect.y += dy
        
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom

        self.rect.x += dx
        self.rect.y += dy

        if pygame.sprite.spritecollide(wolf, greenArrow_group, False):
            if wolf.alive:
                wolf.health -= 50
                self.kill()

enemy_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
greenArrow_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

world_data = []
for row in range(ROWS):
	r = [-1] * COLS
	world_data.append(r)
with open(f'level{level}_data.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for x, row in enumerate(reader):
		for y, tile in enumerate(row):
			world_data[x][y] = int(tile)
world = World()
player = world.process_data(world_data)

run = True
while run:
    clock.tick(FPS)

    background()
    world.draw()
    draw_text(f'Health: {int(player.health)}', font, WHITE, 10, 30)
    draw_text(f'Arrow: {player.ammo}', font, WHITE, 10, 50)
    draw_text(f'Green Arrow: {player.greenArrows}', font, WHITE, 10, 70)
    player.update()
    player.draw()

    for wolf in enemy_group:
        wolf.ai()
        wolf.update()
        wolf.draw()

    arrow_group.update()
    greenArrow_group.update()
    item_box_group.update()
    decoration_group.update()
    water_group.update()
    exit_group.update()
    arrow_group.draw(screen)
    greenArrow_group.draw(screen)
    item_box_group.draw(screen)
    decoration_group.draw(screen)
    water_group.draw(screen)
    exit_group.draw(screen)

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
        scroll -= 2
    if key[pygame.K_RIGHT] and scroll < 1100:
        scroll += 2

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