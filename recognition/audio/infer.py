import argparse
import functools

from mser.predict import MSERPredictor
from mser.utils.utils import add_arguments, print_arguments


class EmotionRecognizer:
    def __init__(self,
                 configs='configs/bi_lstm.yml',
                 use_ms_model='iic/emotion2vec_plus_base',
                 use_gpu=False,
                 model_path='models/BiLSTM_Emotion2Vec/best_model/'):
        self.configs = configs
        self.use_ms_model = use_ms_model
        self.use_gpu = use_gpu
        self.model_path = model_path
        self.predictor = MSERPredictor(configs=self.configs,
                                       use_ms_model=self.use_ms_model,
                                       model_path=self.model_path,
                                       use_gpu=self.use_gpu)

    def predict_emotion(self, audio_path):
        label, score = self.predictor.predict(audio_data=audio_path)
        return label, score


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    add_arg = functools.partial(add_arguments, argparser=parser)
    add_arg('configs', str, 'configs/bi_lstm.yml', '配置文件')
    add_arg('use_ms_model', str, 'iic/emotion2vec_plus_base', '使用ModelScope上公开Emotion2vec的模型')
    add_arg('use_gpu', bool, False, '是否使用GPU预测')
    add_arg('audio_path', str, 'dataset/test.wav', '音频路径')
    add_arg('model_path', str, 'models/BiLSTM_Emotion2Vec/best_model/', '导出的预测模型文件路径')
    args = parser.parse_args()
    print_arguments(args=args)
    return args
