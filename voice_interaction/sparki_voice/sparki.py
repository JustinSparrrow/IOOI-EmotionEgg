#!/usr/bin/env python3
# -*-coding:utf-8 -*-
import ssl
import _thread as thread

import jsonpath
import websocket
from pydub import AudioSegment

from sample import ne_utils, aipass_client
from data import *


# 收到websocket连接建立的处理
def on_open(ws):
    def run():
        # # 清除文件
        # ne_utils.del_file('/Users/moqi/Desktop/竞赛/2024创客赛/emotion-egg/Emotion-Egg/voice_interaction/output')
        # 判断是否是多模请求
        exist_audio = jsonpath.jsonpath(request_data, "$.payload.*.audio")
        exist_video = jsonpath.jsonpath(request_data, "$.payload.*.video")
        multi_mode = True if exist_audio and exist_video else False

        # 获取frame，用于设置发送数据的频率
        frame_rate = None
        if jsonpath.jsonpath(request_data, "$.payload.*.frame_rate"):
            frame_rate = jsonpath.jsonpath(request_data, "$.payload.*.frame_rate")[0]
        time_interval = 40
        if frame_rate:
            time_interval = round((1 / frame_rate) * 1000)

        # 获取待发送的数据
        media_path2data = aipass_client.prepare_req_data(request_data)
        # 发送数据
        aipass_client.send_ws_stream(ws, request_data, media_path2data, multi_mode, time_interval)

    thread.start_new_thread(run, ())


# 收到websocket消息的处理
audio_generated = False  # 全局标志位


def on_message(ws, message):
    global audio_generated
    status = jsonpath.jsonpath(message, "$.header.status")
    if status and status[0] == 2 and not audio_generated:
        # 检查是否有音频数据返回并保存
        audio_data = jsonpath.jsonpath(message, "$.payload.audio.audio")
        if audio_data:
            lame_path = "/Users/moqi/Downloads/超拟人req_demo_python/resource/output/audio.lame"
            wav_path = "/Users/moqi/Downloads/超拟人req_demo_python/resource/output/audio.wav"

            # 使用 pydub 将 LAME 转换为 WAV
            audio = AudioSegment.from_file(lame_path, format="mp3")
            audio.export(wav_path, format="wav")
            print(f"音频已保存为 WAV 格式: {wav_path}")
            audio_generated = True  # 设置标志位，避免重复生成


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws, close_status_code, close_msg):
    print("### 执行结束，连接自动关闭 ###")
    print(f"状态码: {close_status_code}, 消息: {close_msg}")


def speak():
    # 程序启动的时候设置APPID
    request_data['header']['app_id'] = APPId
    auth_request_url = ne_utils.build_auth_request_url(request_url, "GET", APIKey, APISecret)
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(auth_request_url, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
