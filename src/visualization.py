# src/visualization.py
import matplotlib.pyplot as plt
import numpy as np

def plot_raster(spike_data, title="Spike Raster Plot"):
    """Generate a raster plot of spike data."""
    times = spike_data["times"]
    senders = spike_data["senders"]
    
    plt.figure(figsize=(10, 6))
    plt.scatter(times, senders, s=2, color="black")
    plt.xlabel("Time (ms)")
    plt.ylabel("Neuron ID")
    plt.title(title)
    plt.show()

def plot_isi_histogram(isis, bins=50, title="ISI Histogram"):
    """Plot the histogram of inter-spike intervals."""
    plt.figure(figsize=(8, 5))
    plt.hist(isis, bins=bins, color="blue", edgecolor="black")
    plt.xlabel("Inter-Spike Interval (ms)")
    plt.ylabel("Frequency")
    plt.title(title)
    plt.show()

def plot_voltage_trace(voltage_data, title="Membrane Potential Trace"):
    """Plot the membrane potential trace over time."""
    times = voltage_data["times"]
    voltages = voltage_data["V_m"]
    
    plt.figure(figsize=(12, 6))
    plt.plot(times, voltages, color="red")
    plt.xlabel("Time (ms)")
    plt.ylabel("Membrane Potential (mV)")
    plt.title(title)
    plt.show()