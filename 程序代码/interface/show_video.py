import cv2
import os
import random
import time


def get_random_video(emotion):
    video_dir = f'videos/{emotion}'
    if os.path.exists(video_dir):
        video_files = os.listdir(video_dir)
        if video_files:
            return os.path.join(video_dir, random.choice(video_files))
    return None


def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file.")
        return

    # 获取视频帧率，以便同步播放速度
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = int(1000 / fps) if fps > 0 else 25

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Video', frame)
            # 根据视频帧率设置延迟
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break
        else:
            break  # 当读取完所有帧时自动退出

    cap.release()
    cv2.destroyAllWindows()


def monitor_emotion_and_play():
    last_emotion = None
    while True:
        path = "../emotion/global_emotion.txt"
        with open(path, 'r') as file:
            current_emotion = file.read().strip()
            current_emotion = change_emotion(current_emotion)

        if current_emotion != last_emotion:
            video_path = get_random_video(current_emotion)
            if video_path:
                print(f"Playing video for emotion: {current_emotion}")
                play_video(video_path)
                last_emotion = current_emotion
            else:
                print(f"No videos available for this emotion {current_emotion}.")
            time.sleep(1)  # 减少检查频率以减少资源消耗


def change_emotion(emotion):
    if emotion == '中立':
        emotion = 'neutral'
    elif emotion == '生气':
        emotion = 'angry'
    elif emotion == '厌恶':
        emotion = 'disgusted'
    elif emotion == '害怕':
        emotion = 'fear'
    elif emotion == '开心':
        emotion = 'happy'
    elif emotion == '悲伤':
        emotion = 'sad'
    elif emotion == '惊讶':
        emotion = 'surprise'

    return emotion


if __name__ == "__main__":
    monitor_emotion_and_play()
