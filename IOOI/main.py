from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio
import os
import random

from Video_emotion.face_emotion_recognizer import face_emotion_recognition
from Voice_emotion.audio_emotion_recognizer import process_audio, open_agents
from Voice_emotion.save_audio import save_audio_to_file

app = FastAPI()

# 根据情绪获取随机视频
def get_random_video(emotion):
    video_dir = f'videos/{emotion}'
    if os.path.exists(video_dir):
        video_files = os.listdir(video_dir)
        if video_files:
            return os.path.join(video_dir, random.choice(video_files))
    return None

# 转换中文情绪到英文情绪
def change_emotion(emotion):
    emotion_dict = {
        '中立': 'neutral',
        '生气': 'angry',
        '厌恶': 'disgusted',
        '害怕': 'fear',
        '开心': 'happy',
        '悲伤': 'sad',
        '惊讶': 'surprise'
    }
    return emotion_dict.get(emotion, 'neutral')

@app.websocket("/ws/video")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            face_emotion_recognition(data)
    except Exception as e:
        print(e)
    finally:
        await websocket.close()


@app.websocket("/ws/audio")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            audio_data = await websocket.receive_bytes()

            audio_file_path = save_audio_to_file(audio_data)
            print(f"Audio saved to: {audio_file_path}")

            process_audio()
            open_agents()
    except Exception as e:
        print(e)
    finally:
        await websocket.close()


# 监控全局情绪文件并通过WebSocket发送视频
async def monitor_emotion_and_notify(websocket: WebSocket):
    last_emotion = None
    while True:
        path = "../emotion/global_emotion.txt"
        try:
            with open(path, 'r') as file:
                current_emotion = file.read().strip()
                current_emotion = change_emotion(current_emotion)

            if current_emotion != last_emotion:
                video_path = get_random_video(current_emotion)
                if video_path:
                    print(f"Playing video for emotion: {current_emotion}")
                    # 将视频路径发送到客户端
                    await websocket.send_text(video_path)
                    last_emotion = current_emotion
                else:
                    print(f"No videos available for this emotion {current_emotion}.")
            await asyncio.sleep(1)  # 减少检查频率以减少资源消耗
        except Exception as e:
            print(f"Error reading emotion file: {e}")
            break

# WebSocket端点，用于监控情绪并通知客户端播放视频
@app.websocket("/ws/monitor")
async def websocket_emotion_monitor(websocket: WebSocket):
    await websocket.accept()
    try:
        await monitor_emotion_and_notify(websocket)
    except Exception as e:
        print(f"WebSocket connection error: {e}")
    finally:
        await websocket.close()