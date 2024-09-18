from voice_interaction.main_agents.emotion_agent import AngryAgent, DisgustAgent, FearAgent, HappyAgent, NeutralAgent, SadAgent, SurpriseAgent
import random
import time

random.seed(time.time())


class EmotionAgentsManager:
    def __init__(self):
        self.agents = {
            "happy": HappyAgent(),
            "sad": SadAgent(),
            "angry": AngryAgent(),
            "surprise": SurpriseAgent(),
            "fear": FearAgent(),
            "disgust": DisgustAgent(),
            "neutral": NeutralAgent()
        }

    def get_response(self, user_input):
        """随机选择一个智能体生成响应"""
        agent_key = random.choice(list(self.agents.keys()))
        agent = self.agents[agent_key]
        return [agent.generate_message(user_input), agent]
