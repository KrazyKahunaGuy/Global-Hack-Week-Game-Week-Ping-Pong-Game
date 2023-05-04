import pygame
import random
import math

# Initialize  pygame
pygame.init()

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 600
BALL_RADIUS = 10
GAME_POINT = 5
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ping Pong')
font = pygame.font.Font(None, 36)
heading = pygame.font.Font(None, 90)

# Set colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game states
game_running = True
game_paused = False
game_ended = False
running = True


class Paddle:
    def __init__(self, id: int, is_ai: bool) -> None:
        self.width: int = PADDLE_WIDTH
        self.height: int = PADDLE_HEIGHT
        self.id: int = id
        self.pos: float = SCREEN_HEIGHT // 2 - 50
        self.hit: bool = False
        self.hit_time: int
        self.score: int = 0
        self.speed: int = PADDLE_SPEED
        self.is_ai: bool = is_ai
        # Load paddle images and apply surface blur effect
        self.paddle_image: pygame.Surface = pygame.image.load(
            'assets/paddle.png').convert_alpha()
        self.paddle_image = pygame.transform.scale(
            self.paddle_image, (self.width, self.height))

    @staticmethod
    # Define a function to apply surface blur to a surface
    def surface_blur(surface: pygame.Surface, radius: int):
        temp_surface: pygame.Surface = surface.copy()
        for i in range(radius):
            temp_surface.blit(surface, (0, 0))
            pygame.draw.rect(temp_surface, (255, 255, 255),
                             (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 1)
        return temp_surface

    # Define a function to handle wobble
    def wobble(self):
        time_diff = pygame.time.get_ticks() - self.hit_time
        self.pos += math.sin(time_diff * 0.05) * 10  # Wobble the paddle
        if time_diff > 200:  # Stop the wobbling after 200ms
            return False
        return True
    
    # Define a function to handle an AI player
    def ai_move(self, ball):
        if self.is_ai:
            if self.pos + self.height/2 < ball.pos_y:
                self.pos += self.speed/CLOCK.get_fps()
            elif self.pos + self.height/2 > ball.pos_y:
                self.pos -= self.speed/CLOCK.get_fps()

    # Define a function to handle a player winning
    def win(self):
        if self.score == 10:
            return True
        return False


class Ball:
    def __init__(self) -> None:
        self.pos_x: int = SCREEN_WIDTH // 2
        self.pos_y: int = SCREEN_HEIGHT // 2
        self.vel_x: int = random.choice([-5, 5])
        self.vel_y: int = random.choice([-5, 5])

    def update(self) -> None:
        # Move the ball
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y

        # Bounce the ball off the top and bottom walls
        if self.pos_y < 0 or self.pos_y > SCREEN_HEIGHT - 5:
            self.vel_y = -self.vel_y


# Draw intro screen
def draw_intro_screen():
    intro_text = heading.render("PING PONG", True, WHITE)
    instruct_text = font.render("Press SPACE to start", True, WHITE)
    SCREEN.fill(BLACK)
    SCREEN.blit(intro_text, (SCREEN_WIDTH // 2 - intro_text.get_width() //
                2, 158 - intro_text.get_height() // 2))
    SCREEN.blit(instruct_text, (SCREEN_WIDTH // 2 - instruct_text.get_width() //
                2, SCREEN_HEIGHT // 2 - instruct_text.get_height() // 2))
    pygame.display.update()


# Draw pause screen
def show_pause_screen():
    paused_text = font.render("Game Paused", True, BLACK)
    paused_surface = pygame.Surface(
        (paused_text.get_width(), paused_text.get_height()), pygame.SRCALPHA)
    # Set the alpha value to 128 (50% opacity)
    paused_surface.fill((255, 255, 255, 128))
    SCREEN.blit(paused_surface, (SCREEN_WIDTH // 2 - paused_text.get_width() //
                2, SCREEN_HEIGHT // 2 - paused_text.get_height() // 2))
    SCREEN.blit(paused_text, (SCREEN_WIDTH // 2 - paused_text.get_width() //
                2, SCREEN_HEIGHT // 2 - paused_text.get_height() // 2))
    pygame.display.update()


# Draw win screen
def show_winner_screen(winner: Paddle):
    congratulations_text = heading.render(
        f"Player {winner.id} has won!", True, BLACK)
    instruct_text = font.render("Press SPACE to play again, ESC to quit", True, WHITE)
    congratulations_surface = pygame.Surface(
        (congratulations_text.get_width(), congratulations_text.get_height()), pygame.SRCALPHA)
    # Set the alpha value to 128 (50% opacity)
    congratulations_surface.fill((255, 255, 255, 128))
    SCREEN.blit(congratulations_surface, (SCREEN_WIDTH // 2 - congratulations_text.get_width() //
                2, SCREEN_HEIGHT // 2 - congratulations_text.get_height() // 2))
    SCREEN.blit(congratulations_text, (SCREEN_WIDTH // 2 - congratulations_text.get_width() //
                2, SCREEN_HEIGHT // 2 - congratulations_text.get_height() // 2))
    SCREEN.blit(instruct_text, (SCREEN_WIDTH // 2 - instruct_text.get_width() //
                2, 50 + SCREEN_HEIGHT // 2 - instruct_text.get_height() // 2)) 
    pygame.display.update()


while game_running:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_running = False

    # Draw intro screen
    draw_intro_screen()

    # Limit frame rate
    CLOCK.tick(60)

def game(game_paused=game_paused):
    # Setup paddles
    paddle_1 = Paddle(id=1, is_ai=False)
    paddle_2 = Paddle(id=2, is_ai=True)
    # Setup ball
    ball = Ball()
    winner = None
    
    # Main game loop
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = not game_paused
        if not game_paused:
            # Update the ball state
            ball.update()

            # Check for AI's
            if paddle_1.is_ai:
                paddle_1.ai_move(ball=ball)
            if paddle_2.is_ai:
                paddle_2.ai_move(ball=ball)

            # Handle collision for paddle belonging to player 1
            if ball.pos_x < paddle_1.width and paddle_1.pos < ball.pos_y < paddle_1.pos + paddle_1.height:
                ball.vel_x = -ball.vel_x
                paddle_1.hit = True
                paddle_1.hit_time = pygame.time.get_ticks()

            # Handle collision for paddle belonging to player 2
            if ball.pos_x > SCREEN_WIDTH - paddle_2.width and paddle_2.pos < ball.pos_y < paddle_2.pos + paddle_2.height:
                ball.vel_x = -ball.vel_x
                paddle_2.hit = True
                paddle_2.hit_time = pygame.time.get_ticks()

            # Check if ball goes out of bounds
            if ball.pos_x < 0:
                paddle_2.score += 1
                if paddle_2.score == GAME_POINT:
                    paddle_1.score = 0
                    winner = paddle_2
                ball.pos_x, ball.pos_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                ball.vel_x, ball.vel_y = random.choice(
                    [-5, 5]), random.choice([-5, 5])
            elif ball.pos_x > SCREEN_WIDTH:
                paddle_1.score += 1
                if paddle_1.score == GAME_POINT:
                    paddle_1.score = 0
                    winner = paddle_1
                ball.pos_x, ball.pos_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                ball.vel_x, ball.vel_y = random.choice(
                    [-5, 5]), random.choice([-5, 5])

            keys = pygame.key.get_pressed()
            # For player 1
            if not paddle_1.is_ai:
                if keys[pygame.K_w]:
                    # Adjust player speed using delta time
                    paddle_1.pos -= paddle_1.speed * CLOCK.get_time() / 1000
                if keys[pygame.K_s]:
                    # Adjust player speed using delta time
                    paddle_1.pos += paddle_1.speed * CLOCK.get_time() / 1000
            # For player 2
            if not paddle_2.is_ai:
                if keys[pygame.K_UP]:
                    # Adjust player speed using delta time
                    paddle_2.pos -= paddle_2.speed * CLOCK.get_time() / 1000
                if keys[pygame.K_DOWN]:
                    # Adjust player speed using delta time
                    paddle_2.pos += paddle_2.speed * CLOCK.get_time() / 1000

            # Clamp player positions with screen bounds
            paddle_1.pos = max(
                0, min(paddle_1.pos, SCREEN_HEIGHT - paddle_1.height))
            paddle_2.pos = max(
                0, min(paddle_2.pos, SCREEN_HEIGHT - paddle_2.height))

            # Draw the game
            SCREEN.fill(BLACK)

            # Handle wobbling on paddle for player 1
            if paddle_1.hit:
                paddle_1.hit = paddle_1.wobble()
                SCREEN.blit(paddle_1.surface_blur(
                    paddle_1.paddle_image, 10), (0, paddle_1.pos))
            else:
                SCREEN.blit(paddle_1.paddle_image, (0, paddle_1.pos))

            # Handle wobbling on paddle for player 2
            if paddle_2.hit:
                paddle_2.hit = paddle_2.wobble()
                SCREEN.blit(paddle_2.surface_blur(paddle_2.paddle_image, 10),
                            (SCREEN_WIDTH - paddle_2.width, paddle_2.pos))
            else:
                SCREEN.blit(paddle_2.paddle_image, (SCREEN_WIDTH -
                            paddle_2.width, paddle_2.pos))

            pygame.draw.circle(
                SCREEN, WHITE, (ball.pos_x, ball.pos_y), BALL_RADIUS)
            pygame.draw.line(SCREEN, WHITE, (SCREEN_WIDTH // 2, 0),
                             (SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.circle(
                SCREEN, WHITE, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 5)
            score_text = font.render(
                f"{paddle_1.score} - {paddle_2.score}", True, WHITE)
            SCREEN.blit(score_text, (10, 10))

            if winner:
                return winner
            else:
                pygame.display.update()

        else:
            show_pause_screen()

        # Update the screen
        pygame.display.update()

        # Limit the frame rate
        CLOCK.tick(60)

reset = False
winner = game()
if winner:
    while winner:
        show_winner_screen(winner=winner)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
