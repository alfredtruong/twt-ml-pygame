import pygame
pygame.init()

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 15

SCORE_FONT = pygame.font.SysFont("comicsans",50)
WINNING_SCORE = 5

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
        if up and (self.y-self.VEL >= 0):
            self.y -= self.VEL
        if not up and (self.y + self.VEL + self.height <= HEIGHT):
            self.y += self.VEL

class Ball:
    MAX_VEL = 5
    COLOR = WHITE

    def __init__(self, radius):
        self.x_vel = self.MAX_VEL
        self.reset_position()
        self.radius = radius

    def reset_position(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.x_vel *= -1
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

def draw(win, paddles, ball, scores):
    win.fill(BLACK)

    # draw scores
    left_score_text = SCORE_FONT.render(f"{scores[0]}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{scores[1]}", 1, WHITE)
    win.blit(left_score_text,((WIDTH//4) - left_score_text.get_width()//2, 20))
    win.blit(right_score_text,((3 * WIDTH//4) - right_score_text.get_width()//2, 20))

    # draw paddles
    for paddle in paddles:
        paddle.draw(win)

    # draw ball
    ball.draw(win)

    # draw divider
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 -5, i, 10, HEIGHT // 20))

    # do drawing
    pygame.display.update()  # apply all changes

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w]:
        left_paddle.move(up=True)
    if keys[pygame.K_s]:
        left_paddle.move(up=False)
    if keys[pygame.K_UP]:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN]:
        right_paddle.move(up=False)

def handle_collision(ball, left_paddle, right_paddle):
    # check collide top
    if ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    # check collide bottom
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1

    # check collide with paddles
    if ball.x_vel < 0:
        # left paddle
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                # handle x direction
                ball.x_vel *= -1

                # handle y direction
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = left_paddle.height / 2 / ball.MAX_VEL * -1
                ball.y_vel = difference_in_y / reduction_factor
    else:
        # right paddle
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                # handle x direction
                ball.x_vel *= -1

                # handle y direction
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = right_paddle.height / 2 / ball.MAX_VEL * -1
                ball.y_vel = difference_in_y / reduction_factor

def main():
    run = True
    clock = pygame.time.Clock() # result FPS

    # init paddles
    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    # init ball
    ball = Ball(BALL_RADIUS)

    # init game status
    game_started = False

    def reset_items():
        left_paddle.reset_position()
        right_paddle.reset_position()
        ball.reset_position()
        game_started = False

    # init scores
    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, [left_score, right_score])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        if keys:
            game_started = True

        if game_started:
            handle_collision(ball, left_paddle, right_paddle)
            ball.move()

            # score detection
            if ball.x < 0:
                right_score += 1
                reset_items()

            if ball.x > WIDTH:
                left_score += 1
                reset_items()

            # end of game detection
            if left_score == WINNING_SCORE:
                reset_items()
                left_score, right_score = 0, 0

            if right_score == WINNING_SCORE:
                left_score, right_score = 0, 0

    pygame.quit()

if __name__ == "__main__":
    main()
