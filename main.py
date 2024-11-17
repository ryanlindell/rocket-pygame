import pygame
import math
import random

pygame.init()
width = 1200
height = 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
camera = [width/2, height/2]
Dcamera = [0, 0]
map = [3000, 2000]
difficulty = 10
score = 0
running = 1
bullets = []
tick = 0

class Bullet:
    def __init__(self, parent):
        self.speed = 10
        self.accurancy = 100
        if parent.nature:
            self.speed = 8
            self.accurancy = 10
        self.tick = 0
        self.parent = parent
        self.x = parent.x + math.cos(parent.angle / 180 * math.pi) * parent.size
        self.y = parent.y - math.sin(parent.angle / 180 * math.pi) * parent.size

        self.Dy = -math.sin(parent.angle / 180 * math.pi + random.randint(-5, 5) / self.accurancy) * self.speed + parent.Dy
        self.Dx = math.cos(parent.angle / 180 * math.pi + random.randint(-5, 5) / self.accurancy) * self.speed + parent.Dx
        self.size = 5
        self.color = "black"

        self.hitbox = [self.x-self.size, self.y-self.size, self.x+self.size, self.y+self.size]

    def death_check(self):
        if not -map[0] < self.x < map[0]:
            if not -map[1] < self.y < map[1]:
                return 1
        if math.sqrt(self.Dx ** 2 + self.Dy ** 2) < 1:
            return 1
        if self.tick > 1000:
            return 1

    def move(self):
        self.x += self.Dx
        self.y += self.Dy
        self.Dx /= 1.03
        self.Dy /= 1.03
        self.tick += 1

        self.hitbox = [self.x - self.size / 2, self.y - self.size / 2, self.x + self.size / 2, self.y + self.size / 2]

    def collision_check(self, object):
        if not object.hitbox[0] < self.hitbox[2]:
            self.color = "black"
        elif not object.hitbox[2] > self.hitbox[0]:
            self.color = "black"
        elif not object.hitbox[1] < self.hitbox[3]:
            self.color = "black"
        elif not object.hitbox[3] > self.hitbox[1]:
            self.color = "black"
        else:
            self.color = "red"
            if object.nature == self.parent.nature:
                return 0
            object.hp -= 1
            return 1
        return 0

    def draw(self):
        camera_topleft = [camera[0] - width / 2, camera[1] - height / 2]
        pygame.draw.rect(screen, self.color, (self.x-self.size/2-camera_topleft[0], self.y-self.size/2-camera_topleft[1], self.size, self.size))
class Player:
    def __init__(self, nature):
        if nature == 0:
            self.hp = 20
        else:
            self.hp = 1
        self.nature = nature
        if nature == 0:
            self.x = width / 2
            self.y = height / 2
        else:
            self.x = random.randint(-map[0], map[0])
            self.y = random.randint(-map[1], map[1])
            while camera[0] - width/1.5 < self.x < camera[0] + width/1.5 and camera[1] - height/1.5 < self.y < camera[1] + height/1.5:
                self.x = random.randint(-map[0], map[0])
                self.y = random.randint(-map[1], map[1])
        self.color = (0, 0, 0)
        self.Dx = 0
        self.Dy = 0
        self.size = 30
        self.fatigue = 1
        self.angle = 0
        self.Dangle = 0
        self.boost = 0
        self.power = (random.random()+1)*5
        if nature:
            self.bulletSpeed = 1
        else:
            self.bulletSpeed = 5
        self.nature = nature

        #ai characteristics
        self.bias = 0

        self.hitbox = [self.x-self.size/2, self.y-self.size/2, self.x+self.size/2, self.y+self.size/2]
        if self.nature == 0:
            self.image_original = pygame.image.load("playership.png")
        elif self.nature == 1:
            self.image_original = pygame.image.load("enemy1.png")
        self.image_original = pygame.transform.scale(self.image_original, (self.size*3, self.size*3))

    def movement(self):
        # check bounds
        if not -map[0] < self.x + self.Dx < map[0]:
            self.Dx = 0
        if not -map[1] < self.y + self.Dy < map[1]:
            self.Dy = 0
        if not -map[0] < self.x < map[0]:
            self.x = map[0] * self.x / abs(self.x)
        if not -map[1] < self.y < map[1]:
            self.y = map[1] * self.y / abs(self.y)

        self.x += self.Dx
        self.y += self.Dy
        self.angle += self.Dangle/10
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < -360:
            self.angle += 360

        self.Dx /= 1.01
        self.Dy /= 1.01
        self.Dangle /= 1.04

        if 0.1 > self.Dx > -0.1:
            self.Dx = 0
        if 0.1 > self.Dy > -0.1:
            self.Dy = 0
        if 0.001 > self.Dangle > -0.001:
            self.Dangle = 0

        if self.boost:
            self.Dy -= math.sin(self.angle / 180 * math.pi) / 5
            self.Dx += math.cos(self.angle / 180 * math.pi) / 5

        self.hitbox = [self.x - self.size / 2, self.y - self.size / 2, self.x + self.size / 2, self.y + self.size / 2]

    def draw(self):
        self.image = pygame.transform.rotate(self.image_original, self.angle)
        camera_topleft = [camera[0] - width / 2, camera[1] - height / 2]
        self.imageRect = self.image.get_rect(center=(self.x-camera_topleft[0], self.y-camera_topleft[1]))
        screen.blit(self.image, self.imageRect)
        if self.color != (0,0,0):
            var = pygame.PixelArray(self.image_original)
            var.replace(self.color, (round(self.color[0]/1.1), round(self.color[1]/1.1), round(self.color[2]/1.1)))
            self.color = (round(self.color[0]/1.1), round(self.color[1]/1.1), round(self.color[2]/1.1))

    def death_check(self):
        if self.hp <= 0:
            return 1

    def ai_movement(self, player):
        self.bias += (random.random() - 0.5) * 50
        self.bias /= 1.5

        difX = player.x - self.x
        difY = -player.y + self.y
        try:
            angle = math.atan(difY / difX) * 180 / math.pi
        except:
            angle = 0
        if player.x - self.x < 0:
            angle -= 180
        self.angle = angle + self.bias/5
        if math.sqrt((player.x - self.x) ** 2 + (player.y - self.y) ** 2) > 200:
            self.boost = self.power + self.bias
        else:
            self.boost = 0
        self.movement()

    def ai(self):
        self.ai_movement(player)
        if random.randint(1, 100) == 7:
            bullets.append(Bullet(self))

