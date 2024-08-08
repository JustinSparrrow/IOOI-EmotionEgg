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
    """
    try:
        # 保存音频文件
        audio_filename = "/Users/moqi/Desktop/竞赛/2024创客赛/emotion-egg/Emotion-Egg/voice_interaction/output/recorded_audio.wav"
        with open(audio_filename, 'wb') as f:
            f.write(audio_data)

        # 转录音频
        whisper_recognizer = WhisperRecognition()
        print("Transcribing audio...")
        result = whisper_recognizer.transcribe(audio_filename)
        print("Transcription completed.")

        # 进行情感识别
        emotion_recognizer = EmotionRecognizer(configs='configs/bi_lstm.yml',
                                               use_ms_model='iic/emotion2vec_plus_base',
                                               use_gpu=False,
                                               model_path='models/BiLSTM_Emotion2Vec/best_model/')
        print("Detecting emotion from audio...")
        detected_emotion, score = emotion_recognizer.predict_emotion(audio_path=audio_filename)
        print(f"Emotion detection completed. Detected emotion: {detected_emotion}, Score: {score}")

        # 更新全局情绪状态
        emotion_filename = "../emotion/global_emotion.txt"
        globals.update_global_emotion(detected_emotion, emotion_filename)
        print(f"Updated emotion to {globals.read_global_emotion(emotion_filename)}")

        # 保存转录结果
        complete_message = f"我现在的心情是{detected_emotion}。我想说：{result['text']}。"
        transcript_filename = "/Users/moqi/Desktop/竞赛/2024创客赛/emotion-egg/Emotion-Egg/voice_interaction/output/transcript.txt"
        with open(transcript_filename, 'w') as f:
            f.write(complete_message)
        print(f"Transcript saved to {transcript_filename}")

        # 发送结果到客户端
        result_data = {
            "transcript": complete_message,
            "emotion": detected_emotion,
            "score": score
        }
        print("Sending result_data to client:", result_data)
        await websocket.send(json.dumps(result_data))

    except Exception as e:
        error_message = {"error": str(e)}
        print(f"Error during audio processing: {e}")
        await websocket.send(json.dumps(error_message))