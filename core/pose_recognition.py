import mediapipe as mp
import cv2

class PoseRecognition:
    def __init__(self, screen_width, screen_height, callback):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.callback = callback

        # Инициализация Mediapipe для распознавания поз
        self.pose = mp.solutions.pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.current_landmarks = None

    def process_frame(self, frame):
        """Обработка кадра с камеры и вызов колбэка."""
        # Mediapipe работает с RGB-изображениями
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame_rgb)

        if results.pose_landmarks:
            # Сохраняем текущие лендмарки
            self.current_landmarks = results.pose_landmarks
            self.handle_left_hand(frame)

    def handle_left_hand(self, frame):
        """Обработка левой руки Mediapipe (фактически правой руки пользователя)."""
        hand_points = [21, 17, 19]  # Точки пальцев левой руки (в Mediapipe)
        wrist_point = 15  # Точка запястья

        points = []
        for idx in hand_points + [wrist_point]:
            landmark = self.current_landmarks.landmark[idx]
            x = int(landmark.x * self.screen_width)
            y = int(landmark.y * self.screen_height)
            points.append((x, y))
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)  # Отрисовка точки

        # Соединяем пальцы линиями
        for i in range(len(points) - 1):
            cv2.line(frame, points[i], points[i + 1], (0, 255, 0), 2)

        # Передаём координаты запястья для проверки пересечения
        wrist_x, wrist_y = points[-1]
        self.callback(wrist_x, wrist_y)

    def is_hand_over_ball(self, ball_x, ball_y, ball_radius):
        """Проверка пересечения кисти с шариком."""
        if self.current_landmarks:
            hand_points = [17, 19, 21]  # Левые пальцы Mediapipe
            for idx in hand_points:
                landmark = self.current_landmarks.landmark[idx]
                x = int(landmark.x * self.screen_width)
                y = int(landmark.y * self.screen_height)

                # Проверяем, попадает ли точка пальца в радиус шара
                if (x - ball_x) ** 2 + (y - ball_y) ** 2 <= ball_radius ** 2:
                    return True
        return False

    def close(self):
        """Освобождение ресурсов Mediapipe."""
        self.pose.close()
