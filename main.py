import math
import sys
import pygame
import random

# Initialize Pygame
pygame.init()

# Set screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PING PONG")

# Set game variables
ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
ball_speed = [random.choice([-5, 5]), random.choice([-5, 5])]
player1_pos = SCREEN_HEIGHT // 2 - 50
player2_pos = SCREEN_HEIGHT // 2 - 50
player_speed = 600
player_width = 10
player_height = 100
player1_score, player2_score = 0, 0
player1_hit, player2_hit = False, False
hit1_time, hit2_time = 0, 0
font = pygame.font.Font(None, 36)

# Set colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up game loop
clock = pygame.time.Clock()
game_running = True

# Set the game state
game_paused = False

# Draw intro screen
def draw_intro_screen():
    intro_text = font.render("Press SPACE to start", True, WHITE)
    screen.fill(BLACK)
    screen.blit(intro_text, (SCREEN_WIDTH // 2 - intro_text.get_width() // 2, SCREEN_HEIGHT // 2 - intro_text.get_height() // 2))
    pygame.display.update()

def show_pause_screen():
    paused_text = font.render("Game Paused", True, BLACK)
    paused_surface = pygame.Surface((paused_text.get_width(), paused_text.get_height()), pygame.SRCALPHA)
    paused_surface.fill((255, 255, 255, 128))   # Set the alpha value to 128 (50% opacity)
    screen.blit(paused_surface, (SCREEN_WIDTH // 2 - paused_text.get_width() // 2, SCREEN_HEIGHT // 2 - paused_text.get_height() // 2))
    screen.blit(paused_text, (SCREEN_WIDTH // 2 - paused_text.get_width() // 2, SCREEN_HEIGHT // 2 - paused_text.get_height() // 2))
    pygame.display.update()

while game_running:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_running = False

    # Draw intro screen
    draw_intro_screen()

    # Limit frame rate
    clock.tick(60)

# Define a function to apply surface blur to a surface
def surface_blur(surface, radius):
    temp_surface = surface.copy()
    for i in range(radius):
        temp_surface.blit(surface, (0, 0))
        pygame.draw.rect(temp_surface, (255, 255, 255), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 1)
    return temp_surface

# Load paddle images and apply surface blur effect
paddle1_image = pygame.image.load('assets/paddle.png').convert_alpha()
paddle1_image = pygame.transform.scale(paddle1_image, (player_width, player_height))
paddle2_image = pygame.image.load('assets/paddle.png').convert_alpha()
paddle2_image = pygame.transform.scale(paddle2_image, (player_width, player_height))

# Main game loop
running = True
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
        # Move the ball
        ball_pos[0] += ball_speed[0]
        ball_pos[1] += ball_speed[1]

        # Bounce the ball off the top and bottom walls
        if ball_pos[1] < 0 or ball_pos[1] > SCREEN_HEIGHT:
            ball_speed[1] = -ball_speed[1]

        # Check if ball collides with player1
        if ball_pos[0] < player_width and player1_pos < ball_pos[1] < player1_pos + player_height:
            ball_speed[0] = -ball_speed[0]
            player1_hit = True
            hit1_time = pygame.time.get_ticks()

        # Check if ball collides with player2
        if ball_pos[0] > SCREEN_WIDTH - player_width and player2_pos < ball_pos[1] < player2_pos + player_height:
            ball_speed[0] = -ball_speed[0]
            player2_hit = True
            hit2_time = pygame.time.get_ticks()

        # Check if ball goes out of bounds
        if ball_pos[0] < 0:
            player2_score += 1
            ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
            ball_speed = [random.choice([-5, 5]), random.choice([-5, 5])]
        elif ball_pos[0] > SCREEN_WIDTH:
            player1_score += 1
            ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
            ball_speed = [random.choice([-5, 5]), random.choice([-5, 5])]

        # Handle player input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player1_pos -= player_speed * clock.get_time() / 1000   # Adjust player speed using delta time
        if keys[pygame.K_s]:
            player1_pos += player_speed * clock.get_time() / 1000   # Adjust player speed using delta time
        if keys[pygame.K_UP]:
            player2_pos -= player_speed * clock.get_time() / 1000   # Adjust player speed using delta time
        if keys[pygame.K_DOWN]:
            player2_pos += player_speed * clock.get_time() / 1000   # Adjust player speed using delta time

        # Clamp player positions within screen bounds
        player1_pos = max(0, min(player1_pos, SCREEN_HEIGHT - player_height))
        player2_pos = max(0, min(player2_pos, SCREEN_HEIGHT - player_height))

        # Draw the game
        screen.fill(BLACK)

        # Draw player1 paddle
        if player1_hit:
            time_diff1 = pygame.time.get_ticks() - hit1_time
            player1_pos += math.sin(time_diff1 * 0.05) * 10  # Wobble the paddle
            if time_diff1 > 200: # Stop the wobbling after 200ms
                player1_hit = False
            screen.blit(surface_blur(paddle1_image, 10), (0, player1_pos))
        else:
            screen.blit(paddle1_image, (0, player1_pos))

        # Draw player2 paddle
        if player2_hit:
            time_diff2 = pygame.time.get_ticks() - hit2_time
            player2_pos += math.sin(time_diff2 * 0.05) * 10  # Wobble the paddle
            if time_diff2 > 200: # Stop the wobbling after 200ms
                player2_hit = False
            screen.blit(surface_blur(paddle2_image, 10), (SCREEN_WIDTH - player_width, player2_pos))
        else:
            screen.blit(paddle2_image, (SCREEN_WIDTH - player_width, player2_pos))

        pygame.draw.circle(screen, WHITE, ball_pos, 10)
        pygame.draw.line(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))
        pygame.draw.circle(screen, WHITE, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 5)
        score_text = font.render(f"{player1_score} - {player2_score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        pygame.display.update()
    else:
        show_pause_screen()
    
    # Update the screen
    pygame.display.update()

    # Limit frame rate
    clock.tick(60)