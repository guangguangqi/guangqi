import pywt
import numpy as np
import matplotlib.pyplot as plt

# 假设 signal 是一维时序信号
signal = np.sin(np.linspace(0, 10 * np.pi, 1024)) + 0.5 * np.random.randn(1024)

# 连续小波变换（CWT）
scales = np.arange(1, 128)  # 尺度越大 => 分析低频
coefficients, frequencies = pywt.cwt(signal, scales, 'morl')

# 可视化 CWT 结果（时间-频率图）
plt.imshow(np.abs(coefficients), extent=[0, 1, 1, 128], cmap='viridis', aspect='auto',
           vmax=np.abs(coefficients).max(), vmin=0)
plt.gca().invert_yaxis()
plt.title("CWT Spectrogram")
plt.ylabel('Scale')
plt.xlabel('Time')
plt.colorbar()
plt.show()
