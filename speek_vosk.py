import os
import wave
import json
from vosk import Model, KaldiRecognizer
import pyaudio

def correct_text(text):
    replacements = {
        "都保": "豆宝",
        "都宝": "豆宝",
        "豆宝在吗": "豆宝",
        "都保在吗": "豆宝",
    }
    for wrong, right in replacements.items():
        if wrong in text:
            return right
    return text

def respond(text):
    response = "豆宝在这里！✨"
    os.system(f"say '{response}'")  # 使用 macOS 自带的 say 命令

def continuous_listen_and_respond():
    model = Model("vosk-model-cn-0.22")  # 修改为你的模型路径
    recognizer = KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()

    print("🎤 开始持续监听（按 Ctrl+C 停止）...")

    # 打开麦克风
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=4000)

    while True:
        data = stream.read(4000)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = json.loads(result).get("text", "")
            if text:
                print(f"📝 原始识别结果：{text}")
                
                corrected = correct_text(text)
                print(f"📝 纠正后结果：{corrected}")

                if "豆宝" in corrected:
                    print("🚀 检测到豆宝，开始回应！")
                    respond(corrected)

if __name__ == "__main__":
    continuous_listen_and_respond()
