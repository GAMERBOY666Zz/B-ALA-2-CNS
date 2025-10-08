import pygame
import random
import math
from datetime import datetime

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1400, 900
FPS = 60

# Colors (Cyan Blue Theme)
BLACK = (10, 10, 20)
CYAN = (0, 217, 255)
DARK_CYAN = (0, 153, 204)
CYAN_GLOW = (0, 217, 255, 100)
DARK_BG = (13, 13, 13)
NAVY = (10, 10, 46)
DARK_NAVY = (26, 26, 78)
RED = (255, 0, 102)
ORANGE = (255, 170, 0)
DARK_RED = (255, 0, 51)
INFO_BLUE = (0, 170, 255)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("⬡ THREAT MATRIX ⬡")
clock = pygame.time.Clock()

# Fonts
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 24)
font_small = pygame.font.Font(None, 18)
font_tiny = pygame.font.Font(None, 14)

class Particle:
    def __init__(self, width, height):
        self.x = random.uniform(0, width)
        self.y = random.uniform(0, height)
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = random.uniform(-1.5, 1.5)
        self.size = random.uniform(2, 5)
        self.type = random.choice(['normal', 'infected', 'warning', 'critical'])
        self.pulse_phase = random.uniform(0, math.pi * 2)
        self.width = width
        self.height = height
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        
        if self.x < 0 or self.x > self.width:
            self.vx *= -1
        if self.y < 0 or self.y > self.height:
            self.vy *= -1
        
        self.pulse_phase += 0.05
    
    def draw(self, surface):
        colors = {
            'normal': CYAN,
            'infected': RED,
            'warning': ORANGE,
            'critical': DARK_RED
        }
        
        pulse = math.sin(self.pulse_phase) * 0.5 + 0.5
        size = int(self.size + pulse * 2)
        
        color = colors[self.type]
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), size)
        
        # Glow effect
        glow_surf = pygame.Surface((size*4, size*4), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*color, 50), (size*2, size*2), size*2)
        surface.blit(glow_surf, (int(self.x-size*2), int(self.y-size*2)))

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hovered = False
    
    def draw(self, surface):
        color = CYAN if self.hovered else DARK_CYAN
        pygame.draw.rect(surface, NAVY, self.rect)
        pygame.draw.rect(surface, color, self.rect, 2)
        
        text_surf = font_small.render(self.text, True, color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class ThreatMatrix:
    def __init__(self):
        self.particles = []
        self.running = True
        self.paused = False
        
        # Create particles
        for _ in range(60):
            self.particles.append(Particle(700, 540))
        
        # Metrics
        self.cpu = 73
        self.memory = 58
        self.network = 91
        self.threat_level = 45
        
        # Stats
        self.active_nodes = 152
        self.infected = 23
        self.bandwidth = 8.7
        self.uptime = 99.2
        
        # Terminal logs
        self.logs = [
            "[10:34:12] ▲ CRITICAL: Malware signature detected on Node 47",
            "[10:34:15] ◆ System initiated isolation protocol",
            "[10:34:18] ▼ WARNING: Lateral movement detected",
            "[10:34:22] ◈ INFO: Firewall rules updated",
            "[10:34:25] ◆ Network traffic analysis in progress...",
        ]
        
        # Graph data
        self.graph_data = [random.uniform(20, 100) for _ in range(50)]
        
        # Buttons
        self.init_btn = Button(30, 450, 240, 35, "▶ INITIALIZE SCAN")
        self.pause_btn = Button(30, 495, 240, 35, "⏸ PAUSE MONITORING")
        self.quarantine_btn = Button(30, 540, 240, 35, "🛡 QUARANTINE THREATS")
        self.reset_btn = Button(30, 585, 240, 35, "↻ SYSTEM RESET")
        
        self.frame_count = 0
    
    def update_metrics(self):
        self.cpu = max(60, min(100, self.cpu + random.uniform(-2, 2)))
        self.memory = max(50, min(100, self.memory + random.uniform(-1, 1)))
        self.network = max(80, min(100, self.network + random.uniform(-1, 1)))
        self.threat_level = max(30, min(70, self.threat_level + random.uniform(-3, 3)))
        
        self.bandwidth = round(8.0 + random.uniform(-0.5, 0.5), 1)
    
    def add_log(self):
        messages = [
            ("critical", "▲ CRITICAL: Unauthorized access blocked"),
            ("warning", "▼ WARNING: Unusual network pattern detected"),
            ("info", "◈ INFO: Security patch applied"),
            ("normal", "◆ Routine scan completed"),
        ]
        
        msg_type, msg = random.choice(messages)
        now = datetime.now()
        time_str = now.strftime("[%H:%M:%S]")
        self.logs.append(f"{time_str} {msg}")
        
        if len(self.logs) > 8:
            self.logs.pop(0)
    
    def draw_header(self, surface):
        # Header background
        pygame.draw.rect(surface, NAVY, (0, 0, WIDTH, 60))
        pygame.draw.line(surface, CYAN, (0, 60), (WIDTH, 60), 3)
        
        # Logo
        logo = font_large.render("⬡ THREAT MATRIX ⬡", True, CYAN)
        surface.blit(logo, (30, 10))
        
        # Status indicators
        status_x = WIDTH - 400
        pygame.draw.circle(surface, CYAN, (status_x, 30), 4)
        text = font_tiny.render("SYSTEM ACTIVE", True, CYAN)
        surface.blit(text, (status_x + 15, 23))
        
        pygame.draw.circle(surface, RED, (status_x + 150, 30), 4)
        text = font_tiny.render("THREATS: 7", True, CYAN)
        surface.blit(text, (status_x + 165, 23))
    
    def draw_left_panel(self, surface):
        panel_rect = pygame.Rect(0, 60, 300, HEIGHT - 60)
        pygame.draw.rect(surface, DARK_BG, panel_rect)
        pygame.draw.line(surface, CYAN, (300, 60), (300, HEIGHT), 2)
        
        y_pos = 80
        
        # System Resources
        pygame.draw.rect(surface, BLACK, (20, y_pos, 260, 200), border_radius=5)
        pygame.draw.rect(surface, CYAN, (20, y_pos, 260, 200), 2, border_radius=5)
        
        title = font_small.render("⚡ SYSTEM RESOURCES", True, CYAN)
        surface.blit(title, (35, y_pos + 10))
        
        # Metrics
        metrics = [
            ("CPU UTILIZATION", self.cpu),
            ("MEMORY USAGE", self.memory),
            ("NETWORK LOAD", self.network),
            ("THREAT LEVEL", self.threat_level)
        ]
        
        metric_y = y_pos + 40
        for label, value in metrics:
            text = font_tiny.render(f"{label}: {int(value)}%", True, DARK_CYAN)
            surface.blit(text, (35, metric_y))
            
            # Progress bar
            bar_rect = pygame.Rect(35, metric_y + 15, 220, 8)
            pygame.draw.rect(surface, NAVY, bar_rect)
            pygame.draw.rect(surface, CYAN, bar_rect, 1)
            
            fill_width = int(220 * value / 100)
            fill_rect = pygame.Rect(35, metric_y + 15, fill_width, 8)
            pygame.draw.rect(surface, CYAN, fill_rect)
            
            metric_y += 40
        
        # Control buttons
        self.init_btn.draw(surface)
        self.pause_btn.draw(surface)
        self.quarantine_btn.draw(surface)
        self.reset_btn.draw(surface)
        
        # Stats grid
        stats_y = 650
        stats = [
            (self.active_nodes, "ACTIVE NODES"),
            (self.infected, "INFECTED"),
            (self.bandwidth, "GB/s TRAFFIC"),
            (self.uptime, "UPTIME %")
        ]
        
        for i, (value, label) in enumerate(stats):
            x = 30 + (i % 2) * 130
            y = stats_y + (i // 2) * 70
            
            stat_rect = pygame.Rect(x, y, 110, 60)
            pygame.draw.rect(surface, BLACK, stat_rect)
            pygame.draw.rect(surface, CYAN, stat_rect, 1)
            
            val_text = font_medium.render(str(value), True, CYAN)
            val_rect = val_text.get_rect(center=(x + 55, y + 20))
            surface.blit(val_text, val_rect)
            
            lbl_text = font_tiny.render(label, True, DARK_CYAN)
            lbl_rect = lbl_text.get_rect(center=(x + 55, y + 45))
            surface.blit(lbl_text, lbl_rect)
    
    def draw_center_display(self, surface):
        display_rect = pygame.Rect(300, 60, 700, 540)
        pygame.draw.rect(surface, BLACK, display_rect)
        
        # Draw connections
        if not self.paused:
            for i, p1 in enumerate(self.particles):
                for p2 in self.particles[i+1:]:
                    dx = p1.x - p2.x
                    dy = p1.y - p2.y
                    dist = math.sqrt(dx*dx + dy*dy)
                    
                    if dist < 150:
                        alpha = int((1 - dist/150) * 100)
                        line_surf = pygame.Surface((700, 540), pygame.SRCALPHA)
                        pygame.draw.line(line_surf, (*CYAN, alpha), 
                                       (int(p1.x), int(p1.y)), 
                                       (int(p2.x), int(p2.y)), 1)
                        surface.blit(line_surf, (300, 60))
        
        # Draw particles
        particle_surf = pygame.Surface((700, 540), pygame.SRCALPHA)
        for particle in self.particles:
            if not self.paused:
                particle.update()
            particle.draw(particle_surf)
        surface.blit(particle_surf, (300, 60))
        
        # Overlay stats
        overlay_rect = pygame.Rect(320, 80, 200, 80)
        pygame.draw.rect(surface, (0, 0, 0, 200), overlay_rect)
        pygame.draw.rect(surface, CYAN, overlay_rect, 1)
        
        texts = [
            "⬢ REAL-TIME ANALYSIS",
            f"◈ PACKETS: {142000 + random.randint(0, 10000)}/s",
            f"◈ CONNECTIONS: {1200 + random.randint(0, 200)}",
        ]
        
        for i, text in enumerate(texts):
            t = font_tiny.render(text, True, CYAN)
            surface.blit(t, (330, 90 + i * 20))
    
    def draw_right_panel(self, surface):
        panel_rect = pygame.Rect(1000, 60, 400, HEIGHT - 260)
        pygame.draw.rect(surface, DARK_BG, panel_rect)
        pygame.draw.line(surface, CYAN, (1000, 60), (1000, HEIGHT), 2)
        
        y_pos = 80
        title = font_small.render("⚠ THREAT ALERTS", True, RED)
        surface.blit(title, (1020, y_pos))
        
        threats = [
            ("CRITICAL", "TROJAN.RANSOMWARE.X7", RED),
            ("CRITICAL", "WORM.PROPAGATE.Z4", RED),
            ("WARNING", "SUSPICIOUS TRAFFIC", ORANGE),
            ("INFO", "PORT SCAN DETECTED", INFO_BLUE),
        ]
        
        y_pos += 40
        for severity, threat, color in threats:
            threat_rect = pygame.Rect(1020, y_pos, 360, 70)
            pygame.draw.rect(surface, BLACK, threat_rect)
            pygame.draw.rect(surface, color, threat_rect, 1)
            
            sev_text = font_tiny.render(severity, True, BLACK)
            sev_bg = pygame.Rect(1025, y_pos + 5, 80, 18)
            pygame.draw.rect(surface, color, sev_bg)
            surface.blit(sev_text, (1030, y_pos + 7))
            
            threat_text = font_tiny.render(threat, True, color)
            surface.blit(threat_text, (1030, y_pos + 30))
            
            time_text = font_tiny.render("Detected: 2m ago", True, DARK_CYAN)
            surface.blit(time_text, (1030, y_pos + 50))
            
            y_pos += 85
    
    def draw_bottom_panel(self, surface):
        panel_rect = pygame.Rect(0, HEIGHT - 200, WIDTH, 200)
        pygame.draw.rect(surface, DARK_BG, panel_rect)
        pygame.draw.line(surface, CYAN, (0, HEIGHT - 200), (WIDTH, HEIGHT - 200), 2)
        
        # Terminal
        terminal_rect = pygame.Rect(20, HEIGHT - 180, 800, 160)
        pygame.draw.rect(surface, BLACK, terminal_rect)
        
        for i, log in enumerate(self.logs):
            color = CYAN
            if "CRITICAL" in log:
                color = RED
            elif "WARNING" in log:
                color = ORANGE
            elif "INFO" in log:
                color = INFO_BLUE
            
            text = font_tiny.render(log, True, color)
            surface.blit(text, (30, HEIGHT - 170 + i * 20))
        
        # Mini graph
        graph_rect = pygame.Rect(840, HEIGHT - 180, 540, 160)
        pygame.draw.rect(surface, BLACK, graph_rect)
        
        if not self.paused:
            self.graph_data.append(random.uniform(20, 100))
            if len(self.graph_data) > 50:
                self.graph_data.pop(0)
        
        bar_width = 540 / 50
        for i, val in enumerate(self.graph_data):
            height = int((val / 100) * 150)
            x = 840 + i * bar_width
            y = HEIGHT - 30 - height
            pygame.draw.rect(surface, CYAN, (x, y, bar_width - 2, height))
    
    def handle_button_events(self, event):
        if self.init_btn.handle_event(event):
            self.particles = [Particle(700, 540) for _ in range(60)]
        
        if self.pause_btn.handle_event(event):
            self.paused = not self.paused
            self.pause_btn.text = "▶ RESUME MONITORING" if self.paused else "⏸ PAUSE MONITORING"
        
        if self.quarantine_btn.handle_event(event):
            for p in self.particles:
                if p.type in ['infected', 'critical']:
                    p.type = 'warning'
            self.add_log()
        
        if self.reset_btn.handle_event(event):
            self.particles = [Particle(700, 540) for _ in range(60)]
            self.graph_data = [random.uniform(20, 100) for _ in range(50)]
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                self.init_btn.handle_event(event)
                self.pause_btn.handle_event(event)
                self.quarantine_btn.handle_event(event)
                self.reset_btn.handle_event(event)
                
                self.handle_button_events(event)
            
            # Update
            self.frame_count += 1
            if self.frame_count % 60 == 0:
                self.update_metrics()
            
            if self.frame_count % 180 == 0:
                self.add_log()
            
            # Draw
            screen.fill(BLACK)
            self.draw_header(screen)
            self.draw_left_panel(screen)
            self.draw_center_display(screen)
            self.draw_right_panel(screen)
            self.draw_bottom_panel(screen)
            
            pygame.display.flip()
            clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    matrix = ThreatMatrix()
    matrix.run()
