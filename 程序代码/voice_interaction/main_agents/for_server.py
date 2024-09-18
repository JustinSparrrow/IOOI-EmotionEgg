import json
import time

from voice_interaction.main_agents.agents_manager import EmotionAgentsManager

target_file = '/Users/moqi/Desktop/竞赛/2024创客赛/emotion-egg/Emotion-Egg/voice_interaction/output/target.txt'


async def process_text(websocket, transcript):
    """
    根据用户的转录文本生成相应的回应。
    :param websocket: WebSocket, 与客户端的连接
    :param transcript: str, 用户的转录文本
    :return: str, 代理生成的回应
    """
    manager = EmotionAgentsManager()

    response = manager.get_response(transcript)[0]

    with open(target_file, 'w', encoding='utf-8') as file:
        file.write(response)
        time.sleep(0.5)

    print(f"Agent response: {response}")

    result_data = {"response": response}
    await websocket.send(json.dumps(result_data))
