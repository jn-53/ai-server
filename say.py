import threading
import queue
import re
from TTS.api import TTS
import sounddevice as sd
import atexit
import torch
import collections
from TTS.utils.radam import RAdam

# 添加所有需要的类到 PyTorch 安全白名单中
torch.serialization.add_safe_globals({
    RAdam,                      # 自定义优化器
    collections.defaultdict,   # 标准库
    collections.OrderedDict,   # 常用于模型权重结构
    collections.Counter,
    dict                       # 内建类型也要明确声明
})
def normalize_tts_text(text: str) -> str:
    # 替换全角省略号、多个中文句号或逗号为单句号
    text = re.sub(r'[。]{2,}|[\.]{2,}|…{2,}|[.。…]{2,}', '。', text)
    # 去除末尾多余标点或空格，强制加句号结尾
    text = text.strip()
    if not text.endswith(('。', '.', '?', '？', '!', '！')):
        text += '。'
    return text

def split_sentences(text: str, max_len: int = 30):
    # 第一步：按最强标点（。！？）切
    primary_sentences = re.split(r'(?<=[。！？])', text)
    results = []

    for primary in primary_sentences:
        primary = primary.strip()
        if not primary:
            continue

        # 第二步：再按分号（；）切
        secondary_sentences = re.split(r'(?<=[；])', primary)
        for secondary in secondary_sentences:
            secondary = secondary.strip()
            if not secondary:
                continue

            # 第三步：再按逗号、顿号（，、）切，但加长度控制合并
            clauses = re.split(r'(?<=[，、])', secondary)
            buffer = ""
            for clause in clauses:
                buffer += clause
                if len(buffer) >= max_len:
                    results.append(buffer.strip())
                    buffer = ""
            if buffer.strip():
                results.append(buffer.strip())

    return results



class TTSPlayer:
    def __init__(self, model_name="tts_models/zh-CN/baker/tacotron2-DDC-GST"):
        self.tts = TTS(model_name=model_name, progress_bar=False, gpu=False)
        self.play_queue = queue.Queue()
        self.play_thread = threading.Thread(target=self._play_worker, daemon=True)
        self.play_thread.start()
        atexit.register(self._shutdown)  # 程序退出时自动清理

    def _play_worker(self):
        while True:
            wav = self.play_queue.get()
            if wav is None:
                break
            sd.play(wav, samplerate=self.tts.synthesizer.output_sample_rate)
            sd.wait()
            self.play_queue.task_done()

    def speak(self, text: str):
        text = normalize_tts_text(text)
        sentences = split_sentences(text)
        for sentence in sentences:
            wav = self.tts.tts(sentence)
            self.play_queue.put(wav)


    def _shutdown(self):
        """退出时自动关闭播放线程"""
        self.play_queue.put(None)
        self.play_thread.join()



# ttsPlayer = TTSPlayer()

# # ttsPlayer.speak("现在模型应该可以顺利加载了。")
# ttsPlayer.speak("真的吗？我完全不敢相信……太棒了！")
# ttsPlayer.speak("真的吗，我完全不敢相信，太棒了")
# # ttsPlayer.speak("测到停顿，开始识别。。。没有识别到有效语音")
# # ttsPlayer.speak("你現在才對嘛女性的生殖器也叫騷逼男性的生殖器也叫鸡巴")
# ttsPlayer.speak("比如骑士式，你坐在床上，我跨坐在你身上，慢慢地上下运动，感受你的每一次深入；或者试试后入式，你从后面抱住我，我感觉到你的每一次冲刺；又或者试试更刺激的对面坐姿，我们面对面，可以亲吻、抚摸，更加亲密。")
