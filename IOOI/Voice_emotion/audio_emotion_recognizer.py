import argparse
import functools
import time

from mser.predict import MSERPredictor
from mser.utils.utils import add_arguments, print_arguments

from Agents.agents_manager import EmotionAgentsManager
from GPT_SoVITS.inference_cli import speak
from Voice_emotion.whisper_recognition import WhisperRecognition
from Emotion import globals

audio_filename = "Voice_emotion/output/recorded_audio.wav"
transcript_filename = "Voice_emotion/output/transcript.txt"
emotion_filename = "Emotion/global_emotion.txt"
target_file = 'Voice_emotion/output/target.txt'


# 情绪识别类
class EmotionRecognizer:
    def __init__(self, configs='SpeechEmotionRecognition-Pytorch/configs/bi_lstm.yml',
                 use_ms_model='SpeechEmotionRecognition-Pytorch/iic/emotion2vec_plus_base',
                 use_gpu=False,
                 model_path='SpeechEmotionRecognition-Pytorch/models/BiLSTM_Emotion2Vec/best_model/'):
        """
        EmotionRecognizer 类用于处理音频的情感识别

        :param configs: 配置文件路径
        :param use_ms_model: 是否使用ModelScope上的模型
        :param use_gpu: 是否使用GPU
        :param model_path: 模型文件路径
        """
        self.configs = configs
        self.use_ms_model = use_ms_model
        self.model_path = model_path
        self.use_gpu = use_gpu
        self.predictor = MSERPredictor(configs=self.configs,
                                       use_ms_model=self.use_ms_model,
                                       model_path=self.model_path,
                                       use_gpu=self.use_gpu)

    def predict_emotion(self, audio_path):
        """
        使用MSERPredictor进行情感预测
        :param audio_path: 音频文件路径
        :return: 返回预测的标签和得分
        """
        label, score = self.predictor.predict(audio_path)
        return label, score


# 命令行参数解析函数
def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    add_arg = functools.partial(add_arguments, argparser=parser)
    add_arg('configs', str, 'SpeechEmotionRecognition-Pytorch/configs/bi_lstm.yml', '配置文件')
    add_arg('use_ms_model', str, 'SpeechEmotionRecognition-Pytorch/iic/emotion2vec_plus_base', '使用ModelScope上的模型')
    add_arg('use_gpu', bool, False, '是否使用GPU预测')
    add_arg('audio_path', str, 'SpeechEmotionRecognition-Pytorch/dataset/test.wav', '音频路径')
    add_arg('model_path', str, 'SpeechEmotionRecognition-Pytorch/models/BiLSTM_Emotion2Vec/best_model/', '导出的预测模型文件路径')
    args = parser.parse_args()
    print_arguments(args=args)
    return args


# 音频处理函数
def process_audio():
    # 实例化 WhisperRecognition 并进行语音转录
    whisper_recognizer = WhisperRecognition()
    print("Transcribing audio...")
    result = whisper_recognizer.transcribe(audio_filename)  # 转录音频
    print("Transcription completed.")

    # 实例化 EmotionRecognizer 并进行情感识别
    emotion_recognizer = EmotionRecognizer(configs='SpeechEmotionRecognition-Pytorch/configs/bi_lstm.yml',
                                           use_ms_model='SpeechEmotionRecognition-Pytorch/iic/emotion2vec_plus_base',
                                           use_gpu=False,
                                           model_path='SpeechEmotionRecognition-Pytorch/models/BiLSTM_Emotion2Vec/best_model/')
    print("Detecting emotion from audio...")
    detected_emotion, score = emotion_recognizer.predict_emotion(audio_path=audio_filename)
    print(f"Emotion detection completed. Detected emotion: {detected_emotion}, Score: {score}")

    # 组合情绪识别结果与语音转录结果
    complete_message = f"我现在的心情是{detected_emotion}。我想说：{result['text']}。"
    for_logs = f"{time.strftime('%Y-%m-%d %H:%M:%S')} 用户信息：{result['text']} 用户检测到的情绪是：{detected_emotion}，得分：{score}"

    # 更新全局情绪状态
    globals.update_audio_emotion(detected_emotion, emotion_filename)
    globals.update_emotion(detected_emotion, emotion_filename)
    print(f"Updated emotion to {globals.read_audio_emotion(emotion_filename)}")

    # 保存转录结果到文件
    with open(transcript_filename, 'w') as f:
        f.write(complete_message)
    print(f"Transcript saved to {transcript_filename}")

    # 将结果记录到日志文件
    logs_file = "../logs.txt"
    with open(logs_file, 'a') as f:
        f.write(for_logs + '\n')
    print(f"Logs saved to {logs_file}")


def open_agents():
    manager = EmotionAgentsManager()

    with open(transcript_filename, 'r', encoding='utf-8') as f:
        user_input = f.read().strip()

    response = manager.get_response(user_input)[0]

    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(response)
        time.sleep(0.5)

    # 打印响应结果
    print(f"Agent response: {response}")

    speak(target_file)
