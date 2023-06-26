import numpy as np
import matplotlib.pyplot as plt

def minimize_offset(wave1, wave2):
    # Extract time and waveform from input arrays
    t1, waveform1 = wave1
    t2, waveform2 = wave2
    
    # Compute the cross-correlation between the two waveforms
    cross_correlation = np.correlate(waveform1, waveform2, mode='full')
    print(f'{cross_correlation=}')
    
    # Find the index of the maximum cross-correlation
    max_index = np.argmax(cross_correlation)
    print(f'{max_index=}')
    
    # Calculate the time offset
    offset = t2[0] - t1[max_index]
    print(f'{offset=}')
    
    # Shift the second waveform by the calculated offset
    shifted_wave2 = np.vstack((t2 - offset, waveform2))
    print(f'{shifted_wave2[0, 0]=}')
    
    return shifted_wave2

# Parameters
offset = 0
amplitude_ratio = 1
frequency = 2
sr1 = 500
sr2 = sr1 * 0.1
duration = 1
noise_amplitude = 0  # Amplitude of the noise

# Example waves
t1 = np.linspace(0, duration, int(sr1 * duration))
t2 = np.linspace(0, duration, int(sr2 * duration))

# Generate the sine waves
wave1 = np.sin(2 * np.pi * frequency * t1)
wave2 = amplitude_ratio * np.sin(2 * np.pi * frequency * t2)
t2 += offset

# Create arrays with time and waveform
wave1 = np.vstack((t1, wave1))
wave2 = np.vstack((t2, wave2))

# Minimize the offset between the waves
aligned_wave2 = minimize_offset(wave1, wave2)

# Plotting the original waves and the aligned wave
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(wave1[0], wave1[1], label='Wave 1')
plt.plot(wave2[0], wave2[1], label='Wave 2')
plt.title('Original Waves')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(wave1[0], wave1[1], label='Wave 1')
plt.plot(aligned_wave2[0], aligned_wave2[1], label='Aligned Wave 2')
plt.title('Aligned Waves')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()

plt.tight_layout()
plt.show()