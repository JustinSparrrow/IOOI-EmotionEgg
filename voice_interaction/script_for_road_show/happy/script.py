import cv2
import time
import pygame
import os
from gpiozero import Button

# 定义视频计数器和按钮计数器
video_count = 0
button_press_count = 0

# 初始化按钮
button = Button(17)


def play_video_with_sound(video_file):
    cap = cv2.VideoCapture(video_file)

    if not cap.isOpened():
        print(f"无法打开视频文件: {video_file}")
        return

    # 提取音频文件并播放
    audio_file = video_file.replace(".mp4", ".wav")
    if os.path.exists(audio_file):
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        print(f"正在播放音频: {audio_file}")
    else:
        print(f"音频文件 {audio_file} 不存在，只播放视频。")

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


def handle_button_press():
    global button_press_count, video_count

    button_press_count += 1
    print(f"按钮按下次数: {button_press_count}")

    if video_count == 1 and button_press_count >= 2:
        video_count += 1
        play_video_with_sound(f"script{video_count}.mp4")
        button_press_count = 0  # 重置按钮按下计数器
    elif video_count == 2 and button_press_count >= 2:
        video_count += 1
        play_video_with_sound(f"script{video_count}.mp4")
        button_press_count = 0  # 重置按钮按下计数器
    elif video_count == 4 and button_press_count >= 2:
        video_count += 1
        play_video_with_sound(f"script{video_count}.mp4")
        button_press_count = 0  # 重置按钮按下计数器


# 按钮绑定事件
button.when_pressed = handle_button_press

# 在程序启动时自动播放script0
play_video_with_sound("script0.mp4")

# 播放script1的视频和音频
video_count = 1
play_video_with_sound(f"script{video_count}.mp4")

# 循环等待按钮事件
while video_count <= 5:
    time.sleep(0.1)  # 延迟一段时间，避免程序退出

    if video_count == 3:
        play_video_with_sound("script3.mp4")
        video_count += 1

    if video_count == 4:
        play_video_with_sound("script4.mp4")
        video_count += 1

    if video_count == 6:
        play_video_with_sound("script6.mp4")
        break  # 完成所有视频播放，退出循环

print("所有视频已播放完毕。")
