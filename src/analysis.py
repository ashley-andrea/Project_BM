# src/analysis.py
import numpy as np
import matplotlib.pyplot as plt
import neo
import quantities as pq
from elephant.statistics import mean_firing_rate, isi, cv
from elephant.spike_train_correlation import spike_time_tiling_coefficient
from elephant.conversion import BinnedSpikeTrain
from elephant.spectral import welch_psd
from tqdm import tqdm

def analyze_spike_data(spike_data, skip_correlation=False):
    """Analyze spike data using Elephant to compute advanced metrics."""
    times = spike_data["times"]
    senders = spike_data["senders"]
    
    print(f"Starting spike data analysis with {len(times)} spikes from {len(np.unique(senders))} neurons.")
    
    # Handle empty spike data
    if len(times) == 0:
        print("No spikes found in the data.")
        return {
            "firing_rates": [],
            "avg_firing_rate": 0.0,
            "isi_cv": [],
            "correlation_matrix": np.array([]),
            "spike_trains": []
        }

    # Convert to Neo SpikeTrains
    unique_senders = np.unique(senders)
    spike_trains = []
    for sender in unique_senders:
        sender_times = times[senders == sender] / 1000.0  # Convert ms to seconds
        t_stop = np.max(times) / 1000.0 if len(times) > 0 else 0.0
        spike_train = neo.SpikeTrain(sender_times, units='s', t_stop=t_stop)
        spike_trains.append(spike_train)
    print(f"Created {len(spike_trains)} spike trains.")

    # Firing rate analysis
    firing_rates = []
    for st in spike_trains:
        rate = mean_firing_rate(st).rescale('Hz').magnitude.item()
        firing_rates.append(rate)
    avg_firing_rate = np.mean(firing_rates) if firing_rates else 0.0
    print(f"Firing rates calculated - average: {avg_firing_rate:.2f} Hz")

    # ISI analysis
    cv_values = []
    for st in spike_trains:
        if len(st) > 1:
            isi_values = isi(st)
            cv_val = cv(isi_values) if cv(isi_values).size > 0 else np.nan
            if not np.isnan(cv_val):
                cv_values.append(cv_val)
    avg_cv = np.mean(cv_values) if cv_values else np.nan
    print(f"ISI CV calculated - {len(cv_values)} valid values, average: {avg_cv:.2f}")

    # Spike correlation analysis
    cc_matrix = np.array([])
    avg_correlation = np.nan
    if len(spike_trains) > 1 and not skip_correlation:
        print(f"Calculating spike correlations for {len(spike_trains)} neurons...")
        n = len(spike_trains)
        cc_matrix = np.full((n, n), np.nan)
        
        for i in tqdm(range(n)):
            for j in range(i+1, n):
                try:
                    cc = spike_time_tiling_coefficient(spike_trains[i], spike_trains[j])
                    cc_matrix[i, j] = cc
                    cc_matrix[j, i] = cc  # Symmetric matrix
                except Exception as e:
                    print(f"Error calculating STTC between {i} and {j}: {str(e)}")
        
        avg_correlation = np.nanmean(cc_matrix)
        print(f"Average spike correlation: {avg_correlation:.2f}")
    else:
        print("Insufficient spike trains for correlation analysis.")

    return {
        "firing_rates": firing_rates,
        "avg_firing_rate": avg_firing_rate,
        "isi_cv": cv_values,
        "correlation_matrix": cc_matrix,
        "spike_trains": spike_trains
    }

