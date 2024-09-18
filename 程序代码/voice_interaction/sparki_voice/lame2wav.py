import time
from pydub import AudioSegment
from sparki import speak
from pydub.playback import play

start_time = time.time()  # 开始计时

speak()

# 加载 LAME 编码的音频文件
audio = AudioSegment.from_file("/Users/moqi/Desktop/竞赛/2024创客赛/emotion-egg/Emotion-Egg/voice_interaction/sparki_voice/resource/output/audio.lame", format="mp3")

# 导出为 WAV 格式
audio.export("/Users/moqi/Desktop/竞赛/2024创客赛/emotion-egg/Emotion-Egg/voice_interaction/sparki_voice/resource/output/audio.wav", format="wav")

print('done')
end_time = time.time()  # 结束计时
execution_time = end_time - start_time  # 计算执行时间

print(f"执行时间: {execution_time:.2f} 秒")

# 播放音频
play(audio)