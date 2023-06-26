import numpy as np
import matplotlib.pyplot as plt
from Utils import resample_sine_waves, minimize_offset

# Parameters
offset = 2.5
amplitude_ratio = 1
frequency = 2
sr1 = 100
sr2 = sr1 * 0.5
duration = 1
noise_amplitude = 0.1  # Amplitude of the noise



# Generate time axis
t1 = np.linspace(0, duration, int(sr1 * duration))
t2 = np.linspace(0, duration, int(sr2 * duration))

# Generate the sine waves
sine_wave1 = np.sin(2 * np.pi * frequency * t1)
sine_wave2 = amplitude_ratio * np.sin(2 * np.pi * frequency * t2)
t2 += offset

# create an np array with two rows, for sine wave and time
sine_wave1 = np.vstack((t1, sine_wave1)).T
sine_wave2 = np.vstack((t2, sine_wave2)).T

# Add noise
noise1 = np.random.uniform(-noise_amplitude, noise_amplitude, len(t1))
noise2 = np.random.uniform(-noise_amplitude, noise_amplitude, len(t2))
sine_wave1[:, 1] += noise1
sine_wave2[:, 1] += noise2

# Resample the sine waves
# num_samples = min(len(t1), len(t2))
resampled_wave1, resampled_wave2 = resample_sine_waves(sine_wave1, sine_wave2, sampling='average')


# Minimize the offset between the waves
aligned_wave2 = minimize_offset(resampled_wave1, resampled_wave2)
print(f'{aligned_wave2.shape=}')

# plot two scatter plots in subfigures in 2 rows
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 5))
ax1.scatter(sine_wave1[:, 0], sine_wave1[:, 1], c='blue', label='Sine Wave 1')
ax1.scatter(sine_wave2[:, 0], sine_wave2[:, 1], c='red', label='Sine Wave 2')
ax1.set_xlabel('Time', fontweight='bold')
ax1.set_ylabel('Amplitude', fontweight='bold')
ax1.set_title('Original Sine Waves', fontweight='bold')
ax1.legend()

ax2.scatter(resampled_wave1[:,0], resampled_wave1[:, 1], c='blue', label='(Resampled) Sine Wave 1')
ax2.scatter(resampled_wave2[:,0], resampled_wave2[:, 1], c='red', label='(Resampled)Sine Wave 2')
ax2.set_xlabel('Time', fontweight='bold')
ax2.set_ylabel('Amplitude', fontweight='bold')
# make title bold
ax2.set_title('Resampled Sine Waves', fontweight='bold')
ax2.legend()

# plot resaples wave 1 with aligned wave 2
ax3.scatter(resampled_wave1[:,0], resampled_wave1[:, 1], c='blue', label='(Resampled) Sine Wave 1')
ax3.scatter(aligned_wave2[:,0], aligned_wave2[:, 1], c='red', label='Aligned Sine Wave 2')
ax3.set_xlabel('Time')
ax3.set_ylabel('Amplitude')
ax3.set_title('Aligned Sine Waves')
ax3.legend()
# make it full screen
mng = plt.get_current_fig_manager()
mng.window.state('zoomed')
plt.tight_layout()
plt.show()


plt.show()