def analyze_voltage_data(voltage_data):
    """Analyze voltage data with robust parameter validation and error handling."""
    print("\n[Voltage Analysis] Starting analysis...")
    
    # Input validation
    if not isinstance(voltage_data, dict) or 'V_m' not in voltage_data or 'times' not in voltage_data:
        raise ValueError("Invalid voltage data format. Expected dictionary with 'V_m' and 'times' keys.")
    
    voltages = voltage_data["V_m"]
    times = voltage_data["times"]
    
    if len(voltages) != len(times):
        raise ValueError(f"Voltage/time mismatch: {len(voltages)} voltages vs {len(times)} time points")
    if len(voltages) < 2:
        print("Warning: Insufficient data points for analysis (need at least 2 samples)")
        return {
            "psd_freq": np.array([]),
            "psd": np.array([]),
            "dominant_frequency": 0.0,
            "theta_power": 0.0,
            "sampling_rate": 0.0
        }

    print(f"Analyzing {len(voltages)} samples over {times[-1] - times[0]:.1f} ms")

    # Calculate sampling parameters
    try:
        sampling_interval = np.mean(np.diff(times))  # in ms
        fs = 1000.0 / sampling_interval  # Sampling frequency in Hz
        total_duration = (times[-1] - times[0]) / 1000.0  # Convert ms to seconds
    except Exception as e:
        raise ValueError(f"Time array processing failed: {str(e)}") from e

    print(f"Calculated sampling rate: {fs:.2f} Hz")
    print(f"Total duration: {total_duration:.2f} seconds")

    # Create Neo AnalogSignal with validation
    try:
        analog_signal = neo.AnalogSignal(
            voltages.reshape(-1, 1) * pq.mV,
            t_start=times[0] * pq.ms,
            sampling_rate=fs * pq.Hz
        )
    except Exception as e:
        raise ValueError(f"Signal creation failed: {str(e)}") from e

    # Adaptive Welch parameters
    min_segment_length = 0.5  # seconds
    max_segment_length = 5.0  # seconds
    target_segment_length = 1.0  # seconds
    
    # Calculate safe segment length
    if total_duration < min_segment_length:
        print("Using full duration for PSD calculation")
        len_segment = total_duration
        n_segments = 1
        overlap = 0.0
    else:
        len_segment = min(max(target_segment_length, min_segment_length), 
                        min(total_duration, max_segment_length))
        n_segments = max(1, int(total_duration / (len_segment * 0.5)) - 1)
        overlap = 0.5

    # Ensure at least 50% overlap for multiple segments
    if n_segments > 1 and (total_duration - len_segment) < (len_segment * 0.5):
        n_segments = 2
        overlap = (total_duration - len_segment) / len_segment

    # Calculate valid nperseg (number of samples per segment)
    nperseg = int(len_segment * fs)
    if nperseg < 8:  # Minimum required by FFT
        print(f"Adjusting segment length from {len_segment:.2f}s to minimum valid length")
        nperseg = max(8, len(voltages) // 2)
        len_segment = nperseg / fs
        n_segments = 1
        overlap = 0.0

    print(f"PSD parameters:")
    print(f"- Segment length: {len_segment:.2f}s ({nperseg} samples)")
    print(f"- Overlap: {overlap*100:.1f}%")
    print(f"- Segments: {n_segments}")

    # Calculate PSD with multiple fallback strategies
    try:
        freq, psd = welch_psd(
            analog_signal,
            fs=fs * pq.Hz,
            n_segments=n_segments,
            len_segment=len_segment * pq.s,
            overlap=overlap,
            window='hann',
            nfft=max(nperseg, 8)
        )
        freq = freq.rescale('Hz').magnitude.flatten()
        psd = psd.rescale('mV**2/Hz').magnitude.flatten()
    except Exception as e:
        print(f"PSD calculation failed: {str(e)}")
        print("Attempting fallback to simple FFT...")
        try:
            # Last-resort simple FFT
            freq = np.fft.rfftfreq(len(voltages), d=1/fs)
            psd = np.abs(np.fft.rfft(voltages - np.mean(voltages)))**2
            psd /= (fs * len(voltages))
        except Exception as fallback_error:
            print(f"Fallback failed: {str(fallback_error)}")
            return {
                "psd_freq": np.array([]),
                "psd": np.array([]),
                "dominant_frequency": 0.0,
                "theta_power": 0.0,
                "sampling_rate": fs
            }

    # Frequency analysis with validation
    dominant_freq = 0.0
    if len(freq) > 0:
        try:
            valid_mask = (freq > 1) & (psd > 0)
            if np.any(valid_mask):
                dominant_idx = np.argmax(psd[valid_mask])
                dominant_freq = freq[valid_mask][dominant_idx]
        except Exception as e:
            print(f"Dominant frequency detection failed: {str(e)}")

    # Theta power calculation with validation
    theta_power = 0.0
    try:
        theta_band = (4, 8)
        theta_mask = (freq >= theta_band[0]) & (freq <= theta_band[1])
        if np.sum(theta_mask) > 1:
            theta_power = np.trapz(psd[theta_mask], freq[theta_mask])
    except Exception as e:
        print(f"Theta power calculation failed: {str(e)}")

    print("\n[Voltage Analysis] Results:")
    print(f"- Dominant frequency: {dominant_freq:.2f} Hz")
    print(f"- Theta power (4-8 Hz): {theta_power:.2e} mV²/Hz")
    print(f"- Frequency range: {freq[0]:.1f}-{freq[-1]:.1f} Hz" if len(freq) > 0 else "- No frequency data")

    return {
        "psd_freq": freq,
        "psd": psd,
        "dominant_frequency": dominant_freq,
        "theta_power": theta_power,
        "sampling_rate": fs
    }

def get_isi_distribution(spike_trains):
    """Calculate ISI distribution using Elephant."""
    all_isis = []
    for st in spike_trains:
        if len(st) > 1:
            isi_values = isi(st).rescale('ms').magnitude
            all_isis.extend(isi_values)
    return np.array(all_isis)