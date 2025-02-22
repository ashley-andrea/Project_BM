# src/spatial_models.py
import nest
import nest.random
import nest.raster_plot
import src.config as config
from src import models

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
    print(f"Created {n} mossy fibers.")
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
    print(f"Created {n} climbing fibers.")
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
    print(f"Created {n} granule cells.")
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
    print(f"Created {n} Golgi cells.")
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
        center = [0.0, 0.0, 4.25],
        extent = (2, 2, 1))
    purkinje_cells = nest.Create("iaf_psc_alpha", params=config.PURKINJE_CELL_PARAMS, positions=pos)
    print(f"Created {int(n_per_side**2 * config.PURKINJE_CELL_NUM_LAYERS)} Purkinje cells")
    return purkinje_cells


def create_spatial_interneurons(n):
    # Create a population of interneurons with spatial information
    pos = nest.spatial.free(
        pos = [
            nest.random.uniform(-1.0, 1.0),
            nest.random.uniform(-1.0, 1.0),
            nest.random.uniform(4.5, 5.5)
        ], extent = (3, 3, 3))
    interneurons = nest.Create("iaf_psc_alpha", n, params=config.INTERNEURON_PARAMS, positions=pos)
    print(f"Created {n} interneurons.")
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
    print(f"Created {n} deep cerebellar nuclei cells.")
    return dcn_cells

# =============================================================================
# Connectivity rules
# =============================================================================

# Mossy Fibers Connections
def connect_spatial_mossy_to_granule(mossy, granule):
    """
    Mossy -> Granule: Vertical column-like connectivity (z-oriented ellipsoid)
    """
    parameter = config.CONN_MF_TO_GRANULE["p"]
    conndict = {
        "rule": "pairwise_bernoulli",
        "p": parameter,
        "mask": {
            "ellipsoidal": {
                "major_axis": 5.0,  # Vertical orientation
                "minor_axis": 1.8,
                "polar_axis": 1.8,
                "polar_angle": 90  # Align major axis with z-axis
            }
        }
    }
    syndict = config.SYN_MF_TO_GRANULE
    # Updated weight formula to ensure non-negative values:
    # Multiplicative decay with max distance assumed to be 10.0
    syndict["weight"] = syndict["weight"] * (2 - nest.spatial.distance / 10.0)
    nest.Connect(mossy, granule, conn_spec=conndict, syn_spec=syndict)

def connect_spatial_mossy_to_golgi(mossy, golgi):
    """Mossy -> Golgi: Moderate vertical spread"""
    parameter = config.CONN_MF_TO_GOLGI["p"]
    conndict = {
        "rule": "pairwise_bernoulli",
        "p": parameter,
        "mask": {
            "ellipsoidal": {
                "major_axis": 4.0,  # Vertical orientation
                "minor_axis": 2.0,
                "polar_axis": 2.0,
                "polar_angle": 90
            }
        }
    }
    syndict = config.SYN_MF_TO_GOLGI
    # Updated weight formula: multiplicative decay with max distance = 8.0
    syndict["weight"] = syndict["weight"] * (1 - nest.spatial.distance / 8.0)
    nest.Connect(mossy, golgi, conn_spec=conndict, syn_spec=syndict)

def connect_spatial_mossy_to_dcn(mossy, dcn):
    """Mossy -> DCN: Horizontal spread in same layer"""
    parameter = 0.2
    conndict = {
        "rule": "pairwise_bernoulli",
        "p": parameter,
        "mask": {
            "ellipsoidal": {
                "major_axis": 3.0,  # Horizontal orientation
                "minor_axis": 1.5,
                "polar_axis": 1.5,
                "polar_angle": 0  # Major axis in xy-plane
            }
        }
    }
    syndict = config.SYN_MF_TO_DCN
    # Updated weight formula: multiplicative decay with max distance = 15.0
    syndict["weight"] = syndict["weight"] * (1 - nest.spatial.distance / 15.0)
    nest.Connect(mossy, dcn, conn_spec=conndict, syn_spec=syndict)

