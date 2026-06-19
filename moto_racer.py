import pygame
import random
import sys

# Initialize Engine
pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("🏍️ Terminal Moto-Racer Arcade")
clock = pygame.time.Clock()

# Colors (RGB)
ASPHALT = (45, 50, 55)
GRASS = (34, 139, 34)
STRIPE_WHITE = (255, 255, 255)
BIKE_COLOR = (230, 126, 34)   # Safety Orange Rider
OBSTACLE_RED = (231, 76, 60)

# Track Boundaries
TRACK_LEFT = 120
TRACK_RIGHT = 480
TRACK_WIDTH = TRACK_RIGHT - TRACK_LEFT

# --- GAME STATE DATA ---
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 120
player_width, player_height = 24, 55

speed = 0.0
MAX_SPEED = 15.0
ACCELERATION = 0.2
DECELERATION = 0.1
HANDLING = 5.0

# Scrolling Track Background Indicators
stripe_y = 0
score = 0
game_over = False

# Traffic / Obstacles
obstacles = []
spawn_timer = 0

font = pygame.font.SysFont("Arial", 24, bold=True)

# --- MAIN ENGINE LOOP ---
while True:
    clock.tick(60) # Locked at 60 FPS
    
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        keys = pygame.key.get_pressed()
        
        # --- 2. MOTORCYCLE PHYSICS ENGINE ---
        # Forward Throttle / Braking
        if keys[pygame.K_UP]:
            speed = min(MAX_SPEED, speed + ACCELERATION)
        elif keys[pygame.K_DOWN]:
            speed = max(0.0, speed - (ACCELERATION * 2))
        else:
            speed = max(0.0, speed - DECELERATION) # Passive drag friction
            
        # Lateral Steering Handling (Scale steering capability based on speed)
        if speed > 1.0:
            if keys[pygame.K_LEFT]:
                player_x -= HANDLING * (speed / MAX_SPEED + 0.3)
            if keys[pygame.K_RIGHT]:
                player_x += HANDLING * (speed / MAX_SPEED + 0.3)

        # Environment Limits (Crashing into the grass sides slows you down heavily)
        if player_x < TRACK_LEFT or player_x > TRACK_RIGHT - player_width:
            if speed > 3.0:
                speed -= 0.5 # Grass friction penalty

        # --- 3. TRACK ENVIRONMENT GENERATION & SCROLLING ---
        # Move road center stripes downwards relative to current speed
        stripe_y += speed
        if stripe_y >= 80:
            stripe_y = 0
            if speed > 0:
                score += 1 # Distance score accumulates while moving

        # Spawn rival obstacles / track debris
        spawn_timer += speed
        if spawn_timer > 300:
            obs_x = random.randint(TRACK_LEFT + 10, TRACK_RIGHT - 40)
            obstacles.append(pygame.Rect(obs_x, -50, 30, 30))
            spawn_timer = 0

        # Move obstacles down based on player's forward speed
        for obs in obstacles[:]:
            obs.y += speed * 0.4 + 2 # Obstacles have their own slight downward pace
            if obs.y > SCREEN_HEIGHT:
                obstacles.remove(obs)
                
            # COLLISION DETECTION (Crash logic)
            player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
            if player_rect.colliderect(obs):
                game_over = True

    else:
        # If Game Over, look for R key reset
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_over = False
            player_x = SCREEN_WIDTH // 2
            speed = 0.0
            obstacles.clear()
            score = 0

    # --- 4. GRAPHICAL RENDERING ENGINE ---
    # Draw Environment Grass Background
    screen.fill(GRASS)
    
    # Draw Road Asphalt Track
    pygame.draw.rect(screen, ASPHALAL_COLOR := ASPHALT, (TRACK_LEFT, 0, TRACK_WIDTH, SCREEN_HEIGHT))
    
    # Draw Scrolling Center Dividers
    for y in range(-80 + int(stripe_y), SCREEN_HEIGHT, 80):
        pygame.draw.rect(screen, STRIPE_WHITE, (SCREEN_WIDTH // 2 - 4, y, 8, 40))

    # Draw Obstacles / Hazards
    for obs in obstacles:
        pygame.draw.rect(screen, OBSTACLE_RED, obs, border_radius=4)
        pygame.draw.rect(screen, (150, 0, 0), (obs.x + 5, obs.y + 5, 20, 20)) # Internal shadow detail

    # Draw Player Motorcycle (Stylized chassis shape)
    pygame.draw.rect(screen, BIKE_COLOR, (player_x, player_y, player_width, player_height), border_radius=6)
    # Draw Rider's Black Helmet
    pygame.draw.circle(screen, (20, 20, 20), (int(player_x + player_width // 2), int(player_y + 15)), 10)
    # Draw Wheels (Front and back tires)
    pygame.draw.rect(screen, (0, 0, 0), (player_x + player_width//2 - 4, player_y - 5, 8, 12), border_radius=2)
    pygame.draw.rect(screen, (0, 0, 0), (player_x + player_width//2 - 4, player_y + player_height - 7, 8, 12), border_radius=2)

    # UI Telemetry Overlay
    speed_kmh = int(speed * 15)
    hud_speed = font.render(f"SPEED: {speed_kmh} MPH", True, STRIPE_WHITE)
    hud_score = font.render(f"DISTANCE: {score} m", True, STRIPE_WHITE)
    screen.blit(hud_speed, (20, 20))
    screen.blit(hud_score, (20, 50))

    if game_over:
        # Dim screen layout overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        go_text = font.render("💥 WRECKED! GAME OVER 💥", True, OBSTACLE_RED)
        reset_text = font.render("Press [ R ] to Restart Track", True, STRIPE_WHITE)
        screen.blit(go_text, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 20))
        screen.blit(reset_text, (SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 15))

    pygame.display.flip()
