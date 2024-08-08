import json

from audio_handler import AudioHandler
from emotion import globals
from infer import EmotionRecognizer
from whisper_recognition import WhisperRecognition

audio_handler = AudioHandler()

async def process_audio(websocket, audio_data):
    """
    处理音频文件并进行情感识别和转录。
    :param websocket: WebSocket, 与客户端的连接
    :param audio_data: bytes, 传入的音频数据
    :return: dict, 包含转录文本和情感分析结果
    """
    audio_filename = "/Users/moqi/Desktop/竞赛/2024创客赛/emotion-egg/Emotion-Egg/voice_interaction/output/recorded_audio.wav"
    with open(audio_filename, 'wb') as f:
        f.write(audio_data)

    transcript_filename = "/Users/moqi/Desktop/竞赛/2024创客赛/emotion-egg/Emotion-Egg/voice_interaction/output/transcript.txt"
    emotion_filename = "../emotion/global_emotion.txt"

    whisper_recognizer = WhisperRecognition()
    print("Transcribing audio...")
    result = whisper_recognizer.transcribe(audio_filename)
    print("Transcription completed.")

    emotion_recognizer = EmotionRecognizer(configs='configs/bi_lstm.yml',
                                           use_ms_model='iic/emotion2vec_plus_base',
                                           use_gpu=False,
                                           model_path='models/BiLSTM_Emotion2Vec/best_model/')
    print("Detecting emotion from audio...")
    detected_emotion, score = emotion_recognizer.predict_emotion(audio_path=audio_filename)
    print(f"Emotion detection completed. Detected emotion: {detected_emotion}, Score: {score}")

    complete_message = f"我现在的心情是{detected_emotion}。我想说：{result['text']}。"

    globals.update_global_emotion(detected_emotion, emotion_filename)
    print(f"Updated emotion to {globals.read_global_emotion(emotion_filename)}")

    with open(transcript_filename, 'w') as f:
        f.write(complete_message)
    print(f"Transcript saved to {transcript_filename}")

    result_data = {
        "emotion": detected_emotion,
        "score": score
    }

    print("Sending result_data to client:", result_data)  # 添加这行调试信息

    await websocket.send(json.dumps(result_data))