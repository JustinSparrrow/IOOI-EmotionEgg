@echo off

set PYTHONPATH=%cd%

start python agents/test_agents.py
start python interface/interface.py
start python recognition/audio/audio.py
start python recognition/video/face.py

REM
pause