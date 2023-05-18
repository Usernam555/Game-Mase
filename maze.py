#створи гру "Лабіринт"!
from pygame import *
import pygame_menu
init()

mixer.init()
#створи вікно гри
FPS = 60
WIDTH, HEIGHT = 1200, 900
p_down = transform.scale(image.load('w1.png'), (30, 30))
p_up = transform.scale(image.load('w2.png'), (30, 30))
p_left = transform.scale(image.load('w3.png'), (30, 30))
p_right = transform.scale(image.load('w4.png'), (30, 30))

window = display.set_mode((WIDTH, HEIGHT))

mixer.music.load('jungles.ogg')
mixer.music.play()
mixer.music.set_volume(0.5)
kick = mixer.Sound('kick.ogg')
kick.play()
re = 0
l = 1
#задай фон сцени
display.set_caption('Лабіринт')


class GameSprite(sprite.Sprite):
    def __init__(self, p_up, x, y, width, height):
        super().__init__()
        self.image = transform.scale(image.load(p_up), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self):
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def update(self):
        pressed = key.get_pressed()
        if pressed[K_w] and self.rect.y > 0:
            self.image = p_up
            self.rect.y -= 3
            for w in walls:
                if sprite.collide_rect(player, w):
                    self.rect.y += 3
                
                

        if pressed[K_s] and self.rect.y < HEIGHT - 40:
            self.image = p_down
            self.rect.y += 3
            for w in walls:
                if sprite.collide_rect(player, w):
                    self.rect.y -= 3

        if pressed[K_a] and self.rect.x > 0:
            self.image = p_left
            self.rect.x -= 3
            for w in walls:
                if sprite.collide_rect(player, w):
                    self.rect.x += 3


        if pressed[K_d] and self.rect.x < WIDTH - 40:
            self.image = p_right
            self.rect.x += 3
            for w in walls:
                if sprite.collide_rect(player, w):
                    self.rect.x -= 3

class Enemy(GameSprite):
    def __init__(self, x , y , sprite_img = 'snake.png', speed = 1):
        super().__init__(sprite_img, x, y, 30, 30)
        self.speed = speed
    def update(self, walls):
        for w in walls:
            if sprite.collide_rect(self, w):
                self.speed = self.speed * -1

        self.rect.x += self.speed 

class Enem(GameSprite):
    def __init__(self, x , y , sprite_img = 'snake.png', speed = 1):
        super().__init__(sprite_img, x, y, 30, 30)
        self.speed = speed
    def update(self, walls):
        for w in walls:
            if sprite.collide_rect(self, w):
                self.speed = self.speed * -1

        self.rect.y += self.speed 

class Wall(GameSprite):
    def __init__(self, x , y, ):
        super().__init__('wall.png', x, y, 30, 30)
        

class Coin(GameSprite):
    def __init__(self, x , y, ):
        super().__init__('pngegg.png', x, y, 20, 20)
        

bg = transform.scale(image.load("background.jpg"), (WIDTH, HEIGHT))

#створи 2 спрайти та розмісти їх на сцені

player = Player('w1.png', 40 , 350, 30, 30)

gold = GameSprite('key1.png', WIDTH - 100 , 420, 30, 30)
walls = []
enemys = []

coins = []
with open("map.txt", 'r') as file:
    x, y = 0, 0
    map = file.readlines()
    for line in map:
        for symbol in line:
            if symbol == 'W':
                walls.append(Wall(x, y))
            elif symbol == 'S':
                player.rect.x = x
                player.rect.y = y
            elif symbol == 'F':
                gold.rect.x = x
                gold.rect.y = y
            elif symbol == 'E':
                enemys.append(Enemy(x, y))
            elif symbol == 'U':
                enemys.append(Enem(x, y))
            elif symbol == 'C':
                coins.append(Coin(x + 7.5, y + 7.5))
            
                
            x += 30
        y += 30
        x = 0
#оброби подію «клік за кнопкою "Закрити вікно"»
run = True
finish = False
clock = time.Clock()

def set_difficulty(value, difficulty):
    if finish:
        level('map.txt')

    new_speed = 3
    
    if difficulty == 1:
        new_speed = 1

    elif difficulty == 2:
        new_speed = 2

    for e in enemys:
        e.speed = new_speed

def restart():
    global finish, walls, enemys, coins
    menu.disable()
    level('map.txt')

def level(filemap):
    global finish, walls, enemys, coins
    finish = False
    walls = []
    enemys = []
    coins = []
    with open(filemap, 'r') as file:
        x, y = 0, 0
        map = file.readlines()
        for line in map:
            for symbol in line:
                if symbol == 'W':
                    walls.append(Wall(x, y))
                elif symbol == 'S':
                    player.rect.x = x
                    player.rect.y = y
                elif symbol == 'F':
                    gold.rect.x = x
                    gold.rect.y = y
                elif symbol == 'E':
                    enemys.append(Enemy(x, y))
                elif symbol == 'U':
                    enemys.append(Enem(x, y))
                elif symbol == 'C':
                    coins.append(Coin(x + 7.5, y + 7.5))
            
                
                x += 30
            y += 30
            x = 0



def start_the_game():
    if finish:
        level('map.txt')
    menu.disable()

menu = pygame_menu.Menu('Меню', 1200, 900,
                       theme=pygame_menu.themes.THEME_GREEN)


menu.add.selector('Difficulty :', [('Hard', 2), ('Easy', 1)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Restart', restart)
menu.add.button('Quit', pygame_menu.events.EXIT)
font.init()
font1 = font.SysFont('Impact', 70)
result = font1.render('YOU LOSE' , True, (140, 100, 30))
menu.mainloop(window)

while run:

    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                menu.enable()
                menu.mainloop(window)

    if not finish:

        player.update()
        window.blit(bg, (0, 0))
        player.draw()
        
        gold.draw()
        for w in walls:
            w.draw()
            #if sprite.collide_rect(player, w):
                #finish = True

        for e in enemys:
            e.update(walls)
            e.draw()
            if sprite.collide_rect(player, e):
                finish = True
                menu.enable()
                menu.mainloop(window)
  

        

        for c in coins:
            c.draw() 
            if sprite.collide_rect(player, c):
                re += 1
                coins.remove(c)
                
                  

        if sprite.collide_rect(player, gold):
            #if len(coins) == 0:
                if l == 1:
                    level('map2.txt')
                elif l == 2:
                    level('map3.txt')
                elif l == 3:
                    finish = True
                    result = font1.render('YOU WIN'  , True, (210, 150, 100))
                l += 1
            
    else:
        window.blit(result, (450, 400))
    display.update()
    clock.tick(FPS)