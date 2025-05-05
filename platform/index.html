import pygame
import random
import math

# Initialize Pygame
pygame.init()
display_info = pygame.display.Info()
WIDTH, HEIGHT = display_info.current_w, display_info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("GALACTICA: STELLAR CONQUEST")
clock = pygame.time.Clock()
FPS = 60

# Game states
TITLE, PLAYING, PAUSED, GAME_OVER, LEVEL_COMPLETE, BOSS_INTRO, VICTORY = range(7)
game_state = TITLE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 40, 40)
GREEN = (40, 255, 40)
BLUE = (0, 200, 255)
YELLOW = (255, 255, 40)
ORANGE = (255, 140, 0)
PURPLE = (180, 0, 255)
PINK = (255, 100, 255)
GOLD = (255, 215, 0)

# Load images
def load_image(path, size=None, angle=0, flip=False):
    try:
        img = pygame.image.load(path).convert_alpha()
        if size: img = pygame.transform.scale(img, size)
        if angle: img = pygame.transform.rotate(img, angle)
        if flip: img = pygame.transform.flip(img, True, False)
        return img
    except: # Fallback image if file not found
        surf = pygame.Surface(size or (50, 50), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 255), surf.get_rect(), 2)
        return surf

PLAYER_IMG = load_image('platform/assets/player.png', (100, 100))
ENEMY1_IMG = load_image('platform/assets/level 1 boss.png', (80, 80), angle=180)
ENEMY2_IMG = load_image('platform/assets/level 2 boss.png', (100, 100), angle=180)
BOSS_IMG = load_image('platform/assets/final boss.png', (150, 150), angle=180)

# Fonts
font_sm = pygame.font.SysFont(None, 24)
font_md = pygame.font.SysFont(None, 36)
font_lg = pygame.font.SysFont(None, 48, bold=True)
font_xl = pygame.font.SysFont(None, 72, bold=True)

