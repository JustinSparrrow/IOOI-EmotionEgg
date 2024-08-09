import asyncio
import websockets
import pyaudio
import wave
import json


async def record_audio():
    """
    使用系统麦克风录制音频并保存为 WAV 文件。
    :return: str, 录制的音频文件路径
    """
    chunk = 1024  # 每次读取的音频数据块大小
    sample_format = pyaudio.paInt16  # 采样格式
    channels = 1  # 音频通道数量
    fs = 44100  # 采样率
    seconds = 5  # 录音时长
    output_file = "/Users/moqi/Desktop/竞赛/2024创客赛/emotion-egg/Emotion-Egg/voice_interaction/output/recorded_audio.wav"

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

    # 将音频数据保存为 WAV 文件
    wf = wave.open(output_file, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"Finished recording. Audio saved to {output_file}")

    return output_file


async def send_audio_to_server(websocket, audio_file_path):
    with open(audio_file_path, 'rb') as audio_file:
        audio_data = audio_file.read()
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

    if isinstance(audio_data, str):
        # 如果接收到的实际上是错误信息或文本而非二进制数据
        print(f"Server response: {audio_data}")
    else:
        with open("/Users/moqi/Desktop/竞赛/2024创客赛/emotion-egg/Emotion-Egg/voice_interaction/output/output_audio.wav", 'wb') as f:
            f.write(audio_data)
        print("Audio received and saved as output_audio.wav")

        # 播放接收到的音频文件
        play_audio("/Users/moqi/Desktop/竞赛/2024创客赛/emotion-egg/Emotion-Egg/voice_interaction/output/output_audio.wav")


def play_audio(file_path):
    """播放音频文件"""
    wf = wave.open(file_path, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(1024)

    while data:
        stream.write(data)
        data = wf.readframes(1024)

    stream.stop_stream()
    stream.close()
    p.terminate()


async def main():
    uri = "ws://localhost:8765"

    async with websockets.connect(uri) as websocket:
        while True:
            user_input = input("Press 'r' to record audio or 'q' to quit: ")

            if user_input.lower() == 'r':
                audio_file_path = await record_audio()

                result = await send_audio_to_server(websocket, audio_file_path)
                if 'error' in result:
                    print(f"Server error: {result['error']}")
                else:
                    emotion = result.get("emotion", "No emotion detected")
                    transcript = result.get("transcript", "No transcript")
                    print(f"Detected emotion: {emotion}")
                    print(f"Transcript: {transcript}")

                    agent_response = await send_text_to_server(websocket, transcript)
                    if agent_response:
                        print(f"Agent Response: {agent_response}")

                        await receive_audio_from_server(websocket, agent_response)
            elif user_input.lower() == 'q':
                print("Exiting...")
                break
            else:
                print("Invalid input. Please press 'r' to record or 'q' to quit.")


if __name__ == "__main__":
    asyncio.run(main())
