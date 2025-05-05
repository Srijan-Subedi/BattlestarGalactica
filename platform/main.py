import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen settings
display_info = pygame.display.Info()
WIDTH, HEIGHT = display_info.current_w, display_info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Galactica: Ascension")
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE  = (255, 255, 255)
RED    = (255,   0,   0)
GREEN  = (  0, 255,   0)
YELLOW = (255, 255,   0)
BLUE   = (  0, 200, 255)
PURPLE = (180, 0, 255)
ORANGE = (255, 140, 0)
BLACK  = (  0,   0,   0)

# Asset loader
def load_image(path, size=None, flip=False, angle=0):
    img = pygame.image.load(path).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    if angle:
        img = pygame.transform.rotate(img, angle)
    if flip:
        img = pygame.transform.flip(img, True, False)
    return img

# Load your images here
PLAYER_IMG = load_image('platform/assets/player.png',   (100, 100))
ENEMY1_IMG = load_image('platform/assets/level 1 boss.png', (80, 80), angle=180)
ENEMY2_IMG = load_image('platform/assets/level 2 boss.png', (120, 120), angle=180)
BOSS_COLOR = (255, 80, 80)

# Starfield
class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((2,2))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(
            center=(random.randrange(0, WIDTH), random.randrange(-HEIGHT, 0))
        )
        self.speed = random.uniform(1, 4)
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = random.randrange(-HEIGHT // 4, 0)
            self.rect.x = random.randrange(0, WIDTH)
            self.speed = random.uniform(1, 4)

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_IMG
        self.rect  = self.image.get_rect(midbottom=(WIDTH//2, HEIGHT - 20))
        self.speed = 8
        self.lives = 3
        self.cooldown  = 250
        self.last_shot = pygame.time.get_ticks()
        self.invincible = False
        self.invincible_start = 0
        self.shield = False
        self.shield_end = 0
        self.double_shot = False
        self.double_shot_end = 0
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]  and self.rect.left > 0:        self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:   self.rect.x += self.speed
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last_shot >= self.cooldown:
                bullet = Bullet(self.rect.midtop)
                all_sprites.add(bullet); player_bullets.add(bullet)
                if self.double_shot:
                    bullet2 = Bullet((self.rect.midtop[0] + 30, self.rect.midtop[1]))
                    all_sprites.add(bullet2); player_bullets.add(bullet2)
                self.last_shot = now
        # Invincibility blink
        if self.invincible and (pygame.time.get_ticks() - self.invincible_start < 2000):
            if (pygame.time.get_ticks() // 100) % 2 == 0:
                self.image.set_alpha(80)
            else:
                self.image.set_alpha(255)
        else:
            self.invincible = False
            self.image.set_alpha(255)
        # Shield effect
        if self.shield and pygame.time.get_ticks() > self.shield_end:
            self.shield = False
        # Double shot effect
        if self.double_shot and pygame.time.get_ticks() > self.double_shot_end:
            self.double_shot = False

    def draw_shield(self, surface):
        if self.shield:
            pygame.draw.circle(surface, BLUE, self.rect.center, self.rect.width//2+10, 4)

# Enemy with vertical entry and pattern support
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, target_y, level=1, wave=1, boss=False):
        super().__init__()
        self.level   = level
        self.boss    = boss
        self.image   = ENEMY2_IMG if (level==2 or boss) else ENEMY1_IMG
        if boss:
            self.image = self.image.copy()
            self.image.fill(BOSS_COLOR, special_flags=pygame.BLEND_RGB_ADD)
        self.rect    = self.image.get_rect(topleft=(x, -self.image.get_height()))
        self.target_y    = target_y
        self.entry_speed = 2 + wave * 0.1 + (1 if boss else 0)
        self.entering    = True
        self.health      = (3 if level==2 else 1) + (4 if boss else 0)
        self.speed       = random.choice([1.5,2,2.5]) + wave*0.2 + (1.5 if boss else 0)
        self.direction   = random.choice([-1,1])
        self.shoot_interval = random.randint(
            max(400, 1500 - wave * 100),
            max(800, 5000 - wave * 200)
        )
        if boss: self.shoot_interval = random.randint(200, 800)
        self.last_shot      = pygame.time.get_ticks()
        self.color_cycle = 0

    def update(self):
        if self.entering:
            self.rect.y += self.entry_speed
            if self.rect.y >= self.target_y:
                self.entering = False
        else:
            # horizontal patrol
            self.rect.x += self.speed * self.direction
            if self.rect.left < 50 or self.rect.right > WIDTH-50:
                self.direction *= -1
            # shooting
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_interval:
                eb = EnemyBullet(self.rect.midbottom)
                all_sprites.add(eb); enemy_bullets.add(eb)
                self.last_shot = now
            # color cycle for bosses
            if self.boss:
                self.color_cycle = (self.color_cycle + 1) % 60
                if self.color_cycle < 20:
                    self.image.fill((255, 80, 80), special_flags=pygame.BLEND_RGB_ADD)
                elif self.color_cycle < 40:
                    self.image.fill((80, 80, 255), special_flags=pygame.BLEND_RGB_ADD)
                else:
                    self.image.fill((80, 255, 80), special_flags=pygame.BLEND_RGB_ADD)

# Bullets & PowerUps
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((4,10)); self.image.fill(WHITE)
        self.rect  = self.image.get_rect(midbottom=pos)
        self.speed = -10
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0: self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((4,10)); self.image.fill(YELLOW)
        self.rect  = self.image.get_rect(midtop=pos)
        self.speed = 5
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT: self.kill()

class PowerUp(pygame.sprite.Sprite):
    TYPES = ['health','rapid','shield','double','bomb']
    def __init__(self, center):
        super().__init__()
        self.type  = random.choice(self.TYPES)
        self.image = pygame.Surface((28,28), pygame.SRCALPHA)
        color = {
            'health': GREEN,
            'rapid': YELLOW,
            'shield': BLUE,
            'double': PURPLE,
            'bomb': ORANGE
        }[self.type]
        pygame.draw.circle(self.image, color, (14,14), 14)
        self.rect  = self.image.get_rect(center=center)
        self.speed = 3
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT: self.kill()

# Explosion animation
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, frames=12, color=(255,255,0)):
        super().__init__()
        self.frames = []
        for i in range(frames):
            surf = pygame.Surface((80, 80), pygame.SRCALPHA)
            pygame.draw.circle(surf, color + (max(0, 255-20*i),), (40, 40), 40-i*3)
            pygame.draw.circle(surf, (255, 100, 0, max(0, 180-15*i)), (40, 40), 28-i*2)
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

# Groups
all_sprites    = pygame.sprite.Group()
stars          = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets  = pygame.sprite.Group()
enemies        = pygame.sprite.Group()
powerups       = pygame.sprite.Group()
explosions     = pygame.sprite.Group()

# Build starfield
for _ in range(120):
    star = Star()
    stars.add(star)
    all_sprites.add(star)

# Player
player = Player()
all_sprites.add(player)

# Waves
enemy_wave = 1
score      = 0
high_score = 0
font_s = pygame.font.SysFont(None, 36)
font_l = pygame.font.SysFont(None, 72)

# Powerup effect timer
rapid_fire_end = 0

# Combo system
combo = 0
combo_timer = 0

def draw_ui():
    screen.blit(font_s.render(f"Lives: {player.lives}", True, WHITE), (10,10))
    screen.blit(font_s.render(f"Score: {score}",      True, WHITE), (10,50))
    screen.blit(font_s.render(f"Wave: {enemy_wave}",  True, WHITE), (10,90))
    screen.blit(font_s.render(f"High: {high_score}",  True, YELLOW), (10,130))
    if player.cooldown < 250:
        left = max(0, (rapid_fire_end - pygame.time.get_ticks()) // 1000)
        screen.blit(font_s.render(f"Rapid: {left}s", True, YELLOW), (10,170))
    if player.shield:
        left = max(0, (player.shield_end - pygame.time.get_ticks()) // 1000)
        screen.blit(font_s.render(f"Shield: {left}s", True, BLUE), (10,210))
    if player.double_shot:
        left = max(0, (player.double_shot_end - pygame.time.get_ticks()) // 1000)
        screen.blit(font_s.render(f"Double: {left}s", True, PURPLE), (10,250))
    if combo > 1:
        screen.blit(font_s.render(f"Combo x{combo}", True, ORANGE), (10, 290))

def draw_enemy_healthbars():
    for en in enemies:
        if hasattr(en, "level") and (en.level == 2 or en.boss):
            maxh = 7 if en.boss else (5 if enemy_wave % 5 == 0 else 3)
            bar_w, bar_h = en.rect.width, 7
            ratio = en.health / maxh
            pygame.draw.rect(screen, RED,   (en.rect.x, en.rect.y-14, bar_w, bar_h))
            pygame.draw.rect(screen, GREEN, (en.rect.x, en.rect.y-14, int(bar_w*ratio), bar_h))

def wave_intro(wave):
    intro = font_l.render(f"Wave {wave}", True, YELLOW)
    screen.fill(BLACK)
    stars.draw(screen)
    screen.blit(intro, intro.get_rect(center=(WIDTH//2, HEIGHT//2)))
    pygame.display.flip()
    pygame.time.delay(2000)

def spawn_wave(count):
    global enemy_wave
    cols = 6
    padding_x, padding_y = 80, 120
    pattern = enemy_wave % 4
    boss_wave = (enemy_wave % 5 == 0)
    for i in range(count):
        col, row = i % cols, i // cols
        # Default grid
        x = padding_x + col * (ENEMY1_IMG.get_width() + 60)
        y = padding_y + row * (ENEMY1_IMG.get_height() + 40)
        # Pattern 2: Zig-zag
        if pattern == 1:
            if row % 2 == 1:
                x += (ENEMY1_IMG.get_width() + 60) // 2
        # Pattern 3: V-shape
        elif pattern == 2:
            mid = cols // 2
            x += abs(col - mid) * 20 * (1 if col < mid else -1)
            y += abs(col - mid) * 20
        # Pattern 4: Random scatter
        elif pattern == 3:
            x = random.randint(padding_x, WIDTH - padding_x - ENEMY1_IMG.get_width())
            y = random.randint(padding_y, HEIGHT // 3)
        # Boss wave: all level 2, more health, more speed
        if boss_wave:
            lvl = 2
        else:
            lvl = 2 if random.random() < min(0.2 + 0.05 * (enemy_wave-1), 0.7) else 1
        e = Enemy(x, y, level=lvl, wave=enemy_wave, boss=boss_wave)
        if boss_wave:
            e.health = 7
        enemies.add(e)
        all_sprites.add(e)

# initial wave
spawn_wave(16)

# Game Over handler
def game_over_screen():
    global high_score, score
    if score > high_score:
        high_score = score
    screen.fill(BLACK)
    msg = font_l.render("GAME OVER", True, RED)
    sub = font_s.render("Press R to Restart or ESC to Quit", True, WHITE)
    hi = font_s.render(f"High Score: {high_score}", True, YELLOW)
    screen.blit(msg, msg.get_rect(center=(WIDTH//2, HEIGHT//2 - 70)))
    screen.blit(hi, hi.get_rect(center=(WIDTH//2, HEIGHT//2)))
    screen.blit(sub, sub.get_rect(center=(WIDTH//2, HEIGHT//2 + 70)))
    pygame.display.flip()
    waiting = True
    while waiting:
        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_r:
                    waiting = False
                    return True
                if evt.key == pygame.K_ESCAPE:
                    return False

# Main loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            pause_screen()

    all_sprites.update()
    explosions.update()

    # Bullet → Enemy
    hits = pygame.sprite.groupcollide(enemies, player_bullets, False, True)
    if hits:
        now = pygame.time.get_ticks()
        if now - combo_timer < 1200:
            combo += 1
        else:
            combo = 1
        combo_timer = now
    for enemy, blts in hits.items():
        for _ in blts:
            enemy.health -= 1
            if enemy.health <= 0:
                mult = 2 if enemy_wave % 5 == 0 else 1
                score += ((30 if enemy.level==2 or enemy.boss else 10) * mult) * combo
                explosions.add(Explosion(enemy.rect.center, color=(255,80,80) if enemy.boss else (255,255,0)))
                if random.random() < 0.15:
                    pu = PowerUp(enemy.rect.center)
                    powerups.add(pu); all_sprites.add(pu)
                enemy.kill()

    # Bomb powerup
    for pu in [p for p in powerups if p.type == 'bomb' and p.rect.colliderect(player.rect)]:
        for en in enemies:
            explosions.add(Explosion(en.rect.center, color=ORANGE))
            en.kill()
        pu.kill()

    # Enemy bullet → Player
    if not player.invincible and not player.shield and pygame.sprite.spritecollide(player, enemy_bullets, True):
        explosions.add(Explosion(player.rect.center))
        player.lives -= 1
        if player.lives > 0:
            player.invincible = True
            player.invincible_start = pygame.time.get_ticks()
        else:
            if game_over_screen():
                # reset state
                for grp in [enemies, enemy_bullets, player_bullets, powerups, all_sprites, explosions]:
                    grp.empty()
                stars.empty(); all_sprites.empty()
                for _ in range(120):
                    star = Star(); stars.add(star); all_sprites.add(star)
                player = Player(); all_sprites.add(player)
                enemy_wave = 1; score = 0; combo = 0
                spawn_wave(16)
                rapid_fire_end = 0
                continue
            else:
                running = False

    # PowerUp
    for pu in pygame.sprite.spritecollide(player, powerups, True):
        if pu.type=='health' and player.lives<5:
            player.lives += 1
        elif pu.type=='rapid':
            player.cooldown = 80
            rapid_fire_end = pygame.time.get_ticks() + 8000
        elif pu.type=='shield':
            player.shield = True
            player.shield_end = pygame.time.get_ticks() + 6000
        elif pu.type=='double':
            player.double_shot = True
            player.double_shot_end = pygame.time.get_ticks() + 8000

    # PowerUp effect timer
    if player.cooldown < 250 and pygame.time.get_ticks() > rapid_fire_end:
        player.cooldown = 250
    if player.shield and pygame.time.get_ticks() > player.shield_end:
        player.shield = False
    if player.double_shot and pygame.time.get_ticks() > player.double_shot_end:
        player.double_shot = False

    # Next wave with intro and pause
    if not enemies:
        enemy_wave += 1
        wave_intro(enemy_wave)
        spawn_wave(16 + enemy_wave * 2)
        combo = 0

    # Draw
    screen.fill(BLACK)
    stars.draw(screen)
    all_sprites.draw(screen)
    explosions.draw(screen)
    draw_enemy_healthbars()
    player.draw_shield(screen)
    draw_ui()
    pygame.display.flip()

pygame.quit()
