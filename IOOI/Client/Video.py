import cv2
import asyncio
import websockets
import time

# 服务端WebSocket URL
WEBSOCKET_URL = "ws://localhost:8000/ws/video"

async def send_video_to_server():
    # 打开摄像头
    cap = cv2.VideoCapture(0)

    async with websockets.connect(WEBSOCKET_URL) as websocket:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("无法捕捉视频帧")
                break

            # 将帧编码为JPEG格式
            _, buffer = cv2.imencode('.jpg', frame)
            # 将帧数据转换为字节数组
            frame_bytes = buffer.tobytes()

            # 发送帧数据到服务器
            await websocket.send(frame_bytes)

            print("视频帧已发送")
            # 每5秒发送一次
            time.sleep(5)

    # 释放摄像头资源
    cap.release()

# 启动异步任务发送视频
if __name__ == "__main__":
    asyncio.run(send_video_to_server())