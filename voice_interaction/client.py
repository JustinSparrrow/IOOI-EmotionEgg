import asyncio
import websockets
import pyaudio
import wave
import json

async def record_audio():
    """
    使用系统麦克风录制音频并保存为 WAV 文件。
    :return: bytes, 录制的音频数据
    """
    chunk = 1024  # 每次读取的音频数据块大小
    sample_format = pyaudio.paInt16  # 采样格式
    channels = 1  # 音频通道数量
    fs = 44100  # 采样率
    seconds = 5  # 录音时长
    p = pyaudio.PyAudio()  # 实例化 PyAudio 对象

    print("Recording...")

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # 存放录音数据的列表

    for _ in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    print("Finished recording.")

    return b''.join(frames)

async def send_audio_to_server(websocket, audio_data):
    await websocket.send(audio_data)
    response = await websocket.recv()
    result = json.loads(response)
    print("Server response:", result)  # 打印服务器返回的完整响应
    return result

async def send_text_to_server(websocket, transcript):
    """
    将转录文本发送到服务器并接收大模型的响应。
    :param websocket: WebSocket, 与服务器的连接
    :param transcript: str, 转录文本
    :return: str, 服务器生成的响应文本
    """
    await websocket.send(json.dumps({"transcript": transcript}))
    response = await websocket.recv()
    return json.loads(response).get("response")

async def receive_audio_from_server(websocket, text):
    """
    将文本发送到服务器进行音频合成，并接收生成的音频文件。
    :param websocket: WebSocket, 与服务器的连接
    :param text: str, 需要合成的文本
    :return: None
    """
    await websocket.send(json.dumps({"text": text}))
    audio_data = await websocket.recv()

    with open("output_audio.wav", 'wb') as f:
        f.write(audio_data)
    print("Audio received and saved as output_audio.wav")

async def main():
    uri = "ws://localhost:8765"  # 服务器的 WebSocket 地址

    async with websockets.connect(uri) as websocket:
        while True:
            user_input = input("Press 'r' to record audio or 'q' to quit: ")

            if user_input.lower() == 'r':
                audio_data = await record_audio()

                # 发送音频到服务器并获取情感分析结果
                result = await send_audio_to_server(websocket, audio_data)
                if result:
                    print(f"Detected emotion: {result['emotion']}")
                    print(f"Transcript: {result['transcript']}")

                    # 发送转录文本到服务器并获取生成的响应文本
                    agent_response = await send_text_to_server(websocket, result['transcript'])
                    if agent_response:
                        print(f"Agent Response: {agent_response}")

                        # 发送生成的响应文本到服务器以合成音频
                        await receive_audio_from_server(websocket, agent_response)

            elif user_input.lower() == 'q':
                print("Exiting...")
                break
            else:
                print("Invalid input. Please press 'r' to record or 'q' to quit.")

if __name__ == "__main__":
    asyncio.run(main())