# src/config.py
# =============================================================================
# Simulation parameters
# =============================================================================

SIM_TIME = 1000.0   # Total simulation time in ms (increased for robust mean-field convergence)
DT       = 0.1      # Integration time step in ms

# =============================================================================
# Poisson generator inputs (Mossy/Climbing Fibers)
# =============================================================================

MOSSY_FIBER_PARAMS = {
    "rate": 350.0,  
}
MOSSY_FIBER_NUM = 1500

CLIMBING_FIBER_PARAMS = {
    "rate": 1.0,     
}
CLIMBING_FIBER_NUM = 64

# =============================================================================
# Cerebellar cell population parameters
# =============================================================================

GRANULE_CELL_PARAMS = {
    "tau_m": 12.0,    # Membrane time constant (ms), increased slightly for mean field smoothing
    "E_L": -68.0,     # Resting potential (mV)
    "V_th": -42.0,    # Firing threshold (mV)
    "V_reset": -68.0, # Reset potential (mV)
    "t_ref": 2.0      # Refractory period (ms)
}
GRANULE_CELL_NUM = 2500

GOLGI_CELL_PARAMS = {
    "tau_m": 22.0,
    "E_L": -68.0,
    "V_th": -48.0,
    "V_reset": -68.0,
    "t_ref": 2.0
}
GOLGI_CELL_NUM = 30

PURKINJE_CELL_PARAMS = {
    "tau_m": 35.0,
    "E_L": -68.0,
    "V_th": -52.0,
    "V_reset": -78.0,
    "t_ref": 5.0
}
PURKINJE_CELL_NUM = 64
PURKINJE_CELL_NUM_LAYERS = 1

INTERNEURON_PARAMS = {  
    "tau_m": 12.0,
    "E_L": -68.0,
    "V_th": -48.0,
    "V_reset": -68.0,
    "t_ref": 2.0
}
INTERNEURON_NUM = 150

DEEP_CEREBELLAR_NUCLEI_PARAMS = {
    "tau_m": 35.0,
    "E_L": -68.0,
    "V_th": -52.0,
    "V_reset": -68.0,
    "t_ref": 2.0
}
DEEP_CEREBELLAR_NUCLEI_NUM = 20

# =============================================================================
# Synaptic parameters (weights in nS, delays in ms)
# =============================================================================

SYN_MF_TO_GRANULE = {
    "weight": 6.0,  
    "delay": 1.0
}

SYN_MF_TO_GOLGI = {
    "weight": 3,
    "delay": 1.0
}

SYN_MF_TO_DCN = {
    "weight": 1.0,
    "delay": 1.0
}

SYN_GRANULE_TO_GOLGI = {
    "weight": 1.0,
    "delay": 1.5
}

SYN_PARALLEL = {
    "weight": 0.5,
    "delay": 1.5
}

SYN_GRANULE_TO_INTERNEURON = {
    "weight": 0.5,
    "delay": 1.5
}

SYN_GOLGI_TO_GRANULE = {
    "weight": -1.0,
    "delay": 1.0
}

SYN_GOLGI_TO_GOLGI = {
    "weight": -0.1,
    "delay": 1.0
}

SYN_INTERNEURON_TO_PURKINJE = {
    "weight": 1.0,
    "delay": 1.0
}

SYN_INTERNEURON_TO_INTERNEURON = {
    "weight": -0.5,
    "delay": 1.0
}

SYN_PURKINJE_TO_DCN = {
    "weight": -1.5,
    "delay": 1.0
}

SYN_CLIMBING = {
    "weight": 30.0,
    "delay": 1.0
}

# =============================================================================
# Connectivity rules
# =============================================================================

CONN_MF_TO_GRANULE = {
    "rule": "pairwise_bernoulli",
    "p": 0.05  # Increased probability to yield denser connections in the mean field limit
}

CONN_MF_TO_GOLGI = {
    "rule": "pairwise_bernoulli",
    "p": 0.2  
}

CONN_GRANULE_TO_GOLGI = {
    "rule": "pairwise_bernoulli",
    "p": 0.01
}

CONN_GOLGI_TO_GRANULE = {
    "rule": "pairwise_bernoulli",
    "p": 0.1
}

CONN_GOLGI_TO_GOLGI = {
    "rule": "pairwise_bernoulli",
    "p": 0.2
}

CONN_GRANULE_TO_INTERNEURON = {
    "rule": "pairwise_bernoulli",
    "p": 0.3
}

CONN_INTERNEURON_TO_INTERNEURON = {
    "rule": "pairwise_bernoulli",
    "p": 0.4
}

CONN_GRANULE_TO_PURKINJE = {
    "rule": "pairwise_bernoulli",
    "p": 0.9
}

CONN_CLIMBING_TO_PURKINJE = {
    "rule": "one_to_one"  # One climbing fiber per Purkinje cell
}

CONN_INTERNEURON_TO_PURKINJE = {
    "rule": "pairwise_bernoulli",
    "p": 0.2
}

CONN_PURKINJE_TO_DCN = {
    "rule": "fixed_outdegree",
    "outdegree": 5
}

# =============================================================================
# Random Seed for reproducibility
# =============================================================================

SEED = 2025