def connect_spatial_granule_to_golgi(granule, golgi):
    """Granule -> Golgi: Local spherical connections"""
    parameter = config.CONN_GRANULE_TO_GOLGI["p"]
    conndict = {
        "rule": "pairwise_bernoulli",
        "p": parameter,
        "mask": {
            "ellipsoidal": {
                "major_axis": 2.0,
                "minor_axis": 2.0,
                "polar_axis": 2.0,
                "polar_angle": 0  # Spherical orientation
            }
        }
    }
    syndict = config.SYN_GRANULE_TO_GOLGI
    # Updated weight formula: multiplicative decay with max distance = 3.33
    syndict["weight"] = syndict["weight"] * (1 - nest.spatial.distance / 3.33)
    nest.Connect(granule, golgi, conn_spec=conndict, syn_spec=syndict)

def connect_spatial_granule_to_purkinje(granule, purkinje):
    """Granule -> Purkinje (Parallel fibers): Long horizontal spread"""
    parameter = config.CONN_GRANULE_TO_PURKINJE["p"]
    conndict = {
        "rule": "pairwise_bernoulli",
        "p": parameter,
        "mask": {
            "ellipsoidal": {
                "major_axis": 8.0,  # Horizontal orientation (parallel fibers)
                "minor_axis": 2.0,
                "polar_axis": 2.0,
                "polar_angle": 90  # Major axis in xy-plane
            }
        }
    }
    syndict = config.SYN_PARALLEL
    # Updated weight formula: multiplicative decay with max distance = 16.0
    syndict["weight"] = syndict["weight"] * (2 - nest.spatial.distance / 16.0)
    nest.Connect(granule, purkinje, conn_spec=conndict, syn_spec=syndict)

def connect_spatial_granule_to_interneuron(granule, interneuron):
    """Connect granule cells to interneurons with excitatory synapses."""
    parameter = config.CONN_GRANULE_TO_INTERNEURON["p"]
    conndict = {
        "rule": "pairwise_bernoulli",
        "p": parameter,
        "mask": {
            "ellipsoidal": {
                "major_axis": 6.0,
                "minor_axis": 2.0,
                "polar_axis": 2.0,
                "polar_angle": 90
            }
        }
    }
    syndict = config.SYN_GRANULE_TO_INTERNEURON
    # Updated weight formula: multiplicative decay with max distance = 30.0
    syndict["weight"] = syndict["weight"] * (1 - nest.spatial.distance / 30.0)
    nest.Connect(granule, interneuron, conn_spec=conndict, syn_spec=syndict)

def connect_spatial_golgi_to_granule(golgi, granule):
    """Connect Golgi cells to granule cells with inhibitory synapses."""
    parameter = config.CONN_GOLGI_TO_GRANULE["p"]
    conndict = {
        "rule": "pairwise_bernoulli",
        "p": parameter,
        "mask": {
            "ellipsoidal": {
                "major_axis": 5.0,
                "minor_axis": 5.0,
                "polar_axis": 1.0,
                "polar_angle": 0
            }
        }
    }
    syndict = config.SYN_GOLGI_TO_GRANULE
    # Inhibitory synapse: retain original formula (weight is assumed negative)
    syndict["weight"] = 2 * syndict["weight"] - 0.2 * nest.spatial.distance
    nest.Connect(golgi, granule, conn_spec=conndict, syn_spec=syndict)

def connect_spatial_golgi_to_golgi(golgi):
    """Connect Golgi cells to each other with inhibitory synapses."""
    parameter = config.CONN_GOLGI_TO_GOLGI["p"]
    conndict = {
        "rule": "pairwise_bernoulli",
        "p": parameter,
        "mask": {
            "ellipsoidal": {
                "major_axis": 3.0,
                "minor_axis": 3.0,
                "polar_axis": 1.0,
                "polar_angle": 0
            }
        }
    }
    syndict = config.SYN_GOLGI_TO_GOLGI
    # Inhibitory synapse: retain original formula (weight is assumed negative)
    syndict["weight"] = 2 * syndict["weight"] - 0.2 * nest.spatial.distance
    nest.Connect(golgi, golgi, conn_spec=conndict, syn_spec=syndict)

