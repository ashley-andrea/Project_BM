# src/models.py
import nest
from src import config

# Apply the simulation settings to NEST
nest.ResetKernel()
nest.SetKernelStatus({"resolution": config.DT, "print_time": True, "rng_seed": config.SEED})

# -----------------------------------------------------------
# Population creation functions
# -----------------------------------------------------------

def create_mossy_fibers(n):
    """Create a population of mossy fibers (input to granule cells)."""
    mossy_fibers = nest.Create("poisson_generator", n, params=config.MOSSY_FIBER_PARAMS)
    print(f"Created {n} mossy fibers.")
    return mossy_fibers

def create_climbing_fibers(n):
    """Create a population of climbing fibers (input to Purkinje cells)."""
    climbing_fibers = nest.Create("poisson_generator", n, params=config.CLIMBING_FIBER_PARAMS)
    print(f"Created {n} climbing fibers.")
    return climbing_fibers

def create_granule_cells(n):
    """Create a population of granule cells with the specified parameters."""
    granule_cells = nest.Create("iaf_psc_alpha", n, params=config.GRANULE_CELL_PARAMS)
    print(f"Created {n} granule cells.")
    return granule_cells

def create_golgi_cells(n):
    """Create a population of Golgi cells."""
    golgi_cells = nest.Create("iaf_psc_alpha", n, params=config.GOLGI_CELL_PARAMS)
    print(f"Created {n} Golgi cells.")
    return golgi_cells

def create_purkinje_cells(n):
    """Create a population of Purkinje cells."""
    purkinje_cells = nest.Create("iaf_psc_alpha", n, params=config.PURKINJE_CELL_PARAMS)
    print(f"Created {n} Purkinje cells.")
    return purkinje_cells

def create_interneurons(n):
    """Create a population of interneurons (e.g., basket/stellate cells)."""
    interneurons = nest.Create("iaf_psc_alpha", n, params=config.INTERNEURON_PARAMS)
    print(f"Created {n} interneurons.")
    return interneurons

def create_deep_cerebellar_nuclei(n):
    """Create a population of deep cerebellar nuclei cells."""
    dcn_cells = nest.Create("iaf_psc_alpha", n, params=config.DEEP_CEREBELLAR_NUCLEI_PARAMS)
    print(f"Created {n} deep cerebellar nuclei cells.")
    return dcn_cells


# -----------------------------------------------------------
# Connectivity functions
# -----------------------------------------------------------

# ------------------------------
# Mossy Fiber Connections
# ------------------------------

def connect_mossy_to_granule(mossy, granule):
    """
    Connect mossy fibers to granule cells with excitatory synapses.
    
    Parameters:
        mossy: The source population of mossy fibers.
        granule: The target population of granule cells.
    """
    nest.Connect(mossy, granule, conn_spec=config.CONN_MF_TO_GRANULE,
                 syn_spec=config.SYN_MF_TO_GRANULE)

def connect_mossy_to_golgi(mossy, golgi):
    """
    Connect mossy fibers to Golgi cells with excitatory synapses.
    
    Parameters:
        mossy: The source population of mossy fibers.
        golgi: The target population of Golgi cells.
    """
    nest.Connect(mossy, golgi, conn_spec=config.CONN_MF_TO_GOLGI,
                 syn_spec=config.SYN_MF_TO_GOLGI)

def connect_mossy_to_dcn(mossy, dcn):
    """
    Connect mossy fibers to deep cerebellar nuclei with excitatory synapses.
    
    Parameters:
        mossy: The source population of mossy fibers.
        dcn: The target population of deep cerebellar nuclei neurons.
    """
    nest.Connect(mossy, dcn, syn_spec=config.SYN_MF_TO_DCN)


# ------------------------------
# Granule Cell Connections
# ------------------------------

def connect_granule_to_purkinje(granule, purkinje):
    """
    Connect granule cells (via parallel fibers) to Purkinje cells.
    
    Parameters:
        granule: The source population of granule cells.
        purkinje: The target population of Purkinje cells.
    """
    nest.Connect(granule, purkinje, conn_spec=config.CONN_GRANULE_TO_PURKINJE, 
                 syn_spec=config.SYN_PARALLEL)

def connect_granule_to_interneuron(granule, interneuron):
    """
    Connect granule cells to interneurons (inhibitory).
    
    Parameters:
        granule: The source population of granule cells.
        interneuron: The target population of interneurons.
    """
    nest.Connect(granule, interneuron, conn_spec=config.CONN_GRANULE_TO_INTERNEURON, 
                 syn_spec=config.SYN_GRANULE_TO_INTERNEURON)
    
def connect_granule_to_golgi(granule, golgi):
    """
    Connect granule cells to Golgi cells (inhibitory).
    
    Parameters:
        granule: The source population of granule cells.
        golgi: The target population of Golgi cells.
    """
    nest.Connect(granule, golgi, conn_spec=config.CONN_GRANULE_TO_GOLGI, 
                 syn_spec=config.SYN_GRANULE_TO_GOLGI)


# ------------------------------
# Climbing Fiber Connections
# ------------------------------

