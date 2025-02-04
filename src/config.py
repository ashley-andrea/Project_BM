# src/config.py

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
    "tau_m": 25.0,      
    "E_L": -70.0,
    "V_th": -50.0,      
    "V_reset": -70.0,
    "t_ref": 2.0
}
GOLGI_CELL_NUM = 50

PURKINJE_CELL_PARAMS = {
    "tau_m": 30.0,      
    "E_L": -70.0,
    "V_th": -50.0,      
    "V_reset": -65.0,  
    "t_ref": 5.0       
}
PURKINJE_CELL_NUM = 50

INTERNEURON_PARAMS = {
    "tau_m": 10.0,      
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
# Synaptic parameters and connection specifications (expanded)
# -----------------------------------------------------------

# 1. Mossy Fiber connections
SYN_MF_TO_GRANULE = {
    "weight": 1.0, 
    "delay": 1.0
}
SYN_MF_TO_GOLGI = {
    "weight": 1.0,
    "delay": 1.0
}
SYN_MF_TO_DCN = {
    "weight": 1.5,
    "delay": 1.0
}

# 2. Granule Cell connections
SYN_GRANULE_TO_GOLGI = {
    "weight": 1.2,  
    "delay": 1.5
}
SYN_PARALLEL = {
    "weight": 1.0,
    "delay": 1.5
}
SYN_GRANULE_TO_INTERNEURON = {
    "weight": 0.8,
    "delay": 1.5
}

# 3. Golgi Cell connections 
SYN_GOLGI_TO_GRANULE = {
    "weight": -4,  
    "delay": 1.0
}
SYN_GOLGI_TO_GOLGI = {
    "weight": -0.5,   # Recurrent inhibition
    "delay": 1.0
}

# 4. Interneuron connections
SYN_INTERNEURON_TO_PURKINJE = {
    "weight": -1.5,
    "delay": 1.0
}
SYN_INTERNEURON_TO_INTERNEURON = {
    "weight": -0.8,   # Recurrent inhibition
    "delay": 1.0
}

# 5. Purkinje Cell connections
SYN_PURKINJE_TO_DCN = {
    "weight": -2.0,
    "delay": 1.0
}

# 6. Climbing Fiber connections
SYN_CLIMBING = {
    "weight": 15.0, 
    "delay": 1.0
}

# -----------------------------------------------------------
# Connection rules (expanded)
# -----------------------------------------------------------

CONN_MF_TO_GRANULE = {
    "rule": "fixed_total_number",
    "N": MOSSY_FIBER_NUM * GRANULE_CELL_NUM // 5000
}

CONN_MF_TO_GOLGI = {
    "rule": "pairwise_bernoulli",
    "p": 0.5
}

CONN_GRANULE_TO_GOLGI = {
    "rule": "pairwise_bernoulli",
    "p": 0.1
}

CONN_GOLGI_TO_GRANULE = {
    "rule": "pairwise_bernoulli",
    "p": 0.3
}

CONN_GOLGI_TO_GOLGI = {
    "rule": "pairwise_bernoulli",
    "p": 0.15
}

CONN_GRANULE_TO_INTERNEURON = {
    "rule": "pairwise_bernoulli",
    "p": 0.25
}

CONN_INTERNEURON_TO_INTERNEURON = {
    "rule": "pairwise_bernoulli",
    "p": 0.3
}

CONN_GRANULE_TO_PURKINJE = {
    "rule": "pairwise_bernoulli",
    "p": 0.5  
}

CONN_CLIMBING_TO_PURKINJE = {
    "rule": "pairwise_bernoulli",
    "p": 0.2
}

CONN_INTERNEURON_TO_PURKINJE = {
    "rule": "pairwise_bernoulli",
    "p": 0.3
}

CONN_PURKINJE_TO_DCN = {
    "rule": "all_to_all"
}

# Random seed for reproducibility
SEED = 42
