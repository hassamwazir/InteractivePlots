import numpy as np
from scipy.interpolate import interp1d


def resample_sine_waves(sine_wave1, sine_wave2, sampling = 'downsample'):
    """
    Resamples two sine waves to the same sampling rate.
    :param sine_wave1: np array with two columns, first column is time, second column is amplitude
    :param sine_wave2: np array with two columns, first column is time, second column is amplitude
    :param sampling: 'downsample', 'upsample', or 'average'
    :return: resampled_wave1, resampled_wave2
    """

    # Check that the input is valid
    if sine_wave1.shape[1] != 2 or sine_wave2.shape[1] != 2:
        raise ValueError('Input arrays must have two columns')
    
    if sampling not in ['downsample', 'upsample', 'average']:
        raise ValueError('Invalid sampling method')

    # Generate time axis for original waves
    time1 = sine_wave1[:, 0]
    time2 = sine_wave2[:, 0]
    # time1 = sine_wave1[:, 0] - sine_wave1[0, 0]
    # time2 = sine_wave2[:, 0] - sine_wave2[0, 0]

    offset = 0

    # Determine number of samples for resampled waves
    if len(time1) >= len(time2):
        if sampling == 'downsample':
            # last_sample = time2[-1]
            num_samples = len(time2)
        elif sampling == 'upsample':
            # last_sample = time1[-1]
            num_samples = len(time1)
        elif sampling == 'average':
            # last_sample = time2[-1]
            num_samples = len(time2) + len(time1) // 2
        else:
            raise ValueError('Invalid sampling method')
    else:
        if sampling == 'downsample':
            # last_sample = time1[-1]
            num_samples = len(time1)
        elif sampling == 'upsample':
            # last_sample = time2[-1]
            num_samples = len(time2)
        elif sampling == 'average':
            #
            num_samples = len(time2) + len(time1) // 2

    # print(f'{len(time1)=}, {len(time2)=}, {last_sample=}, {time1[-1]}, {time2[-1]}')

    # Generate time axis for resampled waves
    t1_resampled = np.linspace(min(time1), max(time1), num_samples)
    t2_resampled = np.linspace(min(time2), max(time2), num_samples)
    print(f'{t1_resampled.shape=}')

    # Interpolate original waves to obtain resampled waves
    interpolator1 = interp1d(time1, sine_wave1[:, 1], fill_value="extrapolate")
    interpolator2 = interp1d(time2, sine_wave2[:, 1], fill_value="extrapolate")
    resampled_wave1 = interpolator1(t1_resampled)
    resampled_wave2 = interpolator2(t2_resampled)
    resampled_wave1 = np.vstack((t1_resampled, resampled_wave1)).T
    resampled_wave2 = np.vstack((t2_resampled, resampled_wave2)).T

    return resampled_wave1, resampled_wave2



def minimize_offset(wave1, wave2):
    """
    Minimizes the offset between two sine waves by shifting the second wave.
    :param wave1: np array with two columns, first column is time, second column is amplitude
    :param wave2: np array with two columns, first column is time, second column is amplitude
    :return: shifted_wave2
    """

    # Extract time and waveform from input arrays
    t1, waveform1 = wave1[:, 0], wave1[:, 1]
    t2, waveform2 = wave2[:, 0], wave2[:, 1]
    print(f'{wave1.shape=}, {wave2.shape=}')
    print(f'{t1.shape=}, {waveform1.shape=}, {t2.shape=}, {waveform2.shape=}')
    
    # Compute the cross-correlation between the two waveforms
    cross_correlation = np.correlate(waveform1, waveform2, mode='valid')
    
    # Find the index of the maximum cross-correlation
    max_index = np.argmax(cross_correlation)
    print(f'{max_index=}')
    
    # Calculate the time offset
    offset = t2[0] - t1[max_index]
    print(f'{offset=}')
    
    # Shift the second waveform by the calculated offset
    shifted_wave2 = np.vstack((t2 - offset, waveform2))
    print(f'{shifted_wave2[0, 0]=}')
    
    return shifted_wave2.T