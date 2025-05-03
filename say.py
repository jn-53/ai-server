import torch
import collections
from TTS.utils.radam import RAdam
import re

def normalize_tts_text(text: str) -> str:
    # 替换全角省略号、多个中文句号或逗号为单句号
    text = re.sub(r'[。]{2,}|[\.]{2,}|…{2,}|[.。…]{2,}', '。', text)
    # 去除末尾多余标点或空格，强制加句号结尾
    text = text.strip()
    if not text.endswith(('。', '.', '?', '？', '!', '！')):
        text += '。'
    return text


# 添加所有需要的类到 PyTorch 安全白名单中
torch.serialization.add_safe_globals({
    RAdam,                      # 自定义优化器
    collections.defaultdict,   # 标准库
    collections.OrderedDict,   # 常用于模型权重结构
    collections.Counter,
    dict                       # 内建类型也要明确声明
})

from TTS.api import TTS
import sounddevice as sd

# 初始化 TTS 模型
tts = TTS(model_name="tts_models/zh-CN/baker/tacotron2-DDC-GST", gpu=False)

def speak(text):
    text = normalize_tts_text(text)
    ref_wav = "reference.wav"  # 一段语速/停顿合适的语音
    wav = tts.tts(text=text, speaker_wav=ref_wav)
    sd.play(wav, samplerate=tts.synthesizer.output_sample_rate)
    sd.wait()

speak("现在模型应该可以顺利加载了。")
speak("真的吗！？我完全不敢相信……太棒了！")
speak("真的吗，我完全不敢相信，太棒了")
speak("测到停顿，开始识别。。。没有识别到有效语音")
speak("你現在才對嘛女性的生殖器也叫騷逼男性的生殖器也叫鸡巴")