player = Player(0)
enemies = []

while running:
    screen.fill("white")

    # inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_w]:
        player.boost = 1
    else:
        player.boost = 0
    if keys_pressed[pygame.K_a]:
        player.Dangle += 5
    if keys_pressed[pygame.K_d]:
        player.Dangle -= 5
    if not keys_pressed[pygame.K_a] and not keys_pressed[pygame.K_d]:
        playerDangle = 0
    if keys_pressed[pygame.K_SPACE]:
        player.fatigue *= 1.05
        if tick > player.bulletSpeed / 2 + player.fatigue * 5:
            bullets.append(Bullet(player))
            tick = 0
            player.fatigue *= 7

    # physics
    if player.fatigue > 0.000000001:
        player.fatigue /= 1.2
    if player.death_check():
        running = 0
    player.movement()
    for enemy in enemies:
        if enemy.death_check():
            enemies.remove(enemy)
            score += 1
            break
        enemy.ai()
    for bullet in bullets:
        if bullet.death_check():
            bullets.remove(bullet)
            break
        bullet.move()
        if bullet.collision_check(player):
            bullets.remove(bullet)
            var = pygame.PixelArray(player.image_original)
            var.replace(player.color, (255, 0, 0))
            player.color = (255, 0, 0)
            break
        for enemy in enemies:
            if bullet.collision_check(enemy):
                enemies.remove(enemy)
                score += 1
                bullets.remove(bullet)
                break

    # camera movement
    if player.x > camera[0] + width / 10:
        Dcamera[0] += 1
    if player.x < camera[0] - width / 10:
        Dcamera[0] -= 1
    if player.y > camera[1] + height / 10:
        Dcamera[1] += 1
    if player.y < camera[1] - height / 10:
        Dcamera[1] -= 1

    camera[0] += Dcamera[0]
    camera[1] += Dcamera[1]

    Dcamera[0] /= 1.05
    Dcamera[1] /= 1.05

    # drawing background
    block = 100  # size blocks in background
    for i in range(int(width / block) + 3):
        camera_topleft = [camera[0] - width / 2, camera[1] - height / 2]
        x = i * block
        pygame.draw.line(screen, (200, 200, 200), (x - camera_topleft[0] % block, 0), (x - camera_topleft[0] % block, height))
    for i in range(int(height / block) + 3):
        camera_topleft = [camera[0] - width / 2, camera[1] - height / 2]
        y = i * block
        pygame.draw.line(screen, (200, 200, 200), (0, y - camera_topleft[1] % block), (width, y - camera_topleft[1] % block))

    # drawing objects
    player.draw()
    e_drawn = 0
    for enemy in enemies:
        if camera[0] - width/1.5 < enemy.x < camera[0] + width/1.5:
            if camera[1] - height/1.5 < enemy.y < camera[1] + height/1.5:
                enemy.draw()
                e_drawn += 1
    for bullet in bullets:
        if camera[0] - width/1.5 < bullet.x < camera[0] + width/1.5:
            if camera[1] - height/1.5 < bullet.y < camera[1] + height/1.5:
                bullet.draw()
                e_drawn += 1

    pygame.display.update()
    clock.tick(60)

    tick += 1
    if random.randint(1, difficulty) == difficulty-1 and len(enemies) < 25:
        enemies.append(Player(1))
pygame.quit()
print(f"your score is: {score}")