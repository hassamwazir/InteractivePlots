import numpy as np
import matplotlib.pyplot as plt
from fastdtw import fastdtw

def resize_waveform(waveform, size):
    t = np.linspace(0, 1, size)
    resized_waveform = np.interp(t, np.linspace(0, 1, len(waveform)), waveform)
    return resized_waveform

# Parameters
offset = 0.2
amplitude_ratio = 1
frequency = 2
sr1 = 500
sr2 = sr1 * 0.1
duration = 1
noise_amplitude = 0  # Amplitude of the noise

# Example waves
t1 = np.linspace(0, duration, int(sr1 * duration))
t2 = np.linspace(0, duration*2, int(sr2 * duration))

# Generate the sine waves
wave1 = np.sin(2 * np.pi * frequency * t1)
wave2 = amplitude_ratio * np.sin(2 * np.pi * frequency / 2 * t2)
t2 += offset

# Perform Dynamic Time Warping (DTW)
distance, path = fastdtw(wave1, wave2)

# Find the indices for resizing wave2
start_index = path[0][1]
end_index = path[-1][1] + 1  # Add 1 to include the end index

# Resize wave2 using the alignment indices
resized_wave2 = resize_waveform(wave2[start_index:end_index], len(wave1))

# Plotting the original waves and the resized wave
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(t1, wave1, label='Wave 1')
plt.plot(t2, wave2, label='Wave 2')
plt.title('Original Waves')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(t1, wave1, label='Wave 1')
plt.plot(t1, resized_wave2, label='Resized Wave 2')
plt.title('Resized Wave 2')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()

plt.tight_layout()
plt.show()
