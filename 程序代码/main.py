from interface.show_video import monitor_emotion_and_play
from video_recognition.face_main import face_module
from agents.test_agents import test_agents
from voice_interaction.main import main

if __name__ == '__main__':
    monitor_emotion_and_play()
    test_agents()
    face_module()

    main()

