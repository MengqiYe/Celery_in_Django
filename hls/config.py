import os

NAME_UNKNOWN = 'Unknown'

__RTSP_URL__ = 'rtsp://admin:!!123abc@192.168.1.84:554/ffmpeg/ch1/main/av_stream'

__BLINK_TIME__ = 3

__THRESHOLD__ = 0.4

COMPRESSION_RATIO = 2

PROCESS_EVERYOTHER_FRAME = 4

THREAD_COUNT = 2

CROP_EXPAND = 50

__BASE_DIR__ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"__BASE_DIR__ : {__BASE_DIR__}")