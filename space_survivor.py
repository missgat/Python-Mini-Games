import pygame
import random
import sys

# 1. Initialize Pygame Engine
pygame.init()

# Game Window Configurations
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("🌌 Terminal Space Survivor")
clock = pygame.time.Clock()

# Color Palette (RGB)
BLACK = (10, 10, 15)
WHITE = (255, 255, 255)
GREEN = (57, 255, 20)      # Neon Player
RED = (255, 49, 49)        # Alien
YELLOW = (255, 255, 102)   # Laser

# 2. Game Entities & State Tracking
player_width, player_height = 50, 40
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - 60
player_speed = 7

lasers = []
laser_speed = 10

enemies = []
enemy_width, enemy_height = 40, 30
enemy_speed = 3
spawn_timer = 0

score = 0
font = pygame.font.SysFont("Arial", 26)

# 3. Main Graphical Game Loop
running = True
while running:
    # Set game pace to 60 Frames Per Second (FPS)
    clock.tick(60)
    screen.fill(BLACK)
    
    # --- A. EVENT HANDLING (Listening for single keystrokes/X button) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Spawn a laser beam from the top center of the player ship
                lasers.append(pygame.Rect(player_x + player_width//2 - 2, player_y, 4, 15))

    # Continuous key presses for smooth directional movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
        player_x += player_speed

    # --- B. UPDATE POSITION STATES ---
    # Spawn Enemies randomly over time
    spawn_timer += 1
    if spawn_timer > 30: # Spawns roughly every half-second
        enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
        enemies.append(pygame.Rect(enemy_x, -enemy_height, enemy_width, enemy_height))
        spawn_timer = 0

    # Move Lasers upward; remove them if they leave the top screen boundary
    for laser in lasers[:]:
        laser.y -= laser_speed
        if laser.y < 0:
            lasers.remove(laser)

    # Move Enemies downward
    for enemy in enemies[:]:
        enemy.y += enemy_speed
        
        # Check if enemy hits the player (Collision Detection)
        if enemy.colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):
            print(f"💥 Game Over! Final Score: {score}")
            running = False
            
        # Remove enemy if it passes the bottom screen boundary
        if enemy.y > SCREEN_HEIGHT:
            enemies.remove(enemy)

    # --- C. COLLISION HANDLING (Lasers hitting Enemies) ---
    for laser in lasers[:]:
        for enemy in enemies[:]:
            if laser.colliderect(enemy):
                enemies.remove(enemy)
                if laser in lasers:
                    lasers.remove(laser)
                score += 10
                break

    # --- D. RENDERING (Draw the updated frame onto the window) ---
    # Draw Player
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height), border_radius=5)
    
    # Draw Lasers
    for laser in lasers:
        pygame.draw.rect(screen, YELLOW, laser)
        
    # Draw Enemies
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy, border_radius=3)

    # Render Score Interface text
    score_surface = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surface, (15, 15))

    # Flip the display buffer to render the new drawings instantly
    pygame.display.flip()

pygame.quit()
sys.exit()
