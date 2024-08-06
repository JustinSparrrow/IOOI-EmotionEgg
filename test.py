import cv2
import pygame
import time


def play_video_with_sound(video_file):
    cap = cv2.VideoCapture(video_file)

    if not cap.isOpened():
        print(f"无法打开视频文件: {video_file}")
        return

    # 提取音频文件并播放
    audio_file = video_file.replace(".mp4", ".wav")
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Video', frame)

        # 按下 'q' 键退出播放
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.music.stop()


# 在程序启动1秒后自动播放第一个视频
time.sleep(1)
video_file = "script1.mp4"  # 仅播放第一个视频
play_video_with_sound(video_file)
