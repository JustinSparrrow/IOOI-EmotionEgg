# /video_emotion/face_emotion_recognizer.py

from deepface import DeepFace

from Emotion import globals

emotion_file = 'emotion/global_emotion.txt'

# Deepface识别情绪
def face_emotion_recognition(image):
    result = DeepFace.analyze(image, actions=['emotion'], enforce_detection=False)
    emotion = None
    if result:
        emotion = result[0]['dominant_emotion']
        globals.update_video_emotion(emotion)