def connect_climbing_to_purkinje(climbing, purkinje):
    """
    Connect climbing fibers to Purkinje cells with powerful excitatory input.
    
    Parameters:
        climbing: The source population of climbing fibers.
        purkinje: The target population of Purkinje cells.
    """
    nest.Connect(climbing, purkinje, conn_spec=config.CONN_CLIMBING_TO_PURKINJE, 
                 syn_spec=config.SYN_CLIMBING)


# ------------------------------
# Purkinje Cell Connections
# ------------------------------

def connect_purkinje_to_dcn(purkinje, dcn):
    """
    Connect Purkinje cells to deep cerebellar nuclei (inhibitory).
    
    Parameters:
        purkinje: The source population of Purkinje cells.
        dcn: The target population of deep cerebellar nuclei neurons.
    """
    nest.Connect(purkinje, dcn, conn_spec=config.CONN_PURKINJE_TO_DCN, 
                 syn_spec=config.SYN_PURKINJE_TO_DCN)


# ------------------------------
# Golgi Cell Connections
# ------------------------------

def connect_golgi_to_granule(golgi, granule):
    """
    Connect Golgi cells to granule cells (inhibitory).
    
    Parameters:
        golgi: The source population of Golgi cells.
        granule: The target population of granule cells.
    """
    nest.Connect(golgi, granule, conn_spec=config.CONN_GOLGI_TO_GRANULE, 
                 syn_spec=config.SYN_GOLGI_TO_GRANULE)

def connect_golgi_to_golgi(golgi):
    """
    Connect Golgi cells to other Golgi cells (inhibitory).
    
    Parameters:
        golgi: The population of Golgi cells (both source and target).
    """
    nest.Connect(golgi, golgi, conn_spec=config.CONN_GOLGI_TO_GOLGI, 
                 syn_spec=config.SYN_GOLGI_TO_GOLGI)


# ------------------------------
# Interneuron Connections
# ------------------------------

def connect_interneuron_to_purkinje(interneuron, purkinje):
    """
    Connect interneurons (basket/stellate cells) to Purkinje cells (inhibitory).
    
    Parameters:
        interneuron: The source population of interneurons.
        purkinje: The target population of Purkinje cells.
    """
    nest.Connect(interneuron, purkinje, conn_spec=config.CONN_INTERNEURON_TO_PURKINJE, 
                 syn_spec=config.SYN_INTERNEURON_TO_PURKINJE)

def connect_interneuron_to_interneuron(interneuron):
    """
    Connect interneurons to other interneurons (inhibitory).
    
    Parameters:
        interneuron: The population of interneurons (both source and target).
    """
    nest.Connect(interneuron, interneuron, conn_spec=config.CONN_INTERNEURON_TO_INTERNEURON, 
                 syn_spec=config.SYN_INTERNEURON_TO_INTERNEURON)
    

def connect_all(mossy, climbing, granule, golgi, purkinje, interneuron, dcn):
    """Connect all populations according to cerebellar connectivity rules."""
    connect_mossy_to_granule(mossy, granule)
    connect_mossy_to_golgi(mossy, golgi)
    connect_mossy_to_dcn(mossy, dcn)
    connect_granule_to_golgi(granule, golgi)
    connect_granule_to_purkinje(granule, purkinje)
    connect_granule_to_interneuron(granule, interneuron)
    connect_golgi_to_granule(golgi, granule)
    connect_golgi_to_golgi(golgi)
    connect_climbing_to_purkinje(climbing, purkinje)
    connect_interneuron_to_purkinje(interneuron, purkinje)
    connect_interneuron_to_interneuron(interneuron)
    connect_purkinje_to_dcn(purkinje, dcn)

    # Print the amount of connections
    print(f"Number of mossy -> granule connections: {len(nest.GetConnections(source=mossy, target=granule))}")
    print(f"Number of mossy -> golgi connections: {len(nest.GetConnections(source=mossy, target=golgi))}")
    print(f"Number of mossy -> DCN connections: {len(nest.GetConnections(source=mossy, target=dcn))}")
    print(f"Number of granule -> golgi connections: {len(nest.GetConnections(source=granule, target=golgi))}")
    print(f"Number of granule -> purkinje connections: {len(nest.GetConnections(source=granule, target=purkinje))}")
    print(f"Number of granule -> interneuron connections: {len(nest.GetConnections(source=granule, target=interneuron))}")
    print(f"Number of golgi -> granule connections: {len(nest.GetConnections(source=golgi, target=granule))}")
    print(f"Number of golgi -> golgi connections: {len(nest.GetConnections(source=golgi, target=golgi))}")
    print(f"Number of climbing -> purkinje connections: {len(nest.GetConnections(source=climbing, target=purkinje))}")
    print(f"Number of interneuron -> purkinje connections: {len(nest.GetConnections(source=interneuron, target=purkinje))}")
    print(f"Number of interneuron -> interneuron connections: {len(nest.GetConnections(source=interneuron, target=interneuron))}")
    print(f"Number of purkinje -> DCN connections: {len(nest.GetConnections(source=purkinje, target=dcn))}")