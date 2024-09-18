import os


# 更新全局情绪变量到文件
def update_global_emotion(emotion, path):
    abs_path = os.path.abspath(path)
    with open(abs_path, "w") as file:
        file.write(emotion)


# 从文件读取全局情绪变量
def read_global_emotion(path):
    abs_path = os.path.abspath(path)
    try:
        with open(abs_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "neutral"
