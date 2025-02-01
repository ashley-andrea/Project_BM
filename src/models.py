# src/models.py
import nest
from src import config

# -----------------------------------------------------------
# Population creation functions
# -----------------------------------------------------------

def create_mossy_fibers(n):
    """Create a population of mossy fibers (input to granule cells)."""
    mossy_fibers = nest.Create("poisson_generator", n, params=config.MOSSY_FIBER_PARAMS)
    return mossy_fibers

def create_climbing_fibers(n):
    """Create a population of climbing fibers (input to Purkinje cells)."""
    climbing_fibers = nest.Create("poisson_generator", n, params=config.CLIMBING_FIBER_PARAMS)
    return climbing_fibers

def create_granule_cells(n):
    """Create a population of granule cells with the specified parameters."""
    granule_cells = nest.Create("iaf_psc_alpha", n, params=config.GRANULE_CELL_PARAMS)
    return granule_cells

def create_golgi_cells(n):
    """Create a population of Golgi cells."""
    golgi_cells = nest.Create("iaf_psc_alpha", n, params=config.GOLGI_CELL_PARAMS)
    return golgi_cells

def create_purkinje_cells(n):
    """Create a population of Purkinje cells."""
    purkinje_cells = nest.Create("iaf_psc_alpha", n, params=config.PURKINJE_CELL_PARAMS)
    return purkinje_cells

def create_interneurons(n):
    """Create a population of interneurons (e.g., basket/stellate cells)."""
    interneurons = nest.Create("iaf_psc_alpha", n, params=config.INTERNEURON_PARAMS)
    return interneurons

def create_deep_cerebellar_nuclei(n):
    """Create a population of deep cerebellar nuclei cells."""
    dcn_cells = nest.Create("iaf_psc_alpha", n, params=config.DEEP_CEREBELLAR_NUCLEI_PARAMS)
    return dcn_cells


# -----------------------------------------------------------
# Connectivity functions
# -----------------------------------------------------------

def connect_mossy_to_granule(mossy, granule):
    """Connect mossy fibers to granule cells with excitatory synapses."""
    nest.Connect(mossy, granule, syn_spec=config.SYN_MF_TO_GRANULE)

def connect_mossy_to_dcn(mossy, dcn):
    """Connect mossy fibers to deep cerebellar nuclei with excitatory synapses."""
    nest.Connect(mossy, dcn, syn_spec=config.SYN_MF_TO_DCN)

def connect_granule_to_purkinje(granule, purkinje):
    """Connect granule cells (via parallel fibers) to Purkinje cells."""
    nest.Connect(granule, purkinje, conn_spec=config.CONN_GRANULE_TO_PURKINJE, syn_spec=config.SYN_PARALLEL)

def connect_climbing_to_purkinje(climbing, purkinje):
    """Connect climbing fibers to Purkinje cells with powerful excitatory input."""
    nest.Connect(climbing, purkinje, conn_spec=config.CONN_CLIMBING_TO_PURKINJE, syn_spec=config.SYN_CLIMBING)

def connect_golgi_to_granule(golgi, granule):
    """Connect Golgi cells to granule cells (inhibitory)."""
    nest.Connect(golgi, granule, conn_spec=config.CONN_GOLGI_TO_GRANULE, syn_spec=config.SYN_GOLGI_TO_GRANULE)

def connect_interneuron_to_purkinje(interneuron, purkinje):
    """Connect interneurons (basket/stellate cells) to Purkinje cells (inhibitory)."""
    nest.Connect(interneuron, purkinje, conn_spec=config.CONN_INTERNEURON_TO_PURKINJE, syn_spec=config.SYN_INTERNEURON_TO_PURKINJE)

def connect_purkinje_to_dcn(purkinje, dcn):
    """Connect Purkinje cells to deep cerebellar nuclei (inhibitory)."""
    nest.Connect(purkinje, dcn, conn_spec=config.CONN_PURKINJE_TO_DCN, syn_spec=config.SYN_PURKINJE_TO_DCN)
