import os

# 定义情绪文件的路径，默认保存情绪数据的文件
EMOTION_FILE_PATH = "path_to_emotion_file.txt"

# 定义情绪在文件中的行号
VIDEO_EMOTION_LINE = 0  # 视频情绪位于文件的第1行
AUDIO_EMOTION_LINE = 1  # 音频情绪位于文件的第2行
WEIGHTED_EMOTION_LINE = 2  # 加权情绪位于文件的第3行

# 更新特定行的情绪值到文件中
def update_emotion(emotion, line_number, path):
    """
    更新指定行的情绪值并写入文件。

    :param emotion: 要更新的情绪字符串
    :param line_number: 文件中的行号，表示要更新哪一行
    :param path: 文件路径
    """
    abs_path = os.path.abspath(path)  # 获取文件的绝对路径
    lines = read_all_lines(path)  # 读取文件中的所有行

    # 确保文件的行数足够，如果行数不足，填充空行
    if len(lines) <= line_number:
        lines.extend([''] * (line_number - len(lines) + 1))

    # 更新指定行的内容
    lines[line_number] = emotion

    # 将更新后的行写回文件
    with open(abs_path, 'w') as f:
        f.writelines("\n".join(lines) + "\n")  # 保证文件以换行符结束

# 方便的函数，分别更新视频、音频和加权情绪
def update_video_emotion(emotion, path=EMOTION_FILE_PATH):
    """
    更新视频情绪。

    :param emotion: 要更新的视频情绪
    :param path: 文件路径
    """
    update_emotion(emotion, VIDEO_EMOTION_LINE, path)

def update_audio_emotion(emotion, path=EMOTION_FILE_PATH):
    """
    更新音频情绪。

    :param emotion: 要更新的音频情绪
    :param path: 文件路径
    """
    update_emotion(emotion, AUDIO_EMOTION_LINE, path)

def update_weighted_emotion(emotion, path=EMOTION_FILE_PATH):
    """
    更新加权情绪。

    :param emotion: 要更新的加权情绪
    :param path: 文件路径
    """
    update_emotion(emotion, WEIGHTED_EMOTION_LINE, path)

# 读取特定行的情绪值
def read_emotion(line_number, path):
    """
    从文件中读取指定行的情绪值。

    :param line_number: 要读取的行号
    :param path: 文件路径
    :return: 该行的情绪值字符串，若不存在则返回 "neutral"
    """
    abs_path = os.path.abspath(path)  # 获取文件的绝对路径
    lines = read_all_lines(path)  # 读取文件的所有行

    # 如果行号合法，返回对应行的情绪值
    if line_number < len(lines):
        return lines[line_number].strip()
    else:
        return "neutral"  # 如果文件没有该行，返回默认情绪 "neutral"

# 方便的函数，分别读取视频、音频和加权情绪
def read_video_emotion(path=EMOTION_FILE_PATH):
    """
    读取视频情绪。

    :param path: 文件路径
    :return: 视频情绪字符串
    """
    return read_emotion(VIDEO_EMOTION_LINE, path)

def read_audio_emotion(path=EMOTION_FILE_PATH):
    """
    读取音频情绪。

    :param path: 文件路径
    :return: 音频情绪字符串
    """
    return read_emotion(AUDIO_EMOTION_LINE, path)

def read_weighted_emotion(path=EMOTION_FILE_PATH):
    """
    读取加权情绪。

    :param path: 文件路径
    :return: 加权情绪字符串
    """
    return read_emotion(WEIGHTED_EMOTION_LINE, path)

# 读取整个文件并返回每一行组成的列表
def read_all_lines(path):
    """
    读取文件的所有行，并返回一个包含每行文本的列表。

    :param path: 文件路径
    :return: 包含文件每行文本的列表，若文件不存在则返回空列表
    """
    abs_path = os.path.abspath(path)  # 获取文件的绝对路径

    # 检查文件是否存在，若不存在则返回空列表
    if not os.path.exists(abs_path):
        return []

    # 打开文件并读取所有行
    with open(abs_path, 'r') as f:
        return f.readlines()