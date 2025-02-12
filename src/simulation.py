# src/simulation.py
import nest
import src.config as config 
import src.models as models
import src.spatial_models as spatial_models

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
    models.connect_all(
        mossy_fibers, climbing_fibers, granule_cells, golgi_cells, purkinje_cells, interneurons, dcn_cells
    )
    
    print ("Network setup complete.")

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

def setup_spatial_network(plot_model=False):
    # Create cell populations using numbers from the config file
    granule_cells = spatial_models.create_spatial_granule_cells(config.GRANULE_CELL_NUM)
    purkinje_cells = spatial_models.create_spatial_purkinje_cells(config.PURKINJE_CELL_NUM)
    interneurons   = spatial_models.create_spatial_interneurons(config.INTERNEURON_NUM)
    golgi_cells    = spatial_models.create_spatial_golgi_cells(config.GOLGI_CELL_NUM)
    dcn_cells      = spatial_models.create_spatial_deep_cerebellar_nuclei(config.DEEP_CEREBELLAR_NUCLEI_NUM)
    mossy_fibers   = spatial_models.create_spatial_mossy_fibers(config.MOSSY_FIBER_NUM)
    climbing_fibers = spatial_models.create_spatial_climbing_fibers(config.CLIMBING_FIBER_NUM)

    # Connect populations following cerebellar connectivity rules:
    models.connect_all(
        mossy_fibers, climbing_fibers, granule_cells, golgi_cells, purkinje_cells, interneurons, dcn_cells
    )
    print ("Network setup complete.")

    if plot_model:
        fig = nest.PlotLayer(mossy_fibers, nodecolor="purple", nodesize=2)
        nest.PlotLayer(climbing_fibers, fig, nodecolor="black", nodesize=10)
        nest.PlotLayer(granule_cells, fig, nodecolor="red", nodesize=1)
        nest.PlotLayer(golgi_cells, fig, nodecolor="blue", nodesize=40)
        nest.PlotLayer(purkinje_cells, fig, nodecolor="green", nodesize=40)
        nest.PlotLayer(interneurons, fig, nodecolor="orange", nodesize=15)
        nest.PlotLayer(dcn_cells, fig, nodecolor="purple", nodesize=30)

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
    nest.ResetKernel()
    """Set up and run the network simulation."""
    network = setup_network()
    
    # Attach recorders to populations of interest
    sd_purkinje = attach_recorders(network["purkinje"], record_type="spikes")
    vd_purkinje = attach_recorders(network["purkinje"], record_type="voltages")
    sd_dcn = attach_recorders(network["dcn"], record_type="spikes")
    vd_dcn = attach_recorders(network["dcn"], record_type="voltages")
    
    # Run simulation for the specified simulation time
    print ("Simulation running...")
    nest.Simulate(config.SIM_TIME)

    # Return recorded data
    return {
        "purkinje_spikes": nest.GetStatus(sd_purkinje, keys="events")[0],
        "purkinje_voltages": nest.GetStatus(vd_purkinje, keys="events")[0],
        "dcn_spikes": nest.GetStatus(sd_dcn, keys="events")[0],
        "dcn_voltages": nest.GetStatus(vd_dcn, keys="events")[0],
    }

def example_spatial_simulation():
    nest.ResetKernel()
    """Set up and run the spatial network simulation."""
    network = setup_spatial_network(plot_model=True)

    # Attach recorders to populations of interest
    sd_PC = attach_recorders(network["purkinje"], record_type="spikes")
    vd_PC = attach_recorders(network["purkinje"], record_type="voltages")
    sd_GrC = attach_recorders(network["granule"], record_type="spikes")
    vd_GrC = attach_recorders(network["granule"], record_type="voltages")
    sd_GoC = attach_recorders(network["golgi"], record_type="spikes")
    vd_GoC = attach_recorders(network["golgi"], record_type="voltages")

    # Run simulation for the specified simulation time
    print ("Simulation running...")
    nest.Simulate(config.SIM_TIME)

    # Return recorded data
    return {
        "purkinje_spikes": nest.GetStatus(sd_PC, keys="events")[0],
        "purkinje_voltages": nest.GetStatus(vd_PC, keys="events")[0],
        "granule_spikes": nest.GetStatus(sd_GrC, keys="events")[0],
        "granule_voltages": nest.GetStatus(vd_GrC, keys="events")[0],
        "golgi_spikes": nest.GetStatus(sd_GoC, keys="events")[0],
        "golgi_voltages": nest.GetStatus(vd_GoC, keys="events")[0],
    }