import os
from datetime import datetime

# 定义存储音频文件的目录
AUDIO_FILE_PATH = "Voice_emotion/output/recorded_audio.wav"

# 如果存储目录不存在，则创建它
AUDIO_SAVE_DIR = os.path.dirname(AUDIO_FILE_PATH)
if not os.path.exists(AUDIO_SAVE_DIR):
    os.makedirs(AUDIO_SAVE_DIR)

# 用于保存音频数据到固定文件
def save_audio_to_file(audio_data):
    with open(AUDIO_FILE_PATH, 'wb') as f:
        f.write(audio_data)
    return AUDIO_FILE_PATH