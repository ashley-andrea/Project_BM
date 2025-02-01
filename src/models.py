# src/models.py
import nest
from src import config

def create_granule_cells(n):
    """Create a population of granule cells with the specified parameters."""
    granule_cells = nest.Create("iaf_psc_alpha", n, params=config.GRANULE_CELL_PARAMS)
    return granule_cells

def create_purkinje_cells(n):
    """Create a population of Purkinje cells."""
    purkinje_cells = nest.Create("iaf_psc_alpha", n, params=config.PURKINJE_CELL_PARAMS)
    return purkinje_cells

def create_interneurons(n):
    """Create a population of interneurons (like Golgi cells)."""
    interneurons = nest.Create("iaf_psc_alpha", n) 
    return interneurons

def create_mossy_fibers(n, rate=800.0):
    """Create a population of mossy fibers (input to granule cells)."""
    mossy_fibers = nest.Create("poisson_generator", n, params=config.MOSSY_FIBERS_PARAMS)
    return mossy_fibers

def connect_cells(source, target, syn_spec=config.EXCITATORY_SYNAPSE):
    """Connect source neurons to target neurons using the given synaptic specification."""
    nest.Connect(source, target, syn_spec=syn_spec)

