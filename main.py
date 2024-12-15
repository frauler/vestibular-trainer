import cv2
from core.pose_recognition import PoseRecognition
from core.interaction import Interaction
from core.statistics import Statistics

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Ошибка открытия камеры.")
        return

    screen_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    screen_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    stats = Statistics()
    interaction = Interaction(screen_width, screen_height)

    def on_pose_detected(wrist_x, wrist_y):
        """Обработка пересечения кисти с шариком."""
        ball_x, ball_y, ball_radius = interaction.get_ball_properties()
        if pose_recognition.is_hand_over_ball(ball_x, ball_y, ball_radius):
            interaction.caught_ball()
            stats.update(caught=True)  # Пойман шарик

    pose_recognition = PoseRecognition(screen_width, screen_height, on_pose_detected)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Ошибка получения кадра.")
            break

        # Распознавание позы
        pose_recognition.process_frame(frame)

        # Отрисовка объектов
        interaction.draw(frame)

        # Проверка на пропуск шарика
        interaction.check_and_update_ball(stats)

        # Отображаем кадр
        cv2.imshow("Vestibular Trainer", frame)

        # Выход из цикла при нажатии клавиши 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Завершаем работу
    pose_recognition.close()
    cap.release()
    cv2.destroyAllWindows()

    # Вывод статистики
    summary = stats.get_summary()
    print(f"Упражнение завершено за {summary['duration']:.2f} секунд.")
    print(f"Поймано шариков: {summary['caught_balls']}, Пропущено: {summary['missed_balls']}.")

if __name__ == "__main__":
    main()
