#!/bin/bash

# shellcheck disable=SC2155
export PYTHONPATH=$(pwd)

python agents/test_agents.py & python interface/interface_main.py & python recognition/audio/audio_main.py & python recognition/video/face_main.py

wait

#chmod +x for_unix.sh
#./for_unix.sh