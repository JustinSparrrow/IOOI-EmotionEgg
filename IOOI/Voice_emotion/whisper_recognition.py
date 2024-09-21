import whisper

class WhisperRecognition:
    def __init__(self, model_name="base"):
        """加载 Whisper 模型"""
        self.model = whisper.load_model(model_name)


    def transcribe(self, audio_path):
        """对指定的音频文件进行语音识别并返回识别结果"""
        return self.model.transcribe(audio_path)
