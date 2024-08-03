from main_agents.main_agents import open_agents
from main_function import audio
from interface.show_video import monitor_emotion_and_play


def main():
    while True:
        monitor_emotion_and_play()
        audio()
        open_agents()


if __name__ == '__main__':
    main()
