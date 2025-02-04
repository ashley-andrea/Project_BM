# src/config.py
import nest

# Simulation parameters
SIM_TIME = 1000.0  # Total simulation time in ms
DT = 0.1           # Integration time step in ms

# -----------------------------------------------------------
# We consider Mossy and Climbing fibers as Poisson generators, so we only define their firing rates

MOSSY_FIBER_PARAMS = {
    # Poisson generator input parameters
    "rate": 800.0,    # Firing rate in Hz
}
MOSSY_FIBER_NUM = 500

CLIMBING_FIBER_PARAMS = {
    "rate": 1.0,        # Low firing rate
}
CLIMBING_FIBER_NUM = 30



# Now we consider the parameters for the different cell populations in the cerebellar network

GRANULE_CELL_PARAMS = {
    "tau_m": 20.0,      # Membrane time constant (ms)
    "E_L": -70.0,       # Resting membrane potential (mV)
    "V_th": -60.0,      # Firing threshold (mV)
    "V_reset": -70.0,   # Reset potential (mV)
    "t_ref": 2.0        # Refractory period (ms)
}
GRANULE_CELL_NUM = 500

GOLGI_CELL_PARAMS = {
    "tau_m": 25.0,      # Slightly slower dynamics
    "E_L": -70.0,
    "V_th": -50.0,      # A lower threshold might be appropriate for more responsive inhibition
    "V_reset": -70.0,
    "t_ref": 2.0
}
GOLGI_CELL_NUM = 50

PURKINJE_CELL_PARAMS = {
    "tau_m": 30.0,      # Longer integration time
    "E_L": -70.0,
    "V_th": -50.0,      # Lower threshold to reflect the high sensitivity to input
    "V_reset": -65.0,   # A higher reset potential may allow for high-frequency firing under strong drive
    "t_ref": 5.0        # A longer refractory period can help mimic their slower spontaneous firing rates
}
PURKINJE_CELL_NUM = 50

INTERNEURON_PARAMS = {
    "tau_m": 10.0,      # Faster membrane dynamics for rapid inhibition
    "E_L": -70.0,
    "V_th": -55.0,
    "V_reset": -70.0,
    "t_ref": 2.0
}
INTERNEURON_NUM = 100

DEEP_CEREBELLAR_NUCLEI_PARAMS = {
    "tau_m": 20.0,
    "E_L": -70.0,
    "V_th": -55.0,
    "V_reset": -70.0,
    "t_ref": 2.0
}
DEEP_CEREBELLAR_NUCLEI_NUM = 50


# -----------------------------------------------------------
# Synaptic parameters and connection specifications
# -----------------------------------------------------------

# 1. Mossy Fiber to Granule Cell (excitatory)
SYN_MF_TO_GRANULE = {
    "weight": 3.0,     # Strength of excitatory connection
    "delay": 1.0       # Synaptic delay in ms
}

# 2. Mossy Fiber to Deep Cerebellar Nuclei (excitatory)
SYN_MF_TO_DCN = {
    "weight": 1.5,
    "delay": 1.0
}

# 3. Granule Cell to Purkinje Cell (via parallel fibers, excitatory)
SYN_PARALLEL = {
    "weight": 1.0,
    "delay": 1.5
}
CONN_GRANULE_TO_PURKINJE = {
    "rule": "pairwise_bernoulli",
    "p": 0.6     # 10% probability for connection
}

# 4. Climbing Fiber to Purkinje Cell (powerful excitatory input)
SYN_CLIMBING = {
    "weight": 5.0,
    "delay": 1.0
}
CONN_CLIMBING_TO_PURKINJE = {
    "rule": "pairwise_bernoulli",  # Assumes one climbing fiber per Purkinje cell
    "p": 0.2,     # 20% probability for connection
}

# 5. Golgi Cell to Granule Cell (inhibitory)
SYN_GOLGI_TO_GRANULE = {
    "weight": -1.0,   # Negative weight for inhibition
    "delay": 1.0
}
CONN_GOLGI_TO_GRANULE = {
    "rule": "pairwise_bernoulli",
    "p": 0.2     # 20% probability for connection
}

# 6. Interneuron (Basket/Stellate) to Purkinje Cell (inhibitory)
SYN_INTERNEURON_TO_PURKINJE = {
    "weight": -1.5,
    "delay": 1.0
}
CONN_INTERNEURON_TO_PURKINJE = {
    "rule": "pairwise_bernoulli",
    "p": 0.3     # 50% probability for connection
}

# 7. Purkinje Cell to Deep Cerebellar Nuclei (inhibitory)
SYN_PURKINJE_TO_DCN = {
    "weight": -2.0,
    "delay": 1.0
}
CONN_PURKINJE_TO_DCN = {
    "rule": "all_to_all"
}

# Random seed for reproducibility
SEED = 42

# Apply the simulation settings to NEST
nest.ResetKernel()
nest.SetKernelStatus({"resolution": DT, "print_time": True, "rng_seed": SEED})
