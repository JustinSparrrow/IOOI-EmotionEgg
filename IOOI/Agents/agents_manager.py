from emotion_agents import AngryAgent, DisgustAgent, FearAgent, HappyAgent, NeutralAgent, SadAgent, SurpriseAgent
import random
import time

# 设置随机种子，使用当前时间
random.seed(time.time())

# 情绪智能体管理类，管理多个情绪智能体
class EmotionAgentsManager:
    def __init__(self):
        """
        初始化情绪智能体管理器，将不同的情绪智能体实例化并存储在一个字典中。
        字典键为情绪名称，值为相应的智能体对象。
        """
        self.agents = {
            "happy": HappyAgent(),        # 快乐智能体
            "sad": SadAgent(),            # 悲伤智能体
            "angry": AngryAgent(),        # 愤怒智能体
            "surprise": SurpriseAgent(),  # 惊讶智能体
            "fear": FearAgent(),          # 害怕智能体
            "disgust": DisgustAgent(),    # 厌恶智能体
            "neutral": NeutralAgent()     # 中立智能体
        }

    def get_response(self, user_input):
        """
        随机选择一个情绪智能体生成响应并返回。

        :param user_input: 用户的输入内容
        :return: 包含智能体生成的响应消息和被选择的智能体对象
        """
        # 随机从字典中选择一个情绪智能体
        agent_key = random.choice(list(self.agents.keys()))
        agent = self.agents[agent_key]

        # 使用选中的智能体生成响应消息
        return [agent.generate_message(user_input), agent]