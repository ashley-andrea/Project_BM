# src/simulation.py
import nest
import src.config as config 
import src.models as models
import src.spatial_models as spatial_models
import matplotlib.pyplot as plt
import numpy as np

# Apply the simulation settings to NEST
nest.ResetKernel()
nest.SetKernelStatus({"resolution": config.DT, "print_time": True, "rng_seed": config.SEED})

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
    spatial_models.connect_spatial_all(
        mossy_fibers, climbing_fibers, granule_cells, golgi_cells, purkinje_cells, interneurons, dcn_cells
    )
    print ("Network setup complete.")

    if plot_model:
        # Colors
        mossy_color = "darkorange"
        climbing_color = "black"
        granule_color = "red"
        golgi_color = "blue"
        purkinje_color = "green"
        interneuron_color = "orange"
        dcn_color = "purple"

        # ---- Full-Network Plot using PlotLayer ----
        fig = nest.PlotLayer(mossy_fibers, nodecolor=mossy_color, nodesize=2)
        nest.PlotLayer(climbing_fibers, fig, nodecolor=climbing_color, nodesize=10)
        nest.PlotLayer(granule_cells, fig, nodecolor=granule_color, nodesize=1)
        nest.PlotLayer(golgi_cells, fig, nodecolor=golgi_color, nodesize=40)
        nest.PlotLayer(purkinje_cells, fig, nodecolor=purkinje_color, nodesize=40)
        nest.PlotLayer(interneurons, fig, nodecolor=interneuron_color, nodesize=15)
        nest.PlotLayer(dcn_cells, fig, nodecolor=dcn_color, nodesize=30)

        # Create legend with colors matching the nodes
        legend_labels = ["Mossy Fibers", "Climbing Fibers", "Granule Cells", "Golgi Cells", 
                         "Purkinje Cells", "Interneurons", "DCN Cells"]
        legend_colors = [mossy_color, climbing_color, granule_color, golgi_color, purkinje_color, interneuron_color, dcn_color]
        handles = [plt.Line2D([0], [0], marker='o', color='w', markersize=8, markerfacecolor=c) 
                   for c in legend_colors]
        plt.legend(handles, legend_labels, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=10)
        plt.show()

        # ---- Vertical Slice Plot ----
        # Use the same figure dimensions as the full-network plot
        fig_slice, ax_slice = plt.subplots(figsize=fig.get_size_inches())

        def plot_vertical_slice(layer, color, name, nodesize, x_range=(-0.1, 0.1)):
            """
            Extract neurons within a narrow X-range and plot them on the Y-Z plane.
            This mirrors the dimension mapping of the PlotLayer functions.
            """
            positions = np.array(nest.GetPosition(layer))  # positions assumed as [X, Y, Z]
            slice_mask = (positions[:, 0] > x_range[0]) & (positions[:, 0] < x_range[1])
            # Plot using Y for horizontal and Z for vertical
            ax_slice.scatter(positions[slice_mask, 1],
                             positions[slice_mask, 2],
                             c=color,
                             s=nodesize,  # using the same nodesize as in PlotLayer
                             label=name)

        # Define the narrow slice in the X-direction (to "cut" the 3D network)
        slice_x_range = (0.1, 0.3)

        # Plot each layer with the corresponding nodesize
        plot_vertical_slice(mossy_fibers,    mossy_color,    "Mossy Fibers",    2,  slice_x_range)
        plot_vertical_slice(climbing_fibers, climbing_color, "Climbing Fibers", 10, slice_x_range)
        plot_vertical_slice(granule_cells,   granule_color,  "Granule Cells",   1,  slice_x_range)
        plot_vertical_slice(golgi_cells,     golgi_color,    "Golgi Cells",     40, slice_x_range)
        plot_vertical_slice(purkinje_cells,    purkinje_color, "Purkinje Cells",  40, slice_x_range)
        plot_vertical_slice(interneurons,      interneuron_color, "Interneurons",15, slice_x_range)
        plot_vertical_slice(dcn_cells,         dcn_color,      "DCN Cells",       30, slice_x_range)

        # Label axes to match the PlotLayer projection
        ax_slice.set_xlabel("Depth (Y-axis)")
        ax_slice.set_ylabel("Height (Z-axis)")
        ax_slice.set_title("Vertical Slice of the Network (Y-Z plane)")

        # Move the legend outside of the image:
        ax_slice.legend(loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8)
        ax_slice.set_aspect('equal', 'box')  # enforce equal scaling on Y and Z

        plt.show()



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