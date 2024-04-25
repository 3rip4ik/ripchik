from pygame import *
import math

# Инициализация Pygame
init()

# Размеры окна
width, height = 800, 600

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Создание окна
window = display.set_mode((width, height))
display.set_caption("Pacman Mini")

# Класс спрайта игры
class GameSprite(sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Класс игрока
class Player(GameSprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__(picture, w, h, x, y)
        self.x_speed = 0
        self.y_speed = 0

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        if self.rect.x == 0:
            self.rect.x = 700
        if self.rect.x == 800:
            self.rect.x = 0
        if self.rect.y == 0:
            self.rect.y = 560
        if self.rect.y >= 600:
            self.rect.y = 0

# Класс Cute
class Cute(GameSprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__(picture, w, h, x, y)
        self.speed = 10
        self.direction = "right"

    def update(self):
        if self.rect.x <= 570:
            self.direction = "right"

        if self.rect.x >= width - 85:
            self.direction = "left"
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

# Класс пули
class Bullet(GameSprite):
    def __init__(self, picture, w, h, x, y, target_x, target_y):
        super().__init__(picture, w, h, x, y)
        self.speed = 10
        self.direction_x = target_x - x
        self.direction_y = target_y - y
        self.distance = math.sqrt(self.direction_x**2 + self.direction_y**2)

    def update(self):
        self.rect.x += self.direction_x / self.distance * self.speed
        self.rect.y += self.direction_y / self.distance * self.speed

# Класс стены
class Wall(GameSprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__(picture, w, h, x, y)

# Класс выигрышной зоны
class WinZone(GameSprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__(picture, w, h, x, y)

# Создание игрока
player = Player("free-icon-pussy-cat-cartoon-outline-variant-29662.png", 40, 40, 50, 50)

# Создание Cute в группе
cute_group = sprite.Group()
for i in range(1):
    cute = Cute("free-icon-cat-in-black-silhouette-29670.png", 40, 40, 600 + i * 100, 300)
    cute_group.add(cute)

# Создание стен
wall1 = Wall("wall.jpg", 40, 500, 300, 1)
wall2 = Wall("wall.jpg", 40, 400, 500, 200)

walls = sprite.Group(wall1, wall2)

# Создание выигрышной зоны
win_zone = WinZone("win_zone.png", 90, 90, 700, 500)


# Основной игровой цикл
run = True
bullets = sprite.Group()
while run:
    # Очистка окна
    window.fill(WHITE)

    # Обработка событий
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_w:
                player.y_speed = -5
            elif e.key == K_s:
                player.y_speed = 5
            elif e.key == K_a:
                player.x_speed = -5
            elif e.key == K_d:
                player.x_speed = 5
            elif e.key == K_SPACE:
                # Создаем пулю и направляем ее в сторону курсора мыши
                mouse_x, mouse_y = mouse.get_pos()
                bullet = Bullet("пуля.jpg", 10, 10, player.rect.x, player.rect.y, mouse_x, mouse_y)
                bullets.add(bullet)

        elif e.type == KEYUP:
            if e.key == K_w:
                player.y_speed = 0
            elif e.key == K_s:
                player.y_speed = 0
            elif e.key == K_a:
                player.x_speed = 0
            elif e.key == K_d:
                player.x_speed = 0

    # Обновление игрока
    player.update()
    player.reset()

    # Обновление Cute в группе
    cute_group.update()
    cute_group.draw(window)

    # Обновление стен
    walls.draw(window)

    # Обновление выигрышной зоны
    win_zone.reset()

    # Обновление пуль
    bullets.update()
    bullets.draw(window)

    # Проверка столкновений игрока с стенами
    player_collisions = sprite.spritecollide(player, walls, False)
    if player_collisions:
        player.rect.x -= player.x_speed
        player.rect.y -= player.y_speed

    # Проверка попадания игрока в выигрышную зону
    if player.rect.colliderect(win_zone.rect):
        font.init()
        win_font = font.SysFont("Arial", 100)
        win_text = win_font.render("WIN", True, (255, 0, 0))
        window.blit(win_text, (300, 250))
        display.update()
        time.delay(2000)
        run = False

    if sprite.spritecollide(player, cute_group, True):
        font.init()
        loss_font = font.SysFont("Arial Black", 100)
        loss_text = loss_font.render("Loss", True, (255, 0, 0))
        window.blit(loss_text, (300,250))
        display.update()
        time.delay(2000)
        run = False

    sprite.groupcollide(bullets, walls, True, False)

    # Проверка столкновений Cute с пулями
    for bullet in bullets:
        for cute in cute_group:
            if sprite.collide_rect(bullet, cute):
                cute_group.remove(cute)
                bullets.remove(bullet)

    # Обновление экрана
    display.update()

    # Управление частотой обновления экрана
    time.Clock().tick(60)
