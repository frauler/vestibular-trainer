import random
import cv2
import numpy as np
import time  # Для отслеживания времени жизни

class Ball:
    def __init__(self, screen_width, screen_height, life_time):
        self.x = random.randint(50, screen_width - 50)
        self.y = random.randint(50, screen_height - 50)
        self.radius = 25
        self.life_time = life_time  # Время жизни шарика (в секундах)
        self.spawn_time = time.time()  # Время появления шарика

    def draw(self, frame):
        """Рисует шарик на кадре."""
        cv2.circle(frame, (self.x, self.y), self.radius, (0, 0, 255), -1)

    def check_collision(self, hand_x, hand_y):
        """Проверяет пересечение шарика и руки."""
        distance = np.sqrt((self.x - hand_x) ** 2 + (self.y - hand_y) ** 2)
        return distance < self.radius

    def is_lifetime_expired(self):
        """Проверяет, истекло ли время жизни шарика."""
        elapsed_time = time.time() - self.spawn_time
        return elapsed_time > self.life_time

class Interaction:
    def __init__(self, screen_width, screen_height, life_time=5):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.life_time = life_time  # Время жизни шара
        self.ball = Ball(screen_width, screen_height, life_time)  # Создание первого шарика
        self.last_check_time = time.time()  # Время последней проверки

    def draw(self, frame):
        """Отрисовка шара."""
        self.ball.draw(frame)

    def get_ball_properties(self):
        """Возвращает координаты и радиус шара."""
        return self.ball.x, self.ball.y, self.ball.radius

    def caught_ball(self):
        """Обработка события захвата шара (перемещение шара)."""
        self.ball.x = random.randint(self.ball.radius, self.screen_width - self.ball.radius)
        self.ball.y = random.randint(self.ball.radius, self.screen_height - self.ball.radius)
        self.ball.spawn_time = time.time()  # Сбрасываем время жизни при новом положении шара

    def check_and_update_ball(self, stats):
        """Проверка времени жизни шара и его обновление, если время истекло."""
        # Проверяем время жизни шарика
        if self.ball.is_lifetime_expired():
            print("Ball missed!")
            stats.update(caught=False)  # Увеличиваем статистику пропущенных мячей
            self.ball = Ball(self.screen_width, self.screen_height, self.life_time)  # Создаем новый шарик
