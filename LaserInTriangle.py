import pygame
import sys
import math
import random

# Ekran boyutları
WIDTH, HEIGHT = 800, 600

# Renkler
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Top ve çizgi özellikleri
ball_radius = 2
ball_speed = 1
ball_angle = math.radians(64)
ball_x = 400

# Geçmiş konumlar listesi
trail_length = 10000
trail_positions = []

class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.m = (self.end[1] - self.start[1]) / (self.end[0] - self.start[0]) if self.end[0] != self.start[0] else None
        self.b = self.start[1] - self.m * self.start[0] if self.m is not None else None
        self.rect = pygame.Rect(min(self.start[0], self.end[0]), min(self.start[1], self.end[1]),
                                abs(self.end[0] - self.start[0]), abs(self.end[1] - self.start[1]))

    def draw(self, screen):
        pygame.draw.line(screen, BLUE, self.start, self.end, 5)

    def check_collision(self, ball_x, ball_y):
        if self.m is not None and self.b is not None:
            dist_to_line = abs(ball_y - (self.m * ball_x + self.b)) / math.sqrt(1 + self.m ** 2)
            if dist_to_line <= ball_radius and min(self.start[0], self.end[0]) <= ball_x <= max(self.start[0],
                                                                                                self.end[0]):
                incident_angle = math.atan2(-self.m, 1)
                return 2 * incident_angle - ball_angle
        return None

# Çizgileri oluştur
lines = []

# RASTGELE ÇİZGİ EKLER
# for _ in range(2):
#     start_x = random.randint(50, WIDTH - 50)
#     start_y = random.randint(50, HEIGHT - 50)
#     end_x = random.randint(50, WIDTH - 50)
#     end_y = random.randint(50, HEIGHT - 50)
#     lines.append(Line((start_x, start_y), (end_x, end_y)))


# Ekranın ortasını belirle
middle_x = WIDTH / 2
middle_y = HEIGHT / 2

# Üçgenin diğer iki köşesini belirle (örneğin, üçgenin kenarları ekranın yarısı kadar olsun)
triangle_side_length = 500
triangle_height = math.sqrt(3) / 2 * triangle_side_length

triangle_top = (middle_x, middle_y - triangle_height / 2)
triangle_left = (middle_x - triangle_side_length / 2, middle_y + triangle_height / 2)
triangle_right = (middle_x + triangle_side_length / 2, middle_y + triangle_height / 2)

# Üçgenin çizgisini oluştur ve lines listesine ekle
lines.append(Line(triangle_top, triangle_left))
lines.append(Line(triangle_left, triangle_right))
lines.append(Line(triangle_right, triangle_top))

ball_y = (triangle_height*(2/3) + ( middle_y - triangle_height / 2)) # üçgenin merkezinden başlattım


# Pencereyi başlat
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top ve Çizgi Çarpışması")
clock = pygame.time.Clock()


def update_ball_position(ball_x, ball_y, ball_angle):
    ball_x += ball_speed * math.cos(ball_angle)
    ball_y -= ball_speed * math.sin(ball_angle)
    return ball_x, ball_y


def check_boundary_collision(ball_x, ball_y, ball_angle):
    if ball_x <= ball_radius or ball_x >= WIDTH - ball_radius:
        ball_angle = math.pi - ball_angle

    if ball_y <= ball_radius or ball_y >= HEIGHT - ball_radius:
        ball_angle = -ball_angle

    return ball_angle


def check_line_collision(ball_x, ball_y, ball_angle):
    for line in lines:
        reflected_angle = line.check_collision(ball_x, ball_y)
        if reflected_angle is not None:
            return reflected_angle
    return ball_angle

def update_trail(ball_x, ball_y):
    trail_positions.append((ball_x, ball_y))
    if len(trail_positions) > trail_length:
        trail_positions.pop(0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ball_x, ball_y = update_ball_position(ball_x, ball_y, ball_angle)
    ball_angle = check_boundary_collision(ball_x, ball_y, ball_angle)
    ball_angle = check_line_collision(ball_x, ball_y, ball_angle)
    update_trail(ball_x, ball_y)

    screen.fill(GRAY)

    for line in lines:
        line.draw(screen)

    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)

    # Topun izini çiz
    for pos in trail_positions:
        pygame.draw.circle(screen, RED, (int(pos[0]), int(pos[1])), ball_radius)

    pygame.display.flip()
    clock.tick(1000)

pygame.quit()
sys.exit()