def connect_spatial_climbing_to_purkinje(climbing, purkinje):
    """Connect climbing fibers to Purkinje cells with strong excitatory synapses."""
    if len(climbing) != len(purkinje):
        raise ValueError("Number of climbing fibers must match number of Purkinje cells.")
    conndict = {
        "rule": "one_to_one"
    }
    syndict = config.SYN_CLIMBING
    nest.Connect(climbing, purkinje, conn_spec=conndict, syn_spec=syndict)

def connect_spatial_interneuron_to_purkinje(interneuron, purkinje):
    """Connect interneurons to Purkinje cells with inhibitory synapses."""
    parameter = config.CONN_INTERNEURON_TO_PURKINJE["p"]
    conndict = {
        "rule": "pairwise_bernoulli",
        "p": parameter,
        "mask": {
            "ellipsoidal": {
                "major_axis": 2.0,
                "minor_axis": 1.0,
                "polar_axis": 1.0,
                "polar_angle": 90
            }
        }
    }
    syndict = config.SYN_INTERNEURON_TO_PURKINJE
    # Corrected to inhibitory synapses; the formula remains valid for negative weights
    syndict["weight"] = syndict["weight"] - 0.1 * nest.spatial.distance
    nest.Connect(interneuron, purkinje, conn_spec=conndict, syn_spec=syndict)

def connect_spatial_interneuron_to_interneuron(interneuron):
    """Connect interneurons to each other with inhibitory synapses."""
    parameter = config.CONN_INTERNEURON_TO_INTERNEURON["p"]
    conndict = {
        "rule": "pairwise_bernoulli",
        "p": parameter,
        "mask": {
            "ellipsoidal": {
                "major_axis": 4.0,
                "minor_axis": 4.0,
                "polar_axis": 0.5,
                "polar_angle": 0
            }
        }
    }
    syndict = config.SYN_INTERNEURON_TO_INTERNEURON
    syndict["weight"] = syndict["weight"] - 0.2 * nest.spatial.distance
    nest.Connect(interneuron, interneuron, conn_spec=conndict, syn_spec=syndict)

def connect_spatial_purkinje_to_dcn(purkinje, dcn):
    """Connect Purkinje cells to DCN cells with inhibitory synapses."""
    parameter = config.CONN_PURKINJE_TO_DCN["outdegree"]
    conndict = {
        "rule": "fixed_outdegree",
        "outdegree": parameter
    }
    syndict = config.SYN_PURKINJE_TO_DCN
    # Inhibitory synapse: retain original formula (weight is assumed negative)
    syndict["weight"] = 2 * syndict["weight"] - 0.5 * nest.spatial.distance
    nest.Connect(purkinje, dcn, conn_spec=conndict, syn_spec=syndict)


def connect_spatial_all(mossy, climbing, granule, golgi, purkinje, interneuron, dcn):
    """Connect all populations according to cerebellar connectivity rules."""
    connect_spatial_mossy_to_granule(mossy, granule)
    connect_spatial_mossy_to_golgi(mossy, golgi)
    connect_spatial_mossy_to_dcn(mossy, dcn)
    connect_spatial_granule_to_golgi(granule, golgi)
    connect_spatial_granule_to_purkinje(granule, purkinje)
    connect_spatial_granule_to_interneuron(granule, interneuron)
    connect_spatial_golgi_to_granule(golgi, granule)
    connect_spatial_golgi_to_golgi(golgi)
    connect_spatial_climbing_to_purkinje(climbing, purkinje)
    connect_spatial_interneuron_to_purkinje(interneuron, purkinje)
    connect_spatial_interneuron_to_interneuron(interneuron)
    connect_spatial_purkinje_to_dcn(purkinje, dcn)
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