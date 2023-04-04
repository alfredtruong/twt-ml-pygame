# for base game
import pygame
import random
import math

# for neat
import neat
import os
import pickle

##########################################
# code for pong
##########################################
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

    def draw_paddle(self, win):
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
        angle = random.randrange(5,30) # random positive angle between 1 and 30
        angle = math.radians(angle) # in radians

        self.x_vel = self.MAX_VEL * math.cos(angle) * (1 if self.x_vel < 0 else -1) # flip direction
        self.y_vel = self.MAX_VEL * math.sin(angle) * (1 if random.random() < 0.5 else -1) # up or down

    def draw_ball(self, win):
        pygame.draw.circle(
            win,
            self.COLOR,
            (self.x, self.y),
            self.radius
        )

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel


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


class Pong:
    PADDLE_WIDTH = 20
    PADDLE_HEIGHT = 100
    BALL_RADIUS = 15
    WINNING_SCORE = 5
    SCORE_FONT = pygame.font.SysFont("comicsans", 50)

    def __init__(self, win, win_width, win_height, should_draw):
        # plotting device
        self.win = win
        self.WIDTH = win_width
        self.HEIGHT = win_height
        self.should_draw = should_draw

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

    def draw_game(self, draw_scores=True, draw_hits=False):
        self.win.fill(BLACK)

        # draw scores
        if draw_scores:
            left_text = self.SCORE_FONT.render(f"{self.stats.left_score}", 1, WHITE)
            right_text = self.SCORE_FONT.render(f"{self.stats.right_score}", 1, WHITE)
            self.win.blit(left_text, ((self.WIDTH // 4) - left_text.get_width() // 2, 20))
            self.win.blit(right_text, ((3 * self.WIDTH // 4) - right_text.get_width() // 2, 20))

        # draw hits
        if draw_hits:
            left_text = self.SCORE_FONT.render(f"{self.stats.left_hits}", 1, WHITE)
            right_text = self.SCORE_FONT.render(f"{self.stats.right_hits}", 1, WHITE)
            self.win.blit(left_text, ((self.WIDTH // 4) - left_text.get_width() // 2, 20))
            self.win.blit(right_text, ((3 * self.WIDTH // 4) - right_text.get_width() // 2, 20))

        # draw paddles
        self.left_paddle.draw_paddle(self.win)
        self.right_paddle.draw_paddle(self.win)

        # draw ball
        self.ball.draw_ball(self.win)

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
        elif not is_up and (paddle.y + paddle.VEL + paddle.height <= self.HEIGHT):
            paddle.move(is_up)

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
                    self.stats.left_hits += 1

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
                    self.stats.right_hits += 1

                    # handle x direction
                    self.ball.x_vel *= -1

                    # handle y direction
                    middle_y = self.right_paddle.y + self.right_paddle.height / 2
                    difference_in_y = middle_y - self.ball.y
                    reduction_factor = self.right_paddle.height / 2 / self.ball.MAX_VEL * -1
                    self.ball.y_vel = difference_in_y / reduction_factor

    def handle_keyboard_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.single_paddle_movement(self.left_paddle, True)
        if keys[pygame.K_s]:
            self.single_paddle_movement(self.left_paddle, False)
        if keys[pygame.K_UP]:
            self.single_paddle_movement(self.right_paddle, True)
        if keys[pygame.K_DOWN]:
            self.single_paddle_movement(self.right_paddle, False)

    def score_detection(self):
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

    def loop(self):
        self.handle_collision()
        self.ball.move()
        self.score_detection()


##########################################
# window setup
##########################################
WIDTH = 700
HEIGHT = 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
FPS = 60


# human pong
def pong(should_draw = True):
    game = Pong(WIN, WIDTH, HEIGHT, should_draw)
    clock = pygame.time.Clock()  # result FPS

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # game input
        game.handle_keyboard_input()

        # game logic
        game.loop()

        # display
        if should_draw:
            game.draw_game()

    pygame.quit()

# ai pong training
class PongAI:
    def __init__(self, win, width, height, should_draw):
        self.game = Pong(win, width, height, should_draw)
        self.should_draw = should_draw
        self.clock = pygame.time.Clock()  # result FPS

    def train_ai(self, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            # game input
            output1 = net1.activate((self.game.left_paddle.y, self.game.ball.y, abs(self.game.left_paddle.x - self.game.ball.x)))
            output2 = net2.activate((self.game.right_paddle.y, self.game.ball.y, abs(self.game.right_paddle.x - self.game.ball.x)))
            #print(output1, output2)

            decision1 = output1.index(max(output1))
            if decision1 == 0:
                pass
            elif decision1 == 1:
                self.game.single_paddle_movement(self.game.left_paddle, True)
            elif decision1 == 2:
                self.game.single_paddle_movement(self.game.left_paddle, False)

            decision2 = output2.index(max(output2))
            if decision2 == 0:
                pass
            elif decision2 == 1:
                self.game.single_paddle_movement(self.game.right_paddle, True)
            elif decision2 == 2:
                self.game.single_paddle_movement(self.game.right_paddle, False)

            # game logic
            self.game.loop()

            # display
            if self.should_draw:
                self.game.draw_game(False, True)

            if self.game.stats.left_score >= 1 or self.game.stats.right_score >= 1 or self.game.stats.left_hits > 50:
                self.calculate_fitness(genome1, genome2, self.game.stats)
                break

    def calculate_fitness(self, genome1, genome2, stats):
        genome1.fitness += stats.left_hits
        genome2.fitness += stats.right_hits


    def test_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        run = True
        while run:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            # game input
            self.game.handle_keyboard_input()

            output2 = net.activate((self.game.right_paddle.y, self.game.ball.y, abs(self.game.right_paddle.x - self.game.ball.x)))
            decision2 = output2.index(max(output2))
            if decision2 == 0:
                pass
            elif decision2 == 1:
                self.game.single_paddle_movement(self.game.right_paddle, True)
            elif decision2 == 2:
                self.game.single_paddle_movement(self.game.right_paddle, False)

            # game logic
            self.game.loop()

            # display
            self.game.draw_game()

        pygame.quit()


def eval_genomes(genomes, config):
    # train one guy against all others
    for i, (genome_id1, genome1) in enumerate(genomes):
        # initialize fitness
        genome1.fitness = 0

        # look at other but not past end
        if i == len(genomes) - 1:
            break

        for j, (genome_id2, genome2) in enumerate(genomes[i+1:]):
            # initialize fitness
            genome2.fitness = 0 if genome2.fitness is None else genome2.fitness

            # info
            #print(f"combo [{i}, {j}], left_fitness = {genome1.fitness}")

            game = PongAI(WIN, WIDTH, HEIGHT, False)
            game.train_ai(genome1, genome2, config)

def run_neat(config):
    # get current population
    #p = neat.Checkpointer.restore_checkpoint('pong_ai_checkpoints/pong_ai_27')
    p = neat.Population(config)

    # specify dump stats
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1, filename_prefix="pong_ai_checkpoints/pong_ai_"))

    winner = p.run(eval_genomes, 20)  # fitness function

    with open("pong_ai_checkpoints/best.pickle","wb") as f:
        pickle.dump(winner, f)

def test_ai(config):
    with open("pong_ai_checkpoints/best.pickle","rb") as f:
        winner = pickle.load(f)

    game = PongAI(WIN, WIDTH, HEIGHT, True)
    game.test_ai(winner, config)

if __name__ == "__main__":
    should_with_ai = True
    should_test_ai = True

    if should_with_ai:
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, "pong_ai_neat_config.txt")

        config = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path
        )

        if not should_test_ai:
            run_neat(config)
        else:
            test_ai(config)
    else:
        pong()