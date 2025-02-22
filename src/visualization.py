# src/visualization.py
import matplotlib.pyplot as plt
import nest.spatial
import numpy as np
import nest
from elephant.statistics import instantaneous_rate, mean_firing_rate
from elephant.conversion import BinnedSpikeTrain
from quantities import ms, Hz


def plot_raster(spike_data, title="Spike Raster Plot"):
    """Generate a raster plot from Neo spike trains."""
    spike_trains = spike_data["spike_trains"]
    
    plt.figure(figsize=(12, 6))
    for neuron_id, st in enumerate(spike_trains):
        plt.scatter(st.rescale(ms), [neuron_id]*len(st), 
                    s=10, color='black', marker='|')
    
    plt.xlabel("Time (ms)")
    plt.ylabel("Neuron ID")
    plt.title(title)
    plt.xlim(left=0)
    plt.show()

def plot_isi_histogram(isis, bins=50, title="ISI Histogram"):
    """Plot the histogram of inter-spike intervals."""
    plt.figure(figsize=(10, 5))
    plt.hist(isis, bins=bins, color="skyblue", edgecolor="black")  # Convert s to ms
    plt.xlabel("Inter-Spike Interval (ms)")
    plt.ylabel("Count")
    plt.title(title)
    plt.show()

def plot_voltage_trace(voltage_data, title="Membrane Potential Trace"):
    """Plot the membrane potential trace with signal processing results."""
    plt.figure(figsize=(12, 6))
    plt.plot(voltage_data["times"], voltage_data["V_m"], color="purple", alpha=0.8)
    plt.xlabel("Time (ms)")
    plt.ylabel("Membrane Potential (mV)")
    plt.title(title)
    plt.grid(True)
    plt.show()

def plot_spike_analysis_composite(spike_train, kernel_width=50*ms, 
                                bin_size=10*ms, title="Spike Train Analysis"):
    """Composite plot showing multiple representations of spike train data."""
    plt.figure(dpi=150, figsize=(12, 6))
    
    # Basic raster
    plt.plot(spike_train, [0]*len(spike_train), 'r', marker=2, ms=25,
            markeredgewidth=2, lw=0, label='Spike times')
    
    # Mean firing rate
    mean_rate = mean_firing_rate(spike_train)
    plt.hlines(mean_rate, xmin=spike_train.t_start, xmax=spike_train.t_stop,
              linestyle='--', color='green', label='Mean firing rate')
    
    # Time histogram (binned rate)
    binned_st = BinnedSpikeTrain(spike_train, bin_size=bin_size)
    bin_centers = binned_st.bin_edges[:-1] + bin_size/2
    plt.bar(binned_st.bin_edges[:-1], binned_st.to_array().flatten()/bin_size,
           width=bin_size, align='edge', alpha=0.3, color='blue',
           label='Binned rate')
    
    # Instantaneous rate
    inst_rate = instantaneous_rate(spike_train, kernel_width=kernel_width)
    plt.plot(inst_rate.times.rescale(ms), inst_rate.rescale(Hz).magnitude.flatten(),
            color='orange', label='Instantaneous rate')
    
    # Formatting
    plt.xlabel(f'Time [{spike_train.times.dimensionality}]')
    plt.ylabel(f'Firing Rate [{Hz.dimensionality}]')
    plt.xlim(spike_train.t_start, spike_train.t_stop)
    plt.title(title)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def plot_correlation_heatmap(corr_matrix, title="Spike Correlation Matrix"):
    """Plot heatmap of spike train correlations."""
    plt.figure(figsize=(8, 6))
    plt.imshow(corr_matrix, cmap="viridis", vmin=-1, vmax=1)
    plt.colorbar(label="Correlation Coefficient")
    plt.xlabel("Neuron ID")
    plt.ylabel("Neuron ID")
    plt.title(title)
    plt.show()

def plot_spectral_analysis(voltage_results, title="Spectral Analysis"):
    """Plot power spectral density results."""
    plt.figure(figsize=(10, 5))
    plt.semilogy(voltage_results["psd_freq"], voltage_results["psd"], 
                color='navy', linewidth=1.5)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power Spectral Density (mV²/Hz)")
    plt.title(title)
    plt.grid(True)
    plt.show()

def show_connections(network, source, target, print_text=False, perspective=(10, -50)):
    try:
        elev, azim = perspective
    except ValueError:
        raise ValueError("Perspective should be a tuple of two angles (elevation, azimuth).")
    
    try:
        source_pop = network[source]
        target_pop = network[target]
    except KeyError:
        raise ValueError("Source or target population not found in the network.")
    
    # Extract one neuron from source population
    src_neuron = nest.FindCenterElement(source_pop)
    src_neuron_connections = nest.GetConnections(src_neuron, target_pop)
    if len(src_neuron_connections) == 0:
        raise ValueError("No connections found between source and target populations for the selected neuron.")
    if print_text:
        print(f"Connections from {source} to {target}: {len(src_neuron_connections)}")
    weights = src_neuron_connections.get("weight")
    fig = nest.PlotTargets(src_neuron, target_pop, src_color="red", src_size=40, tgt_color="blue", probability_parameter=weights)
    ax = fig.gca()
    ax.set_xlim(-1.0, 1.0)
    ax.set_ylim(-1.0, 1.0)
    ax.set_zlim(0.0, 5.0)
    ax.set_title(f"Synaptic Connections Between the center neuron of '{source}' and its targets in '{target}'\nPerspective: Elevation={elev}, Azimuth={azim}")
    ax.set
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")
    ax.set_zlabel("Z Position")
    ax.set_xticklabels([])
    ax.set_yticklabels([]) 
    ax.set_zticklabels([])
    ax.view_init(elev=elev, azim=azim)
    return fig

