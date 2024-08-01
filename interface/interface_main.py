import sys
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../utils')

from utils.globals import read_global_emotion
import time
import threading
from queue import Queue
import tkinter as tk
from interface.emotion_interface import EmotionInterface


def monitor_emotion_changes(emotion_queue):
    previous_emotion = None
    while True:
        path = "../utils/global_emotion.txt"
        current_emotion = read_global_emotion(path)
        if current_emotion != previous_emotion:
            print(f"Global emotion changed to: {current_emotion}")
            previous_emotion = current_emotion
        time.sleep(2)  # 每2秒检查一次情绪变化


def open_agents():
    root = tk.Tk()
    emotion_queue = Queue()
    app = EmotionInterface(root, emotion_queue)

    # Start a thread to monitor global emotion changes
    thread = threading.Thread(target=monitor_emotion_changes, args=(emotion_queue,))
    thread.daemon = True
    thread.start()

    # Start the tkinter main loop
    root.mainloop()


if __name__ == "__main__":
    open_agents()
