import asyncio
import websockets
import json
from voice_interaction.for_server import process_audio
from voice_interaction.main_agents.for_server import process_text
from voice_interaction.GPT_SoVITS.for_server import speak

async def handle_connection(websocket, path):
    """
    处理客户端的 WebSocket 连接，根据不同的请求类型调用相应的处理函数。
    :param websocket: WebSocket, 与客户端的连接
    :param path: str, WebSocket 路径
    :return: None
    """
    async for message in websocket:
        try:
            # 判断消息是否为 JSON 格式
            try:
                data = json.loads(message)
            except (json.JSONDecodeError, UnicodeDecodeError):
                data = None

            if data:
                # 处理文本请求
                if "transcript" in data:
                    await process_text(websocket, data["transcript"])
                elif "text" in data:
                    audio_file_path = await speak(data["text"])
                    # 发送生成的音频文件给客户端
                    with open(audio_file_path, 'rb') as audio_file:
                        await websocket.send(audio_file.read())
                else:
                    await websocket.send(json.dumps({"error": "Invalid message format."}))
            else:
                # 如果数据不是 JSON 格式，假定它是二进制音频数据
                await process_audio(websocket, message)

        except Exception as e:
            # 捕获并返回任何异常
            error_message = {"error": str(e)}
            await websocket.send(json.dumps(error_message))

# 启动 WebSocket 服务器
start_server = websockets.serve(handle_connection, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()