# Particle system
class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color, size=3, speed=2, direction=None, duration=20):
        super().__init__()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (size//2, size//2), size//2)
        self.rect = self.image.get_rect(center=(x, y))
        self.lifetime = duration
        if direction is None:
            angle = random.uniform(0, math.pi * 2)
            self.velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
        else:
            self.velocity = pygame.Vector2(direction) * speed
            
    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
        elif self.lifetime < 10:  # Fade out
            self.image.set_alpha(int(255 * self.lifetime / 10))

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, frames=15, color=(255, 255, 0)):
        super().__init__()
        self.frames = []
        for i in range(frames):
            surf = pygame.Surface((80, 80), pygame.SRCALPHA)
            radius = 40 - i*2
            pygame.draw.circle(surf, (*color, 255 - i*15), (40, 40), radius)
            pygame.draw.circle(surf, (255, 100, 0, max(0, 180-i*15)), (40, 40), radius - 10)
            self.frames.append(surf)
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=center)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 30  # ms per frame
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.index += 1
            if self.index >= len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.index]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Star(pygame.sprite.Sprite):
    def __init__(self, layer=0):
        super().__init__()
        size = 1 if layer == 0 else (2 if layer == 1 else 3)
        brightness = 100 if layer == 0 else (180 if layer == 1 else 255)
        color = random.choice([BLUE, WHITE, YELLOW]) if layer==2 and random.random()<0.3 else (brightness,)*3
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(random.randrange(WIDTH), random.randrange(-HEIGHT, HEIGHT)))
        self.speed = 0.5 + layer * 1.5
        
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = random.randrange(-50, -10)
            self.rect.x = random.randrange(WIDTH)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_IMG.copy()
        self.rect = self.image.get_rect(midbottom=(WIDTH//2, HEIGHT - 40))
        self.position = pygame.Vector2(self.rect.centerx, self.rect.centery)
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 8
        self.lives = 3
        self.score = 0
        self.max_lives = 5
        
        # Weapons
        self.weapon_type = "standard"  # "standard", "spread", "laser", "homing"
        self.weapon_level = 1
        self.fire_rate = 250
        self.last_shot = 0
        
        # Special abilities
        self.bombs = 1
        self.max_bombs = 3
        self.shield = 0
        self.max_shield = 100
        
        # Status effects
        self.invincible = False
        self.invincible_timer = 0
        self.rapid_fire_timer = 0
        self.shield_timer = 0
        self.spread_timer = 0
        self.double_damage_timer = 0
        
    def update(self):
        # Movement with smooth acceleration
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:    dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:  dy = 1
        
        # Apply acceleration
        target_vx = dx * self.speed
        target_vy = dy * self.speed
        
        # Smooth movement
        self.velocity.x = self.velocity.x * 0.8 + target_vx * 0.2
        self.velocity.y = self.velocity.y * 0.8 + target_vy * 0.2
        
        # Apply velocity
        self.position += self.velocity
        
        # Boundary checking
        self.position.x = max(self.rect.width // 2, min(WIDTH - self.rect.width // 2, self.position.x))
        self.position.y = max(self.rect.height // 2, min(HEIGHT - self.rect.height // 2, self.position.y))
        self.rect.center = (round(self.position.x), round(self.position.y))
        
        # Shooting
        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE]:
            fire_rate = 100 if self.rapid_fire_timer > 0 else self.fire_rate
            if now - self.last_shot > fire_rate:
                self.shoot()
                self.last_shot = now
                
        # Bomb
        if keys[pygame.K_b] and self.bombs > 0:
            self.use_bomb()
            
        # Update timers and effects
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
                self.image.set_alpha(255)
            elif (self.invincible_timer // 5) % 2 == 0:  # Blink effect
                self.image.set_alpha(100)
            else:
                self.image.set_alpha(255)
                
        if self.rapid_fire_timer > 0: self.rapid_fire_timer -= 1
        if self.shield_timer > 0:
            self.shield_timer -= 1
            if self.shield_timer <= 0: self.shield = 0
        if self.spread_timer > 0: self.spread_timer -= 1
        if self.double_damage_timer > 0: self.double_damage_timer -= 1
            
        # Engine particles
        if abs(self.velocity.x) > 0.5 or abs(self.velocity.y) > 0.5:
            if random.random() < 0.3:
                offset = random.randint(-10, 10)
                p = Particle(self.rect.midbottom[0] + offset, self.rect.midbottom[1],
                           random.choice([ORANGE, YELLOW]),
                           size=random.randint(2, 5), duration=random.randint(10, 20))
                particles.add(p)
    
    def shoot(self):
        damage_mult = 2 if self.double_damage_timer > 0 else 1
        
        if self.weapon_type == "spread" or self.spread_timer > 0:
            # Spread shot
            spread_count = min(3 + self.weapon_level // 2, 5)
            angle_step = 10
            for i in range(spread_count):
                angle = (i - (spread_count-1)/2) * angle_step
                bullet = Bullet(self.rect.midtop, damage=damage_mult, angle=angle, color=YELLOW)
                player_bullets.add(bullet)
                all_sprites.add(bullet)
                
        elif self.weapon_type == "laser":
            # Piercing laser beam
            beam = LaserBeam(self.rect.midtop, damage=3*damage_mult, width=max(3, 1+self.weapon_level), color=RED)
            player_bullets.add(beam)
            all_sprites.add(beam)
            
        else:  # Standard weapon
            # Based on weapon level
            bullets_per_shot = min(1 + (self.weapon_level // 2), 3)
            offsets = [-15, 0, 15][:bullets_per_shot]
            
            for offset in offsets:
                pos = (self.rect.midtop[0] + offset, self.rect.midtop[1])
                bullet = Bullet(pos, damage=damage_mult, color=BLUE)
                player_bullets.add(bullet)
                all_sprites.add(bullet)
                
        # Muzzle flash
        p = Particle(self.rect.midtop[0], self.rect.midtop[1] - 5, WHITE,
                    size=random.randint(2, 4), duration=random.randint(5, 15))
        particles.add(p)
            
    def use_bomb(self):
        if self.bombs <= 0: return
        self.bombs -= 1
        
        # Visual effect
        for r in range(10, 300, 30):
            explosion = BombWave(self.rect.center, r)
            effects.add(explosion)
            
        # Clear enemy bullets
        for bullet in enemy_bullets:
            p = Particle(bullet.rect.centerx, bullet.rect.centery, YELLOW,
                       size=random.randint(2, 4), duration=random.randint(5, 15))
            particles.add(p)
            bullet.kill()
            
        # Damage all enemies
        for enemy in enemies:
            dist = pygame.math.Vector2(self.rect.center).distance_to(pygame.math.Vector2(enemy.rect.center))
            if dist < 500:
                damage = max(3, 10 * (1 - dist/500))
                enemy.take_damage(damage)
                explosion = Explosion(enemy.rect.center, frames=10, color=ORANGE)
                effects.add(explosion)
                
    def take_damage(self, amount=1):
        if self.invincible: return False
            
        # Shield absorbs damage first
        if self.shield > 0:
            if self.shield >= amount:
                self.shield -= amount
                # Shield hit effect
                p = Particle(self.rect.centerx, self.rect.centery, BLUE,
                           size=random.randint(2, 4), duration=random.randint(5, 15))
                particles.add(p)
                return False
            else:
                # Shield broken
                remaining = amount - self.shield
                self.shield = 0
                amount = remaining
        
        # Apply damage
        explosion = Explosion(self.rect.center, frames=10, color=RED)
        effects.add(explosion)
        
        self.lives -= 1
        if self.lives > 0:
            self.invincible = True
            self.invincible_timer = 180  # 3 seconds at 60 FPS
            return False
        else:
            return True  # Game over
            
    def add_powerup(self, powerup_type):
        if powerup_type == "health":
            self.lives = min(self.lives + 1, self.max_lives)
        elif powerup_type == "shield":
            self.shield = self.max_shield
            self.shield_timer = 600  # 10 seconds
        elif powerup_type == "rapid":
            self.rapid_fire_timer = 300  # 5 seconds
        elif powerup_type == "spread":
            self.spread_timer = 300  # 5 seconds
        elif powerup_type == "bomb":
            self.bombs = min(self.bombs + 1, self.max_bombs)
        elif powerup_type == "weapon":
            self.weapon_level = min(self.weapon_level + 1, 5)
        elif powerup_type == "double":
            self.double_damage_timer = 300  # 5 seconds
            
    def draw_shield_effect(self, surface):
        if self.shield > 0:
            shield_percent = self.shield / self.max_shield
            pygame.draw.circle(surface, BLUE, self.rect.center, 
                            self.rect.width//2 + 10, 
                            width=3 if shield_percent > 0.6 else 2)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, damage=1, speed=10, angle=0, color=BLUE):
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect(midbottom=pos)
        self.damage = damage
        self.piercing = False
        self.velocity = pygame.Vector2(0, -speed).rotate(angle)
        
    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if (self.rect.bottom < 0 or self.rect.top > HEIGHT or
            self.rect.right < 0 or self.rect.left > WIDTH):
            self.kill()

class LaserBeam(pygame.sprite.Sprite):
    def __init__(self, pos, damage=3, width=4, color=RED):
        super().__init__()
        self.image = pygame.Surface((width, HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect(midtop=pos)
        self.damage = damage
        self.piercing = True
        self.duration = 5
        
    def update(self):
        self.duration -= 1
        if self.duration <= 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle=0, speed=3, color=YELLOW):
        super().__init__()
        self.image = pygame.Surface((6, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect(midtop=pos)
        self.velocity = pygame.Vector2(0, speed).rotate(angle)
        
    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if (self.rect.bottom < 0 or self.rect.top > HEIGHT or
            self.rect.right < 0 or self.rect.left > WIDTH):
            self.kill()

class BombWave(pygame.sprite.Sprite):
    def __init__(self, center, radius=100):
        super().__init__()
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (*ORANGE, 100), (radius, radius), radius, width=3)
        self.rect = self.image.get_rect(center=center)
        self.duration = 10
        
    def update(self):
        self.duration -= 1
        if self.duration <= 0:
            self.kill()
        else:
            self.image.set_alpha(int(100 * self.duration / 10))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, target_y, level=1, wave=1, boss=False):
        super().__init__()
        self.level = level
        self.boss = boss
        self.image = BOSS_IMG if boss else (ENEMY2_IMG if level==2 else ENEMY1_IMG)
        self.rect = self.image.get_rect(topleft=(x, -self.image.get_height()))
        self.position = pygame.Vector2(self.rect.centerx, self.rect.centery)
        
        # Movement
        self.target_y = target_y
        self.entering = True
        self.pattern = random.choice(["linear", "sine", "zigzag"]) if not boss else "boss"
        self.movement_timer = 0
        self.phase = random.uniform(0, 6.28)
        
        # Stats scaling with wave
        wave_scale = 1 + wave * 0.15
        self.entry_speed = 2 + wave * 0.1 + (1 if boss else 0)
        
        if boss:
            self.max_health = 20 * wave_scale
            self.speed = 1.5 + wave * 0.1
            self.shoot_delay = 200
            self.bullet_count = 3
            self.worth = 500
        else:
            self.max_health = (3 if level==2 else 1) * wave_scale
            self.speed = random.uniform(1, 2) + wave * 0.1
            self.shoot_delay = random.randint(1000, 3000)
            self.bullet_count = 1
            self.worth = 30 if level==2 else 10
            
        self.health = self.max_health
        self.last_shot = pygame.time.get_ticks() - random.randint(0, 1000)
        
    def update(self):
        if self.entering:
            self.position.y += self.entry_speed
            if self.position.y >= self.target_y:
                self.entering = False
        else:
            # Movement patterns
            self.movement_timer += 1
            
            if self.pattern == "linear":
                self.position.x += math.sin(self.movement_timer / 60 + self.phase) * self.speed
            elif self.pattern == "sine":
                self.position.x += math.sin(self.movement_timer / 40 + self.phase) * self.speed
                self.position.y += math.cos(self.movement_timer / 80 + self.phase) * self.speed * 0.5
            elif self.pattern == "zigzag":
                if (self.movement_timer // 30) % 2 == 0:
                    self.position.x += self.speed
                else:
                    self.position.x -= self.speed
            elif self.pattern == "boss":
                if self.movement_timer < 120:
                    progress = self.movement_timer / 120
                    self.position.x = WIDTH * (0.2 + 0.6 * progress)
                else:
                    t = (self.movement_timer - 120) / 100
                    self.position.x = WIDTH // 2 + math.sin(t * 2) * WIDTH // 4
                    self.position.y = self.target_y + math.sin(t) * HEIGHT // 8
            
            # Keep in bounds
            self.position.x = max(self.rect.width//2, min(WIDTH-self.rect.width//2, self.position.x))
            self.position.y = max(self.rect.height//2, min(HEIGHT//2, self.position.y))
            
            # Shooting
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.shoot()
                self.last_shot = now
                self.shoot_delay = int(self.shoot_delay * random.uniform(0.8, 1.2))
                
        # Update rect position
        self.rect.center = (round(self.position.x), round(self.position.y))
                
    def shoot(self):
        if self.boss:
            # Boss shoots patterns
            pattern = random.choice(["spread", "circle"])
            
            if pattern == "spread":
                for i in range(self.bullet_count):
                    angle = (i - (self.bullet_count-1)/2) * 15
                    bullet = EnemyBullet(self.rect.midbottom, angle=angle, 
                                      speed=random.uniform(3, 5), color=RED)
                    enemy_bullets.add(bullet)
                    all_sprites.add(bullet)
            else:
                for i in range(8):
                    angle = i * 45
                    bullet = EnemyBullet(self.rect.center, angle=angle,
                                      speed=random.uniform(2, 4), color=ORANGE)
                    enemy_bullets.add(bullet)
                    all_sprites.add(bullet)
        else:
            # Regular enemies
            offset = random.randint(-10, 10)
            bullet = EnemyBullet((self.rect.midbottom[0] + offset, self.rect.midbottom[1]),
                              angle=random.uniform(-10, 10), speed=random.uniform(3, 4))
            enemy_bullets.add(bullet)
            all_sprites.add(bullet)
                
    def take_damage(self, amount):
        self.health -= amount
        
        # Hit effect
        p = Particle(self.rect.centerx + random.randint(-15, 15),
                   self.rect.centery + random.randint(-15, 15), 
                   WHITE, size=random.randint(3, 5), duration=random.randint(5, 15))
        particles.add(p)
            
        if self.health <= 0:
            # Death explosion
            explosion = Explosion(self.rect.center, frames=15, color=ORANGE if self.boss else YELLOW)
            effects.add(explosion)
            
            # Chance to drop power-up
            drop_chance = 0.5 if self.boss else (0.15 if self.level == 2 else 0.1)
            if random.random() < drop_chance:
                self.drop_powerup()
                
            self.kill()
            return True
        return False
        
    def drop_powerup(self):
        options = ["shield", "weapon", "bomb", "double"] if self.boss else ["health", "shield", "rapid", "spread", "bomb"]
        powerup_type = random.choice(options)
        powerup = PowerUp(self.rect.center, powerup_type)
        powerups.add(powerup)
        all_sprites.add(powerup)
        
    def draw_health_bar(self, surface):
        if self.health < self.max_health:
            bar_width = self.rect.width
            bar_height = 5
            x, y = self.rect.x, self.rect.y - 10
            pygame.draw.rect(surface, (60, 0, 0), (x, y, bar_width, bar_height))
            health_width = max(0, int(bar_width * (self.health / self.max_health)))
            if health_width > 0:
                pygame.draw.rect(surface, RED, (x, y, health_width, bar_height))

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center, powerup_type):
        super().__init__()
        self.type = powerup_type
        self.size = 25
        
        colors = {
            "health": GREEN, "shield": BLUE, "rapid": YELLOW,
            "spread": PURPLE, "bomb": ORANGE, "weapon": PINK, "double": GOLD
        }
        
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, colors[self.type], (self.size//2, self.size//2), self.size//2 - 2)
        
        self.rect = self.image.get_rect(center=center)
        self.velocity = pygame.Vector2(0, 2)
        self.wobble = random.uniform(0, 6.28)
        self.wobble_strength = random.uniform(0.5, 1.5)
        
    def update(self):
        self.wobble += 0.1
        self.rect.y += self.velocity.y
        self.rect.x += math.sin(self.wobble) * self.wobble_strength
        if self.rect.top > HEIGHT:
            self.kill()

# Game functions
def spawn_wave(wave_num):
    # Boss wave every 5 levels
    is_boss_wave = (wave_num % 5 == 0)
    
    if is_boss_wave:
        boss = Enemy(WIDTH//2 - 75, HEIGHT//4, level=2, wave=wave_num, boss=True)
        enemies.add(boss)
        all_sprites.add(boss)
    else:
        enemy_count = 10 + wave_num * 2
        level2_chance = min(0.1 + (wave_num * 0.05), 0.5)
        
        cols = 6
        spacing_x = (WIDTH - 200) // (cols - 1)
        
        for i in range(min(enemy_count, 30)):  # Cap at 30 enemies
            col = i % cols
            row = i // cols
            
            x = 100 + col * spacing_x + random.randint(-20, 20)
            target_y = 100 + row * 60 + random.randint(-10, 10)
            
            level = 2 if random.random() < level2_chance else 1
            enemy = Enemy(x, target_y, level=level, wave=wave_num)
            enemies.add(enemy)
            all_sprites.add(enemy)

def draw_ui():
    # Draw game stats
    screen.blit(font_md.render(f"LIVES: {player.lives}", True, WHITE), (20, 20))
    screen.blit(font_md.render(f"SCORE: {player.score}", True, WHITE), (20, 60))
    screen.blit(font_md.render(f"WAVE: {current_wave}", True, WHITE), (20, 100))
    screen.blit(font_md.render(f"BOMBS: {player.bombs}", True, WHITE), (20, 140))
    
    # Power-up indicators
    y_pos = 180
    if player.rapid_fire_timer > 0:
        screen.blit(font_md.render(f"RAPID FIRE: {player.rapid_fire_timer//60}s", True, YELLOW), (20, y_pos))
        y_pos += 40
    if player.shield_timer > 0:
        screen.blit(font_md.render(f"SHIELD: {player.shield_timer//60}s", True, BLUE), (20, y_pos))
        y_pos += 40
    if player.spread_timer > 0:
        screen.blit(font_md.render(f"SPREAD: {player.spread_timer//60}s", True, PURPLE), (20, y_pos))
        y_pos += 40
    if player.double_damage_timer > 0:
        screen.blit(font_md.render(f"DOUBLE DMG: {player.double_damage_timer//60}s", True, GOLD), (20, y_pos))

def show_message_screen(title, subtitle=None, prompt=None, blink_prompt=False):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))  # Semi-transparent black
    screen.blit(overlay, (0, 0))
    
    # Title
    title_surf = font_xl.render(title[0], True, title[1])
    title_rect = title_surf.get_rect(center=(WIDTH//2, HEIGHT//3))
    screen.blit(title_surf, title_rect)
    
    # Subtitle
    if subtitle:
        sub_surf = font_lg.render(subtitle[0], True, subtitle[1])
        sub_rect = sub_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(sub_surf, sub_rect)
    
    # Prompt
    if prompt:
        if not blink_prompt or (pygame.time.get_ticks() // 500) % 2 == 0:
            prompt_surf = font_md.render(prompt[0], True, prompt[1])
            prompt_rect = prompt_surf.get_rect(center=(WIDTH//2, HEIGHT*2//3))
            screen.blit(prompt_surf, prompt_rect)
    
    pygame.display.flip()

def wait_for_key(valid_keys):
    """Wait for a keypress from the list of valid keys."""
    waiting = True
    while waiting:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key in valid_keys:
                    return event.key
    return None

def init_game():
    global game_state, current_wave, high_score, player
    global all_sprites, stars, player_bullets, enemy_bullets, enemies, powerups, particles, effects
    
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    stars = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    particles = pygame.sprite.Group()
    effects = pygame.sprite.Group()
    
    # Create stars
    for _ in range(200):
        layer = random.choices([0, 1, 2], weights=[0.6, 0.3, 0.1])[0]
        star = Star(layer)
        stars.add(star)
    
    # Create player
    player = Player()
    all_sprites.add(player)
    
    # Game variables
    current_wave = 1
    
    # Start first wave
    spawn_wave(current_wave)
    
    game_state = PLAYING

# Initialize variables
high_score = 0
current_wave = 1

# Main game loop
init_game()  # Initialize game objects
running = True

while running:
    clock.tick(FPS)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_state == PLAYING:
                    game_state = PAUSED
                else:
                    running = False
                    
            elif event.key == pygame.K_p and game_state == PLAYING:
                game_state = PAUSED
                
            elif event.key == pygame.K_r and game_state in [GAME_OVER, PAUSED]:
                init_game()
                    
            elif event.key == pygame.K_SPACE:
                if game_state == TITLE:
                    init_game()
                elif game_state == LEVEL_COMPLETE:
                    current_wave += 1
                    spawn_wave(current_wave)
                    game_state = PLAYING
                elif game_state == PAUSED:
                    game_state = PLAYING
    
    # Update based on game state
    if game_state == TITLE:
        stars.update()
        show_message_screen(
            ("GALACTICA", WHITE),
            ("STELLAR CONQUEST", GOLD),
            ("PRESS SPACE TO START", WHITE),
            blink_prompt=True
        )
        
    elif game_state == PLAYING:
        # Update all game objects
        all_sprites.update()
        particles.update()
        effects.update()
        
        # Player bullet → Enemy collisions
        hits = pygame.sprite.groupcollide(enemies, player_bullets, False, lambda bullet, enemy: not bullet.piercing)
        for enemy, bullets in hits.items():
            for bullet in bullets:
                if enemy.take_damage(bullet.damage):
                    player.score += enemy.worth
                    
        # Enemy bullet → Player collisions
        if pygame.sprite.spritecollide(player, enemy_bullets, True):
            if player.take_damage():
                # Game over
                if player.score > high_score:
                    high_score = player.score
                game_state = GAME_OVER
        
        # Player → Powerup collisions
        for powerup in pygame.sprite.spritecollide(player, powerups, True):
            player.add_powerup(powerup.type)
                
        # Check for wave completion
        if len(enemies) == 0:
            game_state = LEVEL_COMPLETE
            
        # Draw everything
        screen.fill(BLACK)
        stars.draw(screen)
        all_sprites.draw(screen)
        particles.draw(screen)
        effects.draw(screen)
        
        # Draw UI elements
        for enemy in enemies:
            enemy.draw_health_bar(screen)
        player.draw_shield_effect(screen)
        draw_ui()
        
        pygame.display.flip()
        
    elif game_state == LEVEL_COMPLETE:
        show_message_screen(
            (f"WAVE {current_wave} COMPLETE!", GREEN),
            (f"BONUS: +{current_wave * 100}", GOLD),
            ("PRESS SPACE TO CONTINUE", WHITE),
            blink_prompt=True
        )
        player.score += current_wave * 100
        
    elif game_state == GAME_OVER:
        show_message_screen(
            ("GAME OVER", RED),
            (f"SCORE: {player.score}", WHITE),
            ("PRESS R TO RESTART, ESC TO QUIT", WHITE)
        )
        
    elif game_state == PAUSED:
        show_message_screen(
            ("PAUSED", WHITE),
            None,
            ("P: RESUME, R: RESTART, ESC: QUIT", WHITE)
        )

pygame.quit()
