# 导入必要的库和类
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../utils')

import time as t
from gtts import gTTS
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from agents_manager import EmotionAgentsManager

transcript_file = "../transcript.txt"


class TranscriptChangeHandler(FileSystemEventHandler):
    def __init__(self, file_path, callback):
        self.file_path = file_path
        self.callback = callback
        self.last_modified = None

    def on_modified(self, event):
        if event.src_path == self.file_path:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            if content != self.last_modified:
                self.last_modified = content
                self.callback(content)


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

    with open('../transcript.txt', 'r', encoding='utf-8') as file:
        user_input = file.read().strip()  # 读取文件内容并去除两端空白字符

    # 使用 manager 获取对应的响应
    response = manager.get_response(user_input)[0]
    emotion_agent = manager.get_response(user_input)[1]

    # 打印响应结果
    print(f"{emotion_agent} response: {response}")

    # 使用 gtts 朗读响应
    speak(response)


def monitor_file(file_path, callback):
    event_handler = TranscriptChangeHandler(file_path, callback)
    observer = Observer()
    observer.schedule(event_handler, file_path, recursive=True)
    observer.start()
    print(f"Started monitoring {file_path}")

    try:
        callback()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


# 当脚本直接运行时执行测试函数
if __name__ == '__main__':
    monitor_file(transcript_file, test_agents)
# print(sys.path)
# print(os.path.dirname(os.path.realpath(__file__)))