from pygame import *

class GameSprite(sprite.Sprite):
  def __init__(self, player_image, player_x, player_y, player_speed):
    super().__init__()
    self.image = transform.scale(image.load(player_image), (60, 60))
    self.speed = player_speed
    self.rect = self.image.get_rect()
    self.rect.x = player_x
    self.rect.y = player_y

  def reset(self):
    window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
  def update(self):
    keys_pressed = key.get_pressed()
    if keys_pressed[K_a] and self.rect.x > 5:
      self.rect.x -= self.speed
    if keys_pressed[K_d] and self.rect.x < 635:
      self.rect.x += self.speed
    if keys_pressed[K_w] and self.rect.y > 5:
      self.rect.y -= self.speed
    if keys_pressed[K_s] and self.rect.y < 435:
      self.rect.y += self.speed

class Enemy(GameSprite):
  def __init__(self, player_image, player_x, player_y, player_speed):
    super().__init__(player_image, player_x, player_y, player_speed)
    self.direction = 'left'
    
  def update(self):
    if self.direction == 'left':
      self.rect.x -= self.speed
    else:
      self.rect.x += self.speed
    if self.rect.x > 620:
      self.direction = 'left'
    if self.rect.x < 450:
      self.direction = 'right'

class Wall(sprite.Sprite):
  def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
    super().__init__()
    self.color_1 = color_1
    self.color_2 = color_2
    self.color_3 = color_3 
    self.width = wall_width
    self.height = wall_height
    self.image = Surface((self.width, self.height))
    self.image.fill((color_1, color_2, color_3))
    self.rect = self.image.get_rect()
    self.rect.x = wall_x
    self.rect.y = wall_y

  def draw_wall(self):
    window.blit(self.image, (self.rect.x, self.rect.y))

#Игровая сцена
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Maze')
background = transform.scale(image.load('background.jpg'), 
(win_width, win_height))

w1 = Wall(0, 255, 100, 50, 50, 10, 300)
#w2, w3, w4,...

player = Player('hero.png', 5, 420, 4)
monster = Enemy('cyborg.png', 620, 280, 2)
finish = GameSprite('treasure.png', 580, 420, 0)

game = True
final = False
clock = time.Clock()
FPS = 60

font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

while game:
  for e in event.get():
    if e.type == QUIT:
      game = False
  
  if final != True:
    window.blit(background, (0,0))
    player.reset()
    monster.reset()
    finish.reset()

    player.update()
    monster.update()
    w1.draw_wall()

    if sprite.collide_rect(player, w1) or sprite.collide_rect(player, monster):
      final = True
      kick.play()
      window.blit(lose, (200,200))

    if sprite.collide_rect(player, finish):
      final = True
      money.play()
      window.blit(win, (200,200))

  display.update()
  clock.tick(FPS)