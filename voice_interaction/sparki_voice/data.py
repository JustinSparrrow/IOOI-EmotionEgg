APPId = "2c70a817"
APIKey = "c44c0ba0c8209d2f441db5223377a11d"
APISecret = "NDE3ZWNmMmFmNmRlMDU4NjE0ZTkzYTBl"

# 请求数据
request_data = {
    "header": {
        "app_id": "123",
        "status":0
    },
    "parameter": {
        "oral": {
            "oral_level": "high"
        },
        "tts": {
            "vcn": "x4_lingxiaoxuan_oral",
            "volume": 50,
            "speed": 50,
            "pitch": 50,
            "bgs": 0,
            "rhy": 0,
            "audio": {
                "encoding": "lame",
                "sample_rate": 16000,
                "channels": 1,
                "bit_depth": 16,
                "frame_size": 0
            },
            "pybuf": {
                "encoding": "utf8",
                "compress": "raw",
                "format": "plain"
            }
        }
    },
    "payload": {
        "text": {
            "encoding": "utf8",
            "compress": "raw",
            "format": "plain",
            "status": 2,
            "seq": 0,
            "text": "/Users/moqi/Desktop/竞赛/2024创客赛/emotion-egg/Emotion-Egg/voice_interaction/output/target.txt"
        }, 
        "user_text": {
            "encoding": "utf8",
            "compress": "raw",
            "format": "plain",
            "status": 2,
            "seq": 0,
            "text": "/Users/moqi/Desktop/竞赛/2024创客赛/emotion-egg/Emotion-Egg/voice_interaction/output/target.txt"
        }
    }
}

# 请求地址
request_url = "ws://cbm01.cn-huabei-1.xf-yun.com/v1/private/medd90fec"

# 用于快速定位响应值

response_path_list = ['$..payload.pybuf', '$..payload.audio', ]