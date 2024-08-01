# interface/emotion_interface.py
import tkinter as tk
from utils import globals


class EmotionInterface:
    def __init__(self, root, emotion_queue):
        self.root = root
        self.emotion_queue = emotion_queue
        self.root.title("Emotion Face")

        # 设置窗体大小为 800x600，并将窗体置于屏幕中央
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 800
        window_height = 600
        position_right = int((screen_width - window_width) / 2)
        position_down = int((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        self.face_canvas = tk.Canvas(self.root, width=800, height=600)
        self.face_canvas.pack()
        self.update_face_canvas()

    def update_face_canvas(self):
        path = "../utils/global_emotion.txt"
        current_emotion = globals.read_global_emotion(path)  # 假设从文件读取情绪

        self.face_canvas.delete("all")  # 清除画布上的所有内容
        width = self.face_canvas.winfo_width()
        height = self.face_canvas.winfo_height()

        # 计算脸部和特征的尺寸和位置
        face_size = min(width, height) * 0.5
        x_center, y_center = width / 2, height / 2
        # 根据情绪调整背景颜色和绘制相应的脸型表情
        if globals.read_global_emotion(path) == "happy":
            self.face_canvas.configure(bg="yellow")
            self.face_canvas.create_oval(x_center - face_size / 2, y_center - face_size / 2, x_center + face_size / 2, y_center + face_size / 2, fill="white")  # 脸
            self.face_canvas.create_arc(x_center - face_size * 0.4, y_center - face_size * 0.1, x_center + face_size * 0.4, y_center + face_size * 0.2, start=0, extent=-180, fill="black")  # 笑脸嘴巴
        elif globals.read_global_emotion(path) == "sad":
            self.face_canvas.configure(bg="blue")
            self.face_canvas.create_oval(x_center - face_size / 2, y_center - face_size / 2, x_center + face_size / 2, y_center + face_size / 2, fill="white")  # 脸
            self.face_canvas.create_arc(x_center - face_size * 0.4, y_center - face_size * 0.1, x_center + face_size * 0.4, y_center + face_size * 0.2, start=0, extent=180, fill="black")  # 哭脸嘴巴
        elif globals.read_global_emotion(path) == "neutral":
            self.face_canvas.configure(bg="grey")
            self.face_canvas.create_oval(x_center - face_size / 2, y_center - face_size / 2, x_center + face_size / 2, y_center + face_size / 2, fill="white")  # 脸
            self.face_canvas.create_line(x_center - face_size * 0.2, y_center + face_size * 0.2,
                                         x_center + face_size * 0.2, y_center + face_size * 0.2, fill="black", width=2)  # 中性嘴巴
        elif globals.read_global_emotion(path) == "angry":
            self.face_canvas.configure(bg="red")
            self.face_canvas.create_oval(x_center - face_size / 2, y_center - face_size / 2, x_center + face_size / 2, y_center + face_size / 2, fill="white")  # 脸
            self.face_canvas.create_arc(x_center - face_size * 0.4, y_center - face_size * 0.1, x_center + face_size * 0.4, y_center + face_size * 0.2, start=0, extent=180, fill="black", style=tk.ARC)  # 生气嘴巴
        elif globals.read_global_emotion(path) == "surprise":
            self.face_canvas.configure(bg="orange")
            self.face_canvas.create_oval(x_center - face_size / 2, y_center - face_size / 2, x_center + face_size / 2, y_center + face_size / 2, fill="white")  # 脸
            self.face_canvas.create_oval(x_center - face_size * 0.1, y_center + face_size * 0.05,
                                         x_center + face_size * 0.1, y_center + face_size * 0.25, fill="black")  # 惊讶嘴巴
        elif globals.read_global_emotion(path) == "fear":
            self.face_canvas.configure(bg="purple")
            self.face_canvas.create_oval(x_center - face_size / 2, y_center - face_size / 2, x_center + face_size / 2, y_center + face_size / 2, fill="white")  # 脸
            self.face_canvas.create_oval(x_center - face_size * 0.4, y_center - face_size * 0.1, x_center + face_size * 0.4, y_center + face_size * 0.2, fill="black")  # 害怕嘴巴
        elif globals.read_global_emotion(path) == "disgust":
            self.face_canvas.configure(bg="green")
            self.face_canvas.create_oval(x_center - face_size / 2, y_center - face_size / 2, x_center + face_size / 2, y_center + face_size / 2, fill="white")  # 脸
            self.face_canvas.create_line(x_center - face_size * 0.3, y_center + face_size * 0.1,
                                         x_center + face_size * 0.3, y_center + face_size * 0.1, fill="black", width=3)  # 厌恶嘴巴
            self.face_canvas.create_line(x_center, y_center + face_size * 0.1,
                                         x_center, y_center + face_size * 0.3, fill="black", width=3)  # 厌恶嘴巴

        eye_size = face_size * 0.1
        # 绘制眼睛
        self.face_canvas.create_oval(x_center - face_size * 0.2, y_center - face_size * 0.1 - eye_size,
                                     x_center - face_size * 0.2 + eye_size, y_center - face_size * 0.1, fill="black")  # 左眼
        self.face_canvas.create_oval(x_center + face_size * 0.2, y_center - face_size * 0.1 - eye_size,
                                     x_center + face_size * 0.2 + eye_size, y_center - face_size * 0.1, fill="black")  # 右眼

        # 每50毫秒检查一次队列
        self.root.after(50, self.update_face_canvas)
