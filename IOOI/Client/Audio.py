import cv2
import websockets
import asyncio
import pygame
import base64

# Initialize pygame mixer for playing audio
pygame.mixer.init()

# Function to receive and play audio from the server
async def receive_audio(websocket):
    while True:
        audio_data = await websocket.recv()
        audio_file = "received_audio.wav"
        with open(audio_file, "wb") as f:
            f.write(base64.b64decode(audio_data))

        # Play the received audio
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

# Function to receive and play video from the server
async def receive_video(websocket):
    while True:
        video_data = await websocket.recv()
        video_file = "received_video.mp4"
        with open(video_file, "wb") as f:
            f.write(base64.b64decode(video_data))

        # Play the video using OpenCV
        cap = cv2.VideoCapture(video_file)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Received Video", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

# Main function to manage WebSocket connections for audio and video
async def listen_to_server():
    async with websockets.connect("ws://localhost:8000/ws/audio") as audio_ws, \
            websockets.connect("ws://localhost:8000/ws/video") as video_ws:

        # Start audio and video reception concurrently
        await asyncio.gather(receive_audio(audio_ws), receive_video(video_ws))

# Start the WebSocket client
asyncio.run(listen_to_server())