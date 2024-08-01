# audio_handler.py
import pyaudio
import wave


class AudioHandler:
    def __init__(self, rate=16000, channels=1, chunk_size=1024):
        """初始化音频处理器设置采样率、通道数和数据块大小"""
        self.rate = rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.format = pyaudio.paInt16
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.recording = False

    def start_recording(self):
        """开始录音"""
        self.frames = []
        self.stream = self.audio.open(format=self.format, channels=self.channels,
                                      rate=self.rate, input=True,
                                      frames_per_buffer=self.chunk_size)
        self.recording = True
        print("Recording started...")

        while self.recording:
            data = self.stream.read(self.chunk_size)
            self.frames.append(data)

        print("Recording stopped.")
        self.stream.stop_stream()
        self.stream.close()
        return self.frames

    def stop_recording(self):
        """停止录音"""
        self.recording = False

    def save_wave_file(self, filename, frames):
        """保存音频到波形文件"""
        wave_file = wave.open(filename, 'wb')
        wave_file.setnchannels(self.channels)
        wave_file.setsampwidth(self.audio.get_sample_size(self.format))
        wave_file.setframerate(self.rate)
        wave_file.writeframes(b''.join(frames))
        wave_file.close()

    def close(self):
        """关闭音频设备"""
        self.audio.terminate()
