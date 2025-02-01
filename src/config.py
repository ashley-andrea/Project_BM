# src/config.py
import nest

# Simulation parameters
SIM_TIME = 1000.0  # Total simulation time in ms
DT = 0.1           # Integration time step in ms

# Neuron model parameters for cerebellar cell types
GRANULE_CELL_PARAMS = {
    "tau_m": 20.0,    # Membrane time constant in ms
    "V_th": -55.0,    # Spike threshold in mV
    "V_reset": -70.0, # Reset potential in mV
    "I_e": 2.0,       # External input current in pA
}

PURKINJE_CELL_PARAMS = {
    "tau_m": 30.0,
    "V_th": -50.0,
    "V_reset": -65.0,
    # You might need more detailed parameters for Purkinje cells, such as adaptive thresholds or conductances.
}

MOSSY_FIBERS_PARAMS = {
    # Poisson generator input parameters
    "rate": 190.0,    # Firing rate in Hz
}

# Synaptic parameters
EXCITATORY_SYNAPSE = {
    "weight": 2.8,   # Adjust based on calibration
    "delay": 1.0,    # Synaptic delay in ms
}

INHIBITORY_SYNAPSE = {
    "weight": -2.0,
    "delay": 1.0,
}

MOSSY_FIBERS_SYNAPSE = {
    "weight": 2.0,
    "delay": 1.0,
}

# Random seed for reproducibility
SEED = 42

# Apply the simulation settings to NEST
nest.ResetKernel()
nest.SetKernelStatus({"resolution": DT, "print_time": True, "rng_seed": SEED})
