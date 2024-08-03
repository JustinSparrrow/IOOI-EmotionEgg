import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../emotion')

from audio_handler import AudioHandler
from infer import EmotionRecognizer
from whisper_recognition import WhisperRecognition
from utils import globals

import threading
from pynput import keyboard

audio_handler = AudioHandler()
recording_thread = None
recording = False


# 键盘事件处理函数
def on_press(key):
    global recording, recording_thread

    try:
        if key.char == 's':
            if recording:
                print("Stopping audio recording...")
                audio_handler.stop_recording()  # 停止录音
                recording_thread.join()  # 等待录音线程结束
                process_audio(audio_handler.frames)  # 处理录音后的音频
                recording = False
            else:
                print("Starting audio recording...")
                recording_thread = threading.Thread(target=audio_handler.start_recording)
                recording_thread.start()
                recording = True
    except AttributeError:
        pass


def process_audio(frames):
    audio_filename = "../recorded_audio.wav"
    transcript_filename = "../transcript.txt"
    emotion_filename = "../emotion/global_emotion.txt"

    # 保存录制的音频
    audio_handler.save_wave_file(audio_filename, frames)
    print(f"Audio saved to {audio_filename}")

    # 实例化 WhisperRecognition
    whisper_recognizer = WhisperRecognition()
    print("Transcribing audio...")
    result = whisper_recognizer.transcribe(audio_filename)  # 转录音频
    print("Transcription completed.")

    # 实例化 EmotionRecognizer
    emotion_recognizer = EmotionRecognizer(configs='configs/bi_lstm.yml',
                                           use_ms_model='iic/emotion2vec_plus_base',
                                           use_gpu=False,
                                           model_path='models/BiLSTM_Emotion2Vec/best_model/')
    print("Detecting emotion from audio...")
    detected_emotion, score = emotion_recognizer.predict_emotion(audio_path=audio_filename)
    print(f"Emotion detection completed. Detected emotion: {detected_emotion}, Score: {score}")

    # 组合心情和转录结果
    complete_message = f"我现在的心情是{detected_emotion}。我想说：{result['text']}。"
    for_logs = f"{time.localtime()} 用户信息：{result['text']} 用户检测到的情绪是：{detected_emotion}，得分：{score}"

    globals.update_global_emotion(detected_emotion, emotion_filename)
    print(f"Updated emotion to {globals.read_global_emotion(emotion_filename)}")

    # 打印并保存转录结果
    print("Transcript:", complete_message)
    with open(transcript_filename, 'w') as f:
        f.write(complete_message)
    print(f"Transcript saved to {transcript_filename}")

    logs_file = "../logs.txt"

    with open(logs_file, 'a') as f:
        f.write(for_logs + '\n')
    print(f"Logs saved to {logs_file}")


def audio():
    # 启动键盘监听
    print("Starting audio recording...")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == '__main__':
    audio()
