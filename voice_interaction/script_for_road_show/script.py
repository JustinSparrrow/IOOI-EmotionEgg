import cv2
import time
import pygame
from pynput import keyboard
import threading

# 定义按键计数器和视频计数器
press_count = 0
video_count = 1

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

def on_press(key):
    global press_count, video_count

    try:
        if key.char == 's':
            press_count += 1

            # 在每个偶数次按下时播放视频
            if press_count % 2 == 0:
                if video_count <= 5:
                    video_file = f"script{video_count}.mp4"
                    play_video_with_sound(video_file)
                    video_count += 1
                else:
                    return False  # 停止监听
    except AttributeError:
        pass

def start_video():
    global video_count
    time.sleep(1)
    video_file = f"script{video_count}.mp4"
    play_video_with_sound(video_file)
    video_count += 1

# 启动播放第一个视频的线程
video_thread = threading.Thread(target=start_video)
video_thread.start()

# 确保第一个视频播放完成后再启动键盘监听
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()