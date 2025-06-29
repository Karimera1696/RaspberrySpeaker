import sounddevice as sd

duration = 1  # 録音時間（秒）

# デフォルト入力デバイスのサンプリングレートを取得
default_input = sd.default.device[0]
if default_input is None:
    raise RuntimeError("デフォルトの入力デバイスが設定されていません")

device_info = sd.query_devices(default_input, "input")
fs = int(device_info["default_samplerate"])

print("録音開始...")
audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
sd.wait()  # 録音終了まで待つ
print("録音終了")

print("shape:", audio.shape)
print("dtype:", audio.dtype)
print("最初の10サンプル:", audio[:10].flatten())
