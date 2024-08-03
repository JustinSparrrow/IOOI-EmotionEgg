# 导入必要的库和类
import sys
import os
from gtts import gTTS

# 设置路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../emotion')

from agents.agents_manager import EmotionAgentsManager

# 文件路径
transcript_file = "../../../transcript.txt"
emotion_file = "../../../emotion/emotion.txt"


def speak(text):
    """ 使用 gtts 将文本转换为语音并播放 """
    tts = gTTS(text=text, lang='zh-cn')  # 使用中文语音
    temp_file = "temp_speech.mp3"
    tts.save(temp_file)
    # 播放音频文件，确保系统支持对应的播放命令
    os.system(f"start {temp_file}" if os.name == 'nt' else f"mpg123 {temp_file}")


def test_agents():
    # 创建 EmotionAgentsManager 实例
    manager = EmotionAgentsManager()

    # 读取 transcript_file 文件的内容
    with open(transcript_file, 'r', encoding='utf-8') as file:
        user_input = file.read().strip()  # 读取文件内容并去除两端空白字符

    # 使用 manager 获取对应的响应
    response = manager.get_response(user_input)

    # 打印响应结果
    print(f"Agent response: {response}")

    # 使用 gtts 朗读响应
    speak(response)


# 当脚本直接运行时执行测试函数
if __name__ == '__main__':
    test_agents()
