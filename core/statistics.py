import time

class Statistics:
    def __init__(self):
        self.start_time = time.time()
        self.caught_balls = 0
        self.missed_balls = 0

    def update(self, caught):
        """Обновляет статистику."""
        if caught:
            self.caught_balls += 1
        else:
            self.missed_balls += 1

    def get_summary(self):
        """Возвращает сводку статистики."""
        duration = time.time() - self.start_time
        return {
            "duration": duration,
            "caught_balls": self.caught_balls,
            "missed_balls": self.missed_balls
        }
