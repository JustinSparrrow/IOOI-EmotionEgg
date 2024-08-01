# DeepFace方式人脸情绪识别
import cv2
from deepface import DeepFace
import time

from utils import globals


class FaceEmotionRecognizer:

    def __init__(self) -> None:
        pass

    def face_emotion_recognition(self):
        cap = cv2.VideoCapture(0)  # 打开摄像头
        last_emotion = None
        last_update_time = time.time()
        display_duration = 2  # 每个情绪显示的时间（秒）
        times = 0

        while cap.isOpened() and times == 0:
            ret, frame = cap.read()  # 读取一帧
            if not ret:
                break

            # 每隔一定时间进行一次情绪识别
            current_time = time.time()
            if current_time - last_update_time >= display_duration:
                result = DeepFace.analyze(img_path=frame, actions=['emotion'], enforce_detection=False)  # 识别图像情绪
                if result:
                    last_emotion = result[0]['dominant_emotion']  # 获取主要情绪
                    last_update_time = current_time

                    print(last_emotion)
                    path = "../../utils/global_emotion.txt"
                    globals.update_global_emotion(last_emotion, path)
                    print(f"Updated global_emotion to {globals.read_global_emotion(path)}")
                    times = 1
                    # update_face_canvas(last_emotion)

            if last_emotion:
                # 在视频上绘制情绪
                cv2.putText(frame, f"{last_emotion}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                            cv2.LINE_AA)

            cv2.imshow('Video', frame)  # 显示视频帧

            # 按 'q' 键退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()  # 释放摄像头
        cv2.destroyAllWindows()  # 关闭所有窗口
