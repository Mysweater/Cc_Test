from pygame import *
import sys
import random
import math

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, wight, height):
        super().__init__()

        self.image = transform.scale(
            image.load(player_image),
            (wight, height)
        )

        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):

    def update_left(self):
        keys = key.get_pressed()

        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed

        if keys[K_s] and self.rect.y < win_height - self.rect.height:
            self.rect.y += self.speed

    def update_right(self):
        keys = key.get_pressed()

        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed

        if keys[K_DOWN] and self.rect.y < win_height - self.rect.height:
            self.rect.y += self.speed


# ==========================
# Game setup
# ==========================

back = (200, 255, 255)

win_width = 600
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Ping Pong")

clock = time.Clock()
FPS = 60

game = True

font.init()
font1 = font.Font(None, 50)

lose1 = font1.render(
    "PLAYER 1 LOSES!",
    True,
    (255, 0, 0)
)

lose2 = font1.render(
    "PLAYER 2 LOSES!",
    True,
    (255, 0, 0)
)

# ==========================
# Sprites
# ==========================

racket1 = Player(
    "racket.png",
    30,
    200,
    5,
    20,
    100
)

racket2 = Player(
    "racket.png",
    550,
    200,
    5,
    20,
    100
)

ball = GameSprite(
    "tenis_ball.png",
    275,
    225,
    4,
    50,
    50
)

# ==========================
# Ball speed i needed to change it to be more independtant althjough i used angles :/
# ==========================

speed = 5

angle = random.uniform(-0.5, 0.5)
speed_x = speed * math.cos(angle)
speed_y = speed * math.sin(angle)

# ==========================
# Main loop
# ==========================

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False

    window.fill(back)

    # Move paddles
    racket1.update_left()
    racket2.update_right()

    # Move ball
    ball.rect.x += speed_x
    ball.rect.y += speed_y

    # Bounce off top wall
    if ball.rect.y <= 0:
        speed_y *= -1

    # Bounce off bottom wall
    if ball.rect.y >= win_height - ball.rect.height:
        speed_y *= -1

    # Left paddle
    if sprite.collide_rect(racket1, ball):
        ball.rect.left = racket1.rect.right + 1
        speed_x = abs(speed_x)

        offset = (ball.rect.centery - racket1.rect.centery)
        speed_y = offset / 10

        speed_x *= 1.05

    # Right paddle
    if sprite.collide_rect(racket2, ball):
        ball.rect.right = racket2.rect.left - 1
        speed_x = -abs(speed_x)

        offset = (ball.rect.centery - racket2.rect.centery)
        speed_y = offset / 10

        speed_x *= 1.05

    # Player 1 loses
    if ball.rect.x < 0:

        window.fill(back)

        racket1.reset()
        racket2.reset()
        ball.reset()

        window.blit(lose1, (150, 220))
        display.update()

        time.delay(3000)

        game = False

    # Player 2 loses
    elif ball.rect.x > win_width:

        window.fill(back)

        racket1.reset()
        racket2.reset()
        ball.reset()

        window.blit(lose2, (150, 220))
        display.update()

        time.delay(3000)

        game = False

    racket1.reset()
    racket2.reset()
    ball.reset()

    display.update()
    clock.tick(FPS)

quit()
sys.exit()