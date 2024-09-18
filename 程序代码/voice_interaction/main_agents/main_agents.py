# 导入必要的库和类
import sys
import os
import time

# 设置路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../emotion')

script_dir = os.path.dirname(os.path.abspath(__file__))
transcript_file = os.path.join(script_dir, "/Users/moqi/Desktop/竞赛/2024创客赛/emotion-egg/Emotion-Egg/voice_interaction/output/transcript.txt")
emotion_file = os.path.join(script_dir, "/Users/moqi/Desktop/竞赛/2024创客赛/emotion-egg/Emotion-Egg/emotion/global_emotion.txt")

from voice_interaction.main_agents.agents_manager import EmotionAgentsManager
from voice_interaction.GPT_SoVITS.inference_cli import speak

target_file = '/Users/moqi/Desktop/竞赛/2024创客赛/emotion-egg/Emotion-Egg/voice_interaction/output/target.txt'

def open_agents():
    # 创建 EmotionAgentsManager 实例
    manager = EmotionAgentsManager()

    # 读取 transcript_file 文件的内容
    with open(transcript_file, 'r', encoding='utf-8') as file:
        user_input = file.read().strip()  # 读取文件内容并去除两端空白字符

    # 使用 manager 获取对应的响应s
    response = manager.get_response(user_input)[0]

    with open(target_file, 'w', encoding='utf-8') as file:
        file.write(response)
        time.sleep(0.5)

    # 打印响应结果
    print(f"Agent response: {response}")

    speak(target_file)

