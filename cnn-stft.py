import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# 加载时序信号（例如音频）
signal, sr = librosa.load('example.wav', sr=None)  # sr: 采样率

# 短时傅里叶变换
stft_result = librosa.stft(signal, n_fft=512, hop_length=256, win_length=512)
spectrogram = np.abs(stft_result)  # 取模

# 转为对数尺度（对数幅度谱，更适合图像模型）
log_spectrogram = librosa.amplitude_to_db(spectrogram)

# 可视化 spectrogram（仅查看）
librosa.display.specshow(log_spectrogram, sr=sr, x_axis='time', y_axis='log')
plt.colorbar()
plt.title("Log Spectrogram")
plt.show()
