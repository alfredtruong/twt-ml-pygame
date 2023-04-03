import pygame
import random
import math

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Paddle:
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, width, height):
        self.original_x = x
        self.original_y = y
        self.reset_position()
        self.width = width
        self.height = height

    def reset_position(self):
        self.x = self.original_x
        self.y = self.original_y

    def draw(self, win):
        pygame.draw.rect(
            win,
            self.COLOR,
            (self.x, self.y, self.width, self.height)
        )

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL


class Ball:
    MAX_VEL = 5
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x_original = x
        self.y_original = y
        self.radius = radius

        self.x_vel = 1 if random.random() < 0.5 else -1 # random starting direction
        self.reset_position()

    def reset_position(self):
        self.x = self.x_original
        self.y = self.y_original

        # direction
        angle = random.randrange(1,30) # random positive angle between 1 and 30
        angle = math.radians(angle) # in radians

        self.x_vel = self.MAX_VEL * math.cos(angle) * (1 if self.x_vel < 0 else -1) # flip direction
        self.y_vel = self.MAX_VEL * math.sin(angle) * (1 if random.random() < 0.5 else -1) # up or down

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel


class Pong:
    WIDTH = 700
    HEIGHT = 500
    PADDLE_WIDTH = 20
    PADDLE_HEIGHT = 100
    BALL_RADIUS = 15
    WINNING_SCORE = 5

    def __init__(self):
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pong")
        self.SCORE_FONT = pygame.font.SysFont("comicsans", 50)

        # init stats
        self.stats = Stats()

        # init paddles
        self.left_paddle = Paddle(10, self.HEIGHT // 2 - self.PADDLE_HEIGHT // 2, self.PADDLE_WIDTH, self.PADDLE_HEIGHT)
        self.right_paddle = Paddle(self.WIDTH - 10 - self.PADDLE_WIDTH, self.HEIGHT // 2 - self.PADDLE_HEIGHT // 2, self.PADDLE_WIDTH, self.PADDLE_HEIGHT)

        # init ball
        self.ball = Ball(self.WIDTH // 2, self.HEIGHT // 2, self.BALL_RADIUS)

    def reset_board(self):
        self.left_paddle.reset_position()
        self.right_paddle.reset_position()
        self.ball.reset_position()

    def reset_game(self):
        self.reset_board()
        self.stats.reset()

    def draw(self):
        self.win.fill(BLACK)

        # draw scores
        left_score_text = self.SCORE_FONT.render(f"{self.stats.left_score}", 1, WHITE)
        right_score_text = self.SCORE_FONT.render(f"{self.stats.right_score}", 1, WHITE)
        self.win.blit(left_score_text, ((self.WIDTH // 4) - left_score_text.get_width() // 2, 20))
        self.win.blit(right_score_text, ((3 * self.WIDTH // 4) - right_score_text.get_width() // 2, 20))

        # draw paddles
        self.left_paddle.draw(self.win)
        self.right_paddle.draw(self.win)

        # draw ball
        self.ball.draw(self.win)

        # draw divider
        for i in range(10, self.HEIGHT, self.HEIGHT // 20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(self.win, WHITE, (self.WIDTH // 2 - 5, i, 10, self.HEIGHT // 20))

        # do drawing
        pygame.display.update()  # apply all changes

    def single_paddle_movement(self, paddle, is_up):
        if is_up and (paddle.y - paddle.VEL >= 0):
            paddle.move(is_up)
        elif (paddle.y + paddle.VEL + paddle.height <= self.HEIGHT):
            paddle.move(is_up)

    def handle_paddle_movements(self, keys):
        if keys[pygame.K_w]:
            self.single_paddle_movement(self.left_paddle, True)
        if keys[pygame.K_s]:
            self.single_paddle_movement(self.left_paddle, False)
        if keys[pygame.K_UP]:
            self.single_paddle_movement(self.right_paddle, True)
        if keys[pygame.K_DOWN]:
            self.single_paddle_movement(self.right_paddle, False)

    def handle_collision(self):
        # check collide top
        if self.ball.y - self.ball.radius <= 0:
            self.ball.y_vel *= -1

        # check collide bottom
        if self.ball.y + self.ball.radius >= self.HEIGHT:
            self.ball.y_vel *= -1

        # check collide with paddles
        if self.ball.x_vel < 0:
            # left paddle
            if self.left_paddle.y <= self.ball.y <= self.left_paddle.y + self.left_paddle.height:
                if self.ball.x - self.ball.radius <= self.left_paddle.x + self.left_paddle.width:
                    # handle x direction
                    self.ball.x_vel *= -1

                    # handle y direction
                    middle_y = self.left_paddle.y + self.left_paddle.height / 2
                    difference_in_y = middle_y - self.ball.y
                    reduction_factor = self.left_paddle.height / 2 / self.ball.MAX_VEL * -1
                    self.ball.y_vel = difference_in_y / reduction_factor
        else:
            # right paddle
            if self.right_paddle.y <= self.ball.y <= self.right_paddle.y + self.right_paddle.height:
                if self.ball.x + self.ball.radius >= self.right_paddle.x:
                    # handle x direction
                    self.ball.x_vel *= -1

                    # handle y direction
                    middle_y = self.right_paddle.y + self.right_paddle.height / 2
                    difference_in_y = middle_y - self.ball.y
                    reduction_factor = self.right_paddle.height / 2 / self.ball.MAX_VEL * -1
                    self.ball.y_vel = difference_in_y / reduction_factor

    def handle_keyboard_input(self):
        keys = pygame.key.get_pressed()
        self.handle_paddle_movements(keys)

    def step_frame(self):
        self.handle_collision()
        self.ball.move()

        # score detection
        if self.ball.x < 0:
            self.stats.right_score += 1
            self.reset_board()

        if self.ball.x > self.WIDTH:
            self.stats.left_score += 1
            self.reset_board()

        # end of game detection
        if self.stats.left_score == self.WINNING_SCORE:
            self.reset_game()

        if self.stats.right_score == self.WINNING_SCORE:
            self.reset_game()


class Stats:
    def __init__(self):
        self.left_hits = 0
        self.right_hits = 0
        self.left_score = 0
        self.right_score = 0

    def reset(self):
        self.left_hits = 0
        self.right_hits = 0
        self.left_score = 0
        self.right_score = 0


FPS = 60


def main():
    run = True
    clock = pygame.time.Clock()  # result FPS
    game = Pong()

    while run:
        clock.tick(FPS)
        game.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        game.handle_keyboard_input()
        game.step_frame()

    pygame.quit()


if __name__ == "__main__":
    main()
