import pyaudio
import wave

# 初始化录音参数
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "record.wav"

# 创建PyAudio对象
audio = pyaudio.PyAudio()

# 打开音频流
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

print("开始录音...")

# 录音缓存区
frames = []

# 录音
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("录音结束！")

# 关闭音频流和PyAudio
stream.stop_stream()
stream.close()
audio.terminate()

# 将录音数据保存到文件中
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print("录音文件已保存为: " + WAVE_OUTPUT_FILENAME)
