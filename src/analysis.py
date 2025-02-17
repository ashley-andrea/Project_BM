# src/analysis.py
import numpy as np
import matplotlib.pyplot as plt
import neo
import quantities as pq
from elephant.statistics import mean_firing_rate, isi, cv
from elephant.spike_train_correlation import spike_time_tiling_coefficient
from elephant.conversion import BinnedSpikeTrain
from elephant.spectral import welch_psd

### FIX THIS FUNCTIONS

def analyze_spike_data(spike_data):
    """Analyze spike data using Elephant to compute advanced metrics."""
    times = spike_data["times"]
    senders = spike_data["senders"]
    
    # Convert to Neo SpikeTrains
    unique_senders = np.unique(senders)
    spike_trains = []
    for sender in unique_senders:
        sender_times = times[senders == sender] / 1000.0  # Convert ms to seconds
        spike_train = neo.SpikeTrain(sender_times, units='s', t_stop=max(times)/1000.0)
        spike_trains.append(spike_train)

    # Firing rate analysis
    firing_rates = [mean_firing_rate(st) for st in spike_trains]
    avg_firing_rate = np.mean(firing_rates) if firing_rates else 0.0
    
    # ISI analysis
    cv_values = [cv(isi(st)) for st in spike_trains if len(st) > 1]
    avg_cv = np.mean(cv_values) if cv_values else 0.0

    # Spike correlation analysis
    corr_matrix = np.zeros((len(spike_trains), len(spike_trains)))
    if len(spike_trains) > 1:
        # Calculate optimal bin size to avoid discarded spikes
        max_time = max(st.t_stop for st in spike_trains)
        bin_size = 10*pq.ms
        num_bins = int(np.ceil(max_time / bin_size))
        adjusted_bin_size = max_time / num_bins
        binned_st = BinnedSpikeTrain(spike_trains, 
                                   bin_size=adjusted_bin_size,
                                   t_stop=max_time)
        
        cc_matrix = np.corrcoef(binned_st.to_array())
        np.fill_diagonal(cc_matrix, np.nan)
        avg_correlation = np.nanmean(cc_matrix)
    else:
        avg_correlation = np.nan

    print(f"Avg firing rate: {avg_firing_rate:.2f} Hz")
    print(f"Avg ISI CV: {avg_cv:.2f}")
    print(f"Avg spike correlation: {avg_correlation:.2f}")

    return {
        "firing_rates": firing_rates,
        "avg_firing_rate": avg_firing_rate,
        "isi_cv": cv_values,
        "correlation_matrix": cc_matrix,
        "spike_trains": spike_trains
    }
def analyze_voltage_data(voltage_data):
    """Analyze voltage data with proper Welch parameter handling and error checking."""
    voltages = voltage_data["V_m"]
    times = voltage_data["times"]
    
    # Input validation
    if len(voltages) != len(times):
        raise ValueError("Voltage and time arrays must have the same length")
    
    print(f"Analyzing {len(voltages)} voltage samples over {times[-1]-times[0]} ms")

    # Convert to Neo AnalogSignal
    sampling_period = np.mean(np.diff(times)) * pq.ms
    analog_signal = neo.AnalogSignal(
        voltages.reshape(-1, 1),
        units='mV',
        sampling_period=sampling_period
    )

    # Calculate Welch parameters adaptively
    fs = 1.0 / sampling_period.rescale('s')  # Sampling rate in Hz
    total_duration = analog_signal.t_stop - analog_signal.t_start  # in seconds
    
    # Adaptive segmentation logic
    min_segment_length = 0.5  # Minimum segment length in seconds
    if total_duration < min_segment_length:
        print(f"Warning: Short voltage trace ({total_duration:.2f}s) - using full duration")
        len_segment = total_duration
        n_segments = 1
    else:
        len_segment = 0.5  # 500ms segments
        n_segments = int((total_duration - len_segment/2) / (len_segment/2))  # 50% overlap

    print(f"Using {n_segments} segments of {len_segment}s each (fs={fs:.1f}Hz)")

    # Calculate PSD with safe parameters
    freq, psd = welch_psd(
        analog_signal,
        fs=fs,
        len_segment=len_segment,
        overlap=0.5,
        window='hann',
        nfft=int(len_segment * fs.magnitude)  # Match FFT size to segment length
    )

    # Process results
    freq = freq.magnitude.flatten()
    psd = psd.magnitude.flatten()

    if len(freq) == 0 or len(psd) == 0:
        raise ValueError("PSD calculation failed - check input data")

    # Find dominant frequency (ignore DC component)
    valid_mask = freq > 1  # Exclude 0-1Hz
    dominant_freq = freq[valid_mask][np.argmax(psd[valid_mask])]

    # Bandpower calculation with safety checks
    theta_band = (4, 8)
    theta_mask = (freq >= theta_band[0]) & (freq <= theta_band[1])
    
    if np.sum(theta_mask) < 2:
        print("Warning: Insufficient points in theta band")
        theta_power = 0.0
    else:
        theta_power = np.trapz(psd[theta_mask], freq[theta_mask])

    print("\nVoltage Analysis Results:")
    print(f"Dominant frequency: {dominant_freq:.2f} Hz (excluding DC)")
    print(f"Theta power (4-8 Hz): {theta_power:.2e} mV²/Hz")
    print(f"Frequency range: {freq[0]:.1f}-{freq[-1]:.1f} Hz")

    return {
        "psd_freq": freq,
        "psd": psd,
        "dominant_frequency": dominant_freq,
        "theta_power": theta_power,
        "sampling_rate": fs
    }

def get_isi_distribution(spike_trains):
    """Calculate ISI distribution using Elephant."""
    all_isis = np.concatenate([isi(st) for st in spike_trains])
    return all_isis
