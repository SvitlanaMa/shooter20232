import pygame
from random import randint

pygame.init()

window = pygame.display.set_mode((700, 500))
pygame.display.set_caption("Shooter")
FPS = 60
clock = pygame.time.Clock()

background = pygame.image.load("galaxy.jpg")
background = pygame.transform.scale(background, (700, 500))

fire_snd = pygame.mixer.Sound("fire.ogg")

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = image
        self.speed = speed
    def paint(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite): 
    def __init__(self, x, y, w, h, image, speed, bullets_max):
        super().__init__(x, y, w, h, image, speed)
        self.bullets_max = bullets_max
        self.have_bullets = bullets_max
        self.need_reload = False

    def move(self):
        k = pygame.key.get_pressed()
    
        if k[pygame.K_a]:
            if self.rect.x >= 0:
                self.rect.x -= self.speed
        if k[pygame.K_d]:
            if self.rect.right <= 700:
                self.rect.x += self.speed

    def shoot(self):
        if not self.need_reload:
            # k = pygame.key.get_pressed()
            # if k[pygame.K_SPACE]:
            # fire_snd.play()
            bullet = Bullet(self.rect.centerx - 2, self.rect.y, 5, 10, bullet_img, 5)
            self.have_bullets -= 1
            if self.have_bullets == 0:
                self.need_reload = True

bullet_group = pygame.sprite.Group()

class Bullet(GameSprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image, speed)
        bullet_group.add(self) 

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom <= 0:
            bullet_group.remove(self)

enemies_group = pygame.sprite.Group()
ban = 0

class Enemy(GameSprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image, speed)
        enemies_group.add(self)

    def update(self):
        global ban
        self.rect.y += self.speed
        if self.rect.y >= 500:
            enemies_group.remove(self)
            ban += 1

enemy_img = pygame.image.load("ufo.png")
# enemy = Enemy(350, 0, 50, 40, enemy_img, 2)

bullet_img = pygame.image.load("bullet.png")

player_img = pygame.image.load("rocket.png")
player = Player(350, 450, 40, 45, player_img, 4, 10)

font1 = pygame.font.SysFont("Arial", 20)

enemy_wait = 20

score = 0
max_score = 0

try:
    with open("hit.txt", "r") as file:
        max_score = int(file.read())
except FileNotFoundError:
    file = open("hit.txt", "x")
    file.close()
except ValueError:
    pass 

print(max_score)
en_min_speed = 1
en_max_speed = 2

game = True
finish = False

while game:

    if not finish:

        if enemy_wait == 0:
            enemy = Enemy(randint(0, 650), -50, 50, 40, enemy_img, randint(en_min_speed, en_max_speed))
            enemy_wait = randint(50, 70)
        else:
            enemy_wait -= 1
        
        window.blit(background, (0, 0))
        points_lb = font1.render("Рахунок: " + str(score), True, (255,255,255))
        lost_lb = font1.render("Пропущено: " + str(ban), True, (255, 255, 255))
        bullets_lb = font1.render("Залишилось куль: " + str(player.have_bullets), True, (255, 255, 255))
        window.blit(lost_lb, (0, 0))
        window.blit(points_lb, (0, 50))
        window.blit(bullets_lb, (400, 0))
        player.paint()
        player.move()
    
        enemies_group.draw(window)
        enemies_group.update()
        bullet_group.draw(window)
        bullet_group.update()
        
        if pygame.sprite.spritecollide(player, enemies_group, False) or ban >=3 :
            finish = True
            if score > max_score:
                max_score = score
                with open("hit.txt", "w") as file:
                    file.write(str(max_score))
                rec = font1.render("Новий рекорд! " + str(max_score), True, (255, 255, 255))
            else:
                rec = font1.render("Ви набрали " + str(score) + " очок", True, (255, 255, 255))
            window.blit(rec, (200, 200))
        if pygame.sprite.groupcollide(enemies_group, bullet_group, True, True):
            score += 1
            if score % 5 == 0:

            # if score == 10 or score == 20:
                en_min_speed += 1
                en_max_speed += 1
            print(score)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.shoot()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and player.need_reload:
            player.have_bullets = player.bullets_max
            player.need_reload = False
    pygame.display.update()
    clock.tick(FPS)