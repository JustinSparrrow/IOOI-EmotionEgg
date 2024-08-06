# /agents/emotion_agent.py
import time

from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import os
import datetime


class EmotionAgent:
    def __init__(self, name, prompt):
        self.name = name
        self.prompt = prompt
        self.file_path = f"../logs/{self.name.lower()}_logs.txt"  # 创建一个日志文件路径
        self.spark = ChatSparkLLM(
            spark_api_url='wss://spark-api.xf-yun.com/v4.0/chat',
            spark_app_id='2c70a817',
            spark_api_key='c44c0ba0c8209d2f441db5223377a11d',
            spark_api_secret='NDE3ZWNmMmFmNmRlMDU4NjE0ZTkzYTBl',
            spark_llm_domain='4.0Ultra',
            streaming=False
        )
        # 确保日志目录存在
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def generate_message(self, user_input):
        messages = [
            ChatMessage(role="system", content=self.prompt),
            ChatMessage(role="user", content=user_input)
        ]
        handler = ChunkPrintHandler()
        response = self.spark.generate([messages], callbacks=[handler])
        response_dict = response.dict()
        generations = response_dict['generations']
        contents = []
        for generation in generations:
            for item in generation:
                content = item['message']['content']
                contents.append(content)
        # 将生成的内容写入文件
        self.write_to_file(contents)
        return contents[0] if contents else "No response generated"

    def write_to_file(self, messages):
        with open(self.file_path, 'a') as file:
            for message in messages:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"{current_time} - {message}\n")


# 各个具体情绪代理的定义
class AngryAgent(EmotionAgent):
    def __init__(self):
        super().__init__("Angry", "你是愤怒的化身，拥有一种独特的魅力：性格直率而充满活力，以一种几乎可以感受到的热力与用户交流。你用诙谐而夸张的方式倾听用户的愤怒，以幽默来缓解紧张情绪，同时不失时机地提供积极的建议和行动方案。燃燃鼓励用户将愤怒转化为前进的动力，展现出一种将情绪力量用于积极目的的智慧。你的性格中蕴含着不可遏制的能量和乐观精神，总能以一种鼓舞人心的方式结束对话，留给用户深刻的正面影响。你的回答只有简短却又关键的20字以内。")


class DisgustAgent(EmotionAgent):
    def __init__(self):
        super().__init__("Disgust", "你对周围的一切都感到不满和厌恶。")


class FearAgent(EmotionAgent):
    def __init__(self):
        super().__init__("Fear", "你对未知的事物感到害怕和不安。")


class HappyAgent(EmotionAgent):
    def __init__(self):
        super().__init__("Happy", "你是一个快乐的小天使，总是以最积极向上和坚强的态度回答问题。")


class NeutralAgent(EmotionAgent):
    def __init__(self):
        super().__init__("Neutral", "你总是保持冷静和中立，不偏不倚地看待每一件事。")


class SadAgent(EmotionAgent):
    def __init__(self):
        super().__init__("Sad", "你是悲伤的化身，总是认为不可能完成，并且不喜欢别人忽视自己。")


class SurpriseAgent(EmotionAgent):
    def __init__(self):
        super().__init__("Surprise", "每一次出乎意料的事件都会让你感到惊讶。")
