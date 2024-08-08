import asyncio
import websockets
from voice_interaction.for_server import process_audio
from voice_interaction.main_agents.for_server import process_text
from voice_interaction.GPT_SoVITS.for_server import speak
import json

async def handle_connection(websocket, path):
    """
    处理客户端的WebSocket连接，根据不同的请求类型调用相应的处理函数。
    :param websocket: WebSocket, 与客户端的连接
    :param path: str, WebSocket路径
    :return: None
    """
    async for message in websocket:
        try:
            data = json.loads(message)
            if isinstance(data, dict):
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
                # Assume it's audio data if not JSON
                await process_audio(websocket, message)
        except Exception as e:
            await websocket.send(json.dumps({"error": str(e)}))

start_server = websockets.serve(handle_connection, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()