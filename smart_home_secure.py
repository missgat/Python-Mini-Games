import pygame
import array
import math
import sys
from datetime import datetime

# 1. Initialize Pygame & Audio Mixer
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 550
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Automated Smart Home Security Monitoring Station")
clock = pygame.time.Clock()

# Professional SCADA/SOC Color Palette
BG_COLOR = (18, 22, 28)
PANEL_COLOR = (28, 35, 46)
TEXT_WHITE = (240, 245, 250)
COLOR_SAFE = (46, 204, 113)     # Green
COLOR_BREACH = (231, 76, 60)    # Red
COLOR_ARMED = (241, 196, 15)    # Yellow
COLOR_DISARMED = (140, 150, 160)# Gray

# 2. Synthesize an Alarm Siren Tone Natively
def generate_siren_sound(freq1=600, freq2=900, duration=0.8):
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    raw_data = array.array('h')
    
    for i in range(num_samples):
        t = i / sample_rate
        # Alternating siren frequency sweep using modulation math
        current_freq = freq1 + (freq2 - freq1) * (0.5 + 0.5 * math.sin(2 * math.pi * 2 * t))
        val = int(10000 * math.sin(2 * math.pi * current_freq * t))
        raw_data.append(val) # Left Channel
        raw_data.append(val) # Right Channel
        
    return pygame.mixer.Sound(buffer=raw_data)

SIREN = generate_siren_sound()

# 3. Security State Tracking
system_armed = True
alarm_triggered = False
log_file = "home_security_audit.log"

# Define our Home Zones and bounding boxes for the visual map
zones = {
    "Front Door": {"rect": pygame.Rect(250, 420, 200, 60), "status": "SAFE", "key": "1"},
    "Living Room": {"rect": pygame.Rect(250, 240, 200, 160), "status": "SAFE", "key": "2"},
    "Garage":      {"rect": pygame.Rect(40, 240, 190, 240), "status": "SAFE", "key": "3"},
    "Backyard":    {"rect": pygame.Rect(40, 60, 620, 160), "status": "SAFE", "key": "4"}
}

def log_incident(message):
    """Appends security telemetry to an external audit log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

# Write initial boot sequence to log file
log_incident("SYSTEM BOOT: Main security dashboard initialization complete.")

font_sm = pygame.font.SysFont("Arial", 16)
font_md = pygame.font.SysFont("Arial", 20, bold=True)
font_lg = pygame.font.SysFont("Arial", 28, bold=True)

# --- MAIN MONITORING LOOP ---
running = True
while running:
    clock.tick(60)
    screen.fill(BG_COLOR)
    
    # --- A. TELEMETRY & INPUT INTERACTION ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            # Toggle Arm / Disarm
            if event.key == pygame.K_SPACE:
                system_armed = not system_armed
                alarm_triggered = False
                pygame.mixer.stop()
                status_str = "ARMED" if system_armed else "DISARMED"
                log_incident(f"USER INTERACTION: System state toggled to {status_str}.")
                # Reset all zones on arm/disarm toggle
                for zone in zones.values():
                    zone["status"] = "SAFE"
                    
            # Clear Alarms / Reset System
            if event.key == pygame.K_r:
                alarm_triggered = False
                pygame.mixer.stop()
                log_incident("USER INTERACTION: Alarm reset signal sent. Clearing alerts.")
                for zone in zones.values():
                    zone["status"] = "SAFE"

            # Check if user tripped a sensor manually (Keys 1-4)
            for name, data in zones.items():
                if event.unicode == data["key"]:
                    if data["status"] == "SAFE":
                        data["status"] = "BREACHED"
                        log_incident(f"SENSOR ALERT: Breach detected in zone [{name}].")
                        if system_armed:
                            alarm_triggered = True
                            SIREN.play(loops=-1) # Loop siren indefinitely
                    else:
                        data["status"] = "SAFE"
                        log_incident(f"SENSOR TELEMETRY: Zone [{name}] returned to nominal status.")

    # --- B. GRAPHICAL UI RENDERING ---
    # Top Control Panel Bar
    pygame.draw.rect(screen, PANEL_COLOR, (0, 0, SCREEN_WIDTH, 45))
    header_title = font_md.render("SMART HOME MATRIX MONITOR", True, TEXT_WHITE)
    screen.blit(header_title, (20, 12))
    
    # Render System Status Badge
    status_label = "ARMED (ACTIVE)" if system_armed else "DISARMED (BYPASS)"
    status_color = COLOR_ARMED if system_armed else COLOR_DISARMED
    status_surf = font_md.render(status_label, True, status_color)
    screen.blit(status_surf, (SCREEN_WIDTH - 220, 12))

    # --- DRAW HOUSE BLUEPRINT MAP ---
    for name, data in zones.items():
        # Pick background frame color based on security severity
        box_color = COLOR_BREACH if data["status"] == "BREACHED" else PANEL_COLOR
        border_color = COLOR_BREACH if data["status"] == "BREACHED" else COLOR_SAFE
        
        # Draw room block shape
        pygame.draw.rect(screen, box_color, data["rect"], border_radius=4)
        pygame.draw.rect(screen, border_color, data["rect"], 2, border_radius=4)
        
        # Render Room Data Labels
        name_surf = font_md.render(name, True, TEXT_WHITE)
        status_surf = font_sm.render(f"Status: {data['status']}", True, border_color)
        key_surf = font_sm.render(f"[Key {data['key']} to trip]", True, (110, 120, 135))
        
        screen.blit(name_surf, (data["rect"].x + 15, data["rect"].y + 12))
        screen.blit(status_surf, (data["rect"].x + 15, data["rect"].y + 35))
        if data["status"] == "SAFE":
            screen.blit(key_surf, (data["rect"].x + data["rect"].width - 110, data["rect"].y + 12))

    # --- C. ALARM WARNING OVERLAY FLASH ---
    if alarm_triggered and (pygame.time.get_ticks() // 250) % 2 == 0:
        # Flashes a massive banner if sensors are tripped while system is armed
        pygame.draw.rect(screen, COLOR_BREACH, (0, SCREEN_HEIGHT - 65, SCREEN_WIDTH, 65))
        alert_text = font_lg.render("ALARM TRIGGERED: INTRUSION ATTEMPT DETECTED", True, TEXT_WHITE)
        screen.blit(alert_text, (40, SCREEN_HEIGHT - 50))
    else:
        # Standard Info Control Footer Legend Bar
        pygame.draw.rect(screen, PANEL_COLOR, (0, SCREEN_HEIGHT - 65, SCREEN_WIDTH, 65))
        legend_txt = font_sm.render("System Controls: [SPACEBAR] Toggle Arm/Disarm System Mode  |  [R] Reset Alarms", True, TEXT_WHITE)
        screen.blit(legend_txt, (20, SCREEN_HEIGHT - 40))

    pygame.display.flip()

pygame.mixer.quit()
pygame.quit()
sys.exit()
