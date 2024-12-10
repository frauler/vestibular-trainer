import cv2
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
from mediapipe import solutions
import numpy as np

# Параметры Mediapipe
BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Путь к модели Mediapipe Pose
model_path = "pose_landmarker_full.task"

# Колбэк для обработки результатов
def draw_landmarks_on_image(rgb_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)

    # Цикл по найденным позам для визуализации
    for idx in range(len(pose_landmarks_list)):
        pose_landmarks = pose_landmarks_list[idx]

        # Преобразование списка поз в формат Mediapipe
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) 
            for landmark in pose_landmarks
        ])
        
        # Отрисовка позы на изображении
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            pose_landmarks_proto,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style()
        )
    return annotated_image

# Функция-обработчик результатов (глобальная переменная для сохранения обработанного изображения)
processed_frame = None
def result_callback(result: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global processed_frame
    # Преобразование выходного изображения Mediapipe в numpy
    rgb_image = output_image.numpy_view()
    processed_frame = draw_landmarks_on_image(rgb_image, result)

# Опции для Mediapipe Pose
options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=result_callback
)

# Захват видео с камеры
cap = cv2.VideoCapture(0)  # 0 — индекс камеры, можно заменить на путь к видеофайлу

if not cap.isOpened():
    print("Не удалось открыть камеру.")
    exit()

# Создание экземпляра PoseLandmarker
with PoseLandmarker.create_from_options(options) as landmarker:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Не удалось получить кадр.")
            break

        # Преобразование кадра OpenCV в формат Mediapipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

        # Текущая метка времени
        timestamp_ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))

        # Обработка кадра
        landmarker.detect_async(mp_image, timestamp_ms)

        # Используем обработанное изображение, если доступно
        if processed_frame is not None:
            frame_to_show = cv2.cvtColor(processed_frame, cv2.COLOR_RGB2BGR)
        else:
            frame_to_show = frame

        # Показ видео с аннотациями
        cv2.imshow("Camera", frame_to_show)

        # Выход по нажатию клавиши 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
