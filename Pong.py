import pygame
import random
import time

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_COLOR = (255, 100, 100)
PADDLE_COLOR = (100, 255, 100)
BG_COLOR = (30, 30, 30)
BUTTON_COLOR = (50, 50, 250)
BUTTON_HOVER_COLOR = (100, 100, 255)

# Ball settings
BALL_RADIUS = 15
BALL_SPEED_X = 7 * random.choice((1, -1))
BALL_SPEED_Y = 7 * random.choice((1, -1))

# Paddle settings
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_SPEED = 10

# Initialize ball position
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2

# Initialize paddle positions
paddle1_x = 50
paddle1_y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2

paddle2_x = SCREEN_WIDTH - 50 - PADDLE_WIDTH
paddle2_y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2

# Initialize scores
score1 = 0
score2 = 0

# Winning score
WINNING_SCORE = 10

# Fonts
title_font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)
score_font = pygame.font.Font(None, 74)
countdown_font = pygame.font.Font(None, 150)

# Button dimensions
button_width = 200
button_height = 80

# Game loop
running = True
clock = pygame.time.Clock()
game_started = False

def draw_ball():
    pygame.draw.circle(SCREEN, BALL_COLOR, (ball_x, ball_y), BALL_RADIUS)

def draw_paddles():
    pygame.draw.rect(SCREEN, PADDLE_COLOR, (paddle1_x, paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(SCREEN, PADDLE_COLOR, (paddle2_x, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT))

def draw_scores():
    score_text1 = score_font.render(str(score1), True, WHITE)
    score_text2 = score_font.render(str(score2), True, WHITE)
    SCREEN.blit(score_text1, (SCREEN_WIDTH // 4, 20))
    SCREEN.blit(score_text2, (SCREEN_WIDTH * 3 // 4, 20))

def starting_screen():
    start_button_rect = pygame.Rect(
        (SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - button_height // 2), 
        (button_width, button_height)
    )
    
    while not game_started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return True
        
        mouse_pos = pygame.mouse.get_pos()
        button_color = BUTTON_HOVER_COLOR if start_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        
        SCREEN.fill(BG_COLOR)
        title_text = title_font.render("Pong", True, WHITE)
        SCREEN.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))
        
        pygame.draw.rect(SCREEN, button_color, start_button_rect)
        button_text = button_font.render("Start!", True, WHITE)
        SCREEN.blit(button_text, (start_button_rect.x + (button_width - button_text.get_width()) // 2,
                                 start_button_rect.y + (button_height - button_text.get_height()) // 2))
        
        pygame.display.flip()
        clock.tick(60)

def countdown():
    for i in range(3, 0, -1):
        SCREEN.fill(BG_COLOR)
        countdown_text = countdown_font.render(str(i), True, WHITE)
        SCREEN.blit(countdown_text, (SCREEN_WIDTH // 2 - countdown_text.get_width() // 2, SCREEN_HEIGHT // 2 - countdown_text.get_height() // 2))
        pygame.display.flip()
        time.sleep(1)

def end_game_screen(winner):
    play_again_button_rect = pygame.Rect(
        (SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 100), 
        (button_width, button_height)
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button_rect.collidepoint(event.pos):
                    return True
        
        mouse_pos = pygame.mouse.get_pos()
        button_color = BUTTON_HOVER_COLOR if play_again_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR

        SCREEN.fill(BG_COLOR)
        winner_text = title_font.render(f"Player {winner} Wins!", True, WHITE)
        SCREEN.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        
        pygame.draw.rect(SCREEN, button_color, play_again_button_rect)
        button_text = button_font.render("Play Again", True, WHITE)
        SCREEN.blit(button_text, (play_again_button_rect.x + (button_width - button_text.get_width()) // 2,
                                  play_again_button_rect.y + (button_height - button_text.get_height()) // 2))
        
        pygame.display.flip()
        clock.tick(60)

while running:
    if not game_started:
        game_started = starting_screen()
        if game_started:
            countdown()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get keys
        keys = pygame.key.get_pressed()
        
        # Move paddles
        if keys[pygame.K_w] and paddle1_y > 0:
            paddle1_y -= PADDLE_SPEED
        if keys[pygame.K_s] and paddle1_y < SCREEN_HEIGHT - PADDLE_HEIGHT:
            paddle1_y += PADDLE_SPEED
        if keys[pygame.K_UP] and paddle2_y > 0:
            paddle2_y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and paddle2_y < SCREEN_HEIGHT - PADDLE_HEIGHT:
            paddle2_y += PADDLE_SPEED

        # Move ball
        ball_x += BALL_SPEED_X
        ball_y += BALL_SPEED_Y

        # Ball collision with top/bottom walls
        if ball_y - BALL_RADIUS <= 0 or ball_y + BALL_RADIUS >= SCREEN_HEIGHT:
            BALL_SPEED_Y *= -1

        # Ball collision with paddles
        if (ball_x - BALL_RADIUS <= paddle1_x + PADDLE_WIDTH and
            paddle1_y < ball_y < paddle1_y + PADDLE_HEIGHT):
            BALL_SPEED_X *= -1

        if (ball_x + BALL_RADIUS >= paddle2_x and
            paddle2_y < ball_y < paddle2_y + PADDLE_HEIGHT):
            BALL_SPEED_X *= -1

        # Ball out of bounds
        if ball_x - BALL_RADIUS <= 0:
            score2 += 1
            ball_x = SCREEN_WIDTH // 2
            ball_y = SCREEN_HEIGHT // 2
            BALL_SPEED_X *= random.choice((1, -1))
            BALL_SPEED_Y *= random.choice((1, -1))

        if ball_x + BALL_RADIUS >= SCREEN_WIDTH:
            score1 += 1
            ball_x = SCREEN_WIDTH // 2
            ball_y = SCREEN_HEIGHT // 2
            BALL_SPEED_X *= random.choice((1, -1))
            BALL_SPEED_Y *= random.choice((1, -1))

        # Drawing
        SCREEN.fill(BG_COLOR)
        draw_ball()
        draw_paddles()
        draw_scores()
        
        pygame.display.flip()
        clock.tick(60)

        # Check for winning condition
        if score1 >= WINNING_SCORE or score2 >= WINNING_SCORE:
            winner = 1 if score1 >= WINNING_SCORE else 2
            game_started = False
            score1, score2 = 0, 0
            game_started = end_game_screen(winner)
            if game_started:
                countdown()
        
pygame.quit()
