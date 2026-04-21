import time
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt

start_time = time.time()

# Загрузка аудиофайла
sample_rate, signal_array = wavfile.read("33.wav")
if len(signal_array.shape) > 1:
    signal_array = signal_array[:, 0]

# Ввод отсчетов
points = int(input("Введите отсчеты: "))
points = min(points, len(signal_array))  # защита от превышения длины

segments = signal_array[:points]

# График отсчетов
plt.figure(figsize=(10, 5))
plt.plot(range(points), segments, '-*')
plt.title("Дискретные отсчеты сигнала")
plt.xlabel("Отсчет")
plt.ylabel("Амплитуда")
plt.grid()
plt.show()

# Осциллограмма
plt.figure(figsize=(10, 5))
plt.plot(np.arange(len(signal_array)) / sample_rate, signal_array)
plt.title("Осциллограмма")
plt.xlabel("Секунды")
plt.ylabel("Амплитуда")
plt.grid()
plt.show()

# Мнимая часть ДПФ
freqs = np.fft.fftfreq(len(signal_array), d=1/sample_rate)

plt.figure(figsize=(10, 5))
plt.plot(freqs, np.imag(np.fft.fft(signal_array)))
plt.title("Мнимая часть ДПФ")
plt.xlabel("Частота")
plt.ylabel("Jm")
plt.grid()
plt.show()

# Гистограмма
plt.figure(figsize=(10, 5))
plt.hist(signal_array, bins=50)
plt.title("Гистограмма")
plt.xlabel("Амплитуда")
plt.ylabel("Отсчет")
plt.grid()
plt.show()

print (time.time() - start_time, "seconds")