# src/simulation.py
import nest
import src.config as config 
import src.models as models
import os

def setup_network():
    """Set up the cerebellar network architecture."""
    # Create cell populations using numbers from the config file
    granule_cells = models.create_granule_cells(config.GRANULE_CELL_NUM)
    purkinje_cells = models.create_purkinje_cells(config.PURKINJE_CELL_NUM)
    interneurons   = models.create_interneurons(config.INTERNEURON_NUM)
    golgi_cells    = models.create_golgi_cells(config.GOLGI_CELL_NUM)
    dcn_cells      = models.create_deep_cerebellar_nuclei(config.DEEP_CEREBELLAR_NUCLEI_NUM)
    mossy_fibers   = models.create_mossy_fibers(config.MOSSY_FIBER_NUM)
    climbing_fibers = models.create_climbing_fibers(config.CLIMBING_FIBER_NUM)
    
    # Connect populations following cerebellar connectivity rules:
    
    # 1. Connect mossy fibers to granule cells (excitatory)
    models.connect_mossy_to_granule(mossy_fibers, granule_cells)
    
    # 2. Connect mossy fibers to deep cerebellar nuclei (excitatory)
    models.connect_mossy_to_dcn(mossy_fibers, dcn_cells)
    
    # 3. Connect granule cells (via parallel fibers) to Purkinje cells (excitatory)
    models.connect_granule_to_purkinje(granule_cells, purkinje_cells)
    
    # 4. Connect climbing fibers to Purkinje cells (powerful excitatory input)
    models.connect_climbing_to_purkinje(climbing_fibers, purkinje_cells)
    
    # 5. Connect Golgi cells to granule cells (inhibitory)
    models.connect_golgi_to_granule(golgi_cells, granule_cells)
    
    # 6. Connect interneurons (basket/stellate cells) to Purkinje cells (inhibitory)
    models.connect_interneuron_to_purkinje(interneurons, purkinje_cells)
    
    # 7. Connect Purkinje cells to deep cerebellar nuclei (inhibitory)
    models.connect_purkinje_to_dcn(purkinje_cells, dcn_cells)
    
    # Return all populations in a dictionary for later use
    return {
        "granule": granule_cells,
        "purkinje": purkinje_cells,
        "interneurons": interneurons,
        "golgi": golgi_cells,
        "dcn": dcn_cells,
        "mossy_fibers": mossy_fibers,
        "climbing_fibers": climbing_fibers,
    }

def attach_recorders(cell_population, record_type="spikes"):
    """Attach a spike recorder or multimeter to a given cell population."""
    if record_type == "spikes":
        spike_recorder = nest.Create("spike_recorder")
        nest.Connect(cell_population, spike_recorder)
        return spike_recorder
    elif record_type == "voltages":
        multimeter = nest.Create("multimeter", params={"record_from": ["V_m"]})
        nest.Connect(multimeter, cell_population)
        return multimeter
    return None

def example_simulation():
    """Set up and run the network simulation."""
    network = setup_network()
    
    # Attach recorders to populations of interest
    sd_purkinje = attach_recorders(network["purkinje"], record_type="spikes")
    vd_purkinje = attach_recorders(network["purkinje"], record_type="voltages")
    
    # Run simulation for the specified simulation time
    nest.Simulate(config.SIM_TIME)
    
    # Return recorded data
    return {
        "purkinje_spikes": nest.GetStatus(sd_purkinje, keys="events")[0],
        "purkinje_voltages": nest.GetStatus(vd_purkinje, keys="events")[0],
    }

def run_simulation():
    nest.ResetKernel()
    network = setup_network()
    nest.Simulate(config.SIM_TIME)
    return network
