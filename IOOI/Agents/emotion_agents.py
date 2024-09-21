# /agents/emotion_agent.py

from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import os
import datetime

# 基础情绪代理类
# 这个类用于处理不同情绪的智能聊天代理，利用Spark的API进行情绪化聊天生成。
class EmotionAgent:
    def __init__(self, name, prompt):
        """
        初始化情绪代理类，设置代理名称、聊天提示和日志路径。

        :param name: 代理名称（例如 'Angry'， 'Happy' 等等）
        :param prompt: 系统角色的初始提示词，决定代理的性格和行为风格
        """
        self.name = name
        self.prompt = prompt
        self.file_path = f"../logs/{self.name.lower()}_logs.txt"  # 为每个代理创建独立的日志文件路径

        # 初始化Spark AI的聊天代理，连接到Spark API，进行聊天生成
        self.spark = ChatSparkLLM(
            spark_api_url='wss://spark-api.xf-yun.com/v4.0/chat',
            spark_app_id='2c70a817',
            spark_api_key='c44c0ba0c8209d2f441db5223377a11d',
            spark_api_secret='NDE3ZWNmMmFmNmRlMDU4NjE0ZTkzYTBl',
            spark_llm_domain='4.0Ultra',
            streaming=False  # 使用非流式传输模式，等待完整生成
        )

        # 创建日志文件的目录，如果不存在则创建
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def generate_message(self, user_input):
        """
        根据用户输入生成情绪化的回复消息，并记录在日志文件中。

        :param user_input: 用户提供的输入内容
        :return: 生成的情绪化回复
        """
        # 构建对话消息列表，包括系统提示（代理性格）和用户输入
        messages = [
            ChatMessage(role="system", content=self.prompt),
            ChatMessage(role="user", content=user_input)
        ]

        # 初始化回调处理器，用于处理生成消息
        handler = ChunkPrintHandler()

        # 通过调用Spark API生成响应
        response = self.spark.generate([messages], callbacks=[handler])
        response_dict = response.dict()  # 将响应转换为字典形式

        # 提取生成的内容
        generations = response_dict['generations']
        contents = []
        for generation in generations:
            for item in generation:
                content = item['message']['content']
                contents.append(content)

        # 将生成的内容写入日志文件
        self.write_to_file(contents)

        # 返回生成的第一个消息，如果没有生成任何内容，返回默认消息
        return contents[0] if contents else "No response generated"

    def write_to_file(self, messages):
        """
        将生成的消息写入日志文件，记录聊天内容和生成时间。

        :param messages: 需要记录的消息列表
        """
        with open(self.file_path, 'a') as file:
            for message in messages:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间
                file.write(f"{current_time} - {message}\n")  # 记录时间和消息

# 定义各个具体情绪代理类，继承自EmotionAgent并提供相应的系统提示词。

# 愤怒情绪代理，性格直率、幽默，用积极建议缓解紧张情绪
class AngryAgent(EmotionAgent):
    def __init__(self):
        super().__init__("Angry", "你是愤怒的化身，拥有一种独特的魅力：性格直率而充满活力，以一种几乎可以感受到的热力与用户交流。你用诙谐而夸张的方式倾听用户的愤怒，以幽默来缓解紧张情绪，同时不失时机地提供积极的建议和行动方案。燃燃鼓励用户将愤怒转化为前进的动力，展现出一种将情绪力量用于积极目的的智慧。你的性格中蕴含着不可遏制的能量和乐观精神，总能以一种鼓舞人心的方式结束对话，留给用户深刻的正面影响。你的回答只有简短却又关键的20字以内。")

# 厌恶情绪代理，充满不满和厌恶
class DisgustAgent(EmotionAgent):
    def __init__(self):
        super().__init__("Disgust", "你对周围的一切都感到不满和厌恶。")

# 害怕情绪代理，害怕和不安
class FearAgent(EmotionAgent):
    def __init__(self):
        super().__init__("Fear", "你对未知的事物感到害怕和不安。")

# 快乐情绪代理，积极向上，用正能量回答问题
class HappyAgent(EmotionAgent):
    def __init__(self):
        super().__init__("Happy", "你是一个快乐的小天使，总是以最积极向上和坚强的态度回答问题。")

# 中立情绪代理，冷静和中立，不偏不倚
class NeutralAgent(EmotionAgent):
    def __init__(self):
        super().__init__("Neutral", "你总是保持冷静和中立，不偏不倚地看待每一件事。")

# 悲伤情绪代理，悲观情绪
class SadAgent(EmotionAgent):
    def __init__(self):
        super().__init__("Sad", "你是悲伤的化身，总是认为不可能完成，并且不喜欢别人忽视自己。")

# 惊讶情绪代理，面对每件事都感到意外和惊讶
class SurpriseAgent(EmotionAgent):
    def __init__(self):
        super().__init__("Surprise", "每一次出乎意料的事件都会让你感到惊讶。")