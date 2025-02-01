# src/simulation.py
import nest
from src import config, models

def setup_network():
    """Set up the cerebellar network architecture."""
    # Example: Create cell populations
    granule_cells = models.create_granule_cells(1000)  # Adjust numbers as needed
    purkinje_cells = models.create_purkinje_cells(100)
    interneurons = models.create_interneurons(200)
    mossy_fibers = models.create_mossy_fibers(300)
    
    # Connect populations following cerebellar connectivity rules:
    # Granule cells to Purkinje cells (via parallel fibers)
    models.connect_cells(granule_cells, purkinje_cells, syn_spec=config.EXCITATORY_SYNAPSE)
    
    # Inhibitory connections: interneurons to granule cells, for example.
    models.connect_cells(interneurons, granule_cells, syn_spec=config.INHIBITORY_SYNAPSE)

    # Mossy fibers to granule cells
    models.connect_cells(mossy_fibers, granule_cells, syn_spec=config.MOSSY_FIBERS_SYNAPSE)
    
    return {
        "granule": granule_cells,
        "purkinje": purkinje_cells,
        "interneurons": interneurons,
        "mossy_fibers": mossy_fibers,
    }

def attach_recorders(cell_population, record_type="spikes"):
    """Attach a spike detector (or multimeter for continuous variables) to a given cell population."""
    if record_type == "spikes":
        spike_detector = nest.Create("spike_recorder")
        nest.Connect(cell_population, spike_detector)
        return spike_detector
    elif record_type == "voltages":
        # Example: Attach a multimeter to record membrane potentials
        multimeter = nest.Create("multimeter", params={"record_from": ["V_m"]})
        nest.Connect(multimeter, cell_population)
        return multimeter
    return None

def run_simulation():
    """Set up and run the network simulation."""
    network = setup_network()
    
    # Attach recorders to populations of interest
    sd_purkinje = attach_recorders(network["purkinje"], record_type="spikes")
    vd_granule = attach_recorders(network["granule"], record_type="voltages")
    
    # Run simulation for the specified simulation time
    nest.Simulate(config.SIM_TIME)
    
    # Return recorded data
    return {
        "purkinje_spikes": nest.GetStatus(sd_purkinje, keys="events")[0],
        "granule_voltages": nest.GetStatus(vd_granule, keys="events")[0],
    }
