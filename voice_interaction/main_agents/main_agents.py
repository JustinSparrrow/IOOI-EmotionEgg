# 导入必要的库和类
import sys
import os
import time

from gtts import gTTS

# 设置路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../../emotion')

script_dir = os.path.dirname(os.path.abspath(__file__))
transcript_file = os.path.join(script_dir, "/Users/moqi/Desktop/竞赛/2024创客赛/emotion-egg/Emotion-Egg/voice_interaction/output/transcript.txt")
emotion_file = os.path.join(script_dir, "/Users/moqi/Desktop/竞赛/2024创客赛/emotion-egg/Emotion-Egg/emotion/global_emotion.txt")

from voice_interaction.main_agents.agents_manager import EmotionAgentsManager
from voice_interaction.GPT_SoVITS.inference_cli import speak


# def speak(text):
#     """ 使用 gtts 将文本转换为语音并播放 """
#     if isinstance(text, list):
#         text = ' '.join(str(item) for item in text)  # 将列表中的每个元素都转换为字符串并连接起来
#
#     tts = gTTS(text=text, lang='zh-cn')  # 使用中文语音
#     temp_file = "temp_speech.mp3"
#     tts.save(temp_file)
#     # 播放音频文件，确保系统支持对应的播放命令
#     os.system(f"start {temp_file}" if os.name == 'nt' else f"mpg123 {temp_file}")


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

