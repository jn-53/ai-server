import sounddevice as sd
import numpy as np
import queue
import threading
import scipy.io.wavfile
import time
import tempfile
from faster_whisper import WhisperModel

# ========== 参数配置 ==========
SAMPLERATE = 16000
BLOCK_DURATION = 0.4  # 每次录音片段时长（秒）
SILENCE_THRESHOLD = 8000  # 音量低于此值视为静音（视环境调）
SILENCE_BLOCKS = 3        # 连续静音块数后认为“说完话”≈ 1.2s
MAX_SEGMENT_SECONDS = 4   # 最多保留多少秒音频用于识别
INPUT_DEVICE = 1          # 麦克风设备编号

# ========== 加载模型 ==========
print("🔄 正在加载 Whisper-small 模型...")
model = WhisperModel("small", compute_type="int8", cpu_threads=6)
print("✅ 模型加载完成")

# ========== 实时监听逻辑 ==========
q = queue.Queue()
recording = True

def audio_callback(indata, frames, time_info, status):
    if status:
        print("⚠️ 输入状态:", status)
    volume = np.linalg.norm(indata)
    print(f"🎙️ 实时音量: {volume:.2f}")
    q.put(indata.copy())

def record_stream():
    with sd.InputStream(samplerate=SAMPLERATE, channels=1, dtype="int16",
                        blocksize=int(SAMPLERATE * BLOCK_DURATION),
                        callback=audio_callback,
                        device=INPUT_DEVICE):
        print("🎧 开始监听，请说话...")
        audio_buffer = []
        silent_count = 0

        while recording:
            block = q.get()
            volume = np.linalg.norm(block)
            audio_buffer.append(block)

            if volume < SILENCE_THRESHOLD:
                silent_count += 1
            else:
                silent_count = 0

            if silent_count >= SILENCE_BLOCKS and len(audio_buffer) > 3:
                print("🛑 检测到停顿，开始识别...")

                audio = np.concatenate(audio_buffer, axis=0)

                # # ⚡️ 限制最大语段长度（例如最近 4 秒）
                # max_samples = int(SAMPLERATE * MAX_SEGMENT_SECONDS)
                # if len(audio) > max_samples:
                #     audio = audio[-max_samples:]

                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                    scipy.io.wavfile.write(tmp.name, SAMPLERATE, audio)

                    # 🧠 中文 + 静音过滤 + 禁用“脑补”
                    segments, _ = model.transcribe(
                        tmp.name,
                        vad_filter=True,
                        language="zh",
                        beam_size=1
                    )

                    text = "".join([seg.text for seg in segments]).strip()
                    if text:
                        print("🗣️ 你说的是：", text)
                    else:
                        print("🤫 没有识别到有效语音")

                audio_buffer = []
                silent_count = 0

def start_listening():
    thread = threading.Thread(target=record_stream)
    thread.start()

# ========== 启动监听 ==========
try:
    print("🎚️ 当前输入设备：", sd.query_devices(INPUT_DEVICE)["name"])
    start_listening()
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    recording = False
    print("👋 监听结束")
