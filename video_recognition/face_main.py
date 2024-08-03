# 人脸情绪识别测试代码
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../emotion')

from face_emotion_recognizer import FaceEmotionRecognizer


def face_module():
    recognizer = FaceEmotionRecognizer()
    recognizer.face_emotion_recognition()


if __name__ == '__main__':
    face_module()
