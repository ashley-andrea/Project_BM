# src/spatial_models.py
import nest
import nest.random
import nest.raster_plot
import src.config as config
from src import models

# Apply the simulation settings to NEST
nest.ResetKernel()
nest.SetKernelStatus({"resolution": config.DT, "print_time": True, "rng_seed": config.SEED})

# We want to setup a spatial model that is basically a section of the cerebellar cortex.
# The populations will be setup one above the other, with mossy fibers at the bottom and deep cerebellar nuclei at the top.
# All of the populations will have random spatial positions within the section, but the Purkinje cells will be placed in a grid.
# The connections will also account for the spatial positions of the populations.

def create_spatial_mossy_fibers(n):
    # Create a population of mossy fibers with spatial information
    pos = nest.spatial.free(
        pos = [
            nest.random.uniform(-1.0, 1.0),
            nest.random.uniform(-1.0, 1.0),
            nest.random.uniform(2.0, 3.0)
        ], extent = (3, 3, 3))
    mossy_fibers = nest.Create("poisson_generator", n, params=config.MOSSY_FIBER_PARAMS, positions=pos)
    return mossy_fibers

def create_spatial_climbing_fibers(n):
    # Create a population of climbing fibers with spatial information
    pos = nest.spatial.free(
        pos = [
            nest.random.uniform(-1.0, 1.0),
            nest.random.uniform(-1.0, 1.0),
            nest.random.uniform(0.0, 2.0)
        ], extent = (3, 3, 3))
    climbing_fibers = nest.Create("poisson_generator", n, params=config.CLIMBING_FIBER_PARAMS, positions=pos)
    return climbing_fibers

def create_spatial_granule_cells(n):
    # Create a population of granule cells with spatial information
    pos = nest.spatial.free(
        pos = [
            nest.random.uniform(-1.0, 1.0),
            nest.random.uniform(-1.0, 1.0),
            nest.random.uniform(3.0, 4.0)
        ], extent = (3, 3, 3))
    granule_cells = nest.Create("iaf_psc_alpha", n, params=config.GRANULE_CELL_PARAMS, positions=pos)
    return granule_cells

def create_spatial_golgi_cells(n):
    # Create a population of Golgi cells with spatial information
    pos = nest.spatial.free(
        pos = [
            nest.random.uniform(-1.0, 1.0),
            nest.random.uniform(-1.0, 1.0),
            nest.random.uniform(3.0, 4.0)
        ], extent = (3, 3, 3))
    golgi_cells = nest.Create("iaf_psc_alpha", n, params=config.GOLGI_CELL_PARAMS, positions=pos)
    return golgi_cells

def create_spatial_purkinje_cells(n):
    # Create a population of Purkinje cells with spatial information
    try:
        n_per_layer = int(n // config.PURKINJE_CELL_NUM_LAYERS)
        n_per_side = int(n_per_layer ** 0.5)
    except ZeroDivisionError:
        n_per_layer = 25
        n_per_side = 5
    pos = nest.spatial.grid(
        shape = [n_per_side, n_per_side, config.PURKINJE_CELL_NUM_LAYERS],
        center = [0.0, 0.0, 4.5],
        extent = (2, 2, 1))
    purkinje_cells = nest.Create("iaf_psc_alpha", params=config.PURKINJE_CELL_PARAMS, positions=pos)
    return purkinje_cells


def create_spatial_interneurons(n):
    # Create a population of interneurons with spatial information
    pos = nest.spatial.free(
        pos = [
            nest.random.uniform(-1.0, 1.0),
            nest.random.uniform(-1.0, 1.0),
            nest.random.uniform(6.0, 7.0)
        ], extent = (3, 3, 3))
    interneurons = nest.Create("iaf_psc_alpha", n, params=config.INTERNEURON_PARAMS, positions=pos)
    return interneurons

def create_spatial_deep_cerebellar_nuclei(n):
    # Create a population of deep cerebellar nuclei cells with spatial information
    pos = nest.spatial.free(
        pos = [
            nest.random.uniform(-1.0, 1.0),
            nest.random.uniform(-1.0, 1.0),
            nest.random.uniform(2.0, 3.0)
        ], extent = (3, 3, 3))
    dcn_cells = nest.Create("iaf_psc_alpha", n, params=config.DEEP_CEREBELLAR_NUCLEI_PARAMS, positions=pos)
    return dcn_cells
