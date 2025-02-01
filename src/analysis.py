# src/analysis.py
import numpy as np
import matplotlib.pyplot as plt

def analyze_spike_data(spike_data):
    """Analyze spike data to compute metrics like firing rates and ISI distributions."""
    times = spike_data["times"]
    senders = spike_data["senders"]
    
    # Compute overall firing rate
    total_spikes = len(times)
    if times.size > 0:
        firing_rate = total_spikes / (max(times) / 1000.0)  # spikes per second (Hz)
    else:
        firing_rate = 0.0
    print(f"Overall firing rate: {firing_rate:.2f} Hz")
    
    # Optionally, compute ISI histograms, per-neuron rates, etc.
    return {"firing_rate": firing_rate, "times": times, "senders": senders}

def analyze_voltage_data(voltage_data):
    """Analyze voltage data to compute metrics like mean and peak voltages."""
    voltages = voltage_data["V_m"]
    
    # Compute mean and peak voltages
    mean_voltage = np.mean(voltages)
    peak_voltage = np.max(voltages)
    print(f"Mean voltage: {mean_voltage:.2f} mV")
    print(f"Peak voltage: {peak_voltage:.2f} mV")
    
    # Optionally, analyze voltage traces further (e.g., bursting, spiking patterns)
    return {"mean_voltage": mean_voltage, "peak_voltage": peak_voltage}

def get_isi_distribution(times):
    """Calculate the inter-spike interval (ISI) distribution."""
    sorted_times = np.sort(times)
    isis = np.diff(sorted_times)
    return isis
