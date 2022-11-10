import wave  # 可读、写wav类型的音频文件。
import requests  # 基于urllib，采⽤Apache2 Licensed开源协议的 HTTP 库。在本项目中用于传递headers和POST请求
import time
import base64  # 讯飞语音要求对本地语音二进制数据进行base64编码
from pyaudio import PyAudio, paInt16  # 音频处理模块，用于将音频流输送到计算机声卡上

framerate = 16000  # 采样率
num_samples = 2000  # 采样点
channels = 1  # 声道
sampwidth = 2  # 采样宽度2bytes
FILEPATH = 'speech.wav'

# 组装url获取token
base_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
APIKey = "aSMKT6Q51f7C1zAHjwATcpp1"
SecretKey = "6fU2m80lc3h8nmGrWd1qA4AHN5w5ubbX"
HOST = base_url % (APIKey, SecretKey)


def getToken(host):
    res = requests.post(host)
    r = res.json()['access_token']
    return r


def save_wave_file(filepath, data):
    wf = wave.open(filepath, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b''.join(data))
    wf.close()


# 录音
def my_record():
    pa = PyAudio()
    # 打开一个新的音频stream
    stream = pa.open(format=paInt16, channels=channels,
                     rate=framerate, input=True, frames_per_buffer=num_samples)
    my_buf = []  # 存放录音数据
    t = time.time()
    print('正在录音...')
    while time.time() < t + 5:  # 设置录音时间（秒）
        # 循环read，每次read 2000frames
        string_audio_data = stream.read(num_samples)
        my_buf.append(string_audio_data)
    print('录音结束.')
    save_wave_file(FILEPATH, my_buf)
    stream.close()


def get_audio(file):
    with open(file, 'rb') as f:
        data = f.read()
    return data


# 传入语音二进制数据，token
# dev_pid为百度语音识别提供的几种语言选择，默认1537为有标点普通话
def speech2text(speech_data, token, dev_pid=1537):
    FORMAT = 'wav'
    RATE = '16000'
    CHANNEL = 1
    CUID = '*******'
    SPEECH = base64.b64encode(speech_data).decode('utf-8')
    data = {
        'format': FORMAT,
        'rate': RATE,
        'channel': CHANNEL,
        'cuid': CUID,
        'len': len(speech_data),
        'speech': SPEECH,
        'token': token,
        'dev_pid': dev_pid
    }
    url = 'https://vop.baidu.com/server_api'  # 短语音识别请求地址
    headers = {'Content-Type': 'application/json'}
    print('正在识别...')
    r = requests.post(url, json=data, headers=headers)
    Result = r.json()
    if 'result' in Result:
        return Result['result'][0]
    else:
        return Result